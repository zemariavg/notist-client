import os
from cryptolib.utils import read_note
from cryptolib.unprotect import unprotect_note
from datetime import datetime
from config import NOTES_DIR, PRIV_KEY
import json


def find_note(json_content, note_title):
    for role in ["owner", "editor", "viewer"]:
        notes = json_content.get(role, [])
        for note in notes:
            if note.get("title") == note_title:
                return note
    return None

def read_user_note(user, note_title: str) -> None:
    try:
        note_path = os.path.join(NOTES_DIR, f"{user}_notes.json")
        print(f"Reading note '{note_title}' ...\n")
        
        with open(note_path, 'r', encoding='utf-8') as file:
            json_content = json.load(file)

        note = find_note(json_content, note_title)

        if not note:
            raise Exception(f"Note '{note_title}' not found for user '{user}'.")
        else:
            # unprotect note
            unprotected = unprotect_note(note, PRIV_KEY)[0]
            print(f"Title: {unprotected['title']}")
            print(f"Version: {unprotected['version']}, Last modified by: {unprotected['last_modified_by']}")
            print(f"Content: {unprotected['note_content']}\n")
    except Exception as e:
        print(f"Error reading note: {e}\n")
        return