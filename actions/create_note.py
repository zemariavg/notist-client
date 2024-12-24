import os
from cryptolib.protect import protect_note
from cryptolib.utils.noteparser import build_user_unprotected_json, generate_secret_key
from datetime import datetime
from config import NOTES_DIR, PUB_KEY
from utils.noteutils import write_title, write_note_content, write_note
import json

def create_note(user: str) -> None:
    try:
        notes_path = os.path.join(NOTES_DIR, f"{user}_notes.json")

        title = write_title(user)
        content = write_note_content()

        # build json
        json_content = build_user_unprotected_json(title=title, note=content, 
            date_created=datetime.now().isoformat(), date_modified=datetime.now().isoformat(),
            last_modified_by=user, version=1, owner_username=user, 
            editors=[], viewers=[])

        # protect and store note
        aes_key = generate_secret_key()
        protected_note = protect_note(json_content, aes_key, PUB_KEY)
        write_note(notes_path, protected_note)

        print(f"Note '{title}' created, stored and protected successfully.")
        # TODO: backup on create note. Backup to DB before writing locally? (To check duplicate note title)
    except Exception as e:
        print(f"Error creating note: {e}")
        return
