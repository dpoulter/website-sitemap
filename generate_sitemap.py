import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from lxml.etree import Element, tostring
from lxml.builder import E
import argparse

visited = set()

def same_domain(url1, url2):
    return urlparse(url1).netloc == urlparse(url2).netloc

def crawl(url, base_url):
    visited.add(url)
    print(f"Attempting to visit {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()  # raise exception if the request failed
        print(f"Successfully fetched {url}")
    except Exception as e:
        print(f"Failed to fetch {url}. Exception: {e}")
        return
    soup = BeautifulSoup(response.text, 'html.parser')
    for a_tag in soup.find_all('a'):
        href = a_tag.get('href')
        if href and not href.startswith('#') and not href.startswith('mailto:'):
            full_url = urljoin(url, href)
            if same_domain(full_url, base_url) and full_url not in visited:
                print(f'Parsed URL: {full_url}')  # print parsed URL
                yield full_url
                yield from crawl(full_url, base_url)

def build_sitemap(start_url):
    print(f"Building sitemap for {start_url}")
    urlset = E.urlset()
    for url in crawl(start_url, start_url):
        urlset.append(
            E.url(
                E.loc(url),
                E.lastmod('2023-07-03'),  # You should replace this with the actual last modification date
                E.changefreq('monthly'),  # Change this based on how frequently the URL is expected to update
                E.priority('0.5'),  # Change this based on the priority of the URL
            )
        )
        print(f"Added {url} to sitemap")
    return tostring(urlset, pretty_print=True)

def main():
    parser = argparse.ArgumentParser(description='Generate a sitemap for a website.')
    parser.add_argument('start_url', help='The URL of the website to generate a sitemap for.')
    args = parser.parse_args()
    
    print(f"Starting sitemap generation for {args.start_url}")
    sitemap = build_sitemap(args.start_url)

    with open('sitemap.xml', 'wb') as f:
        f.write(sitemap)

    print("Finished sitemap generation")

if __name__ == '__main__':
    main()
