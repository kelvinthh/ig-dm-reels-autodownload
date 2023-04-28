import os
import json
import time
from dotenv import load_dotenv
from instagrapi import Client
from instagrapi.exceptions import LoginRequired

load_dotenv()
username = os.environ.get("IG_USERNAME")
email = os.environ.get("IG_EMAIL")
password = os.environ.get("IG_PASSWORD")

cl = Client()
cl.delay_range = [1, 3]

session_file = "session.json"

if os.path.exists(session_file):
    cl.load_settings(session_file)
    try:
        cl.login(username, password)
        cl.get_timeline_feed()  # check if the session is valid
    except LoginRequired:
        # session is invalid, re-login and save the new session
        cl.login(username, password)
        cl.dump_settings(session_file)
else:
    cl.login(username, password)
    cl.dump_settings(session_file)

user_id = cl.user_id_from_username(username)
print(f"The user id is {user_id}")

# Initialize an empty set to store the ids of the messages already seen
seen_message_ids = set()

while True:
    threads = cl.direct_threads()
    for thread in threads:
        thread_id = thread.id
        messages = cl.direct_messages(thread_id)
        for message in messages:
            if message.id not in seen_message_ids:
                print(f"New message in thread {thread_id}: {message.text}")
                seen_message_ids.add(message.id)
    
    time.sleep(10)  # check for new messages every 10 seconds
