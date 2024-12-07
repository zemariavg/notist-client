from ast import Eq
from utils import file
from utils import cryptoutils as crypto
import json

def error(message: str) -> None:
    raise ValueError(f"noteparser.py error: {message}")
    
""" 
JSON note file handling functions 
    These functions check if the JSON note has all the required fields and valid types. 
    They allow to validate if a plain note is valid or if a ciphered note is valid.
    
    Check /example_notes/ for examples of valid notes.
"""

##################### USER JSON NOTE ############################
def read_user_json(file_path: str, mode: str) -> dict: 
    """ reads json note file and returns content as a dictionary """
    file_content = file.read_file_content(file_path)
    json_content = json.loads(file_content)
   
    if mode == 'CIPHERED' and is_valid_user_protected_json(json_content):
        return json_content
    elif mode == 'PLAIN' and is_valid_user_unprotected_json(json_content):
        return json_content
    else:
        error(f"read_json: Invalid JSON content or mode '{mode}' in file {file_path}")
        return {}
        
def write_user_json(file_path: str, json_content: dict, mode: str) -> None:
    """ writes content to a note json file """
        
    if mode == 'CIPHERED' and is_valid_user_protected_json(json_content):
        file_path = file_path.replace('.json', '_protected.json')
        file.write_file_content(file_path, json.dumps(json_content, indent=4))
    elif mode == 'PLAIN' and is_valid_user_unprotected_json(json_content):
        file.write_file_content(file_path, json.dumps(json_content, indent=4))
    else:
        error(f"write_json: Invalid JSON content or mode '{mode}' in file {file_path}")
   
def build_server_metadata(json_content: dict) -> dict:
    return { 
        'id': json_content['id'],
        'version': json_content['version'],
        'last_modified_by': json_content['last_modified_by'],
        'owner': json_content['owner'],
        'editors': json_content['editors'],
        'viewers': json_content['viewers']
    }
    
def build_user_protected_json(note: bytes, note_tag: bytes, iv: bytes, note_key: bytes, 
        server_metadata: bytes, server_metadata_tag: bytes, server_key: bytes) -> dict:
    """ builds a protected user JSON note with values encoded in base64 """
    return {
        'iv': crypto.encode_base64(iv),
        'note': crypto.encode_base64(note),
        'note_tag': crypto.encode_base64(note_tag),
        'note_key': crypto.encode_base64(note_key),
        'server_metadata': crypto.encode_base64(server_metadata),
        'server_metadata_tag': crypto.encode_base64(server_metadata_tag),
        'server_metadata_key': crypto.encode_base64(server_key)
    }

def build_user_unprotected_json(id: int, title: str, note: str, date_created: str, 
            date_modified: str,last_modified_by: int, version: int, owner_id: int, 
            owner_username: str, editors: list, viewers: list) -> dict:
    """ builds a user JSON note """
    return {
        'id': id,
        'note': note,
        'date_created': date_created,
        'date_modified': date_modified,
        'last_modified_by': last_modified_by,
        'version': version,
        'owner': {
            'id': owner_id,
            'username': owner_username
        },
        'editors': editors,
        'viewers': viewers
    }

def is_valid_user_protected_json(json_content: dict) -> bool:
    """ checks if a protected user note has all the required fields and valid types"""
    allowed_fields = [{'iv', 'note', 'note_tag', 'note_key', 'server_metadata',
                        'server_metadata_tag', 'server_metadata_key'}]
    allowed_types = [{'iv': str, 'note': str, 'note_tag': str, 'note_key': str,
                    'server_metadata': str, 'server_metadata_tag': str, 
                    'server_metadata_key': str}]
    return is_valid_json(json_content, allowed_fields, allowed_types)

def is_valid_user_unprotected_json(json_content: dict) -> bool:
    """ checks if a note has all the required fields and valid types """
    allowed_fields =  [{'id', 'title', 'note', 'date_created', 'date_modified', 
                        'last_modified_by', 'version', 'owner', 'editors', 'viewers'},
                        {'id', 'username'}, {'id', 'username'}]
    allowed_types = [{'id': int, 'title': str, 'note': str, 'date_created': str, 
                    'date_modified': str, 'last_modified_by': int, 'version': int,
                    'owner': dict, 'editors': list, 'viewers': list},
                    {'id': int, 'username': str},
                    {'id': int, 'username': str}] 
    return is_valid_json(json_content, allowed_fields, allowed_types)

