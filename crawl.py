from urllib.parse import urlparse,urljoin, ParseResult
from bs4 import BeautifulSoup, PageElement

def normalize_url(url: str) -> str:
    parsed: ParseResult = urlparse(url)
    netloc: str = parsed.netloc.lstrip("www.")
    path: str = parsed.path.lstrip("www.")
    return netloc + path

def get_urls_from_html(html: str, base_url: str) -> list[str]:
 
    parsed: BeautifulSoup = BeautifulSoup(html,'html.parser')
    urls: list[str] = []
    a_tags: list[PageElement] = parsed.find_all('a')

    for tag in a_tags:
        if href := tag.get('href'):
            extract: str = urljoin(base_url,href)
            urls.append(extract)
    return urls