#!/usr/bin/env python3
"""Generate a portable static catalog; no third-party dependencies required."""
import json
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent


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
    print(f"Built index.html with {len(paths)} reports.")


if __name__ == "__main__":
    main()
