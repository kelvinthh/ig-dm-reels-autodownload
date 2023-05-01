# Instagram DM Reels Auto-downloader (DM Reel Bot/Downloader)

This script monitors Instagram direct messages and downloads reels shared via direct messages every 30 to 60 minutes into a `download` folder. It uses the [instagrapi](https://github.com/adw0rd/instagrapi) library to access and interact with the instagrapi.

⚠️ Warning ⚠️

Using this script may go against Instagram's community guidelines and result in the permanent ban of your account. Proceed with caution and do not use your personal account. We do not take responsibility for any consequences that may arise from the use of this script. Use at your own risk. Also, it is recommended to run this script with a brand new account, since it considers all previous chats as 'new' messages on the first time you run it.


## Features

- Authenticate with Instagram using a session file
- Monitor direct messages
- Download reels shared in direct messages
- Log story videos shared in direct messages

## Installation

1. Clone the repository:

```
git clone https://github.com/kelvinthh/ig-dm-reels-autodownload.git
cd ig-dm-reels-autodownload
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
LOGIN_ONLY=False
```

Replace `your_username`, `your_email`, and `your_password` with your actual Instagram username, email, and password.

## Usage

By default, the script will authenticate with Instagram, monitor your direct messages, and download reels shared in direct messages. It will also log story videos shared in direct messages.

Optionally, you can set the `LOGIN_ONLY` environment variable to `True` to skip the monitoring and downloading steps and only generate a session file. This can be useful if you just want to authenticate with Instagram and save the session file for later use. If `LOGIN_ONLY` is set to `True`, the script will not monitor your direct messages or download reels.

To set `LOGIN_ONLY` to `True`, add the following line to your `.env` file:

```
LOGIN_ONLY=True
```
To set `LOGIN_ONLY` to `False`:
```
LOGIN_ONLY=False
```

Note that if `LOGIN_ONLY` is set to `False`, the script will generate a session file if it does not already exist, then proceed to monitor your direct messages and download reels as usual.

Finally, to start the script, run:

```
python script.py
```
_Note: Chats in 'Pending' are not monitored. Please accept message request from any account you want the script to monitor using Instagram web/logging into the account with a mobile device before you proceed._
