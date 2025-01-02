from requests import Session
from config import NOTES_DIR, FRONTEND_URL, SERVER_TIMEOUT
import requests
import os
import json
import urllib3
# suppress InsecureRequestWarning due to server certificate being self-signed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def retrieve_notes(httpsession: Session, username: str):
    try:
        response = httpsession.get(f"{FRONTEND_URL}/users/{username}/notes", timeout=SERVER_TIMEOUT, verify=False)
        notes = response.json()
        
        if response.status_code == 500:
            print("Internal server error.")
            return

        note_path = os.path.join(NOTES_DIR, f"{username}_notes.json")
        with open(note_path, "w") as note_file:
            json.dump(notes, note_file, indent=4)

    except Exception as e:
        print(f"An error occurred: {e}")

