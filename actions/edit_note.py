import os
from cryptolib.unprotect import unprotect_note
from cryptolib.protect import protect_note
from cryptolib.utils.noteparser import is_valid_protected_note
from datetime import datetime
from config import NOTES_DIR, PRIV_KEY, PUB_KEY
import json

def find_note(json_content, note_title, permission):
    roles = []
    if permission == "read":
        roles = ["owner", "editor", "viewer"]
    elif permission == "edit":
        roles = ["owner", "editor"]

    for role in roles:
        notes = json_content.get(role, [])
        for note in notes:
            if note.get("title") == note_title:
                return note
    return None

def read_note(note_path):
    with open(note_path, 'r', encoding='utf-8') as file:
        return json.load(file)

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

def write_note(notes_path, json_content):
    with open(notes_path, 'w', encoding='utf-8') as file:
        json.dump(json_content, file, indent=4)
def overwrite_note(notes_path, json_content, protected_note):
    roles = ["owner", "editor"]  # Roles with editing permissions
    for role in roles:
        notes = json_content.get(role, [])
        for i, note in enumerate(notes):
            if note.get("title") == protected_note['title']:
                notes[i] = protected_note  # Update the note
                break
    write_note(notes_path, json_content)

def edit_note(note_title: str, user: str) -> None:
    try:
        notes_path = os.path.join(NOTES_DIR, f"{user}_notes.json")

        formatted_title = f"{user}_{note_title.replace(' ', '_')}"
        json_content = read_note(notes_path)
        protected_note = find_note(json_content, formatted_title, "edit")

        if not protected_note:
            raise Exception(f"Note '{note_title}' not found for user '{user}' or user has no access.")
        elif is_valid_protected_note(protected_note):
            unprotected, note_key = unprotect_note(protected_note, PRIV_KEY)
            print(f"Editing note '{note_title}' ...")
            print(f"Current content: {unprotected['note_content']}")

            #edit note
            content = write_note_content()
            unprotected['note_content'] = content
            unprotected['date_modified'] = datetime.now().isoformat()
            unprotected['last_modified_by'] = user
            unprotected['version'] += 1

            # protect note
            protected = protect_note(unprotected, note_key, PUB_KEY)
            overwrite_note(notes_path, json_content, protected)
            print(f"Note '{note_title}' edited successfully.")
        else:
            raise Exception(f"read_note.py: Note '{note_title}': Invalid protected json")
    except Exception as e:
        print(f"Error editing note: {e}")
        return