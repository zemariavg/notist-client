import os
from cryptolib.utils import read_note
from cryptolib.unprotect import unprotect_note
from datetime import datetime
from config import NOTES_DIR, PRIV_KEY

def read_user_note(note_name: str) -> None:
    try:
        #TODO: Fix read/edit note. Needs to read/edit from the correct directory if has read/edit access
        note_path = os.path.join(NOTES_DIR, f"{note_name}.json").replace('.json', '_protected.json')
        print(f"Reading note {note_name}...")
        
        # unprotect note
        json_content = read_note(note_path, 'PROTECTED')
        unprotected = unprotect_note(json_content, PRIV_KEY)[0]
        print(f"Title: {unprotected['title']}")
        print(f"Version: {unprotected['version']}, Last modified by: {unprotected['last_modified_by']}")
        print(f"Content: {unprotected['note_content']}")
    except Exception as e:
        print(f"Error reading note: {e}")
        return