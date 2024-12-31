from utils.noteutils import read_note, find_note
from config import NOTES_DIR
import json, os

def list_notes(username: str):
    try:
        notes_path = os.path.join(NOTES_DIR, f"{username}_notes.json")
        json_content = read_note(notes_path)

        print(f"Notes for user '{username}':")
        for permission, notes in json_content.items():
            for note in notes:
                print(f"{note['title']}, {permission}")

    except FileNotFoundError:
        print(f"Error: The file {notes_path} does not exist.")
    except json.JSONDecodeError:
        print(f"Error: Failed to parse the JSON file {notes_path}.")
    except KeyError as e:
        print(f"Error: Missing expected key {e} in the JSON structure.")


