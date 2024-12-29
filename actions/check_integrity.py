import requests
import json
import os
import tempfile
from config import FRONTEND_URL, PRIV_KEY, SERVER_TIMEOUT
from cryptolib.check import check_note

def check_integrity(user: str, note_title: str, version: int) -> None:
    if type(version) != int or version < 1:
        print("Version must be 1 or greater.")
        return

    try:
        response = requests.get(f"{FRONTEND_URL}/users/{user}/notes/{note_title}/{version}", timeout=SERVER_TIMEOUT, verify=False)
        note = response.json()
        
        if 'error' in note:
            print(f"Error fetching note: {note['error']}")
            return
        
        if note is None:
            print(f"Note {note_title} version {version} not found.")
            return
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_note:
            json.dump(note, temp_note)
            temp_note_path = temp_note.name
            
        try:  
            check_note(temp_note_path, PRIV_KEY)
            print(f"Note {note_title} version {version} is intact.")
        except Exception as e:
            print(f"Note {note_title} version {version} has been tampered with: {e}")
       
        os.unlink(temp_note_path)
        
    except Exception as e:
        print(f"Error checking note integrity: {e}")