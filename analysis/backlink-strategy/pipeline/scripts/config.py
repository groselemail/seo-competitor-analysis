import os

# === ПУТИ ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# BASE_DIR = analysis/backlink-strategy/
DATA_DIR = os.path.join(BASE_DIR, '..', '..', 'data_for_task', 'backlinks')
PIPELINE_DIR = os.path.join(BASE_DIR, 'pipeline')
NORMALIZED_DIR = os.path.join(PIPELINE_DIR, 'normalized')
INTERMEDIATE_DIR = os.path.join(PIPELINE_DIR, 'intermediate')
SECTIONS_DIR = os.path.join(PIPELINE_DIR, 'sections')

# === REPORT TYPE -> DIRECTORY ===
REPORT_DIRS = {
    'A': 'referring_domains',
    'B': 'anchors',
    'C': 'backlinks_one_per_domain',
    'D': 'link_intersect',
}

# Normalized output subdirectories
NORMALIZED_SUBDIRS = {
    'A': 'referring_domains',
    'B': 'anchors',
    'C': 'backlinks',
    'D': 'link_intersect',
}

# === ДОМЕНЫ ===
DOMAINS = {
    # Наши
    'freesoft.net':  {'dr': 51, 'lang': 'EN', 'ours': True},
    'freesoft.ru':   {'dr': 59, 'lang': 'RU', 'ours': True},
    'frees0ft.fr':   {'dr': 23, 'lang': 'FR', 'ours': True},
    # Конкуренты
    'softonic.com':  {'dr': 86, 'lang': 'MULTI', 'ours': False},
    'uptodown.com':  {'dr': 83, 'lang': 'MULTI', 'ours': False},
    'malavida.com':  {'dr': 74, 'lang': 'MULTI', 'ours': False},
    'softonic.ru':   {'dr': 37, 'lang': 'RU', 'ours': False},
    'trashbox.ru':   {'dr': 45, 'lang': 'RU', 'ours': False},
    'filehippo.com': {'dr': 75, 'lang': 'EN', 'ours': False},
    'clubic.com':    {'dr': 76, 'lang': 'FR', 'ours': False},
    '01net.com':     {'dr': 79, 'lang': 'FR', 'ours': False},
    'commentcamarche.net': {'dr': 81, 'lang': 'FR', 'ours': False},
}

OUR_DOMAINS = [d for d, info in DOMAINS.items() if info['ours']]
COMPETITOR_DOMAINS = [d for d, info in DOMAINS.items() if not info['ours']]

