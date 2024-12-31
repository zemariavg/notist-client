from config import NOTES_DIR, FRONTEND_URL, SERVER_TIMEOUT
import json, os
import requests
from utils.noteutils import read_note, find_note
from requests.sessions import Session

def list_notes(httpsession: Session, username: str):
    try:
        # locally
        notes_path = os.path.join(NOTES_DIR, f"{username}_notes.json")
        json_content_local = read_note(notes_path)

        has_notes = any(len(notes) > 0 for notes in json_content_local.values())
        if not has_notes:
            print(f"No notes found for user '{username}'.")
            return
        print(f"Local notes for user '{username}':")
        for permission, notes in json_content_local.items():
            for note in notes:
                print(f"{note['title']}, {permission}")
                
        # on server
        response = httpsession.get(f"{FRONTEND_URL}/users/{username}/notes", timeout=SERVER_TIMEOUT, verify=False)
        json_content_server = response.json()
        
        if response.status_code == 500:
            print("Internal server error.")
            return
            
        has_notes = any(len(notes) > 0 for notes in json_content_server.values())
        if not has_notes:
            print(f"No notes found for user '{username}'.")
            return
        print(f"Server notes for user '{username}':")
        for permission, notes in json_content_server.items():
            for note in notes:
                print(f"{note['title']}, {permission}")

    except FileNotFoundError:
        print(f"Error: The file {notes_path} does not exist.")
    except json.JSONDecodeError:
        print(f"Error: Failed to parse the JSON file {notes_path}.")
    except KeyError as e:
        print(f"Error: Missing expected key {e} in the JSON structure.")


