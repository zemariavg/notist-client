import os

""" File handling functions """
def get_file_path(file_name: str) -> str:
    sanitized_file_name = os.path.basename(file_name)
    return os.path.join(os.path.dirname(__file__), sanitized_file_name)

def read_file_content(file_name: str) -> str:
    try:
        with open(get_file_path(file_name), 'r') as file:
            return file.read()
    except (FileNotFoundError, PermissionError):
        return f"utils.py: Error reading file {file_name}"
            
def write_file_content(file_name: str, content: str) -> str:
    try:
        with open(get_file_path(file_name), 'w') as file:
            file.write(content)
        return f"utils.py: File {file_name} written successfully"
    except (FileNotFoundError, IOError):
        return f"utils.py: Error writing to file {file_name}"
        
""" Cryptography functions """
# def generate_aes_iv() -> bytes:
#     return os.urandom(16) # 16 bytes = 128 bits
