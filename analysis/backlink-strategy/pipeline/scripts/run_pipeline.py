import os, sys, json, re, logging
from datetime import datetime
from collections import Counter, defaultdict
from urllib.parse import urlparse

import pandas as pd
import numpy as np

# Добавить scripts/ в path для импорта config
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Global gambling log
GAMBLING_LOG = []

# ──────────────────────────────────────────────
# CHECKPOINT
# ──────────────────────────────────────────────
def step_complete(output_path, min_size_bytes=100):
    """Проверяет что output существует и валиден."""
    if not os.path.exists(output_path):
        return False
    if os.path.getsize(output_path) < min_size_bytes:
        return False
    if output_path.endswith('.json'):
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                json.load(f)
            return True
        except Exception:
            return False
    return True

def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    logger.info(f"Saved: {path} ({os.path.getsize(path)} bytes)")

# ──────────────────────────────────────────────
# ЗАГРУЗКА CSV
# ──────────────────────────────────────────────
def load_csv(filepath, column_map=None):
    """Загрузка CSV с auto-detect encoding."""
    for enc in ['utf-16-le', 'utf-8', 'latin-1']:
        try:
            df = pd.read_csv(filepath, encoding=enc, sep='\t')
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    else:
        raise ValueError(f"Cannot read {filepath} with any encoding")

    # Strip BOM из первой колонки
    first_col = df.columns[0]
    if first_col.startswith('\ufeff'):
        df = df.rename(columns={first_col: first_col.lstrip('\ufeff')})
    # Strip кавычки из заголовков
    df.columns = [c.strip().strip('"') for c in df.columns]

    # Rename по column_map
    if column_map:
        rename = {k: v for k, v in column_map.items() if k in df.columns}
        df = df.rename(columns=rename)

    return df

def get_column_map(report_type):
    """Return the appropriate column map for a report type."""
    return {
        'A': config.COLUMN_MAP_A,
        'B': config.COLUMN_MAP_B,
        'C': config.COLUMN_MAP_C,
        'D': config.COLUMN_MAP_D,
    }[report_type]

def get_data_filepath(filename, report_type):
    """Return full path to a data file."""
    subdir = config.REPORT_DIRS[report_type]
    return os.path.join(config.DATA_DIR, subdir, filename)

def get_expected_columns(report_type):
    """Return set of expected internal column names for a report type."""
    cmap = get_column_map(report_type)
    return set(cmap.values())

# ──────────────────────────────────────────────
# GAMBLING FILTER
# ──────────────────────────────────────────────
def apply_gambling_filter(df, report_type, domain):
    """Два паттерна: strict (word boundaries) + loose. По конкретным полям."""
    fields = config.GAMBLING_FILTER_FIELDS.get(report_type, [])
    strict = re.compile(config.GAMBLING_PATTERNS['strict'])
    loose = re.compile(config.GAMBLING_PATTERNS['loose'])
    log_entries = []

    mask = pd.Series(False, index=df.index)
    for field in fields:
        if field not in df.columns:
            continue
        col = df[field].astype(str)
        s_match = col.str.contains(strict, na=False)
        l_match = col.str.contains(loose, na=False)
        field_mask = s_match | l_match
        for idx in df[field_mask & ~mask].index:
            log_entries.append({
                'domain': domain, 'field': field,
                'value': str(df.at[idx, field])[:100],
                'pattern': 'strict' if s_match.at[idx] else 'loose'
            })
        mask = mask | field_mask

    filtered = df[~mask].copy()
    return filtered, log_entries

def clean_numeric(series):
    """Clean numeric columns: remove spaces, commas from numbers."""
    return pd.to_numeric(
        series.astype(str).str.replace(r'[\s,]', '', regex=True),
        errors='coerce'
    )

# ──────────────────────────────────────────────
# ЭТАП 1: ВАЛИДАЦИЯ
# ──────────────────────────────────────────────
def validate_all():
    logger.info("=== STEP 1: VALIDATION ===")
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_files_expected': len(config.FILE_TO_DOMAIN),
        'total_files_found': 0,
        'status': 'PASS',
        'files': [],
        'warnings': [],
        'errors': [],
    }

    file_counter = {'A': 0, 'B': 0, 'C': 0, 'D': 0}

    for filename, (domain, report_type) in config.FILE_TO_DOMAIN.items():
        file_counter[report_type] += 1
        file_id = f"{report_type}{file_counter[report_type]}"

        filepath = get_data_filepath(filename, report_type)
        entry = {
            'id': file_id,
            'domain': domain,
            'report_type': config.REPORT_DIRS[report_type],
            'filename': filename,
            'rows': 0,
            'columns': 0,
            'encoding': 'unknown',
            'separator': 'tab',
            'ahrefs_limit_hit': False,
            'missing_columns': [],
            'status': 'OK',
        }

        if not os.path.exists(filepath):
            entry['status'] = 'MISSING'
            report['errors'].append(f"File not found: {filename}")
            report['status'] = 'FAIL'
            report['files'].append(entry)
            continue

        report['total_files_found'] += 1

        # Detect encoding
        detected_enc = None
        for enc in ['utf-16-le', 'utf-8', 'latin-1']:
            try:
                df = pd.read_csv(filepath, encoding=enc, sep='\t', nrows=5)
                detected_enc = enc
                break
            except (UnicodeDecodeError, UnicodeError):
                continue

        if detected_enc is None:
            entry['status'] = 'FAIL'
            report['errors'].append(f"Cannot detect encoding: {filename}")
            report['status'] = 'FAIL'
            report['files'].append(entry)
            continue

        entry['encoding'] = detected_enc

        # Load full file for row count and column check
        try:
            df = load_csv(filepath, get_column_map(report_type))
            entry['rows'] = len(df)
            entry['columns'] = len(df.columns)

            # Check for Ahrefs limit
            if len(df) == 30000:
                entry['ahrefs_limit_hit'] = True
                report['warnings'].append(f"Ahrefs 30K limit hit: {filename} ({domain})")

            # Check expected columns
            expected = get_expected_columns(report_type)
            present = set(df.columns)
            missing = expected - present
            if missing:
                entry['missing_columns'] = list(missing)
                report['warnings'].append(f"Missing columns in {filename}: {missing}")

        except Exception as e:
            entry['status'] = 'FAIL'
            report['errors'].append(f"Error reading {filename}: {str(e)}")
            report['status'] = 'FAIL'

        report['files'].append(entry)

    # Check for unknown files in directories
    for report_type, subdir in config.REPORT_DIRS.items():
        dir_path = os.path.join(config.DATA_DIR, subdir)
        if not os.path.exists(dir_path):
            continue
        for f in os.listdir(dir_path):
            if not f.endswith('.csv'):
                continue
            if f not in config.FILE_TO_DOMAIN:
                report['warnings'].append(f"Unknown file in {subdir}/: {f} (ignored)")

    output_path = os.path.join(config.INTERMEDIATE_DIR, 'validation_report.json')
    save_json(report, output_path)

    total_rows = sum(e['rows'] for e in report['files'])
    logger.info(f"Validation: {report['total_files_found']}/{report['total_files_expected']} files found, "
                f"{total_rows} total rows, status={report['status']}")
    logger.info(f"  Warnings: {len(report['warnings'])}, Errors: {len(report['errors'])}")
    for w in report['warnings']:
        logger.warning(f"  {w}")
    for e in report['errors']:
        logger.error(f"  {e}")

    return report

