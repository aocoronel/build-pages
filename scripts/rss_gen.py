#!/usr/bin/env python3

from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import datetime
import os
import pytz
import re
from var import index_file
from var import lang
from var import description
from var import link
from var import username
from var import rss_output_file

with open(index_file, 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

fg = FeedGenerator()
fg.title(username)
fg.link(href=link)
fg.description(description)
fg.language(lang)

posts_section = soup.find('h1', {'id': 'posts'})
if posts_section:

    next_node = posts_section.find_next_sibling()
    while next_node and next_node.name not in ['hr', 'h1']:
        if next_node.name == 'p':
            date_text = next_node.get_text(strip=True).split('•')[0].strip()
            link_tag = next_node.find('a')
            if link_tag and date_text:
                title = link_tag.text
                link = link + link_tag['href']

                try:
                    naive_datetime = datetime.datetime.strptime(date_text, '%b %d, %Y')
                    timezone = pytz.timezone('UTC')
                    pub_date = timezone.localize(naive_datetime)
                except Exception as e:
                    print(f"Error parsing date {date_text}: {e}")
                    next_node = next_node.find_next_sibling()
                    continue

                fe = fg.add_entry()
                fe.title(title)
                fe.link(href=link)
                fe.description(f"{title}")
                fe.pubDate(pub_date)
        next_node = next_node.find_next_sibling()

rss_feed = fg.rss_str(pretty=True)

if isinstance(rss_feed, bytes):
    rss_feed = rss_feed.decode('utf-8')

os.makedirs(os.path.dirname(rss_output_file), exist_ok=True)

try:
    with open(rss_output_file, 'w', encoding='utf-8') as file:
        file.write(rss_feed)
    print("RSS feed generated successfully!")
except Exception as e:
    print(f"An error occurred while writing the file: {e}")
