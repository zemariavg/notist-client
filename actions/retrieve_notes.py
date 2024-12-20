from config import NOTES_DIR, PRIV_KEY, PUB_KEY, FRONTEND_URL, SERVER_TIMEOUT, SUBDIRECTORIES
import requests
import os
import json

def retrieve_notes(user: str):
    try:
        response = requests.get(f"{FRONTEND_URL}/users/{user}/notes", timeout=SERVER_TIMEOUT)
        response.raise_for_status()
        notes_data = response.json()

        for role in SUBDIRECTORIES:
            role_dir = os.path.join(NOTES_DIR, role)

            for note in notes_data.get(role, []):
                note_title = note["note_title"].replace(" ", "_")  # Sanitize file name
                note_path = os.path.join(role_dir, f"{note_title}.json")

                # Write note to a file
                with open(note_path, "w") as note_file:
                    json.dump(note, note_file, indent=4)

        print(f"Notes for user '{user}' successfully retrieved and stored.")

    except requests.exceptions.RequestException as e:
        print(f"HTTP request error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

