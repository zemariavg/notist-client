import json
import os

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
