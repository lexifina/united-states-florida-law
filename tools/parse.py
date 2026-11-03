"""Read the cached Online Sunshine pages into corpus.json (no network; deterministic).

    python parse.py
Acts: the Florida Constitution and Florida Statutes Title XXXVI (business organizations), Title XL (real and personal
property) and Title XLVI (crimes), from the 2026 Florida Statutes as published by the Florida Legislature. Each act has
one version (the oldest available), credited to the publisher. Each section is one unit: heading, then one provision per
line (subsections, paragraphs and subparagraphs keep their designators), then the History line and any Note.
"""
import json, os, re, sys
import lxml.html
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'world-law'))
from state_corpus import clean, unit_key, add_unit, sha256_bytes, write  # noqa: E402

CACHE = os.path.join(HERE, '.cache')
LOG = json.load(open(os.path.join(CACHE, 'fetch-log.json')))
DAY = '2026-10-29'
TITLES = [('XXXVI', 'title-36-business-organizations', 'Florida Statutes, Title XXXVI: Business Organizations', 'Fla. Stat. XXXVI'),
          ('XL', 'title-40-real-and-personal-property', 'Florida Statutes, Title XL: Real and Personal Property', 'Fla. Stat. XL'),
          ('XLVI', 'title-46-crimes', 'Florida Statutes, Title XLVI: Crimes', 'Fla. Stat. XLVI')]


def load(path):
    b = open(path, 'rb').read()
    try:
        t = b.decode('utf-8')
    except UnicodeDecodeError:
        t = b.decode('cp1252', 'replace')
    return b, t


def text(el):
    return clean(lxml.html.tostring(el, encoding='unicode', method='html'))


def cls(el):
    return (el.get('class') or '').split()


def blocks(node):
    """Lines for the provisions below node: direct text spans make one line; child divs make their own lines."""
    own, subs = [], []
    for ch in node:
        if ch.tag == 'div':
            subs.append(ch)
        elif ch.tag == 'span' and ch.find('.//div') is not None:
            sub = list(blocks(ch))
            if own:
                yield ' '.join(own)
                own = []
            yield from sub
        elif ch.tag in ('span', 'p', 'a', 'b', 'i'):
            t = text(ch)
            if t:
                own.append(t)
        elif ch.tag == 'table':
            t = text(ch)
            if t:
                own.append(t)
    if own:
        yield ' '.join(own)
    for d in subs:
        if 'History' in cls(d) or 'Note' in cls(d):
            continue
        yield from blocks(d)


def tail_lines(sec):
    out = []
    for d in sec.findall('./div'):
        c = cls(d)
        if 'History' in c or 'Note' in c:
            t = text(d)
            t = re.sub(r'^(History\.|Note\.)\s*-\s*', r'\1-', t)
            if t:
                out.append(t)
    return out


def section_unit(sec, heading_num):
    num_el = sec.find("./span[@class='SectionNumber']")
    cat = sec.find(".//span[@class='CatchlineText']")
    catch = text(cat) if cat is not None else ''
    body = sec.find("./span[@class='SectionBody']")
    lines = list(blocks(body)) if body is not None else []
    lines += tail_lines(sec)
    return catch, lines


def parse_chapter(num):
    b, t = load(os.path.join(CACHE, 'ch', num + '.html'))
    doc = lxml.html.fromstring(t)
    out = []
    for sec in doc.iter('div'):
        if 'Section' not in cls(sec) or sec.get('class') != 'Section':
            continue
        n_el = sec.find("./span[@class='SectionNumber']")
        if n_el is None:
            continue
        number = text(n_el)
        catch, lines = section_unit(sec, number)
        out.append((number, catch, lines))
    return b, out


def parse_title(tcode):
    units, h = {}, b''
    chapters = sorted(n.split('/')[-1] for n, t in LOG['chapters'].items() if t == tcode)
    for num in chapters:
        b, secs = parse_chapter(num)
        h += num.encode() + b'\0' + sha256_bytes(b).encode()
        for number, catch, lines in secs:
            heading = f'# {number}. {catch}'.rstrip()
            add_unit(units, unit_key(number), {'label': number, 'kind': 'section',
                                              'text': '\n'.join([heading] + lines) + '\n'})
    return units, sha256_bytes(h)


