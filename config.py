# notist-client configuration
from dotenv import load_dotenv
import os

load_dotenv()

NOTES_DIR = os.path.join(os.path.expanduser("~"), "notist", "notes")
def get_keys_dir(username):
    return os.path.join(os.path.expanduser("~"), "notist", f"{username}_keys")

def get_priv_key(username):
    return os.path.join(get_keys_dir(username), "priv.pem")

def get_pub_key(username):
    return os.path.join(get_keys_dir(username), "pub.pem")

#KEYS_DIR = os.path.join(os.path.expanduser("~"), "notist", f"{username}_keys")
#PRIV_KEY = os.path.join(KEYS_DIR, "priv.pem")
#PUB_KEY = os.path.join(KEYS_DIR, "pub.pem")

FRONTEND_URL = os.getenv("FRONTEND_URL")
SERVER_TIMEOUT = 60 # seconds
