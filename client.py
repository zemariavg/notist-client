import argparse
import requests
import os
from datetime import datetime
from cryptolib import notist, protect, unprotect
from cryptolib.utils import noteparser as np

LINK = 'https://localhost'
PORT = 5000
SERVER = f"{LINK}:{PORT}"
NOTES_DIR = os.path.join(os.path.expanduser('~'), 'notist', 'notes')

# change keys to read from safe file with user password
KEYS_DIR = os.path.join(os.path.expanduser('~'), 'notist', 'keys')
PRIV_KEY = os.path.join(KEYS_DIR, 'priv.pem')
PUB_KEY = os.path.join(KEYS_DIR, 'pub.pem')
USER = 'admin'

def print_actions() -> None:
    print("Notist. The fully encripted note-taking app.")
    print("\t1 - create note")
    print("\t2 - read note")
    print("\t3 - edit note")
    print("\t4 - add editor/viewer")
    print("\t5 - remove editor/viewer")
    print("\t6 - backup notes")
    print("\t7 - restore notes")
    print("\t8 - check integrity")
    print("\t9 - exit")
    
def clear_screen() -> None:
    print("\033[H\033[J")

def login() -> str:
    user = input("Username: ")
    password = input("Password: ")
    response = requests.post(f"{SERVER}/login", json={"username": user, "password": password})
    
    if response.status_code == 200:
        return response.json()["token"]
    else:
        # print("Login failed.")
        # show server messages
        exit(1)
        
def handle_create_note() -> None:
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
        json_content = np.build_user_unprotected_json(title=title, note=content, 
            date_created=datetime.now().isoformat(), date_modified=datetime.now().isoformat(),
            last_modified_by=USER, version=1, owner_username=USER, 
            editors=[], viewers=[])
        # protect note
        aes_key = notist.generate_secret_key()
        protected = notist.protect_note(json_content, aes_key, PUB_KEY)
        protected_path = note_path.replace('.json', '_protected.json')
        notist.write_note(protected_path, protected, 'PROTECTED')
        print(f"Note {title} created successfully.")
    except Exception as e:
        print(f"Error creating note: {e}")
        return

def handle_read_note(note_name: str) -> None:
    try:
        note_path = os.path.join(NOTES_DIR, f"{note_name}.json").replace('.json', '_protected.json')
        print(f"Reading note {note_name}...")
        
        # unprotect note
        json_content = notist.read_note(note_path, 'PROTECTED')
        unprotected = unprotect.unprotect_note(json_content, PRIV_KEY)[0]
        print(f"Title: {unprotected['title']}")
        print(f"Version: {unprotected['version']}, Last modified by: {unprotected['last_modified_by']}")
        print(f"Content: {unprotected['note_content']}")
    except Exception as e:
        print(f"Error reading note: {e}")
        return
    
def handle_edit_note(note_name: str) -> None:
    try:
        note_path = os.path.join(NOTES_DIR, f"{note_name}.json").replace('.json', '_protected.json')
        
        # unprotect note
        json_content = notist.read_note(note_path, 'PROTECTED')
        unprotected, note_key = unprotect.unprotect_note(json_content, PRIV_KEY)
        
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
        unprotected['last_modified_by'] = USER
        unprotected['version'] += 1
        
        # protect note
        protected = notist.protect_note(unprotected, note_key, PUB_KEY)
        notist.write_note(note_path, protected, 'PROTECTED')
        print(f"Note {note_name} edited successfully.")
    except Exception as e:
        print(f"Error editing note: {e}")
        return

def handle_add_editor_viewer(note: str) -> None:
    # verify if owner of note first
    pass
    
def handle_remove_editor_viewer(note: str) -> None:
    # verify if owner of note first
    pass

def handle_backup_notes() -> None:
    pass
    
def handle_restore_notes() -> None:
    pass
    
def handle_check_integrity(note: str) -> None:
    pass


if __name__ == '__main__':
    # auth_token = login()
   
    if not os.path.exists(NOTES_DIR):
        os.makedirs(NOTES_DIR)

    # main loop
    while True:
        print_actions()
        action = input("Action: ")
    
        if action == "1":
            handle_create_note()
        
        elif action == "2":
            note_name = input("Note name: ")
            handle_read_note(note_name)
            
        elif action == "3":
            note_name = input("Note name: ")
            handle_edit_note(note_name)
        
        elif action == "4":
            note = input("Note to add editor/viewer: ")
            handle_add_editor_viewer(note)

        elif action == "5":
            note = input("Note to remove editor/viewer: ")
            handle_remove_editor_viewer(note)
            
        elif action == "6":
            print("Backing up notes...")
            handle_backup_notes()
            
        elif action == "7":
            print("Restoring notes...")
            handle_restore_notes()
        
        elif action == "8":
            note = input("Note to check integrity: ")
            version = input("Version to check: ")
            handle_check_integrity(note)
            
        elif action == "9":
            print("Exiting...")
            break
        
        else:
            print("Invalid action.")
            continue 