# ──────────────────────────────────────────────
# ЭТАП 2: НОРМАЛИЗАЦИЯ
# ──────────────────────────────────────────────
def normalize_all():
    logger.info("=== STEP 2: NORMALIZATION ===")
    global GAMBLING_LOG

    for filename, (domain, report_type) in config.FILE_TO_DOMAIN.items():
        # Determine output path
        norm_subdir = config.NORMALIZED_SUBDIRS[report_type]

        if report_type == 'D':
            out_name = config.LINK_INTERSECT_OUTPUT_NAMES.get(domain)
            if out_name is None:
                logger.warning(f"No output name for D file {domain}, skipping")
                continue
        else:
            slug = domain.replace('.', '_')
            out_name = f"{slug}.tsv"

        out_path = os.path.join(config.NORMALIZED_DIR, norm_subdir, out_name)

        # Checkpoint: skip if already normalized
        if os.path.exists(out_path) and os.path.getsize(out_path) > 100:
            logger.info(f"SKIP (exists): {out_path}")
            continue

        filepath = get_data_filepath(filename, report_type)
        if not os.path.exists(filepath):
            logger.error(f"File not found: {filepath}")
            continue

        logger.info(f"Normalizing: {filename} -> {out_name}")

        cmap = get_column_map(report_type)
        df = load_csv(filepath, cmap)

        # Clean numeric columns
        numeric_cols_by_type = {
            'A': ['dr', 'dofollow_ref_domains', 'dofollow_linked_domains', 'traffic', 'keywords',
                   'links_to_target', 'dofollow_links'],
            'B': ['ref_domains', 'top_dr', 'ref_pages', 'links_to_target', 'dofollow_links'],
            'C': ['dr', 'ur', 'domain_traffic', 'referring_domains', 'linked_domains',
                   'external_links', 'page_traffic', 'keywords', 'http_code', 'links_in_group'],
            'D': ['dr', 'domain_traffic', 'intersect'],
        }
        for col in numeric_cols_by_type.get(report_type, []):
            if col in df.columns:
                df[col] = clean_numeric(df[col])

        # Apply gambling filter
        df, gambling_entries = apply_gambling_filter(df, report_type, domain)
        if gambling_entries:
            GAMBLING_LOG.extend(gambling_entries)
            logger.info(f"  Gambling filtered: {len(gambling_entries)} rows from {domain}")

        # Save normalized TSV
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        df.to_csv(out_path, sep='\t', index=False, encoding='utf-8')
        logger.info(f"  Saved: {out_path} ({len(df)} rows)")

    # Save gambling log
    if GAMBLING_LOG:
        log_path = os.path.join(config.INTERMEDIATE_DIR, 'gambling_filter_log.json')
        save_json(GAMBLING_LOG, log_path)

    logger.info(f"Normalization complete. Total gambling filtered: {len(GAMBLING_LOG)}")

# ──────────────────────────────────────────────
# HELPER: Load normalized TSV
# ──────────────────────────────────────────────
def load_normalized(report_type, domain):
    """Load a normalized TSV for a given report type and domain."""
    norm_subdir = config.NORMALIZED_SUBDIRS[report_type]
    slug = domain.replace('.', '_')
    path = os.path.join(config.NORMALIZED_DIR, norm_subdir, f"{slug}.tsv")
    return pd.read_csv(path, sep='\t', encoding='utf-8')

def load_normalized_d(key):
    """Load a normalized link intersect TSV."""
    out_name = config.LINK_INTERSECT_OUTPUT_NAMES[key]
    path = os.path.join(config.NORMALIZED_DIR, 'link_intersect', out_name)
    return pd.read_csv(path, sep='\t', encoding='utf-8')

def extract_domain_from_url(url):
    """Extract domain from a URL."""
    try:
        parsed = urlparse(str(url))
        hostname = parsed.hostname
        if hostname:
            return hostname.lower()
    except Exception:
        pass
    return ''

def extract_subdomain_from_url(url):
    """Extract full subdomain (e.g. en.softonic.com) from a URL."""
    try:
        parsed = urlparse(str(url))
        hostname = parsed.hostname
        if hostname:
            return hostname.lower()
    except Exception:
        pass
    return ''

