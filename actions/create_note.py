import os
from cryptolib.protect import protect_note
from cryptolib.utils import write_note, build_user_unprotected_json, generate_secret_key
from datetime import datetime
from config import NOTES_DIR, PUB_KEY
import json

def write_content():
    title = input("Enter the title: ").strip()
    if title == "":
        print("Title cannot be empty.")
        return

    print("Enter the note content (press Enter twice to finish):")
    lines = []
    while True:
        line = input()  # Read a line of text
        if line == "":  # Stop if the user presses Enter twice
            break
        lines.append(line)

    content = "\n".join(lines)
    return title, content

def add_local_note(notes_path, note):
    if os.path.exists(notes_path):
        # Append to existing file
        with open(notes_path, 'r+') as f:
            notes_data = json.load(f)
            notes_data.setdefault('owner', []).append(note)
            f.seek(0)
            json.dump(notes_data, f, indent=4)
    else:
        # Create new file with initial structure
        notes_file = {
            "owner": [note],
            "editor": [],
            "viewer": []
        }
        with open(notes_path, 'w') as f:
            json.dump(notes_file, f, indent=4)

def create_note(user: str) -> None:
    try:
        notes_path = os.path.join(NOTES_DIR, f"{user}_notes.json")

        title, content = write_content()

        # build json
        json_content = build_user_unprotected_json(title=title, note=content, 
            date_created=datetime.now().isoformat(), date_modified=datetime.now().isoformat(),
            last_modified_by=user, version=1, owner_username=user, 
            editors=[], viewers=[])

        # protect note
        aes_key = generate_secret_key()
        protected_note = protect_note(json_content, aes_key, PUB_KEY)

        add_local_note(notes_path, protected_note)

        """
        # protect note
        aes_key = generate_secret_key()
        protected_note = protect_note(json_content, aes_key, PUB_KEY)
        protected_path = note_path.replace('.json', '_protected.json')
        write_note(protected_path, protected_note, 'PROTECTED')
        """

        print(f"Note '{title}' created, stored and protected successfully.")
        # TODO: Note titles - <owner username>_A. Ex: alice_A, alice_B
        # TODO: backup on create note
        # TODO: Create/Backup needs to check if there is already a note with the same title in DB
        # TODO: On Create/Backup add note key to collaborator table
    except Exception as e:
        print(f"Error creating note: {e}")
        return
