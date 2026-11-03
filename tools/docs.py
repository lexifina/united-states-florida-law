import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'world-law'))
from state_docs import write_docs

c = json.load(open(os.path.join(HERE, 'corpus.json'), encoding='utf-8'))
acts = []
for a in c['acts']:
    v = a['versions'][0]
    acts.append({'folder': a['slug'], 'title': a['title'] + f" ({len(v['units'])} sections)", 'versions': 1,
                 'history': "One version: the text as the Florida Legislature publishes it in the 2026 Florida Statutes, "
                            + ("captured 30 October 2026 (dated 29 October)" if v['from'] == '2026-10-29' else "captured 3 November 2026")
                            + "; the source gives no in-force day for it"})
write_docs(HERE, {
    'name': 'Florida', 'code': 'FL', 'slug': 'united-states-florida', 'date': '2026-11-03', 'domain': 'statutes-florida',
    'publisher': 'the Florida Legislature (Online Sunshine)',
    'acts': acts,
    'build': 'built: the Florida Constitution and all 49 titles of the 2026 Florida Statutes, current text only (one version each)',
    'source': ("The text is read from **Online Sunshine**, <https://www.leg.state.fl.us/statutes/>, where the **Florida Legislature** "
              "publishes the Constitution and the 2026 Florida Statutes. Each chapter comes from the site's \"View Entire Chapter\" "
              "page and the Constitution from one page. Each section keeps its catchline, its "
              "text with subsection, paragraph and subparagraph designators in the order the page gives them, its History line "
              "(the session laws behind it) and any Note the Legislature prints inside the section, with the page's own "
              "punctuation (curly quotes and dashes) and a word break wherever the page breaks a line. Footnote markers are dropped. "
              "Two sections show an image (sections 320.0842 and 322.051, the accessibility and deaf symbols); the images are "
              "not in this record yet and will be added, byte for byte, once the shared builder stores images."),
    'dates': ("- Each act has **one version**, the text as the pages showed it when captured: the Constitution and Titles XXXVI, XL "
              "and XLVI were captured on 30 October 2026 and are dated 29 October, the day before; the other titles were captured "
              "and are dated on 3 November 2026. The site prints no in-force day for the edition or a title, so these are capture "
              "days (`Text-as-of`), not days the text took effect; the correction commits say so (`In-force-basis`). Dates some "
              "sections state for themselves (such as Art. XII s. 42 of the Constitution) are part of their text. Earlier "
              "editions (1997 onward) are online but not in this record.\n"
              "- The first commit of each act is credited to the Florida Legislature as \"oldest version available\".\n"
              "- The session laws in each History line are part of the text, not the commit dates.\n"
              "- The correction commits restore the page's own text: its punctuation (an "
              "earlier build had made curly quotes and dashes ASCII), the word breaks at line breaks, and text that follows "
              "a list back after it. They are appended; the earlier commits are unchanged."),
    'limits': ("- Any amendment history: the Statutes before the 2026 edition.\n"
              "- The Laws of Florida (session laws) and regulations.\n"
              "- The two images in sections 320.0842 and 322.051, until the shared builder stores images.\n"
              "- Nothing here is an official publication."),
    'licence': ("The legal text is the Constitution of the State of Florida and the 2026 Florida Statutes as published by the "
                "Florida Legislature at https://www.leg.state.fl.us/statutes/. Statutes are not copyrightable "
                "(Georgia v. Public.Resource.Org, Inc., 590 U.S. 255 (2020)). The text is republished unaltered in its wording, with "
                "credit to the Florida Legislature as its publisher."),
})
