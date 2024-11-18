#!/usr/bin/env python3
import os
import yaml
import requests
import hashlib
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree

def load_config():
    """Load feed configuration from config.yml"""
    with open('config.yml', 'r') as f:
        return yaml.safe_load(f)

def sanitize_filename(url):
    """Create a safe filename from URL"""
    return hashlib.md5(url.encode()).hexdigest() + '.xml'

def fetch_feed(url):
    """Fetch feed content with proper headers"""
    headers = {
        'User-Agent': 'PodcastMirror/1.0 (GitHub; +https://github.com/yourusername/podcast-mirror)'
    }
    response = requests.get(url, headers=headers, verify=True)
    response.raise_for_status()
    return response.text

def is_feed_changed(content, filepath):
    """Check if feed content has changed"""
    if not filepath.exists():
        return True

    with open(filepath, 'r', encoding='utf-8') as f:
        old_content = f.read()
    return old_content != content

def save_feed(content, filepath):
    """Save feed content to file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def update_index_html(feed_files):
    """Update index.html with links to all feeds"""
    html_template = """<!DOCTYPE html>
<html>
<head>
    <title>Podcast Feed Mirror</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 1rem; }
        .feed { margin: 1rem 0; padding: 1rem; border: 1px solid #ccc; }
    </style>
</head>
<body>
    <h1>Podcast Feed Mirror</h1>
    <p>Last updated: {timestamp}</p>
    {feeds}
</body>
</html>"""

    feed_entries = []
    for feed_file in feed_files:
        try:
            tree = ElementTree.parse(feed_file)
            root = tree.getroot()

            # Try to get feed title (works for both RSS and Atom)
            title = root.find('.//title').text

            feed_entries.append(f"""
    <div class="feed">
        <h2>{title}</h2>
        <p>Mirror URL: <a href="{feed_file.name}">{feed_file.name}</a></p>
    </div>""")
        except Exception as e:
            print(f"Error processing {feed_file}: {e}")

    html_content = html_template.format(
        timestamp=datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M:%S UTC'),
        feeds='\n'.join(feed_entries)
    )

    with open('feeds/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

def main():
    config = load_config()
    feeds_dir = Path('feeds')
    feeds_dir.mkdir(exist_ok=True)

    updated_feeds = []

    for feed in config['feeds']:
        try:
            print(f"Fetching {feed['url']}")
            content = fetch_feed(feed['url'])

            filepath = feeds_dir / sanitize_filename(feed['url'])
            if is_feed_changed(content, filepath):
                print(f"Updating {filepath}")
                save_feed(content, filepath)
                updated_feeds.append(filepath)
            else:
                print(f"No changes for {filepath}")

        except Exception as e:
            print(f"Error processing {feed['url']}: {e}")

    update_index_html(feeds_dir.glob('*.xml'))

if __name__ == '__main__':
    main()
