import os
from cryptolib.unprotect import unprotect_note
from cryptolib.protect import protect_note
from cryptolib.utils import read_note, write_note
from datetime import datetime
from config import NOTES_DIR, PRIV_KEY, PUB_KEY 
    
def edit_note(note_name: str, user: str) -> None:
    try:
        note_path = os.path.join(NOTES_DIR, f"{note_name}.json").replace('.json', '_protected.json')
        
        # unprotect note
        json_content = read_note(note_path, 'PROTECTED')
        unprotected, note_key = unprotect_note(json_content, PRIV_KEY)
        
        print(f"Editing note {note_name}...")
        print(f"Current content: {unprotected['note_content']}")
        
        print("Enter the new content (press Enter twice to finish):")
        lines = []
        
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        
        content = "\n".join(lines)
        unprotected['note_content'] = content
        unprotected['date_modified'] = datetime.now().isoformat()
        unprotected['last_modified_by'] = user
        unprotected['version'] += 1
        
        # protect note
        protected = protect_note(unprotected, note_key, PUB_KEY)
        write_note(note_path, protected, 'PROTECTED')
        print(f"Note {note_name} edited successfully.")
    except Exception as e:
        print(f"Error editing note: {e}")
        return