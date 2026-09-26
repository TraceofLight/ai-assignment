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


def main():
    required = [
        "README.md", "SUBMISSION.md", "src/index.html",
        "docs/CONTRIBUTING.md", "docs/conflict-resolution.md",
        "docs/troubleshooting-log.md", "team/traceoflight.md",
    ]
    errors = [f"누락: {name}" for name in required if not (ROOT / name).is_file()]
    pages = [ROOT / "README.md", ROOT / "SUBMISSION.md", *sorted((ROOT / "team").glob("*.md"))]
    html_path = ROOT / "src/index.html"
    if html_path.is_file():
        pages.append(html_path)
    for path in pages:
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        if path.suffix == ".html":
            parser = Links()
            parser.feed(content)
            links = parser.links
        else:
            links = re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", content)
        for link in links:
            url = urlsplit(link)
            if url.scheme or url.netloc or not url.path:
                continue
            target = path.parent / unquote(url.path)
            if not target.is_file():
                errors.append(f"깨진 링크: {path.relative_to(ROOT)} -> {link}")
    for error in errors:
        print(error)
    print(f"문서·HTML 점검: {len(pages)}개 파일, 오류 {len(errors)}개")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