##################### SERVER JSON NOTE #####################
def read_server_json(file_path: str, mode: str) -> dict:
    """Reads JSON note file and returns content as a dictionary"""
    file_content = file.read_file_content(file_path)
    json_content = json.loads(file_content)

    mode_validation = {
        'CIPHERED': is_valid_server_protected_json,
        'PLAIN': is_valid_server_unprotected_json
    }

    if mode in mode_validation and mode_validation[mode](json_content):
        return json_content

    error(f"read_json: Invalid JSON content or mode '{mode}' in file {file_path}")
    return {}

def write_server_json(file_path: str, json_content: dict, mode: str) -> None:
    """Writes content to a note JSON file"""

    mode_validation = {
        'CIPHERED': is_valid_server_protected_json,
        'PLAIN': is_valid_server_unprotected_json
    }

    if mode in mode_validation and mode_validation[mode](json_content):
        file.write_file_content(file_path, json.dumps(json_content, indent=4))
    else:
        error(f"write_json: Invalid JSON content or mode '{mode}' in file {file_path}")

def build_protected_json_server(note: bytes, note_tag: bytes, iv: bytes, 
                                                                note_key: bytes) -> dict:
    """ builds a protected server JSON note with values encoded in base64 """
    return {
        'iv': crypto.encode_base64(iv),
        'note': crypto.encode_base64(note),
        'note_tag': crypto.encode_base64(note_tag),
        'note_key': crypto.encode_base64(note_key)
    }

def build_unprotected_json_server(iv: bytes, note: str, note_tag: bytes, note_key: bytes,
        server_metadata: dict, server_metadata_tag: bytes, server_metadata_key: bytes) -> dict:
    """ builds an unprotected server JSON note """
    return {
        'iv': crypto.encode_base64(iv),
        'note': note,
        'note_tag': crypto.encode_base64(note_tag),
        'note_key': crypto.encode_base64(note_key),
        'server_metadata': server_metadata,
        'server_metadata_tag': crypto.encode_base64(server_metadata_tag),
        'server_metadata_key': crypto.encode_base64(server_metadata_key)
    }

def is_valid_server_protected_json(json_content: dict) -> bool:
    """ checks if a protected server note has all the required fields and valid types """
    allowed_fields = [{"iv", "note", "note_tag", "note_key", "server_metadata", 
                        "server_metadata_tag", "server_metadata_key"}]
    allowed_types = [{"iv": str, "note": str, "note_tag": str, "note_key": str, 
                    "server_metadata": dict, "server_metadata_tag": str, 
                    "server_metadata_key": str}]
    return is_valid_json(json_content, allowed_fields, allowed_types)

def is_valid_server_unprotected_json(json_content: dict) -> bool:
    allowed_fields = [
        {"iv", "note", "note_tag", "note_key", "server_metadata", "server_metadata_tag", 
        "server_metadata_key"},
        {"id", "version", "last_modified_by", "owner", "editors", "viewers"},
        {"id", "username"},
        {"id", "username"}
    ]
    allowed_types = allowed_types = [
        {"iv": str, "note": str, "note_tag": str, "note_key": str, 
         "server_metadata": dict, "server_metadata_tag": str, "server_metadata_key": str},
        {"id": int, "version": int, "last_modified_by": int, "owner": dict, 
         "editors": list, "viewers": list},
        {"id": int, "username": str},
        {"id": int, "username": str}
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
                if not all(isinstance(i, dict) for i in value):
                    errors.append(f"Invalid type for key {key}: expected list of dictionaries")
                else:
                    for item in value:
                        if not is_valid_json(item, allowed_fields, allowed_types, nesting_level + 1):
                            errors.append(f"Invalid nested data in list for key {key}")
        else:
            errors.append(f"No type defined for key {key}")
    if errors:
        raise ValueError(f"noteparser.py error: {'; '.join(errors)}")
    return True