def extract_lang_subdomain(url, target_domain):
    """Extract language-level subdomain from target_url.

    For softonic.com with URL like https://kmplayer.en.softonic.com/...
    returns 'en.softonic.com' (strips app-level prefix).

    For freesoft.net with URL like https://freesoft.net/...
    returns 'freesoft.net' (root domain).
    """
    try:
        parsed = urlparse(str(url))
        hostname = parsed.hostname
        if not hostname:
            return target_domain
        hostname = hostname.lower()

        # Find the target domain in the hostname
        td = target_domain.lower()
        if hostname == td:
            return td

        if hostname.endswith('.' + td):
            # Get the subdomain part before the target domain
            prefix = hostname[: -(len(td) + 1)]  # e.g. 'kmplayer.en' or 'en'
            parts = prefix.split('.')
            # Common language codes (2-letter)
            lang_codes = {'en', 'fr', 'de', 'es', 'ru', 'pt', 'it', 'nl', 'pl', 'tr',
                          'ja', 'ko', 'zh', 'ar', 'id', 'vi', 'th', 'sv', 'da', 'no',
                          'fi', 'cs', 'hu', 'ro', 'bg', 'uk', 'el', 'hr', 'sk', 'sl',
                          'www', 'br', 'mx'}

            # If the last part is a lang code, use that as subdomain
            # e.g. kmplayer.en -> en.softonic.com
            if parts[-1] in lang_codes:
                return parts[-1] + '.' + td

            # If single part and it's 2-3 chars, treat as language
            if len(parts) == 1 and len(parts[0]) <= 3:
                return parts[0] + '.' + td

            # Otherwise, keep the last part as subdomain
            # e.g. articulos -> articulos.softonic.com
            if len(parts) == 1:
                return parts[0] + '.' + td

            # Multiple parts: try to find the language code
            for p in reversed(parts):
                if p in lang_codes:
                    return p + '.' + td

            # Fallback: use last part
            return parts[-1] + '.' + td

        return hostname
    except Exception:
        return target_domain

def extract_tld(domain):
    """Extract TLD from a domain name."""
    parts = str(domain).rsplit('.', 1)
    if len(parts) == 2:
        return '.' + parts[1].lower()
    return ''

# ──────────────────────────────────────────────
# ЭТАП 3a: R1 — Language Links
# ──────────────────────────────────────────────
def aggregate_r1():
    logger.info("=== STEP 3a: R1 AGGREGATION ===")
    result = {
        'metadata': {
            'source_report': 'C (backlinks_one_per_domain)',
            'total_domains_analyzed': 12,
            'gambling_filtered': len([e for e in GAMBLING_LOG if e.get('domain') in
                                      list(config.DOMAINS.keys())]),
            'generated_at': datetime.now().isoformat(),
        },
        'domains': {},
    }

    all_domains = list(config.DOMAINS.keys())

    for domain in all_domains:
        logger.info(f"  R1: Processing {domain}")
        try:
            df = load_normalized('C', domain)
        except Exception as e:
            logger.warning(f"  Cannot load C for {domain}: {e}")
            continue

        total_backlinks = len(df)

        # Extract language-level subdomain from target_url
        if 'target_url' not in df.columns:
            logger.warning(f"  No target_url column for {domain}")
            continue

        df['_subdomain'] = df['target_url'].apply(lambda u: extract_lang_subdomain(u, domain))

        # Extract referring domain from referring_page_url
        if 'referring_page_url' in df.columns:
            df['_ref_domain'] = df['referring_page_url'].apply(extract_domain_from_url)
        else:
            df['_ref_domain'] = ''

        subdomains_data = {}
        # First pass: count links per subdomain and identify significant ones
        subdomain_counts = df.groupby('_subdomain').size()
        MIN_LINKS_THRESHOLD = 5

        for subdomain, group in df.groupby('_subdomain'):
            if not subdomain or subdomain == 'nan':
                continue

            links_count = len(group)

            # Only include subdomains with >= MIN_LINKS_THRESHOLD links
            # to keep JSON manageable
            if links_count < MIN_LINKS_THRESHOLD:
                continue

            pct = round(links_count / total_backlinks * 100, 1) if total_backlinks > 0 else 0

            # Unique referring domains
            unique_refs = group['_ref_domain'].dropna().unique()
            unique_ref_count = len([r for r in unique_refs if r and r != 'nan'])

            # Average DR
            avg_dr = round(group['dr'].dropna().mean(), 1) if 'dr' in group.columns else 0

            # Language distribution
            lang_dist = {}
            if 'language' in group.columns:
                lang_counts = group['language'].dropna().value_counts()
                for lang, cnt in lang_counts.head(10).items():
                    lang_dist[str(lang)] = int(cnt)

            # Top-5 referring domains by count
            if 'dr' in df.columns:
                ref_domain_stats = group.groupby('_ref_domain').agg(
                    links=('_ref_domain', 'size'),
                    dr=('dr', 'first')
                ).sort_values('links', ascending=False).head(5)
                top_refs = []
                for ref_dom, row in ref_domain_stats.iterrows():
                    if ref_dom and str(ref_dom) != 'nan':
                        top_refs.append({
                            'domain': str(ref_dom),
                            'dr': int(row['dr']) if pd.notna(row['dr']) else 0,
                            'links': int(row['links']),
                        })
            else:
                top_refs = []

            subdomains_data[subdomain] = {
                'links': links_count,
                'pct_of_total': pct,
                'unique_referring_domains': unique_ref_count,
                'avg_dr': avg_dr if pd.notna(avg_dr) else 0,
                'referring_languages': lang_dist,
                'top_referring_domains': top_refs,
            }

        # Add "other" bucket for small subdomains
        small_subs = subdomain_counts[subdomain_counts < MIN_LINKS_THRESHOLD]
        if len(small_subs) > 0:
            other_links = int(small_subs.sum())
            subdomains_data['_other'] = {
                'links': other_links,
                'pct_of_total': round(other_links / total_backlinks * 100, 1) if total_backlinks > 0 else 0,
                'unique_referring_domains': 0,
                'avg_dr': 0,
                'referring_languages': {},
                'top_referring_domains': [],
                'note': f'{len(small_subs)} subdomains with <{MIN_LINKS_THRESHOLD} links each',
            }

        result['domains'][domain] = {
            'total_backlinks': total_backlinks,
            'subdomains': subdomains_data,
        }

    output_path = os.path.join(config.INTERMEDIATE_DIR, 'r1_language_links.json')
    save_json(result, output_path)
    logger.info(f"R1 aggregation complete: {len(result['domains'])} domains")

