import os, json, time, random, sys
from dotenv import load_dotenv
from instagrapi import Client
from instagrapi.exceptions import LoginRequired

load_dotenv()
username = os.environ.get("IG_USERNAME")
email = os.environ.get("IG_EMAIL")
password = os.environ.get("IG_PASSWORD")

def authenticate(client, session_file):
    if os.path.exists(session_file):
        client.load_settings(session_file)
        try:
            client.login(username, password)
            client.get_timeline_feed()  # check if the session is valid
        except LoginRequired:
            # session is invalid, re-login and save the new session
            client.login(username, password)
            client.dump_settings(session_file)
    else:
        client.login(username, password)
        client.dump_settings(session_file)

def load_seen_messages(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return set(json.load(f))
    else:
        return set()

def save_seen_messages(file, messages):
    with open(file, "w") as f:
        json.dump(list(messages), f)

cl = Client()
cl.delay_range = [1, 3]

session_file = "session.json"
seen_messages_file = "seen_messages.json"
authenticate(cl, session_file)

user_id = cl.user_id_from_username(username)
print(f"Logged in as user ID {user_id}")

seen_message_ids = load_seen_messages(seen_messages_file)
print("Loaded seen messages.")

while True:
    try:
        threads = cl.direct_threads()
        print("Retrieved direct threads.")
        cl.delay_range = [1, 3]

        for thread in threads:
            thread_id = thread.id
            messages = cl.direct_messages(thread_id)
            print("Retrieved messages.")
            cl.delay_range = [1, 3]

            for message in messages:
                if message.id not in seen_message_ids:
                    match message.item_type:
                        case "clip":
                            print(
                                f"New reel in thread {thread_id}: {message.clip.video_url}"
                            )
                        case "xma_story_share":
                            print(f"New story video in thread {thread_id}: {message.id}")
                            # story_info = cl.story_info(message.id)
                            # print(f"Story info: {story_info.video_url}")
                        case _:
                            print(f"New message in thread {thread_id}: {message.text}")
                    seen_message_ids.add(message.id)
                    save_seen_messages(seen_messages_file, seen_message_ids)

    except Exception as e:
        print(f"An exception occurred: {e}")
        print("Deleting the session file and restarting the script.")
        if os.path.exists(session_file):
            os.remove(session_file)
        os.execv(sys.executable, ["python"] + sys.argv)

    # check for new messages every random seconds
    sleep_time = random.randint(90, 300)
    print(f"Timeout duration: {sleep_time} seconds.")
    time.sleep(sleep_time)
