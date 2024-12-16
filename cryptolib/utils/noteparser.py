from ast import Eq
from .file import * 
from .cryptoutils import *
import json

"""
JSON note file handling functions
    These functions check if the JSON note has all the required fields and valid types.
    They allow to validate if a note is structured correctly.

    Check /example_notes/ for examples of valid notes.
"""

def error(message: str) -> None:
    print(f"note_parser.py error: {message}")

def read_note(file_path: str, mode: str) -> dict:
    """ Reads json note file and returns content as a dictionary """
    file_content = file.read_file_content(file_path)
    json_content = json.loads(file_content)

    if mode == 'PROTECTED' and is_valid_protected_note(json_content):
        return json_content
    elif mode == 'UNPROTECTED' and is_valid_unprotected_note(json_content):
        return json_content
    else:
        error(f"read_note: Invalid JSON content or mode '{mode}' in file {file_path}")
        return {}

def write_note(file_path: str, json_content: dict, mode: str) -> None:
    """ Writes content to a note json file. if protected, writes to _protected.json """

    if mode == 'PROTECTED' and is_valid_protected_note(json_content):
        file.write_file_content(file_path, json.dumps(json_content, indent=4))
    elif mode == 'UNPROTECTED' and is_valid_unprotected_note(json_content):
        file.write_file_content(file_path, json.dumps(json_content, indent=4))
    else:
        error(f"write_note: Invalid JSON content or mode '{mode}' in file {file_path}")

def build_server_metadata(json_content: dict) -> dict:
    return {
        'id': json_content['id'],
        'version': json_content['version'],
        'last_modified_by': json_content['last_modified_by'],
        'owner': json_content['owner'],
        'editors': json_content['editors'],
        'viewers': json_content['viewers']
    }

def build_user_protected_json(note: bytes, note_tag: bytes, iv: bytes, note_key: bytes) -> dict:
    """ builds a protected user JSON note with values encoded in base64 """
    return {
        'iv': encode_base64(iv),
        'note': encode_base64(note),
        'note_tag': encode_base64(note_tag),
        'note_key': encode_base64(note_key),
    }

def build_user_unprotected_json(title: str, note: str, date_created: str, date_modified: str,
        last_modified_by: str, version: int, owner_username: str, editors: list, viewers: list) -> dict:
    """ builds a user JSON note """
    return {
        'title': title,
        'note_content': note,
        'date_created': date_created,
        'date_modified': date_modified,
        'last_modified_by': last_modified_by,
        'version': version,
        'owner': owner_username,
        'editors': editors,
        'viewers': viewers
    }

def is_valid_protected_note(json_content: dict) -> bool:
    """ checks if a protected user note has all the required fields and valid types"""
    allowed_fields = [{"iv", "note", "note_tag", "note_key"}]
    allowed_types = [{"iv": str, "note": str, "note_tag": str, "note_key": str}]
    return is_valid_json(json_content, allowed_fields, allowed_types)

def is_valid_unprotected_note(json_content: dict) -> bool:
    """ Checks if a note has all the required fields and valid types for the unprotected note format. """
    # Define allowed fields and their types
    allowed_fields = [
        {
            'title', 'note_content', 'date_created', 'date_modified',
            'last_modified_by', 'version', 'owner', 'editors', 'viewers'
        }
    ]
    allowed_types = [
        {
            'title': str,
            'note_content': str,
            'date_created': str, 
            'date_modified': str,
            'last_modified_by': str,
            'version': int,
            'owner': str,
            'editors': list,  
            'viewers': list   
        },
    ]
    
    return is_valid_json(json_content, allowed_fields, allowed_types)

def is_valid_json(json: dict, allowed_fields: list, allowed_types: list,
                                                                nesting_level: int = 0) -> bool:
    """ Validates JSON data against allowed fields and types at each nesting level. """
    errors = []

    if nesting_level >= len(allowed_fields):
        return True

    for key, value in json.items():
        if key not in allowed_fields[nesting_level]:
            errors.append(f"Invalid key: {key}")

        expected_type = allowed_types[nesting_level].get(key)
        if expected_type:
            if not isinstance(value, expected_type):
                errors.append(f"Invalid type for key {key}: expected {expected_type}, got {type(value)}")
            elif isinstance(value, dict):
                if not is_valid_json(value, allowed_fields, allowed_types, nesting_level + 1):
                    errors.append(f"Invalid nested data for key {key}")
            elif isinstance(value, list):
                for item in value:
                    if not isinstance(item, str):
                        errors.append(f"Invalid list item for key {key}")
        else:
            errors.append(f"No type defined for key {key}")
    if errors:
        error(f"Invalid JSON data: {errors}")
        return False
    return True
