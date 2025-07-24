import sys
from crawl import get_html,crawl_page, crawl_site_async
import asyncio
async def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)
    website = sys.argv[1]
    max_concurent = sys.argv[2]
    max_pages = sys.argv[3]
    pages = await crawl_site_async(website,int(max_concurent),int(max_pages))
    print_report(pages, website)

def print_report(pages,base_url):
    print(f"""
=============================
  REPORT for {base_url}
=============================
          """)
    for page in pages:
        print(f"Found {pages[page]} internal links to {page}")

if __name__ == "__main__":
    asyncio.run(main())
