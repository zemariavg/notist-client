from cryptolib import *
from cryptolib.utils import read_note
from cryptolib.unprotect import unprotect_note
from cryptolib.protect import protect_note
from datetime import datetime
from config import NOTES_DIR, PRIV_KEY, PUB_KEY, FRONTEND_URL
import requests
import os
import json

def backup_notes() -> None:
    try:
        notes = os.listdir(NOTES_DIR)
        headers = { "Content-Type": "application/json" }
        for note in notes:
            if note.startswith('.') or not note.endswith('_protected.json'):
                # skip hidden files and non protected json files
                continue
                
            note_path = os.path.join(NOTES_DIR, note)
            print(note_path)
            
            note_json = read_note(note_path, 'PROTECTED')
            unprotected_note, note_key = unprotect.unprotect_note(note_json, PRIV_KEY)
            
            metadata = {
                "version": unprotected_note['version'],
                "last_modified_by": unprotected_note['last_modified_by'],
                "owner": unprotected_note['owner'],
                "editors": unprotected_note['editors'],
                "viewers": unprotected_note['viewers']
            }
        
            note_json['server_metadata'] = metadata
            
            # send note to server
            response = requests.post(f"{FRONTEND_URL}/note", json=note_json, headers=headers)
            print(f"sent note {note} to server. Response: {response.status_code}")
            print(f"note content: {note_json}")
    except Exception as e:
        print(f"Error backing up notes: {e}")
        return