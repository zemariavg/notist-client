from utils.file import *
from utils.cryptoutils import *
from utils.noteparser import *
import argparse
import json

def protect_user_note(note_file_path: str, secret_key_path: str, public_key_path: str) -> str:
    """ Ciphers note content with AES GCM and gets metadata for server, also ciphered """
    """ Ciphers AES key with RSA public key """

    jsonDict = read_user_json(note_file_path, 'PLAIN')
    
    iv = generate_random_iv()
    notekey = read_file_bytes(secret_key_path)
    pubKey = read_rsa_public_key(public_key_path)
    serverKey = generate_secret_key() # !! random key for server metadata every time !!
    
    # cipher everything
    note = json.dumps(jsonDict).encode()
    ciphered_note, note_tag = aes_gcm_encrypt(note, notekey, iv)
    
    # get metadata for server from note
    server_metadata = build_server_metadata(jsonDict)
    server_metadata = json.dumps(server_metadata).encode()
    server_metadata, server_metadata_tag = aes_gcm_encrypt(server_metadata, serverKey, iv)
    
    # cipher AES key w/ RSA public key
    note_key = rsa_encrypt(notekey, pubKey)
    server_key = rsa_encrypt(serverKey, pubKey)
    
    protected_json = build_user_protected_json(ciphered_note, note_tag, iv, note_key, 
                                        server_metadata, server_metadata_tag, server_key)
    
    write_user_json(note_file_path, protected_json, 'CIPHERED')
    return f"protect.py: File {note_file_path} protected successfully"
