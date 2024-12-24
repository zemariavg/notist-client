import os
from cryptolib.protect import protect_note
from cryptolib.utils.noteparser import build_user_unprotected_json, generate_secret_key
from datetime import datetime
from config import NOTES_DIR, PUB_KEY
import json

def write_note_content():
    print("Enter the note content (press Enter twice to finish):")
    lines = []
    while True:
        line = input()  # Read a line of text
        if line == "":  # Stop if the user presses Enter twice
            break
        lines.append(line)
    content = "\n".join(lines)
    return content

def write_title(user):
    title = input("Enter the title: ").strip()
    if title == "":
        print("Title cannot be empty.")
        return
    formatted_title = f"{user}_{title.replace(' ', '_')}"
    return formatted_title

def write_note(notes_path, note):
    if os.path.exists(notes_path):
        # Append to existing file
        with open(notes_path, 'r+') as f:
            notes_data = json.load(f)
            notes_data.setdefault('owner', []).append(note)
            f.seek(0)
            json.dump(notes_data, f, indent=4)

def create_note(user: str) -> None:
    try:
        notes_path = os.path.join(NOTES_DIR, f"{user}_notes.json")

        title = write_title(user)
        content = write_note_content()

        # build json
        json_content = build_user_unprotected_json(title=title, note=content, 
            date_created=datetime.now().isoformat(), date_modified=datetime.now().isoformat(),
            last_modified_by=user, version=1, owner_username=user, 
            editors=[], viewers=[])

        # protect and store note
        aes_key = generate_secret_key()
        protected_note = protect_note(json_content, aes_key, PUB_KEY)
        write_note(notes_path, protected_note)

        print(f"Note '{title}' created, stored and protected successfully.")
        # TODO: backup on create note. Backup to DB before writing locally? (To check duplicate note title)
    except Exception as e:
        print(f"Error creating note: {e}")
        return