# ──────────────────────────────────────────────
# ЭТАП 3b: R2 — PBN Signals
# ──────────────────────────────────────────────
def aggregate_r2():
    logger.info("=== STEP 3b: R2 AGGREGATION ===")
    result = {
        'metadata': {
            'source_reports': ['A (referring_domains)', 'C (backlinks)'],
            'detectors': ['low_dr_clusters', 'suspicious_tlds', 'exclusive_domains',
                          'temporal_spikes', 'spam_flagged', 'links_in_group'],
            'generated_at': datetime.now().isoformat(),
        },
        'domains': {},
    }

    all_domains = list(config.DOMAINS.keys())
    suspicious_tlds = {'.xyz', '.info', '.site', '.click', '.top', '.buzz', '.work', '.space'}

    # For Detector 3: build a map of referring_domain -> set of targets it links to
    logger.info("  R2: Building exclusive domain map...")
    ref_domain_to_targets = defaultdict(set)
    for domain in all_domains:
        try:
            df_a = load_normalized('A', domain)
            if 'domain' in df_a.columns:
                for rd in df_a['domain'].dropna().unique():
                    ref_domain_to_targets[str(rd).lower()].add(domain)
        except Exception as e:
            logger.warning(f"  Cannot load A for {domain} (detector 3): {e}")

    for domain in all_domains:
        logger.info(f"  R2: Processing {domain}")
        domain_result = {
            'summary': {},
            'low_dr_clusters': [],
            'suspicious_tlds': {},
            'exclusive_domains': {},
            'temporal_spikes': [],
            'spam_flagged': {},
            'links_in_group': {},
        }

        # Load Report A
        try:
            df_a = load_normalized('A', domain)
        except Exception as e:
            logger.warning(f"  Cannot load A for {domain}: {e}")
            result['domains'][domain] = domain_result
            continue

        total_ref_domains = len(df_a)

        # --- Detector 1: Low DR clusters ---
        if 'dr' in df_a.columns and 'domain' in df_a.columns:
            low_dr = df_a[df_a['dr'] <= 10].copy()
            if len(low_dr) > 0:
                low_dr['_tld'] = low_dr['domain'].astype(str).apply(extract_tld)
                tld_groups = low_dr.groupby('_tld').agg(
                    count=('domain', 'size'),
                    avg_dr=('dr', 'mean'),
                ).reset_index()
                tld_groups = tld_groups[tld_groups['count'] >= 5].sort_values('count', ascending=False)

                for _, row in tld_groups.iterrows():
                    samples = low_dr[low_dr['_tld'] == row['_tld']]['domain'].head(10).tolist()
                    domain_result['low_dr_clusters'].append({
                        'tld': row['_tld'],
                        'count': int(row['count']),
                        'avg_dr': round(float(row['avg_dr']), 1),
                        'pct_of_total': round(int(row['count']) / total_ref_domains * 100, 2) if total_ref_domains > 0 else 0,
                        'sample_domains': [str(s) for s in samples],
                    })

        # --- Detector 2: Suspicious TLDs ---
        if 'domain' in df_a.columns:
            df_a['_tld'] = df_a['domain'].astype(str).apply(extract_tld)
            tld_counts = df_a['_tld'].value_counts()
            susp_tld_data = {}
            total_suspicious = 0
            for tld in suspicious_tlds:
                if tld in tld_counts.index:
                    susp_tld_data[tld] = int(tld_counts[tld])
                    total_suspicious += int(tld_counts[tld])
            domain_result['suspicious_tlds'] = susp_tld_data
            susp_tld_pct = round(total_suspicious / total_ref_domains * 100, 2) if total_ref_domains > 0 else 0

        # --- Detector 3: Exclusive domains ---
        if 'domain' in df_a.columns:
            exclusive_count = 0
            exclusive_list = []
            for _, row_a in df_a.iterrows():
                rd = str(row_a.get('domain', '')).lower()
                if rd and rd in ref_domain_to_targets and len(ref_domain_to_targets[rd]) == 1:
                    exclusive_count += 1
                    if len(exclusive_list) < 20:
                        exclusive_list.append({
                            'domain': rd,
                            'dr': int(row_a['dr']) if pd.notna(row_a.get('dr')) else 0,
                        })
            # Sort top-20 by DR desc
            exclusive_list.sort(key=lambda x: x['dr'], reverse=True)
            domain_result['exclusive_domains'] = {
                'count': exclusive_count,
                'pct_of_total': round(exclusive_count / total_ref_domains * 100, 2) if total_ref_domains > 0 else 0,
                'top_20': exclusive_list[:20],
            }

        # --- Detector 4: Temporal spikes ---
        if 'first_seen' in df_a.columns:
            df_a['_first_seen_dt'] = pd.to_datetime(df_a['first_seen'], errors='coerce')
            valid_dates = df_a.dropna(subset=['_first_seen_dt']).copy()
            if len(valid_dates) > 10:
                valid_dates['_week'] = valid_dates['_first_seen_dt'].dt.isocalendar().apply(
                    lambda x: f"{x.year}-W{x.week:02d}", axis=1
                )
                weekly_counts = valid_dates.groupby('_week').agg(
                    new_domains=('domain', 'size'),
                    avg_dr=('dr', 'mean'),
                ).reset_index()

                if len(weekly_counts) > 4:
                    mean_c = weekly_counts['new_domains'].mean()
                    std_c = weekly_counts['new_domains'].std()
                    if std_c > 0:
                        weekly_counts['zscore'] = (weekly_counts['new_domains'] - mean_c) / std_c
                        spikes = weekly_counts[weekly_counts['zscore'] > 2]
                        for _, spike in spikes.iterrows():
                            spike_week = spike['_week']
                            week_domains = valid_dates[valid_dates['_week'] == spike_week]
                            samples = week_domains['domain'].head(10).tolist()
                            domain_result['temporal_spikes'].append({
                                'week': spike_week,
                                'new_domains': int(spike['new_domains']),
                                'avg_dr': round(float(spike['avg_dr']), 1) if pd.notna(spike['avg_dr']) else 0,
                                'z_score': round(float(spike['zscore']), 2),
                                'sample_domains': [str(s) for s in samples],
                            })

        # --- Detector 5: Spam flagged ---
        if 'is_spam' in df_a.columns:
            spam_mask = df_a['is_spam'].astype(str).str.lower().isin(['true', 'yes', '1'])
            spam_count = int(spam_mask.sum())
            spam_pct = round(spam_count / total_ref_domains * 100, 2) if total_ref_domains > 0 else 0
            spam_samples = df_a[spam_mask]['domain'].head(10).tolist() if 'domain' in df_a.columns else []
            domain_result['spam_flagged'] = {
                'count': spam_count,
                'pct': spam_pct,
                'sample_domains': [str(s) for s in spam_samples],
            }
        else:
            spam_pct = 0
            spam_count = 0

        # --- Detector 6: Links in group ---
        try:
            df_c = load_normalized('C', domain)
            if 'links_in_group' in df_c.columns and 'dr' in df_c.columns:
                suspicious_links = df_c[
                    (df_c['links_in_group'] >= 20) & (df_c['dr'] <= 20)
                ]
                lig_count = len(suspicious_links)
                avg_lig = round(float(suspicious_links['links_in_group'].mean()), 1) if lig_count > 0 else 0
                lig_samples = []
                if 'referring_page_url' in suspicious_links.columns:
                    for _, row_c in suspicious_links.head(10).iterrows():
                        ref_dom = extract_domain_from_url(row_c.get('referring_page_url', ''))
                        lig_samples.append(ref_dom)
                domain_result['links_in_group'] = {
                    'count': lig_count,
                    'avg_links_in_group': avg_lig,
                    'sample_domains': lig_samples,
                }
        except Exception as e:
            logger.warning(f"  Cannot load C for {domain} (detector 6): {e}")

        # --- Summary & PBN risk score ---
        low_dr_pct = round(
            sum(c['count'] for c in domain_result['low_dr_clusters']) / total_ref_domains * 100, 2
        ) if total_ref_domains > 0 else 0

        # PBN risk score
        risk_signals = 0
        if spam_pct > 15:
            risk_signals += 2
        elif spam_pct > 10:
            risk_signals += 1
        if low_dr_pct > 30:
            risk_signals += 2
        elif low_dr_pct > 20:
            risk_signals += 1
        if susp_tld_pct > 10:
            risk_signals += 1
        if len(domain_result['temporal_spikes']) > 3:
            risk_signals += 1
        exclusive_pct = domain_result.get('exclusive_domains', {}).get('pct_of_total', 0)
        if exclusive_pct > 50:
            risk_signals += 1

        if risk_signals >= 4:
            pbn_risk = 'high'
        elif risk_signals >= 2:
            pbn_risk = 'medium'
        else:
            pbn_risk = 'low'

        domain_result['summary'] = {
            'total_ref_domains': total_ref_domains,
            'spam_pct': spam_pct,
            'low_dr_pct': low_dr_pct,
            'suspicious_tld_pct': susp_tld_pct if 'susp_tld_pct' in dir() else 0,
            'exclusive_domains_count': domain_result.get('exclusive_domains', {}).get('count', 0),
            'temporal_spikes_count': len(domain_result['temporal_spikes']),
            'pbn_risk_score': pbn_risk,
        }

        result['domains'][domain] = domain_result

    output_path = os.path.join(config.INTERMEDIATE_DIR, 'r2_pbn_signals.json')
    save_json(result, output_path)
    logger.info(f"R2 aggregation complete: {len(result['domains'])} domains")

