#!/usr/bin/env python3
from bs4 import BeautifulSoup
import os
from datetime import datetime
from var import index_file
from var import link
from var import sitemap_output_file

with open(index_file, 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

static_pages = [
    {'loc': link, 'lastmod': datetime.now().strftime('%Y-%m-%d')},
    {'loc': link + '/about.html', 'lastmod': datetime.now().strftime('%Y-%m-%d')},
    {'loc': link + '/tech/', 'lastmod': datetime.now().strftime('%Y-%m-%d')},
]

posts = []
posts_section = soup.find('h1', {'id': 'posts'})
if posts_section:
    next_node = posts_section.find_next_sibling()
    while next_node and next_node.name not in ['hr', 'h1']:
        if next_node.name == 'p':
            link_tag = next_node.find('a')
            if link_tag:
                posts.append({
                    'loc': link + '/' + link_tag['href'],
                    'lastmod': next_node.get_text(strip=True).split('•')[0].strip()
                })
        next_node = next_node.find_next_sibling()

for post in posts:
    try:
        date = datetime.strptime(post['lastmod'], '%b %d, %Y')
        post['lastmod'] = date.strftime('%Y-%m-%d')
    except:
        post['lastmod'] = datetime.now().strftime('%Y-%m-%d')

sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'''

for page in static_pages + posts:
    sitemap += f'''
    <url>
        <loc>{page['loc']}</loc>
        <lastmod>{page['lastmod']}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>'''

sitemap += '''
</urlset>'''

os.makedirs(os.path.dirname(sitemap_output_file), exist_ok=True)

try:
    with open(sitemap_output_file, 'w', encoding='utf-8') as file:
        file.write(sitemap)
    print("Sitemap generated successfully!")
except Exception as e:
    print(f"An error occurred while writing the file: {e}")