def parse_constitution():
    b, t = load(os.path.join(CACHE, 'const.html'))
    doc = lxml.html.fromstring(t)
    units = {}
    pre = doc.xpath("//div[@class='Preamble']")
    if pre:
        lines = [text(p) for p in pre[0].findall('./p')]
        add_unit(units, 'preamble', {'label': 'Preamble', 'kind': 'preamble', 'text': '\n'.join(['# Preamble'] + [l for l in lines[1:] if l]) + '\n'})
    for art in doc.xpath("//div[@class='Article']"):
        anum = text(art.find("./div[@class='ArticleNumber']"))
        aname = text(art.find("./div[@class='ArticleName']"))
        roman = re.sub(r'^ARTICLE\s+', '', anum)
        for sec in art.findall("./div[@class='Section']"):
            a = sec.find("./span[@class='SectionNumber']/a")
            sn = text(a) if a is not None else ''
            name = a.get('name') if a is not None else ''
            m = re.match(r'^A(\d+)S(\w+)$', name or '')
            catch, lines = section_unit(sec, sn)
            sno = re.sub(r'^SECTION\s+', '', sn).rstrip('.')
            label = f'Art. {roman}, Sec. {sno}'
            heading = f'# {label}. {catch}'.rstrip()
            key = f'art-{int(m.group(1)):02d}-sec-{m.group(2).lower()}' if m else unit_key(label, 'art')
            add_unit(units, key, {'label': label, 'kind': 'section', 'text': '\n'.join([heading] + lines) + '\n'})
    return units, sha256_bytes(b)


def main():
    acts = []
    units, digest = parse_constitution()
    print('constitution', len(units))
    acts.append({'slug': 'constitution', 'short': 'Fla. Const.', 'title': 'Constitution of the State of Florida',
                 'url': 'https://www.leg.state.fl.us/statutes/index.cfm?Mode=Constitution&Submenu=3&Tab=statutes',
                 'first_law': None, 'earlier_laws': [],
                 'versions': [{'from': DAY, 'source_url': 'https://www.leg.state.fl.us/statutes/index.cfm?Mode=Constitution&Submenu=3&Tab=statutes',
                               'sha256': digest, 'units': units,
                               'note': 'Current text as published by the Florida Legislature (Online Sunshine); earlier versions are not in this build.'}]})
    for tcode, slug, title, short in TITLES:
        units, digest = parse_title(tcode)
        print(tcode, len(units), len([k for k in units if '-dup' in k]), 'dups')
        acts.append({'slug': slug, 'short': short, 'title': title,
                     'url': f'https://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Index&Title_Request={tcode}',
                     'first_law': None, 'earlier_laws': [],
                     'versions': [{'from': DAY, 'source_url': f'https://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Index&Title_Request={tcode}',
                                   'sha256': digest, 'units': units,
                                   'note': 'The 2026 Florida Statutes as published by the Florida Legislature (Online Sunshine); earlier editions are not in this build.'}]})
    corpus = {
        'country': {'code': 'US-FL', 'name': 'Florida', 'slug': 'united-states-florida', 'lang': 'en', 'tz': 'America/New_York',
                    'future_branch': 'future',
                    'publisher': {'name': 'Florida Legislature (Online Sunshine)', 'email': 'legislature@statutes-florida.invalid'},
                    'default_in_force_rule': {'text': 'Fla. Stat. 11.2421: the Florida Statutes are adopted annually; a session law takes effect on the date it states, otherwise on the 60th day after the legislature adjourns (Fla. Const. art. III, s. 9); this first build holds only the 2026 Florida Statutes as published, dated by the day before retrieval',
                                              'source': 'https://www.leg.state.fl.us/statutes/'},
                    'licence_note': 'The 2026 Florida Statutes, The Florida Legislature, https://www.leg.state.fl.us/statutes/ (statutory text only).'},
        'sources': [{'name': 'Online Sunshine: The Florida Constitution and the 2026 Florida Statutes (The Florida Legislature)',
                     'url': 'https://www.leg.state.fl.us/statutes/', 'retrieved': '2026-10-30', 'requests': LOG['requests'],
                     'licence': 'Statute text is not copyrightable (Georgia v. Public.Resource.Org, 2020). The Legislature publishes the Florida Statutes and the Constitution for free public use; its footer reads "Copyright 1995-2026 The Florida Legislature" and no annotations are taken.',
                     'notes': 'Each chapter comes from its View Entire Chapter page.'}],
        'laws': {}, 'acts': acts, 'applies': [],
        'decisions': ['First build: only the Constitution and Titles XXXVI (business organizations), XL (real and personal property) and XLVI (crimes) of the 2026 Florida Statutes, as retrieved on 2026-10-30. Each act has one version, credited to the publisher as the oldest version available.',
                      'The version is dated 2026-10-29, the last full day before retrieval, so that no commit is dated ahead of the build; the site prints no edition date.',
                      'Each section keeps its History line (the session laws behind it) and any editors\' Note the Legislature prints inside the section; no annotations are taken.'],
        'ai_use': ['none']}
    write(os.path.join(HERE, 'corpus.json'), corpus)


if __name__ == '__main__':
    main()
