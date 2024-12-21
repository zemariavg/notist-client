from config import NOTES_DIR, PRIV_KEY, PUB_KEY, FRONTEND_URL, SERVER_TIMEOUT
import requests
import os
import json

def retrieve_notes(user: str):
    try:
        response = requests.get(f"{FRONTEND_URL}/users/{user}/notes", timeout=SERVER_TIMEOUT)
        notes = response.json()

        note_path = os.path.join(NOTES_DIR, f"{user}_notes.json")
        with open(note_path, "w") as note_file:
            json.dump(notes, note_file, indent=4)

        print(f"Notes for user '{user}' successfully retrieved and stored.")

    except Exception as e:
        #TODO: User Not Found Exception - abort in the server
        print(f"An error occurred: {e}")