# ──────────────────────────────────────────────
# ЭТАП 3c: R3 — Intersections
# ──────────────────────────────────────────────
def aggregate_r3():
    logger.info("=== STEP 3c: R3 AGGREGATION ===")
    result = {
        'metadata': {
            'source_reports': ['A (referring_domains)', 'D (link_intersect)'],
            'generated_at': datetime.now().isoformat(),
        },
        'overlap_matrix': {},
        'link_intersect_targets': {},
        'multi_competitor_domains': {},
    }

    all_domains = list(config.DOMAINS.keys())

    # --- Part 1: Overlap matrix from Report A ---
    logger.info("  R3: Building overlap matrix...")
    domain_refdomains = {}  # domain -> set of referring domains
    for domain in all_domains:
        try:
            df_a = load_normalized('A', domain)
            if 'domain' in df_a.columns:
                refs = set(df_a['domain'].dropna().astype(str).str.lower())
                domain_refdomains[domain] = refs
            else:
                domain_refdomains[domain] = set()
        except Exception as e:
            logger.warning(f"  Cannot load A for {domain}: {e}")
            domain_refdomains[domain] = set()

    # Build 12x12 matrix
    overlap_counts = []
    jaccard_matrix = []
    for d1 in all_domains:
        row_counts = []
        row_jaccard = []
        for d2 in all_domains:
            intersection = len(domain_refdomains[d1] & domain_refdomains[d2])
            union = len(domain_refdomains[d1] | domain_refdomains[d2])
            row_counts.append(intersection)
            row_jaccard.append(round(intersection / union, 4) if union > 0 else 0)
        overlap_counts.append(row_counts)
        jaccard_matrix.append(row_jaccard)

    result['overlap_matrix'] = {
        'domains': all_domains,
        'counts': overlap_counts,
        'jaccard': jaccard_matrix,
    }

    # --- Part 2: Link intersect targets from Report D ---
    logger.info("  R3: Processing link intersect targets...")
    d_configs = {
        'D1_EN': {
            'lang_key': 'EN',
            'config_desc': 'softonic.com + uptodown.com + malavida.com vs freesoft.net',
        },
        'D2_RU': {
            'lang_key': 'RU',
            'config_desc': 'softonic.ru + trashbox.ru vs freesoft.ru',
        },
        'D3_FR': {
            'lang_key': 'FR',
            'config_desc': 'clubic.com + 01net.com + commentcamarche.net vs frees0ft.fr',
        },
    }

    for d_key, d_info in d_configs.items():
        try:
            df_d = load_normalized_d(d_key)
            total_domains = len(df_d)

            # Filter: DR >= 20, Intersect >= 2
            if 'dr' in df_d.columns and 'intersect' in df_d.columns:
                df_d['dr'] = clean_numeric(df_d['dr'])
                df_d['intersect'] = clean_numeric(df_d['intersect'])
                filtered = df_d[(df_d['dr'] >= 20) & (df_d['intersect'] >= 2)].copy()
            else:
                filtered = df_d.copy()

            filtered_count = len(filtered)

            # Sort by DR desc, take top 50
            filtered = filtered.sort_values('dr', ascending=False).head(50)

            top_50 = []
            # Find dynamic columns (domain/ columns)
            static_cols = {'domain', 'dr', 'domain_traffic', 'intersect'}
            dynamic_cols = [c for c in df_d.columns if c not in static_cols]

            for _, row in filtered.iterrows():
                entry = {
                    'domain': str(row.get('domain', '')),
                    'dr': int(row['dr']) if pd.notna(row.get('dr')) else 0,
                    'traffic': int(row['domain_traffic']) if pd.notna(row.get('domain_traffic')) else 0,
                    'intersect': int(row['intersect']) if pd.notna(row.get('intersect')) else 0,
                    'links_to': {},
                }
                for dc in dynamic_cols:
                    val = row.get(dc)
                    if pd.notna(val):
                        try:
                            entry['links_to'][dc.rstrip('/')] = int(float(val))
                        except (ValueError, TypeError):
                            entry['links_to'][dc.rstrip('/')] = str(val)
                top_50.append(entry)

            result['link_intersect_targets'][d_info['lang_key']] = {
                'source_file': d_key,
                'config': d_info['config_desc'],
                'total_domains': total_domains,
                'filtered_dr20_intersect2': filtered_count,
                'top_50': top_50,
            }
        except Exception as e:
            logger.warning(f"  Cannot process {d_key}: {e}")

    # --- Part 3: Multi-competitor domains from Report A ---
    logger.info("  R3: Finding multi-competitor domains...")
    competitor_domains_list = config.COMPETITOR_DOMAINS

    # For each referring domain, count how many competitors it links to
    ref_to_competitors = defaultdict(set)
    ref_dr = {}  # store DR for each ref domain
    for comp in competitor_domains_list:
        if comp in domain_refdomains:
            for rd in domain_refdomains[comp]:
                ref_to_competitors[rd].add(comp)

    # Get DR values from Report A data
    for domain in all_domains:
        try:
            df_a = load_normalized('A', domain)
            if 'domain' in df_a.columns and 'dr' in df_a.columns:
                for _, row in df_a.iterrows():
                    rd = str(row.get('domain', '')).lower()
                    if rd and rd not in ref_dr and pd.notna(row.get('dr')):
                        ref_dr[rd] = int(row['dr'])
        except Exception:
            pass

    # 3+ competitors
    three_plus = []
    exactly_two = []
    for rd, comps in ref_to_competitors.items():
        if len(comps) >= 3:
            three_plus.append({
                'domain': rd,
                'dr': ref_dr.get(rd, 0),
                'links_to_count': len(comps),
                'links_to': sorted(list(comps)),
            })
        elif len(comps) == 2:
            exactly_two.append({
                'domain': rd,
                'dr': ref_dr.get(rd, 0),
                'links_to_count': 2,
                'links_to': sorted(list(comps)),
            })

    # Sort by DR desc, take top 50
    three_plus.sort(key=lambda x: x['dr'], reverse=True)
    exactly_two.sort(key=lambda x: x['dr'], reverse=True)

    result['multi_competitor_domains'] = {
        '3_plus_competitors': {
            'count': len(three_plus),
            'top_50': three_plus[:50],
        },
        'exactly_2_competitors': {
            'count': len(exactly_two),
            'top_50': exactly_two[:50],
        },
    }

    output_path = os.path.join(config.INTERMEDIATE_DIR, 'r3_intersections.json')
    save_json(result, output_path)
    logger.info(f"R3 aggregation complete")

