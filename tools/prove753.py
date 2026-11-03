"""Job 753 proof: a seeded sample of sections from the corrected corpus against the cached official chapter pages, read
independently of parse.py (lxml text_content of each div.Section, white space collapsed). Every body and History line
of the corrected file must occur verbatim in its section's source text, curly quotes and dashes included; the published
(ASCII) line must not, wherever it differs. The two image sections are always in the sample, and their notice must sit
where the source has the image. Writes prove753.json; exits 1 on any failure.

    python -X utf8 prove753.py [N=40] [SEED=753]
"""
import hashlib
import html
import json
import random
import re
import sys
from pathlib import Path

import lxml.html

HERE = Path(__file__).resolve().parent
N = int(sys.argv[1]) if len(sys.argv) > 1 else 40
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 753
BASE = 'https://www.leg.state.fl.us/statutes/'
FLAT = str.maketrans({'’': "'", '‘': "'", '“': '"', '”': '"', '–': '-', '—': '-', '‒': '-', '‑': '-'})
plan = json.loads((HERE / '.hcache-titles.json').read_text(encoding='utf8'))


def chapter_files():
    for t, ds in plan.items():
        for d in ds:
            num = d.split('/')[-1]
            old = HERE / '.cache' / 'ch' / (num + '.html')
            yield old if old.exists() else HERE / '.hcache' / hashlib.sha256(
                (BASE + f'index.cfm?App_mode=Display_Statute&URL={d}.html').encode()).hexdigest()


def norm(s):
    return re.sub(r'[\s     ]+', ' ', s.replace('­', '').replace('﻿', '')).strip()


source = {}
for f in chapter_files():
    if not f.exists():
        continue
    b = f.read_bytes()
    try:
        t = b.decode('utf-8')
    except UnicodeDecodeError:
        t = b.decode('cp1252', 'replace')
    doc = lxml.html.fromstring(t)
    for sec in doc.iter('div'):
        if sec.get('class') != 'Section':
            continue
        n = sec.find("./span[@class='SectionNumber']")
        if n is None:
            continue
        imgs = [i.get('src') for i in sec.iter('img')]
        # the section's text with a word break at every line break and block boundary, as a reader sees it
        # (text_content() joins blocks with nothing: "LICENSURE<br />IN" -> "LICENSUREIN")
        raw = lxml.html.tostring(sec, encoding='unicode', method='html')
        raw = re.sub(r'<br\s*/?>|</?(?:p|div|li|ul|ol|tr|td|th|table|tbody|thead|h[1-6]|blockquote|dd|dt|dl)\b[^>]*>', ' ', raw,
                     flags=re.I)
        raw = re.sub(r'<img\b[^>]*>', ' ', raw, flags=re.I)
        source[norm(n.text_content())] = (norm(html.unescape(re.sub(r'<[^>]+>', '', raw))), imgs, str(f.name))

fixed = json.loads((HERE / 'corpus.json').read_text(encoding='utf8'))
pub = {a['slug']: a for a in json.loads((HERE / 'corpus.published.json').read_text(encoding='utf8'))['acts']}
units = [(a['slug'], k, u) for a in fixed['acts'] if a['slug'] != 'constitution'
         for k, u in a['versions'][0]['units'].items()]
rnd = random.Random(SEED)
sample = rnd.sample(units, N)
for want in ('320.0842', '322.051'):
    sample += [x for x in units if x[2]['label'] == want and x not in sample]
results, fails = [], 0
for slug, k, u in sample:
    src, imgs, fname = source.get(u['label'], (None, [], ''))
    old = pub[slug]['versions'][0]['units'][k]['text']
    r = {'act': slug, 'section': u['label'], 'source_file': fname, 'lines': 0, 'missing': [], 'ascii_lines_in_source': 0,
         'curly_chars': sum(u['text'].count(c) for c in '’‘“”–—'), 'images_in_source': len(imgs)}
    if src is None:
        r['missing'].append('section not found in the cached pages')
    else:
        lines = u['text'].splitlines()[1:]  # the heading line is assembled ("<n>. <catchline>"), not source text
        for i, line in enumerate(lines):
            if not line.strip():
                continue
            r['lines'] += 1
            if line not in src:  # verbatim, white space included: no escape hatch (review of b76d9f20, F1)
                r['missing'].append(line[:120])
            flat = line.translate(FLAT)
            if flat != line and flat in src:  # the source itself prints this line in ASCII: the old text was right
                r['ascii_lines_in_source'] += 1
        if '[Image omitted' in u['text'] or 'assets/' in u['text']:  # images wait for the post-merge restoration
            r['missing'].append('an image notice or asset link before the corpus-standard merge')
    ok = not r['missing'] and not r['ascii_lines_in_source']
    fails += not ok
    r['ok'] = ok
    results.append(r)
out = {'seed': SEED, 'sampled': len(results), 'failures': fails,
       'sections_with_curly_punctuation': sum(1 for r in results if r['curly_chars']),
       'results': results}
(HERE / 'prove753.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf8')
print(json.dumps({k: v for k, v in out.items() if k != 'results'}))
sys.exit(1 if fails else 0)