# === FILE_TO_DOMAIN ===
FILE_TO_DOMAIN = {
    # Report A (Referring Domains)
    'freesoft.net-refdomains-subdomains_2026-03-13_09-56-45.csv': ('freesoft.net', 'A'),
    'freesoft.ru-refdomains-subdomains_2026-03-13_09-57-21.csv': ('freesoft.ru', 'A'),
    'frees0ft.fr-refdomains-subdomains_2026-03-13_09-56-03.csv': ('frees0ft.fr', 'A'),
    'softonic.com-refdomains-subdomains_2026-03-13_09-57-51.csv': ('softonic.com', 'A'),
    'uptodown.com-refdomains-subdomains_2026-03-13_09-58-19.csv': ('uptodown.com', 'A'),
    'malavida.com-refdomains-subdomains_2026-03-13_09-58-40.csv': ('malavida.com', 'A'),
    'softonic.ru-refdomains-subdomains_2026-03-13_09-59-05.csv': ('softonic.ru', 'A'),
    'trashbox.ru-refdomains-subdomains_2026-03-13_09-59-29.csv': ('trashbox.ru', 'A'),
    'filehippo.com-refdomains-subdomains_2026-03-13_09-59-53.csv': ('filehippo.com', 'A'),
    'clubic.com-refdomains-subdomains_2026-03-13_10-00-12.csv': ('clubic.com', 'A'),
    '01net.com-refdomains-subdomains_2026-03-13_10-00-37.csv': ('01net.com', 'A'),
    'commentcamarche_net_refdomains_subdomains_2026_03_13_10_01_00.csv': ('commentcamarche.net', 'A'),
    # Report B (Anchors)
    'freesoft.net-anchors-subdomains_2026-03-13_10-07-25.csv': ('freesoft.net', 'B'),
    'freesoft.ru-anchors-subdomains_2026-03-13_10-07-05.csv': ('freesoft.ru', 'B'),
    'frees0ft.fr-anchors-subdomains_2026-03-13_10-06-48.csv': ('frees0ft.fr', 'B'),
    'softonic.com-anchors-subdomains_2026-03-13_10-06-26.csv': ('softonic.com', 'B'),
    'uptodown.com-anchors-subdomains_2026-03-13_10-05-45.csv': ('uptodown.com', 'B'),
    'malavida.com-anchors-subdomains_2026-03-13_10-05-20.csv': ('malavida.com', 'B'),
    'softonic.ru-anchors-subdomains_2026-03-13_10-03-34.csv': ('softonic.ru', 'B'),
    'trashbox.ru-anchors-subdomains_2026-03-13_10-03-14.csv': ('trashbox.ru', 'B'),
    'filehippo.com-anchors-subdomains_2026-03-13_10-02-52.csv': ('filehippo.com', 'B'),
    'clubic.com-anchors-subdomains_2026-03-13_10-02-26.csv': ('clubic.com', 'B'),
    '01net.com-anchors-subdomains_2026-03-13_10-02-04.csv': ('01net.com', 'B'),
    'commentcamarche.net-anchors-subdomains_2026-03-13_10-01-29.csv': ('commentcamarche.net', 'B'),
    # Report C (Backlinks One Per Domain)
    'freesoft.net-backlinks-subdomains_2026-03-13_10-15-44.csv': ('freesoft.net', 'C'),
    'freesoft.ru-backlinks-subdomains_2026-03-13_10-16-14.csv': ('freesoft.ru', 'C'),
    'frees0ft.fr-backlinks-subdomains_2026-03-13_10-16-42.csv': ('frees0ft.fr', 'C'),
    'softonic.com-backlinks-subdomains_2026-03-13_10-17-08.csv': ('softonic.com', 'C'),
    'uptodown.com-backlinks-subdomains_2026-03-13_10-17-37.csv': ('uptodown.com', 'C'),
    'malavida.com-backlinks-subdomains_2026-03-13_10-18-05.csv': ('malavida.com', 'C'),
    'softonic.ru-backlinks-subdomains_2026-03-13_10-18-28.csv': ('softonic.ru', 'C'),
    'trashbox.ru-backlinks-subdomains_2026-03-13_10-19-35.csv': ('trashbox.ru', 'C'),
    'filehippo.com-backlinks-subdomains_2026-03-13_10-20-02.csv': ('filehippo.com', 'C'),
    'clubic.com-backlinks-subdomains_2026-03-13_10-20-26.csv': ('clubic.com', 'C'),
    '01net.com-backlinks-subdomains_2026-03-13_10-20-53.csv': ('01net.com', 'C'),
    'commentcamarche.net-backlinks-subdomains_2026-03-13_10-21-28.csv': ('commentcamarche.net', 'C'),
    # Report D (Link Intersect) — только эти 3 файла!
    'freesoft_net_link_intersect_refdomains_subdo_2026_03_13_10_26_36.csv': ('D1_EN', 'D'),
    'freesoft_ru_link_intersect_refdomains_subdom_2026_03_13_10_28_53.csv': ('D2_RU', 'D'),
    'frees0ft_fr_link_intersect_refdomains_subdom_2026_03_13_10_29_48.csv': ('D3_FR', 'D'),
}

