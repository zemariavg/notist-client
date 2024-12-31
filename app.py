import argparse
import requests
import os
import getpass
from config import NOTES_DIR, KEYS_DIR, PRIV_KEY, PUB_KEY, FRONTEND_URL
from requests import Session
from actions.create_note import create_note
from actions.read_note import read_user_note
from actions.edit_note import edit_note
from actions.backup_notes import backup_all_notes
from actions.retrieve_notes import retrieve_notes
from actions.add_collaborator import add_collaborator, add_collaborator
from actions.check_integrity import check_integrity
from actions.list_notes import list_notes

def print_actions() -> None:
    print("Select Action:")
    print("\t1 - create note")
    print("\t2 - read note")
    print("\t3 - edit note")
    print("\t4 - add editor/viewer")
    print("\t5 - backup notes")
    print("\t6 - retrieve notes")
    print("\t7 - check integrity")
    print("\t8 - list notes")
    print("\t9 - exit")

def clear_screen() -> None:
    print("\033[H\033[J")

def mount_folders():
    if not os.path.exists(NOTES_DIR):
        os.makedirs(NOTES_DIR)

def login():
    print("LOGIN NOTIST")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    try:
        session = requests.Session()
        response = session.post(f"{FRONTEND_URL}/login", json={"username": username, "password": password}, verify=False)

        if(response.status_code != 200):
            raise Exception(response)

        mount_folders()

        token = response.json()['token']
        headers = {'Authorization': f'Bearer {token}'}
        session.headers.update(headers)

        retrieve_notes(session, username)
        print(f"Successfully logged in as '{username}'")
        return username, session
    except Exception as e:
        raise e

if __name__ == '__main__':
    try:
        username, session = login()
    except Exception as e:
        print(f"Failed to login")
        exit(1)

    # main loop
    print("Welcome to Notist. The fully encrypted note-taking app.")
    while True:
        print_actions()
        action = input("Action: ")
        print("")

        if action == "1":
            create_note(session, username)
            print("")
        elif action == "2":
            note_title = input("Note Title: ")
            read_user_note(username, note_title)
            print("")
        elif action == "3":
            note_title = input("Note Title: ")
            # list notes
            edit_note(session, note_title, username)
            print("")
        elif action == "4":
            add_collaborator(session, username)
            print("")
        elif action == "5":
            backup_all_notes(session, username)
            print("")
        elif action == "6":
            print("Retrieving notes from server...")
            retrieve_notes(session, username)
            print(f"Notes for user '{username}' successfully retrieved and stored.")
            print("")
        elif action == "7":
            note = input("Note to check integrity: ")
            version = input("Version to check integrity: ")
            if not version.isnumeric():
                print("Version must be an integer.")
                continue

            check_integrity(username, note, int(version))
            print("")
        elif action == "8":
            list_notes(session, username)
            print("")
        elif action == "9":
            print("Exiting...")
            print("")
            break

        else:
            print("Invalid action.")
            print("")
            continue
