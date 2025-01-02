import os
from cryptolib.unprotect import unprotect_note
from cryptolib.protect import protect_note
from cryptolib.utils.noteparser import is_valid_protected_note
from datetime import datetime
from config import NOTES_DIR, get_pub_key, get_priv_key
from utils.noteutils import read_note, find_note, write_note_content
from actions.backup_notes import backup_on_server
from actions.retrieve_notes import retrieve_notes
from requests import Session
import json

def edit_note(httpsession: Session, note_title: str, user: str) -> None:
    try:
        notes_path = os.path.join(NOTES_DIR, f"{user}_notes.json")

        json_content = read_note(notes_path)
        protected_note = find_note(json_content, note_title, "edit")

        if not protected_note:
            print(f"Note '{note_title}' not found for user '{user}' or user has no access.")
            return
        elif is_valid_protected_note(protected_note):
            unprotected, note_key = unprotect_note(protected_note, get_priv_key(user))
            print(f"Editing note '{note_title}' ...")
            print(f"Current content: {unprotected['note_content']}")

            # edit note
            content = write_note_content()
            unprotected['note_content'] = content
            unprotected['date_modified'] = datetime.now().isoformat()
            unprotected['last_modified_by'] = user
            unprotected['version'] += 1

            # protect note
            protected = protect_note(unprotected, note_key, get_pub_key(user))

            if backup_on_server(httpsession, user, protected) == 0:
                return

            retrieve_notes(httpsession, user)
            print(f"Note '{note_title}' edited successfully.")
        else:
            raise Exception(f"edit_note.py: Note '{note_title}': Invalid protected json")
    except Exception as e:
        print(f"Error editing note: {e}")
        return
