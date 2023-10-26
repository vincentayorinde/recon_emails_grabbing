import requests
import requests.exceptions
from collections import deque
import urllib.parse
import re
from bs4 import BeautifulSoup

original_url = str(input('[+] Enter Target URL: '))
unscraped_urls = deque([original_url])

scraped_urls = set()
emails = set()

# The scraping process

depth = 0

try:
    while len(unscraped_urls):
        depth += 1
        if depth == 200:
            break
        url = unscraped_urls.popleft()
        scraped_urls.add(url)

        parts = urllib.parse.urlsplit(url)
        base_url = '{0.scheme}://{0.netloc}'.format(parts)
        if '/' in parts.path:
            path=url[:url.rfind('/')+1]
        else:
            path = url
        print('[%d] Scrapping %s' % (depth, url))

        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+]", response.text, re.I))
        emails.update(new_emails)

        soup = BeautifulSoup(response.text, features="lxml")

        for anchor in soup.find_all("a"):
            if "href" in anchor.attrs:
                link = anchor.attrs["href"]
            else: 
                link = ''
            
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            if not link in unscraped_urls and not link in scraped_urls:
                unscraped_urls.append(link)


except KeyboardInterrupt:
    print('[-] Existing...')

for email in emails:
    print(email)