# ──────────────────────────────────────────────
# ЭТАП 3d: R4 — Link Profiles
# ──────────────────────────────────────────────
def classify_anchor(anchor_text, domain):
    """Classify an anchor into branded/exact_match/url/generic/other."""
    anchor_lower = str(anchor_text).lower().strip()

    if not anchor_lower or anchor_lower == 'nan':
        return 'other'

    # URL check
    if any(x in anchor_lower for x in ['http://', 'https://', 'www.', '.com/', '.net/', '.ru/', '.fr/']):
        return 'url'

    # Branded check: contains domain name parts
    domain_parts = domain.replace('.', ' ').replace('0', 'o').split()
    for part in domain_parts:
        if len(part) > 2 and part.lower() in anchor_lower:
            return 'branded'

    # Generic check
    generic_terms = {'click here', 'here', 'see more', 'learn more', 'read more',
                     'link', 'website', 'site', 'visit', 'тут', 'здесь', 'ссылка',
                     'подробнее', 'ici', 'cliquez', 'lien', 'voir', 'plus',
                     'click', 'source', 'this', 'page'}
    if anchor_lower in generic_terms or anchor_lower.strip() in generic_terms:
        return 'generic'

    # Exact match: download keywords
    download_terms = {'download', 'скачать', 'telecharger', 'télécharger', 'descargar',
                      'apk', 'free download', 'install', 'установить', 'get',
                      'baixar', 'indir', 'scaricare'}
    if any(t in anchor_lower for t in download_terms):
        return 'exact_match'

    return 'other'


