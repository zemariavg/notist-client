from cryptolib import *
from cryptolib.utils import read_note
from cryptolib.unprotect import unprotect_note
from cryptolib.protect import protect_note
from datetime import datetime
from config import NOTES_DIR, PRIV_KEY, PUB_KEY, FRONTEND_URL, SERVER_TIMEOUT
import requests
import os
import json

def backup_notes(user: str) -> None:
    try:
        notes = os.listdir(NOTES_DIR)
        headers = { "Content-Type": "application/json" }
        
        notes = [note for note in notes if note.endswith('_protected.json')]        
        if not notes:
            print("No notes to backup.")
            return
        
        for note in notes:
            try: 
                note_path = os.path.join(NOTES_DIR, note)
                print(note_path)
                
                note_json = read_note(note_path, 'PROTECTED')
                unprotected_note, note_key = unprotect.unprotect_note(note_json, PRIV_KEY)
                
                note_json['server_metadata'] = {
                    "req_from": user,
                    "title" : unprotected_note['title'],
                    "version": unprotected_note['version'],
                    "last_modified_by": unprotected_note['last_modified_by'],
                    "owner": unprotected_note['owner'],
                    "editors": unprotected_note['editors'],
                    "viewers": unprotected_note['viewers']
                }
                
                print("Sending notes to server...")
                response = requests.post(f"{FRONTEND_URL}/note", json=note_json, headers=headers, timeout=SERVER_TIMEOUT)
                if response.status_code != 201:
                    print(f"Failed to send note to server. Response: {response.status_code}")
                else:
                    print(f"sent note {note} to server. Response: {response.status_code}")
            except Exception as e:
                print(f"Error sending note to server: {e}")
                continue
    except Exception as e:
        print(f"Error backing up notes: {e}")
        return