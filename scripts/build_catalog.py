#!/usr/bin/env python3
"""Generate a portable static catalog; no third-party dependencies required."""
import json
import re
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
NAV_START = "<!-- MUSESPARK-NAV:START -->"
NAV_END = "<!-- MUSESPARK-NAV:END -->"


def add_report_navigation(paths):
    """Refresh navigation once per report, including reports added in future."""
    for index, path in enumerate(paths):
        source = path.read_text(encoding="utf-8")
        source = re.sub(r"\n?" + re.escape(NAV_START) + r".*?" + re.escape(NAV_END), "", source, flags=re.S)
        links = ['<a href="index.html" aria-label="Return to the report catalog">← All reports</a>']
        if index > 0:
            links.append(f'<a href="{quote(paths[index - 1].name, safe="")}" aria-label="Previous report">← Previous</a>')
        links.append(f'<span>{index + 1} / {len(paths)}</span>')
        if index + 1 < len(paths):
            links.append(f'<a href="{quote(paths[index + 1].name, safe="")}" aria-label="Next report">Next →</a>')
        block = f'''{NAV_START}
<style>
body {{ padding-bottom: 90px !important; }}
#musespark-report-nav {{ all: initial; position: fixed; bottom: 16px; right: 16px; left: auto; z-index: 2147483647; display: flex; align-items: center; gap: 4px; max-width: calc(100vw - 32px); box-sizing: border-box; padding: 7px; border: 1px solid #cfd5c7; border-radius: 10px; background: #f6f5f0; box-shadow: 0 4px 20px #0002; }}
#musespark-report-nav a, #musespark-report-nav span {{ all: initial; box-sizing: border-box; display: block; padding: 10px 9px; color: #243c32; font: 12px/1.3 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; white-space: nowrap; }}
#musespark-report-nav a {{ cursor: pointer; border-radius: 5px; }}
#musespark-report-nav a:hover {{ background: #e5ebdc; }}
#musespark-report-nav a:focus-visible {{ outline: 2px solid #526d37; outline-offset: -2px; }}
#musespark-report-nav span {{ color: #616b62; font-size: 11px; }}
@media (max-width: 380px) {{ #musespark-report-nav {{ right: 8px; bottom: 8px; max-width: calc(100vw - 16px); gap: 0; }} #musespark-report-nav a, #musespark-report-nav span {{ padding: 10px 6px; }} }}
@media print {{ #musespark-report-nav {{ display: none; }} body {{ padding-bottom: 0 !important; }} }}
</style>
<nav id="musespark-report-nav" aria-label="Research library">{"".join(links)}</nav>
{NAV_END}'''
        closing = list(re.finditer(r"</body\s*>", source, flags=re.I))
        if closing:
            position = closing[-1].start()
            source = source[:position] + block + "\n" + source[position:]
        else:
            source += "\n" + block + "\n"
        path.write_text(source, encoding="utf-8")


class TitleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.parts.append(data)


def main():
    metadata = json.loads((ROOT / "reports.json").read_text())
    paths = sorted(
        (p for p in ROOT.iterdir() if p.suffix.lower() in {".html", ".htm"}
         and p.name != "index.html"),
        key=lambda p: (list(metadata).index(p.name) if p.name in metadata else len(metadata), p.name.lower()),
    )
    cards = []
    topics = set()
    for number, path in enumerate(paths, 1):
        parser = TitleParser()
        parser.feed(path.read_text(encoding="utf-8"))
        entry = metadata.get(path.name, {})
        title = entry.get("title", "".join(parser.parts).strip() or path.stem)
        description = entry.get("description", "Explore the complete report.")
        topic = entry.get("topic", "Research")
        language = entry.get("language", "Unspecified")
        topics.add(topic)
        search = escape(" ".join([title, description, topic, language, path.name]), quote=True)
        cards.append(f'''<article class="report" data-topic="{escape(topic, quote=True)}" data-language="{escape(language, quote=True)}" data-search="{search}">
          <div class="card-top"><span class="topic">{escape(topic)}</span><span class="number">{number:02d}</span></div>
          <h3><a href="{quote(path.name, safe='')}">{escape(title)}</a></h3>
          <p>{escape(description)}</p>
          <div class="card-bottom"><span>{escape(language)} <span aria-hidden="true">·</span> HTML report</span><span class="arrow" aria-hidden="true">↗</span></div>
        </article>''')
    topic_options = "".join(f'<option>{escape(topic)}</option>' for topic in sorted(topics))
    template = (ROOT / "scripts/catalog.template.html").read_text()
    for token, value in {"{{CARDS}}": "\n".join(cards), "{{COUNT}}": str(len(paths)), "{{TOPICS}}": topic_options}.items():
        template = template.replace(token, value)
    (ROOT / "index.html").write_text(template, encoding="utf-8")
    add_report_navigation(paths)
    print(f"Built index.html with {len(paths)} reports.")


if __name__ == "__main__":
    main()
