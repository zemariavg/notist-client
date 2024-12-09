import argparse
import requests
import os
from datetime import datetime
from cryptolib import notist
from cryptolib.utils import noteparser as np

LINK = 'https://localhost'
PORT = 5000
SERVER = f"{LINK}:{PORT}"
NOTES_DIR = os.path.join(os.path.expanduser('~'), 'notist')

def print_actions() -> None:
    print("Notist. The fully encripted note-taking app.")
    print("\t1 - create note")
    print("\t2 - read note")
    print("\t3 - add editor/viewer")
    print("\t4 - remove editor/viewer")
    print("\t5 - backup notes")
    print("\t6 - restore notes")
    print("\t7 - check integrity")
    print("\t8 - exit")

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
        np.write_note(note_path, np.build_user_unprotected_json(
            id=-1, title=title, note=content, date_created=str(datetime.now()), 
            date_modified=str(datetime.now()), last_modified_by=0, version=0, 
            owner_id=0, owner_username="admin", editors=[], viewers=[]
        ), mode='UNPROTECTED')
        # race condition here ? (file is not protected yet)
        # Create a new aes key for the note?
        # notist.protect_note(note_path, 
        
    except Exception as e:
        print(f"Error creating note: {e}")
        return

def handle_read_note(note: str) -> None:
    pass

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
        print("\033[H\033[J") # clear screen
        print_actions()
        action = input("Action: ")
    
        if action == "1":
            handle_create_note()
        
        elif action == "2":
            note = input("Note name: ")
            handle_read_note(note)
        
        elif action == "3":
            note = input("Note to add editor/viewer: ")
            handle_add_editor_viewer(note)

        elif action == "4":
            note = input("Note to remove editor/viewer: ")
            handle_remove_editor_viewer(note)
            
        elif action == "5":
            print("Backing up notes...")
            handle_backup_notes()
            
        elif action == "6":
            print("Restoring notes...")
            handle_restore_notes()
        
        elif action == "7":
            note = input("Note to check integrity: ")
            version = input("Version to check: ")
            handle_check_integrity(note)
            
        elif action == "8":
            print("Exiting...")
            break
        
        else:
            print("Invalid action.")
            continue 