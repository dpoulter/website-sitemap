import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from lxml.etree import Element, SubElement, tostring
from lxml.builder import E
import argparse

visited = set()

def crawl(url):
    visited.add(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for a_tag in soup.find_all('a'):
        href = a_tag.get('href')
        if href and not href.startswith('#'):
            full_url = urljoin(url, href)
            if full_url not in visited:
                yield full_url
                yield from crawl(full_url)

def build_sitemap(start_url):
    urlset = E.urlset()
    for url in crawl(start_url):
        urlset.append(
            E.url(
                E.loc(url),
                E.lastmod('2023-07-03'),  # You should replace this with the actual last modification date
                E.changefreq('monthly'),  # Change this based on how frequently the URL is expected to update
                E.priority('0.5'),  # Change this based on the priority of the URL
            )
        )
    return tostring(urlset, pretty_print=True)

def main():
    parser = argparse.ArgumentParser(description='Generate a sitemap for a website.')
    parser.add_argument('start_url', help='The URL of the website to generate a sitemap for.')
    args = parser.parse_args()
    
    sitemap = build_sitemap(args.start_url)

    with open('sitemap.xml', 'wb') as f:
        f.write(sitemap)

if __name__ == '__main__':
    main()
