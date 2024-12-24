import os
from cryptolib.unprotect import unprotect_note
from cryptolib.utils.noteparser import is_valid_protected_note
from datetime import datetime
from config import NOTES_DIR, PRIV_KEY
from utils.noteutils import read_note, find_note
import json

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