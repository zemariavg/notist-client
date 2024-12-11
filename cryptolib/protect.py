from ast import NotEq
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptolib.utils.file import *
from cryptolib.utils.cryptoutils import *
from cryptolib.utils.noteparser import *
import argparse
import json

def protect_note_path(note_path: str, aes_key_path: str, pub_key_path: str) -> None:
    """ Protects a note file with AES GCM and RSA """
    try:
        aes_key = read_file_bytes(aes_key_path)
        json_content = json.loads(read_file_bytes(note_path))
        protected = protect_note(json_content, aes_key, pub_key_path)
        protected_path = note_path.replace('.json', '_protected.json')
        write_note(protected_path, protected, 'PROTECTED')    
    except Exception as e:
        error(f"Error during protect: {e}")
        

def protect_note(note_json: dict, note_key: bytes, pub_key_path: str) -> dict:
    """ Ciphers note with AES GCM and AES key with RSA public key """
    try:
        iv = generate_random_iv()
        note = json.dumps(note_json).encode()
        ciphered_note, note_tag = aes_gcm_encrypt(note, note_key, iv)
        
        # cipher AES key w/ RSA public key
        pub_key = read_rsa_public_key(pub_key_path)
        ciphered_note_key = rsa_encrypt(note_key, pub_key)
        
        protected_note = build_user_protected_json(ciphered_note, note_tag, iv, ciphered_note_key)
        return protected_note
    except Exception as e:
        error(f"protect_user_note: {e}") 
        return {}