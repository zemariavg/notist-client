# notist-client configuration
from dotenv import load_dotenv
import os

load_dotenv()

NOTES_DIR = os.path.join(os.path.expanduser("~"), "notist", "notes")
KEYS_DIR = os.path.join(os.path.expanduser("~"), "notist", "keys")
PRIV_KEY = os.path.join(KEYS_DIR, "priv.pem")
PUB_KEY = os.path.join(KEYS_DIR, "pub.pem")
FRONTEND_URL = os.getenv("FRONTEND_URL")
SERVER_TIMEOUT = 60 # seconds
