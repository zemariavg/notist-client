import os
from cryptolib.protect import protect_note
from cryptolib.utils import write_note, build_user_unprotected_json, generate_secret_key
from datetime import datetime
from config import NOTES_DIR, PUB_KEY

def create_note(user: str) -> None:
    try:
        title = input("Enter the title: ").strip()
        note_path = os.path.join(NOTES_DIR, f"{title}.json")
        if os.path.exists(note_path) or os.path.exists(note_path.replace('.json', '_protected.json')):
            print("Note with the same title already exists.")
            return
        
        print("Enter the note content (press Enter twice to finish):")
        
        lines = []
        while True:
            line = input()  # Read a line of text
            if line == "":  # Stop if the user presses Enter twice
                break
            lines.append(line)
            
        content = "\n".join(lines)
        
        # build json
        json_content = build_user_unprotected_json(title=title, note=content, 
            date_created=datetime.now().isoformat(), date_modified=datetime.now().isoformat(),
            last_modified_by=user, version=1, owner_username=user, 
            editors=[], viewers=[])
        # protect note
        aes_key = generate_secret_key()
        protected = protect_note(json_content, aes_key, PUB_KEY)
        protected_path = note_path.replace('.json', '_protected.json')
        write_note(protected_path, protected, 'PROTECTED')
        print(f"Note {title} created successfully.")
    except Exception as e:
        print(f"Error creating note: {e}")
        return
