# Podcast Feed Mirror

A simple, automated system to mirror and archive podcast RSS feeds using GitHub Actions and Pages.

## Motivation

Some devices are incompatible with modern SSL certificates. This mirror system is a workaround
to allow access to feeds using these modern certificates.

## Overview

- creates local mirrors of podcast RSS feeds and hosts them via GitHub Pages. It automatically updates the feeds every 6 hours and maintains an index page listing all mirrored feeds.

## Features

- 🔄 Automatic feed updates every 6 hours
- 📑 Clean index page showing all mirrored feeds
- 🔍 Change detection to avoid unnecessary updates
- 🚀 Automated deployment to GitHub Pages
- 📱 Mobile-friendly interface

## Setup

1. Fork this repository

2. Enable GitHub Pages:
   - Go to repository Settings
   - Navigate to Pages
   - Select "GitHub Actions" as the source

3. Configure your feeds:
   - Edit `config.yml` to add your podcast feeds:
   ```yaml
   feeds:
     - url: https://example.com/podcast.rss
       name: Example Podcast
   ```

4. The GitHub Action will automatically run and create mirrors of your configured feeds

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/podcast-feed-mirror.git
cd podcast-feed-mirror
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the update script:
```bash
python update_feeds.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Notes

- The script uses MD5 hashing for filename generation
- Feed updates are checked every 6 hours
- Changes are only committed when feed content has actually changed
