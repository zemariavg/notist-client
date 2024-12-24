import os
from cryptolib.unprotect import unprotect_note
from cryptolib.utils.noteparser import is_valid_protected_note
from datetime import datetime
from config import NOTES_DIR, PRIV_KEY
import json

def find_note(json_content, note_title, permission):
    roles = []
    if permission == "read":
        roles = ["owner", "editor", "viewer"]
    elif permission == "edit":
        roles = ["owner", "editor"]

    for role in roles:
        notes = json_content.get(role, [])
        for note in notes:
            if note.get("title") == note_title:
                return note
    return None

def read_note(note_path):
    with open(note_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def read_user_note(user, note_title: str) -> None:
    try:
        note_path = os.path.join(NOTES_DIR, f"{user}_notes.json")
        print(f"Reading note '{note_title}' ...\n")

        formatted_title = f"{user}_{note_title.replace(' ', '_')}"
        json_content = read_note(note_path)
        protected_note = find_note(json_content, formatted_title, "read")

        if not protected_note:
            raise Exception(f"Note '{note_title}' not found for user '{user}' or user has no access.")
        elif is_valid_protected_note(protected_note):
            # unprotect note
            unprotected = unprotect_note(protected_note, PRIV_KEY)[0]
            print(f"Title: {unprotected['title']}")
            print(f"Version: {unprotected['version']}, Last modified by: {unprotected['last_modified_by']}")
            print(f"Content: {unprotected['note_content']}\n")
        else:
            raise Exception(f"read_note.py: Note '{note_title}': Invalid protected json")
    except Exception as e:
        print(f"Error reading note: {e}\n")
        return