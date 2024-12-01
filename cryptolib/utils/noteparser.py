from utils import file
from utils import cryptoutils as crypto
import json

def error(message: str) -> None:
    raise ValueError(f"parser.py error: {message}")
    
""" JSON note file handling functions """
""" These functions check if the JSON note has all the required fields and valid types. """
""" They allow to validate if a plain note is valid or if a ciphered note is valid. """
""" Check example_notes/ for examples of valid notes. """

# mode is either 'CIPHERED' or 'PLAIN'
def read_json(file_path: str, mode: str) -> dict: 
    """ reads json note file and returns content as a dictionary """
    file_content = file.read_file_content(file_path)
    json_content = json.loads(file_content)
    if mode == 'CIPHERED':
        if is_valid_ciphered_json_note(json_content):
            return json_content
        else:
            error(f"read_json: Invalid JSON content in file {file_path}")
            return {}
    elif mode == 'PLAIN':
        if is_valid_json_note(json_content):
            return json_content
        else:
            error(f"read_json: Invalid JSON content in file {file_path}")
            return {}
    else:
        error(f"read_json: Invalid mode {mode}")
        return {}
        
def write_json(file_path: str, json_content: dict, mode: str) -> None:
    """ writes content to a note json file """
    if mode == 'CIPHERED':
        if is_valid_ciphered_json_note(json_content):
            file.write_file_content(file_path, json.dumps(json_content, indent=4))
        else:
            error(f"write_json: Invalid JSON content in file {file_path}")
    elif mode == 'PLAIN':
        if is_valid_json_note(json_content):
            file.write_file_content(file_path, json.dumps(json_content, indent=4))
        else:
            error(f"write_json: Invalid JSON content in file {file_path}")
    else:
        error(f"write_json: Invalid mode {mode}")

def build_ciphred_json_note(note: bytes, note_tag: bytes, metadata: bytes, 
                        metadata_tag: bytes, iv: bytes, key: bytes) -> dict:
    """ builds a JSON note dictionary with values encoded in base64 """
    return {
        'note': crypto.encode_base64(note),
        'note_tag': crypto.encode_base64(note_tag),
        'metadata': crypto.encode_base64(metadata),
        'metadata_tag': crypto.encode_base64(metadata_tag),
        'iv': crypto.encode_base64(iv),
        'key': crypto.encode_base64(key)
    }

def build_json_note(note: str, metadata: dict) -> dict:
    """ builds a JSON note dictionary """
    return {
        'note': note,
        'metadata': metadata
    }

def is_valid_ciphered_json_note(json_content: dict) -> bool:
    """ checks if a ciphered note has all the required fields and valid types"""
    allowed_fields = {'note', 'note_tag', 'metadata', 'metadata_tag', 'iv', 'key'}
    extra_fields = set(json_content.keys()) - allowed_fields
    
    if extra_fields:
        error(f"Unexpected fields in JSON: {extra_fields}")
        return False
    
    for field in allowed_fields:
        if field not in json_content:
            error(f"Missing field in JSON: {field}")
            return False
        if not isinstance(json_content[field], str):
            error(f"Field {field} is not a string")
            return False
    return True

def is_valid_json_note(json_content: dict) -> bool:
    """ checks if a note has all the required fields and valid types """
    allowed_fields = {'note', 'metadata'}
    allowed_metadata_fields = {'id', 'date_created', 'date_modified', 'last_modified_by', 'version', 'owner', 'editors', 'viewers'}
    allowed_owner_fields = {'id', 'username'}
    allowed_editors_viewers_fields = {'id', 'username'}

    extra_fields = set(json_content.keys()) - allowed_fields
    if extra_fields:
        error(f"Unexpected fields in JSON: {extra_fields}")
        return False
    
    for field in allowed_fields:
        if field not in json_content:
            error(f"Missing field in JSON: {field}")
            return False
            
    for field in allowed_metadata_fields:
        if field not in json_content["metadata"]:
            error(f"Missing field in metadata: {field}")
            return False
    
    metadata = json_content["metadata"]
    if not isinstance(metadata["id"], int) or \
        not isinstance(metadata["title"], str) or \
        not isinstance(metadata["date_created"], str) or \
        not isinstance(metadata["date_modified"], str) or \
        not isinstance(metadata["last_modified_by"], int) or \
        not isinstance(metadata["version"], int) or \
        not isinstance(metadata["owner"], dict):
        error("Metadata fields have wrong types")
        return False
        
    owner = metadata["owner"]
    if "id" not in owner or "username" not in owner:
        error("Owner missing fields")
        return False
    
    if not isinstance(owner["id"], int) or not isinstance(owner["username"], str):
        error("Owner fields have wrong types")
        return False
    
    if "editors" in metadata:
        for editor in metadata["editors"]:
            if "id" not in editor or "username" not in editor:
                error("Editor missing fields")
                return False
            if not isinstance(editor["id"], int) or not isinstance(editor["username"], str):
                error("Editor fields have wrong types")
                return False
                
    if "viewers" in metadata:
        for viewer in metadata["viewers"]:
            if "id" not in viewer or "username" not in viewer:
                error("Viewer missing fields")
                return False
            if not isinstance(viewer["id"], int) or not isinstance(viewer["username"], str):
                error("Viewer fields have wrong types")
                return False
    return True
    