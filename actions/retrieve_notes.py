from config import NOTES_DIR, PRIV_KEY, PUB_KEY, FRONTEND_URL, SERVER_TIMEOUT
import requests
import os
import json
import urllib3
# suppress InsecureRequestWarning due to server certificate being self-signed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def retrieve_notes(user: str):
    print(f"Retrieving notes for user {user}...")
    try:
        response = requests.get(f"{FRONTEND_URL}/users/{user}/notes", timeout=SERVER_TIMEOUT, verify=False) 
        notes = response.json()
        
        if response.status_code == 500:
            print("Internal server error.")
            return

        note_path = os.path.join(NOTES_DIR, f"{user}_notes.json")
        with open(note_path, "w") as note_file:
            json.dump(notes, note_file, indent=4)

        #TODO: On Retrieve, get note_key from collaborator table for a note
        print(f"Notes for user '{user}' successfully retrieved.")
    except Exception as e:
        #TODO: User Not Found Exception - abort in the server
        print(f"An error occurred: {e}")

