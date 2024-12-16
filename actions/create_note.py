from cryptolib import *
from cryptolib.utils import *
from cryptolib.protect import protect_note
from datetime import datetime
from config import NOTES_DIR, PUB_KEY

def create_note(user: str) -> None:
    try:
        title = input("Enter the title: ").strip()
        print("Enter the note content (press Enter twice to finish):")
        
        lines = []
        while True:
            line = input()  # Read a line of text
            if line == "":  # Stop if the user presses Enter twice
                break
            lines.append(line)
            
        content = "\n".join(lines)
        
        note_path = os.path.join(NOTES_DIR, f"{title}.json")
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