def aggregate_r4():
    logger.info("=== STEP 3d: R4 AGGREGATION ===")
    result = {
        'metadata': {
            'source_reports': ['A', 'B', 'C'],
            'generated_at': datetime.now().isoformat(),
        },
        'domains': {},
        'niche_benchmarks': {},
    }

    all_domains = list(config.DOMAINS.keys())

    # Collect data for benchmarks
    competitor_stats = {
        'dr_distribution_means': [],
        'dofollow_pcts': [],
        'text_links_pcts': [],
        'branded_anchors_pcts': [],
        'spam_pcts': [],
    }

    for domain in all_domains:
        logger.info(f"  R4: Processing {domain}")
        domain_result = {
            'overview': {
                'total_ref_domains': 0,
                'total_backlinks_sample': 0,
                'ahrefs_limit_hit': False,
                'dr': config.DOMAINS[domain]['dr'],
            },
            'dr_distribution': {'buckets': {}, 'stats': {}},
            'follow_ratio': {},
            'link_types': {},
            'anchor_profile': {'top_20': [], 'type_distribution': {}},
            'link_age': {'buckets': {}, 'growth_last_12m': 0},
            'spam_ratio': {'count': 0, 'pct': 0},
        }

        # --- Load Report A ---
        try:
            df_a = load_normalized('A', domain)
            total_ref_domains = len(df_a)
            domain_result['overview']['total_ref_domains'] = total_ref_domains
            if total_ref_domains == 30000:
                domain_result['overview']['ahrefs_limit_hit'] = True
        except Exception as e:
            logger.warning(f"  Cannot load A for {domain}: {e}")
            df_a = pd.DataFrame()
            total_ref_domains = 0

        # --- Load Report C ---
        try:
            df_c = load_normalized('C', domain)
            total_backlinks = len(df_c)
            domain_result['overview']['total_backlinks_sample'] = total_backlinks
            if total_backlinks == 30000:
                domain_result['overview']['ahrefs_limit_hit'] = True
        except Exception as e:
            logger.warning(f"  Cannot load C for {domain}: {e}")
            df_c = pd.DataFrame()
            total_backlinks = 0

        # --- Load Report B ---
        try:
            df_b = load_normalized('B', domain)
        except Exception as e:
            logger.warning(f"  Cannot load B for {domain}: {e}")
            df_b = pd.DataFrame()

        # --- Metric 1: DR distribution (from Report A) ---
        if 'dr' in df_a.columns and total_ref_domains > 0:
            dr_vals = df_a['dr'].dropna()
            buckets = {}
            bucket_ranges = [(0, 10), (11, 20), (21, 30), (31, 40), (41, 50),
                             (51, 60), (61, 70), (71, 80), (81, 90), (91, 100)]
            for low, high in bucket_ranges:
                label = f"{low}-{high}"
                count = int(((dr_vals >= low) & (dr_vals <= high)).sum())
                pct = round(count / total_ref_domains * 100, 1)
                buckets[label] = {'count': count, 'pct': pct}

            stats = {
                'mean': round(float(dr_vals.mean()), 1) if len(dr_vals) > 0 else 0,
                'median': int(dr_vals.median()) if len(dr_vals) > 0 else 0,
                'p25': int(dr_vals.quantile(0.25)) if len(dr_vals) > 0 else 0,
                'p75': int(dr_vals.quantile(0.75)) if len(dr_vals) > 0 else 0,
            }
            domain_result['dr_distribution'] = {'buckets': buckets, 'stats': stats}

            if not config.DOMAINS[domain]['ours']:
                competitor_stats['dr_distribution_means'].append(stats['mean'])

        # --- Metric 2: Follow ratio (from Report C) ---
        if total_backlinks > 0 and len(df_c) > 0:
            nofollow_count = 0
            ugc_count = 0
            sponsored_count = 0

            if 'nofollow' in df_c.columns:
                nofollow_count = int(df_c['nofollow'].astype(str).str.lower().isin(['true', 'yes', '1']).sum())
            if 'ugc' in df_c.columns:
                ugc_count = int(df_c['ugc'].astype(str).str.lower().isin(['true', 'yes', '1']).sum())
            if 'sponsored' in df_c.columns:
                sponsored_count = int(df_c['sponsored'].astype(str).str.lower().isin(['true', 'yes', '1']).sum())

            dofollow_count = total_backlinks - nofollow_count
            # dofollow_count might still have ugc/sponsored overlap, but this is the standard calc

            domain_result['follow_ratio'] = {
                'dofollow': {'count': dofollow_count, 'pct': round(dofollow_count / total_backlinks * 100, 1)},
                'nofollow': {'count': nofollow_count, 'pct': round(nofollow_count / total_backlinks * 100, 1)},
                'ugc': {'count': ugc_count, 'pct': round(ugc_count / total_backlinks * 100, 1)},
                'sponsored': {'count': sponsored_count, 'pct': round(sponsored_count / total_backlinks * 100, 1)},
            }

            if not config.DOMAINS[domain]['ours']:
                dofollow_pct = round(dofollow_count / total_backlinks * 100, 1)
                competitor_stats['dofollow_pcts'].append(dofollow_pct)

        # --- Metric 3: Link types (from Report C) ---
        if 'type' in df_c.columns and total_backlinks > 0:
            type_counts = df_c['type'].fillna('other').astype(str).str.lower().value_counts()
            link_types = {}
            for t, cnt in type_counts.items():
                link_types[t] = {
                    'count': int(cnt),
                    'pct': round(int(cnt) / total_backlinks * 100, 1),
                }
            domain_result['link_types'] = link_types

            text_pct = link_types.get('text', {}).get('pct', 0)
            if not config.DOMAINS[domain]['ours']:
                competitor_stats['text_links_pcts'].append(text_pct)

        # --- Metric 4: Anchor profile (from Report B) ---
        if len(df_b) > 0 and 'anchor_text' in df_b.columns:
            # Top-20 by ref_domains
            sort_col = 'ref_domains' if 'ref_domains' in df_b.columns else 'links_to_target'
            if sort_col in df_b.columns:
                top_anchors = df_b.nlargest(20, sort_col)
            else:
                top_anchors = df_b.head(20)

            top_20_list = []
            for _, row in top_anchors.iterrows():
                anchor = str(row.get('anchor_text', ''))
                atype = classify_anchor(anchor, domain)
                ref_doms = int(row[sort_col]) if pd.notna(row.get(sort_col)) else 0
                top_20_list.append({
                    'anchor': anchor,
                    'ref_domains': ref_doms,
                    'type': atype,
                })

            # Type distribution across ALL anchors
            all_types = Counter()
            total_anchor_refs = 0
            for _, row in df_b.iterrows():
                anchor = str(row.get('anchor_text', ''))
                atype = classify_anchor(anchor, domain)
                refs = int(row[sort_col]) if sort_col in df_b.columns and pd.notna(row.get(sort_col)) else 1
                all_types[atype] += refs
                total_anchor_refs += refs

            type_dist = {}
            for atype, cnt in all_types.items():
                type_dist[atype] = {
                    'pct': round(cnt / total_anchor_refs * 100, 1) if total_anchor_refs > 0 else 0,
                }

            domain_result['anchor_profile'] = {
                'top_20': top_20_list,
                'type_distribution': type_dist,
            }

            branded_pct = type_dist.get('branded', {}).get('pct', 0)
            if not config.DOMAINS[domain]['ours']:
                competitor_stats['branded_anchors_pcts'].append(branded_pct)

        # --- Metric 5: Link age (from Report A/C) ---
        date_col_source = None
        date_df = None
        if 'first_seen' in df_a.columns and len(df_a) > 0:
            date_df = df_a
            date_col_source = 'A'
        elif 'first_seen' in df_c.columns and len(df_c) > 0:
            date_df = df_c
            date_col_source = 'C'

        if date_df is not None:
            dates = pd.to_datetime(date_df['first_seen'], errors='coerce')
            now = pd.Timestamp.now()
            ages = (now - dates).dt.days / 365.25

            age_buckets = {
                '<1y': int((ages < 1).sum()),
                '1-3y': int(((ages >= 1) & (ages < 3)).sum()),
                '3-5y': int(((ages >= 3) & (ages < 5)).sum()),
                '>5y': int((ages >= 5).sum()),
            }

            # Growth last 12 months
            one_year_ago = now - pd.Timedelta(days=365)
            growth_12m = int((dates >= one_year_ago).sum())

            domain_result['link_age'] = {
                'buckets': age_buckets,
                'growth_last_12m': growth_12m,
            }

        # --- Metric 6: Spam ratio (from Report A) ---
        if 'is_spam' in df_a.columns and total_ref_domains > 0:
            spam_count = int(df_a['is_spam'].astype(str).str.lower().isin(['true', 'yes', '1']).sum())
            spam_pct = round(spam_count / total_ref_domains * 100, 2)
            domain_result['spam_ratio'] = {'count': spam_count, 'pct': spam_pct}

            if not config.DOMAINS[domain]['ours']:
                competitor_stats['spam_pcts'].append(spam_pct)

        result['domains'][domain] = domain_result

    # --- Niche benchmarks (median across 9 competitors) ---
    result['niche_benchmarks'] = {
        'description': 'Медианные значения по 9 конкурентам (без наших доменов)',
        'median_dr_distribution_mean': round(float(np.median(competitor_stats['dr_distribution_means'])), 1) if competitor_stats['dr_distribution_means'] else 0,
        'median_dofollow_pct': round(float(np.median(competitor_stats['dofollow_pcts'])), 1) if competitor_stats['dofollow_pcts'] else 0,
        'median_text_links_pct': round(float(np.median(competitor_stats['text_links_pcts'])), 1) if competitor_stats['text_links_pcts'] else 0,
        'median_branded_anchors_pct': round(float(np.median(competitor_stats['branded_anchors_pcts'])), 1) if competitor_stats['branded_anchors_pcts'] else 0,
        'median_spam_pct': round(float(np.median(competitor_stats['spam_pcts'])), 2) if competitor_stats['spam_pcts'] else 0,
    }

    output_path = os.path.join(config.INTERMEDIATE_DIR, 'r4_link_profiles.json')
    save_json(result, output_path)
    logger.info(f"R4 aggregation complete: {len(result['domains'])} domains")

