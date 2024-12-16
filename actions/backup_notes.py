from typing import Union
from cryptolib import *
from cryptolib.utils import *
from cryptolib.unprotect import unprotect_note
from cryptolib.protect import protect_note
from datetime import datetime
from config import NOTES_DIR, PRIV_KEY, PUB_KEY, FRONTEND_URL
import requests

def backup_notes() -> None:
    notes = os.listdir(NOTES_DIR)
    for note in notes:
        if note.startswith('.') or not note.endswith('_protected.json'):
            # skip hidden files and non protected json files
            continue
            
        note_path = os.path.join(NOTES_DIR, note)
        print(note_path)
        
        json_content = read_note(note_path, 'PROTECTED')
        # unprotect note to get metadata
        unprotected, note_key = unprotect.unprotect_note(json_content, PRIV_KEY)
        
        # build metadata
        metadata = {
            "version": unprotected['version'],
            "last_modified_by": unprotected['last_modified_by'],
            "owner": unprotected['owner'],
            "editors": unprotected['editors'],
            "viewers": unprotected['viewers']
        }
        
        # append metadata to protected note
        json_content['server_metadata'] = metadata
        # pretty print json
        json_content = json.dumps(json_content, indent=4)
        print(json_content)
        
        # send note to server
        response = requests.post(f"{FRONTEND_URL}/note", json=json_content)
