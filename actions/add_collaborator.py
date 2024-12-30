import requests
import tempfile
from datetime import datetime
from config import FRONTEND_URL, PRIV_KEY, SERVER_TIMEOUT, NOTES_DIR, PUB_KEY
from utils.noteutils import *
from requests import Session
from cryptolib.unprotect import unprotect_note
from cryptolib.protect import protect_note

def add_collaborator(httpsession: Session, user: str):
    try:
        note_title = input("Enter the note title: ")
        notes_path = os.path.join(NOTES_DIR, f"{user}_notes.json")
        notes_file_json_content = read_note(notes_path)
        note = fetch_note(notes_file_json_content, note_title, user)
        if note is None:
            return

        user_to_add = input("Enter the user to add as editor/viewer: ")
        if user == user_to_add:
            print("You cannot add yourself as editor/viewer.")
            return

        user_to_add_pub_key = fetch_user_pub_key(httpsession, user_to_add)
        if not user_to_add_pub_key:
            return

        ciphered_note_key = note.get("ciphered_note_key")
        unprotected_note, note_key =  unprotect_note(note, PRIV_KEY)
        
        permission = input("Enter the permission (editor/viewer): ")
        if not update_note_permissions(unprotected_note, user_to_add, permission):
            return

        update_note_metadata(unprotected_note, user)
        collaborator_protected_note = protect_with_new_key(unprotected_note, note_key, user_to_add_pub_key)
        collaborator_protected_note['version'] = unprotected_note['version']

        add_collaborator_to_backend(httpsession, user_to_add, permission, collaborator_protected_note, note_title)
        
        # protect with this user's public key so he can access it
        edited_note = protect_note(unprotected_note, note_key, PUB_KEY)
        overwrite_note(notes_path, notes_file_json_content, edited_note)

    except Exception as e:
        print(f"Error adding editor/viewer: {str(e)}")

def fetch_note(json_content, note_title, user):
    note = find_note(json_content, note_title, "edit")
    if note is None:
        print(f"Cannot find the note {note_title}. Do you have access to {note_title}?")
    return note

def fetch_user_pub_key(httpsession, user_to_add):
    response = httpsession.get(
        f"{FRONTEND_URL}/users/{user_to_add}/pub_key",
        timeout=SERVER_TIMEOUT,
        verify=False
    )
    if response.status_code == 404 or response.status_code != 200:
        print(f"User {user_to_add} not found.")
        return None

    user_to_add_pub_key = response.json().get("pub_key")
    if not user_to_add_pub_key:
        print(f"User {user_to_add} has no public key.")
    return user_to_add_pub_key

def update_note_permissions(unprotected_note, user_to_add, permission):
    if permission not in ["editor", "viewer"]:
        print("Invalid permission.")
        return False

    if permission == "editor":
        unprotected_note["editors"].append(user_to_add)
    elif permission == "viewer":
        unprotected_note["viewers"].append(user_to_add)
    return True

def update_note_metadata(unprotected_note, user):
    unprotected_note["version"] += 1
    unprotected_note["date_modified"] = datetime.now().isoformat()
    unprotected_note["last_modified_by"] = user

def protect_with_new_key(unprotected_note, note_key, user_to_add_pub_key):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_pub_key:
        temp_pub_key.write(user_to_add_pub_key)
        temp_pub_key_path = temp_pub_key.name

    try:
        return protect_note(unprotected_note, note_key, temp_pub_key_path)
    finally:
        os.unlink(temp_pub_key_path)

def add_collaborator_to_backend(httpsession, user_to_add, permission, protected_note, note_title):
    response = httpsession.post(
        f"{FRONTEND_URL}/add_collaborator",
        json={"collaborator": user_to_add, "permission": permission, "note": protected_note},
        timeout=SERVER_TIMEOUT,
        verify=False
    )
    if response.status_code == 201:
        print(f"User {user_to_add} added as {permission} to note {note_title}")
    else:
        print(f"Failed to add user {user_to_add} as {permission} to note {note_title}")
        print(response.json().get("error", "Unknown error"))