# ──────────────────────────────────────────────
# ЭТАП 4: ИНВЕНТАРИЗАЦИЯ
# ──────────────────────────────────────────────
def create_inventory():
    logger.info("=== STEP 4: INVENTORY ===")

    # Load validation report for metadata
    vr_path = os.path.join(config.INTERMEDIATE_DIR, 'validation_report.json')
    try:
        with open(vr_path, 'r', encoding='utf-8') as f:
            validation = json.load(f)
    except Exception:
        validation = {'files': []}

    total_rows_raw = sum(f.get('rows', 0) for f in validation.get('files', []))
    ahrefs_limit_files = [
        f"{f['domain']} ({f['report_type']})"
        for f in validation.get('files', [])
        if f.get('ahrefs_limit_hit', False)
    ]

    # Count gambling filtered
    gambling_log_path = os.path.join(config.INTERMEDIATE_DIR, 'gambling_filter_log.json')
    gambling_filtered = 0
    if os.path.exists(gambling_log_path):
        try:
            with open(gambling_log_path, 'r', encoding='utf-8') as f:
                gl = json.load(f)
                gambling_filtered = len(gl)
        except Exception:
            pass

    # Count normalized rows per domain
    per_domain_summary = {}
    all_domains = list(config.DOMAINS.keys())
    total_rows_normalized = 0

    for domain in all_domains:
        slug = domain.replace('.', '_')
        summary = {}
        for rtype, subdir in config.NORMALIZED_SUBDIRS.items():
            if rtype == 'D':
                continue
            path = os.path.join(config.NORMALIZED_DIR, subdir, f"{slug}.tsv")
            if os.path.exists(path):
                try:
                    # Just count lines (faster than loading full file)
                    with open(path, 'r', encoding='utf-8') as f:
                        row_count = sum(1 for _ in f) - 1  # minus header
                    key = f"{rtype}_rows"
                    summary[key] = row_count
                    total_rows_normalized += row_count
                except Exception:
                    pass
        per_domain_summary[domain] = summary

    # Count link intersect rows
    for d_key, out_name in config.LINK_INTERSECT_OUTPUT_NAMES.items():
        path = os.path.join(config.NORMALIZED_DIR, 'link_intersect', out_name)
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    row_count = sum(1 for _ in f) - 1
                total_rows_normalized += row_count
            except Exception:
                pass

    inventory = {
        'total_files': len(config.FILE_TO_DOMAIN),
        'total_rows_raw': total_rows_raw,
        'total_rows_after_gambling_filter': total_rows_normalized,
        'gambling_filtered_rows': gambling_filtered,
        'data_collection_date': '2026-03-13',
        'ahrefs_limit_files': ahrefs_limit_files,
        'per_domain_summary': per_domain_summary,
    }

    output_path = os.path.join(config.INTERMEDIATE_DIR, 'inventory.json')
    save_json(inventory, output_path)
    logger.info(f"Inventory complete: {total_rows_raw} raw rows, {gambling_filtered} gambling filtered")

# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────
def main():
    logger.info("=== PIPELINE START ===")

    output = os.path.join(config.INTERMEDIATE_DIR, 'validation_report.json')
    if not step_complete(output):
        validate_all()
    else:
        logger.info("SKIP: validation already complete")

    normalize_all()  # checkpoint внутри по файлам

    for name, func, filename in [
        ('R1', aggregate_r1, 'r1_language_links.json'),
        ('R2', aggregate_r2, 'r2_pbn_signals.json'),
        ('R3', aggregate_r3, 'r3_intersections.json'),
        ('R4', aggregate_r4, 'r4_link_profiles.json'),
    ]:
        output = os.path.join(config.INTERMEDIATE_DIR, filename)
        if not step_complete(output):
            logger.info(f"Running {name} aggregation...")
            func()
        else:
            logger.info(f"SKIP: {name} aggregation already complete")

    output = os.path.join(config.INTERMEDIATE_DIR, 'inventory.json')
    if not step_complete(output):
        create_inventory()
    else:
        logger.info("SKIP: inventory already complete")

    logger.info("=== PIPELINE COMPLETE ===")

if __name__ == '__main__':
    main()
