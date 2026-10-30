import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'world-law'))
from state_docs import write_docs

c = json.load(open(os.path.join(HERE, 'corpus.json'), encoding='utf-8'))
acts = []
for a in c['acts']:
    v = a['versions'][0]
    acts.append({'folder': a['slug'], 'title': a['title'] + f" ({len(v['units'])} sections)", 'versions': 1,
                 'history': "One version: the text as the Florida Legislature publishes it in the 2026 Florida Statutes, retrieved 30 October 2026"})
write_docs(HERE, {
    'name': 'Florida', 'code': 'FL', 'slug': 'united-states-florida', 'date': '2026-10-30', 'domain': 'statutes-florida',
    'publisher': 'the Florida Legislature (Online Sunshine)',
    'acts': acts,
    'build': 'built: Florida Constitution and Statutes Titles XXXVI, XL and XLVI, 2026 Florida Statutes, current text only (one version each)',
    'source': ("The text is read from **Online Sunshine**, <https://www.leg.state.fl.us/statutes/>, where the **Florida Legislature** "
              "publishes the Constitution and the 2026 Florida Statutes. Its robots.txt (30 October 2026) disallows only `/employees/` "
              "(and two named bots) and sets no crawl delay. Each chapter was fetched once through the site's \"View Entire Chapter\" "
              "link and the Constitution as one page, 94 requests in all, about 1.5 seconds apart. Each section keeps its catchline, its "
              "text with subsection, paragraph and subparagraph designators, its History line (the session laws behind it) and any "
              "Note the Legislature prints inside the section. Footnote markers are dropped."),
    'dates': ("- Each act has **one version**, dated 29 October 2026, the last full day before the pages were retrieved on 30 October "
              "2026 (the site prints no edition date, and no commit is dated ahead of the build). It is the oldest version available in "
              "this build: earlier years' statutes exist online (1997 onward) but are not in it.\n"
              "- The first commit of each act is credited to the Florida Legislature as \"oldest version available\".\n"
              "- The session laws in each History line are part of the text, not the commit dates."),
    'limits': ("- Any amendment history: the Statutes before the 2026 edition.\n"
              "- The other 44 titles of the Florida Statutes, the Laws of Florida and regulations.\n"
              "- Nothing here is an official publication."),
    'licence': ("The legal text is the Constitution of the State of Florida and Titles XXXVI, XL and XLVI of the 2026 Florida Statutes "
                "as published by the Florida Legislature at https://www.leg.state.fl.us/statutes/. Statutes are not copyrightable "
                "(Georgia v. Public.Resource.Org, Inc., 590 U.S. 255 (2020)). The text is republished unaltered in its wording, with "
                "credit to the Florida Legislature as its publisher."),
})
