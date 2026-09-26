"""팀 소개 HTML과 저장소의 로컬 링크를 점검한다."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {"href", "src"} and value:
                self.links.append(value)


def page_links(path):
    content = path.read_text(encoding="utf-8")
    if path.suffix != ".html":
        return re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", content)
    parser = Links()
    parser.feed(content)
    return parser.links


def broken_links(path):
    errors = []
    for link in page_links(path):
        url = urlsplit(link)
        if url.scheme or url.netloc or not url.path:
            continue
        target = path.parent / unquote(url.path)
        if not target.is_file():
            errors.append(f"깨진 링크: {path.relative_to(ROOT)} -> {link}")
    return errors


def main():
    required = [
        "README.md", "SUBMISSION.md", "src/index.html",
        "docs/CONTRIBUTING.md", "docs/conflict-resolution.md",
        "docs/troubleshooting-log.md", "team/traceoflight.md",
        "team/nansu0425.md", "team/chanpago.md",
    ]
    errors = [f"누락: {name}" for name in required if not (ROOT / name).is_file()]
    pages = [ROOT / "README.md", ROOT / "SUBMISSION.md"]
    pages += sorted((ROOT / "team").glob("*.md"))
    pages += sorted((ROOT / "docs").glob("*.md"))
    pages.append(ROOT / "src/index.html")
    for path in pages:
        if path.is_file():
            errors.extend(broken_links(path))
    for error in errors:
        print(error)
    print(f"문서·HTML 점검: {len(pages)}개 파일, 오류 {len(errors)}개")
    return int(bool(errors))


if __name__ == "__main__":
    sys.exit(main())
