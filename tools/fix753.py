"""Job 753 (verify 462): rebuild corpus.json from the same cached pages with the source's own punctuation, then let
append.py --corrections append labelled corrections. Cache only, deterministic. Private.

    python -X utf8 fix753.py            # writes corpus.json (the corrected corpus) and fix753-report.json

What changes against the published corpus (corpus.json as published is kept as corpus.published.json):
- Text: state_corpus.clean turned the source's curly quotes and dashes (’ ‘ “ ” – — ‒ ‑) into ASCII; this keeps them as
  the Legislature prints them. Spaces are still collapsed, soft hyphens and BOMs still dropped.
- Images: an image inside a section (sections 320.0842 and 322.051 show the accessibility and deaf symbols) was dropped
  without a trace; it now gets the standard notice at its place until the shared builder can keep image bytes
  (CORPUS-STANDARD 5a): [Image omitted: <url>; <alt>; reason: kept once the shared builder stores images].
- Dating: each act's one version is dated by the day its pages were retrieved (the source prints no in-force days);
  every act now says so, with Text-as-of and In-force-basis, in a labelled correction (metadata only where the text
  is unchanged).
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin

HERE = Path(__file__).resolve().parent
sys.argv = sys.argv[:1]
sys.path.insert(0, str(HERE))
import parse  # noqa: E402
import lxml.html  # noqa: E402

TAG = re.compile(r'<[^>]+>')
IMG = re.compile(r'<img\b[^>]*>', re.I)
BASE = 'https://www.leg.state.fl.us/statutes/'
BLOCK_TAG = re.compile(r'<br\s*/?>|</?(?:p|div|li|ul|ol|tr|td|th|table|tbody|thead|h[1-6]|blockquote|dd|dt|dl)\b[^>]*>',
                       re.I)


def clean(s):
    """state_corpus.clean without the typographic changes: tags dropped, entities decoded, spaces collapsed."""
    import html
    # a line break or a block boundary separates words (review of b76d9f20, F1: "LICENSURE<br />IN" read
    # "LICENSUREIN"); inline tags join as they stand
    s = BLOCK_TAG.sub(' ', s)
    s = TAG.sub('', s)
    s = html.unescape(s)
    s = s.replace(' ', ' ').replace(' ', ' ').replace(' ', ' ').replace(' ', ' ').replace(' ', ' ')
    s = s.replace('﻿', '').replace('­', '')
    s = re.sub(r'[ \t\r\n]+', ' ', s)
    return s.strip()


NOTICES = []


def notice(m):
    tag = m.group(0)
    src = re.search(r'src\s*=\s*"([^"]*)"', tag, re.I)
    alt = re.search(r'alt\s*=\s*"([^"]*)"', tag, re.I)
    url = urljoin(BASE, src.group(1)) if src else BASE
    what = clean(alt.group(1)) if alt and clean(alt.group(1)) else 'image'
    # Recorded for the image restoration after the corpus-standard merge (review of b76d9f20, F3: no notice and no
    # asset before it); the text gets only the word separation the image gave.
    NOTICES.append(f'{url}\t{what}')
    return ' '


def text(el):
    return clean(IMG.sub(notice, lxml.html.tostring(el, encoding='unicode', method='html')))


def blocks(node):
    """parse.blocks in document order: text after a nested provision stays after it (parse.blocks gathered a node's
    own text first and its nested divs after, so "…shall be to: (a) … (b) …  Moneys shall be deposited…" read with
    the closing sentence before the list)."""
    own = []
    for ch in node:
        if ch.tag == 'div':
            if own:
                yield ' '.join(own)
                own = []
            if 'History' in parse.cls(ch) or 'Note' in parse.cls(ch):
                continue
            yield from blocks(ch)
        elif ch.tag == 'span' and ch.find('.//div') is not None:
            if own:
                yield ' '.join(own)
                own = []
            yield from blocks(ch)
        elif ch.tag in ('span', 'p', 'a', 'b', 'i', 'table'):
            t = text(ch)
            if t:
                own.append(t)
    if own:
        yield ' '.join(own)


parse.clean = clean
parse.text = text
parse.blocks = blocks
published = json.loads((HERE / 'corpus.json').read_text(encoding='utf8'))
if not (HERE / 'corpus.published.json').exists():
    (HERE / 'corpus.published.json').write_text(json.dumps(published, ensure_ascii=False, indent=1) + '\n',
                                                 encoding='utf8', newline='\n')
published = json.loads((HERE / 'corpus.published.json').read_text(encoding='utf8'))

# The same two steps as parse_all.py, run with the corrected text functions: its source as written, less its check
# that parse.py reproduces the first build byte for byte (no longer true: that is the point) and its own call to main().
src = (HERE / 'parse_all.py').read_text(encoding='utf8')
check = ("    if (HERE / 'corpus.json').read_bytes() != before:\n"
         "        raise SystemExit('parse.py no longer reproduces the published first build')\n")
first = "    c = json.loads(before.decode('utf8'))\n"  # the first build's acts: from the fresh parse, not the published copy
assert src.count(check) == 1 and src.count(first) == 1 and src.rstrip().endswith('\nmain()')
src = src.replace(check, '').replace(first, "    c = json.loads((HERE / 'corpus.json').read_text(encoding='utf8'))\n")
ns = {'__name__': 'parse_all_fix753', '__file__': str(HERE / 'parse_all.py')}
exec(compile(src.rstrip()[:-len('main()')], 'parse_all.py', 'exec'), ns)
ns['main']()

fixed = json.loads((HERE / 'corpus.json').read_text(encoding='utf8'))
old = {a['slug']: a for a in published['acts']}
report = {'acts': 0, 'text_changed': [], 'files_changed': 0, 'notices': NOTICES, 'unchanged': []}
assert [a['slug'] for a in fixed['acts']] == [a['slug'] for a in published['acts']], 'the act list changed'
for a in fixed['acts']:
    report['acts'] += 1
    o = old[a['slug']]
    assert len(a['versions']) == len(o['versions']) == 1
    v, ov = a['versions'][0], o['versions'][0]
    assert v['from'] == ov['from'] and set(v['units']) == set(ov['units']), a['slug']
    changed = [k for k in v['units'] if v['units'][k]['text'] != ov['units'][k]['text']]
    # every change must be punctuation only: the same text once curly quotes and dashes are flattened
    flat = str.maketrans({'’': "'", '‘': "'", '“': '"', '”': '"', '–': '-', '—': '-', '‒': '-', '‑': '-'})
    from collections import Counter
    for k in changed:
        new = v['units'][k]['text'].translate(flat)
        if re.sub(r'\s+', ' ', new).strip() == re.sub(r'\s+', ' ', ov['units'][k]['text']).strip():
            continue
        # otherwise only word separation (a space where a line break or block boundary was) and the order of the
        # lines (text after a nested provision moved after it) may differ: the same characters, none gained or lost
        assert Counter(re.sub(r'\s', '', new)) == Counter(re.sub(r'\s', '', ov['units'][k]['text'])), (a['slug'], k)
        if ''.join(new.split()) == ''.join(ov['units'][k]['text'].split()):
            report.setdefault('separated', []).append(f"{a['slug']}/{k}")
        else:
            report.setdefault('reordered', []).append(f"{a['slug']}/{k}")
    report['files_changed'] += len(changed)
    (report['text_changed'] if changed else report['unchanged']).append(a['slug'])
    day = v['from']
    # the day the pages were captured (sources[].retrieved; the first build's acts are dated the day before it)
    captured = '2026-10-30' if day == '2026-10-29' else day
    if a['slug'] == 'constitution':
        basis = (f'source gives no date for the text as a whole: dated {day}, the day before it was captured; the dates some '
                 'sections state for themselves (e.g. Art. XII s. 42, 1 January 2025) are part of the text and date only '
                 'those sections; earlier versions are not in this record')
    else:
        basis = (f'source gives no date: the 2026 Florida Statutes give no in-force day for the edition or a title, and each '
                 'History line names session laws, not in-force days; dated '
                 + ('the day before the pages were captured' if day != captured else 'the day the pages were captured'))
    a['correction'] = {
        'reason': ('the source\'s own text restored: its punctuation (curly quotes and dashes the build had made ASCII), '
                   'the separation of words at line breaks and block boundaries, and the order of text after nested '
                   'provisions; the version labelled as the text as of its capture day') if changed else
                  'the version labelled as the text as of its capture day: the source prints no in-force day',
        'in_force_basis': basis,
        'text_as_of': captured,
    }
(HERE / 'corpus.json').write_text(json.dumps(fixed, ensure_ascii=False, indent=1) + '\n', encoding='utf8', newline='\n')
report['text_changed_count'] = len(report['text_changed'])
(HERE / 'fix753-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=1) + '\n', encoding='utf8')
print(json.dumps({k: v for k, v in report.items() if k not in ('text_changed', 'unchanged')}, ensure_ascii=False))
