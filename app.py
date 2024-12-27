import argparse
import requests
import os
from config import NOTES_DIR, KEYS_DIR, PRIV_KEY, PUB_KEY, FRONTEND_URL
from actions.create_note import create_note
from actions.read_note import read_user_note
from actions.edit_note import edit_note
from actions.backup_notes import backup_all_notes, backup_note
from actions.retrieve_notes import retrieve_notes
from actions.add_collaborator import add_collaborator, add_collaborator
from actions.check_integrity import check_integrity

def print_actions() -> None:
    print("Notist. The fully encripted note-taking app.")
    print("\t1 - create note")
    print("\t2 - read note")
    print("\t3 - edit note")
    print("\t4 - add editor/viewer")
    print("\t5 - backup notes")
    print("\t6 - retrieve notes")
    print("\t7 - check integrity")
    print("\t8 - exit")

def clear_screen() -> None:
    print("\033[H\033[J")
    
def mount_folders():
    if not os.path.exists(NOTES_DIR):
        os.makedirs(NOTES_DIR)

def login() -> str:
    user = input("Login as: ")
    #password = input("Password: ")
    #response = requests.post(f"{FRONTEND_URL}/login", json={"username": user, "password": password})

    mount_folders()
    retrieve_notes(user) # retrieve_notes on login
    return user

    # if response.status_code == 200:
    #     return response.json()["token"]
    # else:
    #     print("Login failed.")
    #     exit(1)


if __name__ == '__main__':
    user = login()

    # main loop
    while True:
        print_actions()
        action = input("Action: ")

        if action == "1":
            create_note(user)

        elif action == "2":
            note_title = input("Note Title: ")
            read_user_note(user, note_title)

        elif action == "3":
            note_title = input("Note Title: ")
            # list notes
            # note = input("Note to edit: ")
            edit_note(note_title, user)

        elif action == "4":
            add_collaborator(user)

        elif action == "5":
            backup_all_notes(user)
            
        elif action == "6":
            # print("Retrieving notes from server...")
            retrieve_notes(user)
            print(f"Notes for user '{user}' successfully retrieved and stored.")
        elif action == "7":
            note = input("Note to check integrity: ")
            version = input("Version to check integrity: ")
            if not version.isnumeric():
                print("Version must be an integer.")
                continue

            check_integrity(user, note, int(version))

        elif action == "8":
            print("Exiting...")
            break

        else:
            print("Invalid action.")
            continue
