from urllib.parse import urlparse,urljoin, ParseResult
from bs4 import BeautifulSoup, PageElement
from requests import Response, exceptions, get
import aiohttp
import asyncio

class AsyncCrawler():
    def __init__(self,base_url,max_concurrency, max_pages):
        self.base_url = base_url
        self.base_domain = urlparse(self.base_url).netloc
        self.pages = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None 
        self.max_pages = max_pages
	
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if normalized_url in self.pages:
                self.pages[normalized_url] += 1
                return False
            self.pages[normalized_url] = 1
            return True
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
        
    async def get_html(self, url: str) -> str:
        async with self.session.get(url) as response:
            if response.status >= 400:
                print(f"Expected 'text/html' in Content-Type header but got: {response.status}")
                return None
            if "text/html" not in response.headers['Content-Type']:
                print(f"Content Type Recieved Not Type Html: {response.headers['content-type']}")
                return  None
            text = await response.text()
            return text
        
    async def crawl(self):
        await self.crawl_page()
        return self.pages

    async def crawl_page(self, current_url=None) -> dict[str,int]:
        async with self.lock:
            if len(self.pages) > self.max_pages:
                return
        if current_url == None:
            current_url = self.base_url
        if self.pages == None:
            self.pages = {}

        base_url_obj = urlparse(self.base_url)
        current_url_obj = urlparse(current_url)
        if current_url_obj.netloc != base_url_obj.netloc:
            return 
        
        normalised_current_url = normalize_url(current_url)

        is_new = await self.add_page_visit(normalised_current_url)
        if not is_new:
            return

        async with self.semaphore:
            print(
                f"Crawling {current_url} (Active: {self.max_concurrency - self.semaphore._value})"
            )
            html = await self.get_html(current_url)
            if html is None:
                return 

            urls = get_urls_from_html(html, current_url)
        tasks = []
        for url in urls:
            tasks.append(asyncio.create_task(self.crawl_page(url)))
        if tasks:
            await asyncio.gather(*tasks)    


async def crawl_site_async(base_url,max_concurrency,max_pages):
    async with AsyncCrawler(base_url,max_concurrency,max_pages) as crawl:
        pages = await crawl.crawl()
    return pages


def normalize_url(url: str) -> str:
    parsed: ParseResult = urlparse(url)
    netloc: str = parsed.netloc
    path: str = parsed.path
    path = parsed.path.rstrip('/')
    if not path:
        path = '/'
    return (netloc + path).lower()

def get_urls_from_html(html: str, base_url: str) -> list[str]:
    parsed: BeautifulSoup = BeautifulSoup(html,'html.parser')
    urls: list[str] = []
    a_tags: list[PageElement] = parsed.find_all('a')

    for tag in a_tags:
        if href := tag.get('href'):
            extract: str = urljoin(base_url,href)
            urls.append(extract)
    return urls

def get_html(url: str) -> str:
    response: Response = get(url)
    if response.status_code >= 400:
        print(f"Expected 'text/html' in Content-Type header but got: {response.status_code}")
        return None
    if "text/html" not in response.headers['Content-Type']:
        print(f"Content Type Recieved Not Type Html: {response.headers['content-type']}")
        return None
    return response.text

def crawl_page(base_url, current_url=None, pages=None) -> dict[str,int]:
    if current_url == None:
        current_url = base_url
    if pages == None:
        pages = {}

    base_url_obj = urlparse(base_url)
    current_url_obj = urlparse(current_url)
    if current_url_obj.netloc != base_url_obj.netloc:
        return pages
    
    normalised_current_url = normalize_url(current_url)

    if normalised_current_url in pages:
        pages[normalised_current_url] += 1
        return pages
    
    pages[normalised_current_url] = 1

    html = safe_get_html(current_url)
    if html is None:
        return pages
    print(html)

    urls = get_urls_from_html(html, current_url)
    for url in urls:
        pages = crawl_page(base_url,url,pages)

    return pages

def safe_get_html(url: str) -> str:
    try:
        return get_html(url)
    except Exception as e:
        print(f"Exception occured during getting HMTL: {e}")
        return None