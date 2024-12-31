from cryptolib.unprotect import unprotect_note
from cryptolib.protect import protect_note
from datetime import datetime
from config import NOTES_DIR, get_priv_key, get_pub_key, FRONTEND_URL, SERVER_TIMEOUT
from utils.noteutils import find_note, read_note
from requests import Session
import requests
import os
import json

def backup_on_server(httpsession: Session, user: str, note_json: dict) -> int:
    unprotected_note, ciphered_note_key = unprotect_note(note_json, get_priv_key)

    # print(f"Sending note {note_title} to server")
    headers = {
        "Content-Type": "application/json",
        "version": str(unprotected_note['version'])  
    }
    response = httpsession.post(f"{FRONTEND_URL}/backup_note", json=note_json, headers=headers,
                             timeout=SERVER_TIMEOUT, verify=False)

    if response.status_code == 403:
        print(f"{response}: User has no write permissions.")
        return 0
    elif response.status_code == 405:
        print(f"{response}: Invalid JSON received/Version is outdated.")
        return 0
    elif response.status_code != 201:
        print(f"{response}: Failed to send note to server.")
        return 0
    else:
        # print(f"sent note {note_title} to server.")
        return 1

def backup_note_from_file(httpsession: Session, user: str, note_title: str) -> int:
    notes_file_path = os.path.join(NOTES_DIR, f"{user}_notes.json")

    try:
        with open(notes_file_path, 'r', encoding='utf-8') as file:
            notes_file = json.load(file)

        note_json = find_note(notes_file, note_title, "edit")

        if not note_json:
            print(f"Note '{note_title}' not found for user '{user}'.")
            return 0
        else:
            return backup_on_server(httpsession, user, note_json)

    except Exception as e:
        print(note_title)
        print(f"Error sending note to server: {e}")
        return 0


def backup_all_notes(httpsession: Session, user: str) -> None:
    # print session data
    try:
        notes_file_path = os.path.join(NOTES_DIR, f"{user}_notes.json")

        if not os.path.exists(notes_file_path):
            print(f"No notes found for user '{user}'.")
            return

        notes_file = read_note(notes_file_path)

        if not any(notes_file.values()):
            print(f"No notes found for user '{user}'.")
            return

        print(f"Backing up notes for user '{user}'...")
        total, backed = 0, 0
        for role in ["owner", "editor"]:
            notes = notes_file.get(role, [])
            for note in notes:
                total += 1
                backed += backup_note_from_file(httpsession, user, note['title'])
        print(f"{backed}/{total} notes successfully backed up")
    except Exception as e:
        print(f"Error backing up notes: {e}")
        return
