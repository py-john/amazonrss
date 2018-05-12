#!/usr/bin/env python3

"""
    amazon-rss.py: Search within Amazon's gold box rss feed
"""

import html
import requests
import constants
from bs4 import BeautifulSoup as bs

print('Loading...')

# create soup from rss html
url = 'https://rssfeeds.s3.amazonaws.com/goldbox'
res = requests.get(url, headers=constants.headers)
text = res.text
text = html.unescape(text)
soup = bs(text, 'html.parser')

# item list from all items on the site
items = soup.rss.channel.select('item')

# search for term within items. break when there's no input
while(True):

    search_term = input('\nSearch: ').lower()
    if not search_term:
        break

    for item in items:

        # get title and link text
        title = item.find('title').getText()
        link = item.link.getText().replace(';', '')

        # check if search term is in title
        if search_term in title.lower():
            print(title)
            # get and print description table text
            cells = item.description.table.findAll('td')
            for cell in cells:
                if cell.tr:
                    continue
                cell_text = cell.getText()
                if cell_text and cell_text.strip() != title:
                    print(cell_text)

            # format link text to take out ref and rss tag
            if '/s/' not in link:
                print(link.rpartition('ref=')[0])
            else:
                if 'ref=' in link and '&tag=rss' in link:
                    parts = link.split('ref=')
                    end_ref = parts[1].index('/') + 1
                    start_tag = parts[1].index('&tag=rss')
                    link = parts[0] + parts[1][end_ref:start_tag]
                print(link)

            print()
