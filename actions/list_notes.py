from config import NOTES_DIR, FRONTEND_URL, SERVER_TIMEOUT
import os
import json
import requests
from utils.noteutils import read_note
from requests.sessions import Session


def list_notes_from_json(json_content: dict, source: str):
    """Lists notes from the provided JSON content."""
    if not any(len(notes) > 0 for notes in json_content.values()):
        print(f"No notes found in {source}.")
        return

    print(f"Notes from {source}:")
    for permission, notes in json_content.items():
        for note in notes:
            print(f"{note['title']}, {permission}")


def fetch_notes_local(notes_path: str, username: str) -> dict:
    """Fetches notes locally from a JSON file."""
    try:
        json_content = read_note(notes_path)
        list_notes_from_json(json_content, "local storage")
        return json_content
    except FileNotFoundError:
        print(f"Error: The file {notes_path} does not exist.")
    except json.JSONDecodeError:
        print(f"Error: Failed to parse the JSON file {notes_path}.")
    return {}


def fetch_notes_server(httpsession: Session, username: str) -> dict:
    """Fetches notes from the server."""
    try:
        response = httpsession.get(
            f"{FRONTEND_URL}/users/{username}/notes", timeout=SERVER_TIMEOUT, verify=False
        )
        if response.status_code == 500:
            print("Internal server error.")
            return {}

        json_content = response.json()
        list_notes_from_json(json_content, "server")
        return json_content
    except requests.RequestException as e:
        print(f"Error: Failed to fetch server notes. Details: {e}")
    return {}


def list_notes(httpsession: Session, username: str):
    """Lists notes both locally and from the server."""
    notes_path = os.path.join(NOTES_DIR, f"{username}_notes.json")
    fetch_notes_local(notes_path, username)
    fetch_notes_server(httpsession, username)
