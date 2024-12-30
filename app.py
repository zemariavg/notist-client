import argparse
import requests
import os
from config import NOTES_DIR, KEYS_DIR, PRIV_KEY, PUB_KEY, FRONTEND_URL
from actions.create_note import create_note
from actions.read_note import read_user_note
from actions.edit_note import edit_note
from actions.backup_notes import backup_all_notes
from actions.retrieve_notes import retrieve_notes

def print_actions() -> None:
    print("Notist. The fully encripted note-taking app.")
    print("\t1 - create note")
    print("\t2 - read note")
    print("\t3 - edit note")
    print("\t4 - add editor/viewer")
    print("\t5 - remove editor/viewer")
    print("\t6 - backup notes")
    print("\t7 - retrieve notes")
    print("\t8 - check integrity")
    print("\t9 - exit")

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
            # note = input("Note to add editor/viewer: ")
            # add_editor_viewer(note)
            print("Not implemented.")

        elif action == "5":
            # note = input("Note to remove editor/viewer: ")
            # remove_editor_viewer(note)
            print("Not implemented.")

        elif action == "6":
            backup_all_notes(user)
            
        elif action == "7":
            # print("Retrieving notes from server...")
            retrieve_notes(user)
            print(f"Notes for user '{user}' successfully retrieved and stored locally.")
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
