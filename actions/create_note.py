import os, requests
from cryptolib.protect import protect_note
from cryptolib.utils.noteparser import build_user_unprotected_json, generate_secret_key
from datetime import datetime
from config import NOTES_DIR, get_pub_key, FRONTEND_URL, SERVER_TIMEOUT
from utils.noteutils import write_title, write_note_content, write_note
from requests import Session
import json

def create_note(httpsession: Session, user: str) -> None:
    try:
        notes_path = os.path.join(NOTES_DIR, f"{user}_notes.json")

        title = write_title(user)
        if title == None:
           return
        content = write_note_content()

        # build json
        json_content = build_user_unprotected_json(title=title, note=content, 
            date_created=datetime.now().isoformat(), date_modified=datetime.now().isoformat(),
            last_modified_by=user, version=1, owner_username=user, 
            editors=[], viewers=[])

        # protect and store note
        aes_key = generate_secret_key()
        protected_note = protect_note(json_content, aes_key, get_pub_key(user))

        headers = {
            "Content-Type": "application/json",
            "version": str(json_content['version'])  # TODO: Se alguem intersepta esta note e altera a versao tamos fdds
        }
        
        response = httpsession.post(f"{FRONTEND_URL}/create_note", json=protected_note, headers=headers, timeout=SERVER_TIMEOUT, verify=False)

        if response.status_code == 401:
            print(f"{response}: Note already exists in the database.")
            return
        elif response.status_code != 201:
            print(f"{response}: Failed to send note to server.")
            return

        write_note(notes_path, protected_note)
        print(f"Note '{title}' created, stored and protected successfully.")
    except Exception as e:
        print(f"Error creating note: {e}")
        return
