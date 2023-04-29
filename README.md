# Instagram Scraper (DM Reel Bot/Downloader)

This script monitors Instagram direct messages and downloads reels shared via direct messages. It uses the `instagrapi` library to access and interact with the instagrapi.

## Features

- Authenticate with Instagram using a session file
- Monitor direct messages
- Download reels shared in direct messages
- Log story videos shared in direct messages

## Installation

1. Clone the repository:

```
git clone https://github.com/kelvinthh/ig-scrape.git
cd ig-scrape
```

2. Install the required packages:
```
pip install -r requirements.txt
```

3. Create a `.env` file with your Instagram credentials:

```
# Development settings
IG_USERNAME=your_username
IG_EMAIL=your_email
IG_PASSWORD=your_password
LOGIN_ONLY=True_or_False
```

Replace `your_username`, `your_email`, and `your_password` with your actual Instagram username, email, and password.

## Usage

To start the script, run:

```
python script.py

```

The script will authenticate with Instagram, monitor your direct messages, and download reels shared in direct messages. It will also log story videos shared in direct messages.