# === LINK_INTERSECT_FILES ===
LINK_INTERSECT_FILES = {
    "D1_EN": "freesoft_net_link_intersect_refdomains_subdo_2026_03_13_10_26_36.csv",
    "D2_RU": "freesoft_ru_link_intersect_refdomains_subdom_2026_03_13_10_28_53.csv",
    "D3_FR": "frees0ft_fr_link_intersect_refdomains_subdom_2026_03_13_10_29_48.csv",
}

# Link intersect output names
LINK_INTERSECT_OUTPUT_NAMES = {
    "D1_EN": "en_top3_vs_freesoft_net.tsv",
    "D2_RU": "ru_vs_freesoft_ru.tsv",
    "D3_FR": "fr_vs_frees0ft_fr.tsv",
}

# === COLUMN_MAP_A/B/C/D ===
COLUMN_MAP_A = {
    '"Domain"': 'domain', 'Domain': 'domain',
    'Is spam': 'is_spam', 'DR': 'dr',
    'Dofollow ref. domains': 'dofollow_ref_domains',
    'Dofollow linked domains': 'dofollow_linked_domains',
    'Traffic ': 'traffic', 'Traffic': 'traffic',
    'Keywords ': 'keywords', 'Keywords': 'keywords',
    'Links to target': 'links_to_target',
    'Dofollow links': 'dofollow_links',
    'First seen': 'first_seen', 'Lost': 'lost',
}

COLUMN_MAP_B = {
    'Anchor text': 'anchor_text',
    'Ref. domains': 'ref_domains',
    'Top DR': 'top_dr',
    'Ref. pages': 'ref_pages',
    'Links to target': 'links_to_target',
    'Dofollow links': 'dofollow_links',
    'First seen': 'first_seen',
    'Lost': 'lost',
}

COLUMN_MAP_C = {
    'Referring page title': 'referring_page_title',
    'Referring page URL': 'referring_page_url',
    'Language': 'language',
    'Platform': 'platform',
    'Referring page HTTP code': 'http_code',
    'Domain rating': 'dr',
    'UR': 'ur',
    'Domain traffic': 'domain_traffic',
    'Referring domains': 'referring_domains',
    'Linked domains': 'linked_domains',
    'External links': 'external_links',
    'Page traffic': 'page_traffic',
    'Keywords': 'keywords',
    'Target URL': 'target_url',
    'Left context': 'left_context',
    'Anchor': 'anchor',
    'Right context': 'right_context',
    'Redirect Chain URLs': 'redirect_chain_urls',
    'Redirect Chain status codes': 'redirect_chain_codes',
    'Type': 'type',
    'Is spam': 'is_spam',
    'Content': 'content',
    'Nofollow': 'nofollow',
    'UGC': 'ugc',
    'Sponsored': 'sponsored',
    'Rendered': 'rendered',
    'Raw': 'raw',
    'Lost status': 'lost_status',
    'Drop reason': 'drop_reason',
    'Discovered status': 'discovered_status',
    'First seen': 'first_seen',
    'Last seen': 'last_seen',
    'Lost': 'lost',
    'Author': 'author',
    'Page type': 'page_type',
    'Page category': 'page_category',
    'Links in group': 'links_in_group',
}
# 37 колонок!

COLUMN_MAP_D = {
    'Domain': 'domain',
    'Domain rating': 'dr',
    'Domain traffic': 'domain_traffic',
    'Intersect': 'intersect',
}

# === GAMBLING FILTER ===
GAMBLING_PATTERNS = {
    'strict': r'(?i)\b(bets|betting|slots|adult)\b',
    'loose': r'(?i)(casino|gambling|poker|roulette|jackpot|porn|xxx|nsfw|букмекер|казино|ставки|порно)',
}

GAMBLING_FILTER_FIELDS = {
    'A': ['domain'],
    'B': ['anchor_text'],
    'C': ['referring_page_url', 'anchor', 'target_url'],
    'D': ['domain'],
}
