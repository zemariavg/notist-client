from cryptolib.utils.file import *
from cryptolib.utils.cryptoutils import *
from cryptolib.utils.noteparser import *
import argparse
import json

def protect_note(note_file_path: str, secret_key_path: str, public_key_path: str) -> None:
    """ Ciphers note content with AES GCM and gets metadata for server, also ciphered """
    """ Ciphers AES key with RSA public key """
    try:
        jsonDict = read_note(note_file_path, 'UNPROTECTED') 
        iv = generate_random_iv()
        notekey = read_file_bytes(secret_key_path)
        pubKey = read_rsa_public_key(public_key_path)
        
        # cipher everything and get only server metadata from note
        note = json.dumps(jsonDict).encode()
        ciphered_note, note_tag = aes_gcm_encrypt(note, notekey, iv)
        server_metadata = build_server_metadata(jsonDict)
        
        # cipher AES key w/ RSA public key
        note_key = rsa_encrypt(notekey, pubKey)
        
        protected_note = build_user_protected_json(ciphered_note, note_tag, iv, note_key)
        write_note(note_file_path, protected_note, 'PROTECTED')
    except Exception as e:
        error(f"protect_user_note: {e}") 