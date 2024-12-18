import argparse
import requests
import os
from config import NOTES_DIR, KEYS_DIR, PRIV_KEY, PUB_KEY, FRONTEND_URL 
from actions.create_note import create_note
from actions.read_note import read_user_note
from actions.edit_note import edit_note
from actions.backup_notes import backup_notes   

# while login not implemented
user = 'user1'

def print_actions() -> None:
    print("Notist. The fully encripted note-taking app.")
    print("\t1 - create note")
    print("\t2 - read note")
    print("\t3 - edit note")
    print("\t4 - add editor/viewer")
    print("\t5 - remove editor/viewer")
    print("\t6 - backup notes")
    print("\t7 - get notes")
    print("\t8 - check integrity")
    print("\t9 - exit")
    
def clear_screen() -> None:
    print("\033[H\033[J")

def login() -> str:
    user = input("Username: ")
    password = input("Password: ")
    response = requests.post(f"{FRONTEND_URL}/login", json={"username": user, "password": password})
    
    return ""
    if response.status_code == 200:
        return response.json()["token"]
    else:
        print("Login failed.")
        exit(1)

if __name__ == '__main__':
    # auth_token = login()
   
    if not os.path.exists(NOTES_DIR):
        os.makedirs(NOTES_DIR)

    # main loop
    while True:
        print_actions()
        action = input("Action: ")
    
        if action == "1":
            create_note(user)
        
        elif action == "2":
            note_name = input("Note name: ")
            read_user_note(note_name)
            
        elif action == "3":
            note_name = input("Note name: ")
            # list notes
            # note = input("Note to edit: ")
            edit_note(note_name, user)
        
        elif action == "4":
            # note = input("Note to add editor/viewer: ")
            # add_editor_viewer(note)
            print("Not implemented.")

        elif action == "5":
            # note = input("Note to remove editor/viewer: ")
            # remove_editor_viewer(note)
            print("Not implemented.")
            
        elif action == "6":
            backup_notes()
            
        elif action == "7":
            # print("Retrieving notes from server...")

        
        elif action == "8":
            # note = input("Note to check integrity: ")
            # version = input("Version to check: ")
            # check_integrity(note)
            print("Not implemented.")
            
        elif action == "9":
            print("Exiting...")
            break
        
        else:
            print("Invalid action.")
            continue 