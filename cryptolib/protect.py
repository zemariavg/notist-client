import argparse
import json
from .utils.file import *
from .utils.cryptoutils import *
from .utils.noteparser import *

def protect_note(note_json: dict, note_key: bytes, pub_key_path: str) -> dict:
    """ Ciphers note with AES GCM and AES key with RSA public key """
    try:
        print("Protecting note...") 
        print("Generating random IV...")
        iv = generate_random_iv()
        note = json.dumps(note_json).encode()
        
        print("Encrypting note with AES GCM...")
        encrypted_note, note_tag = aes_gcm_encrypt(note, note_key, iv)
        
        print("Encrypting AES key with RSA public key...")
        # cipher AES key w/ RSA public key
        pub_key = read_rsa_public_key(pub_key_path)
        ciphered_note_key = rsa_encrypt(note_key, pub_key)
        
        protected_note = build_user_protected_json(note_json['title'], encrypted_note, note_tag, iv, ciphered_note_key)
        return protected_note
    except Exception as e:
        raise e