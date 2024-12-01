import os

""" File handling functions """
def read_file_content(file_path: str) -> str:
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except (FileNotFoundError, PermissionError) as e:
        raise RuntimeError(f"file.py: Error reading file {file_path}: {e}") from e 

def read_file_bytes(file_path: str) -> bytes:
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except (FileNotFoundError, PermissionError) as e:
        raise RuntimeError(f"file.py: Error reading file {file_path}: {e}") from e
            
def write_file_content(file_path: str, content: str):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return f"utils.py: File {file_path} written successfully"
    except (FileNotFoundError, IOError) as e:
        raise RuntimeError(f"file.py: Error writing file {file_path}: {e}") from e
        
def write_file_bytes(file_path: str, content: bytes):
    try:
        with open(file_path, 'wb') as file:
            file.write(content)
        return f"utils.py: File {file_path} written successfully"
    except (FileNotFoundError, IOError) as e:
        raise RuntimeError(f"file.py: Error writing file {file_path}: {e}") from e
