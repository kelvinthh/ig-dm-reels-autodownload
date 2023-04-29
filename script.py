import os, json, time, random, sys, datetime, ast
from dotenv import load_dotenv
from instagrapi import Client
from instagrapi.exceptions import LoginRequired

load_dotenv()
username = os.environ.get("IG_USERNAME")
email = os.environ.get("IG_EMAIL")
password = os.environ.get("IG_PASSWORD")
login_only = ast.literal_eval(os.environ.get("LOGIN_ONLY"))


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


def get_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    cl = Client()
    cl.delay_range = [1, 3]

    session_file = "session.json"
    seen_messages_file = "seen_messages.json"
    authenticate(cl, session_file)

    user_id = cl.user_id_from_username(username)
    print(f"[{get_now()}] Logged in as user ID {user_id}")

    if login_only:
        print(f"[{get_now()}] LOGIN_ONLY is set to true, the script ends here")
        return

    seen_message_ids = load_seen_messages(seen_messages_file)
    print(f"[{get_now()}] Loaded seen messages.")

    while True:
        try:
            threads = cl.direct_threads()
            print(f"[{get_now()}] Retrieved direct threads.")
            cl.delay_range = [1, 3]

            for thread in threads:
                thread_id = thread.id
                messages = cl.direct_messages(thread_id)
                print(f"[{get_now()}] Retrieved messages.")
                cl.delay_range = [1, 3]

                for message in messages:
                    if message.id not in seen_message_ids:
                        match message.item_type:
                            case "clip":
                                print(
                                    f"[{get_now()}] Downloading reel {message.clip.pk}"
                                )
                                try:
                                    # Get the current working directory
                                    cwd = os.getcwd()

                                    # Construct the path to the download folder
                                    download_path = os.path.join(cwd, "download")

                                    # Check if the download folder exists
                                    if not os.path.exists(download_path):
                                        os.makedirs(download_path)
                                        print(f"[{get_now()}] Created {download_path}")

                                    cl.video_download(message.clip.pk, "download")
                                    print(f"[{get_now()}] Downloaded {message.clip.pk}")
                                    cl.delay_range = [1, 3]
                                except Exception as e:
                                    print(e)
                            case "xma_story_share":
                                print(
                                    f"[{get_now()}] New story video in thread {thread_id}: {message.id}"
                                )
                            case _:
                                print(
                                    f"[{get_now()}] New message in thread {thread_id}: {message.text}"
                                )
                        seen_message_ids.add(message.id)
                        save_seen_messages(seen_messages_file, seen_message_ids)

        except Exception as e:
            print(f"[{get_now()}] An exception occurred: {e}")
            print("[{get_now()}] Deleting the session file and restarting the script.")
            if os.path.exists(session_file):
                os.remove(session_file)
            os.execv(sys.executable, ["python"] + sys.argv)

        # check for new messages every random seconds
        sleep_time = random.randint(15 * 60, 30 * 60)
        print(f"[{get_now()}] Timeout duration: {sleep_time} seconds.")
        for remaining_time in range(sleep_time, 0, -1):
            sys.stdout.write(f"\r[{get_now()}] Time remaining: {remaining_time}s")
            sys.stdout.flush()
            time.sleep(1)

        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
