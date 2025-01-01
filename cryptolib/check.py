import argparse
import json
from .utils.file import *
from .utils.cryptoutils import *
from .utils.noteparser import *

def check_note(note_file_path: str, private_key_path: str) -> bool:
    """ Checks integrity of note content """
    try: 
        print("Checking note integrity...")
        print("Reading note...")
        jsonDict = read_note(note_file_path, 'PROTECTED')
        print("Reading IV...")
        iv = decode_base64(jsonDict['iv'])
        privKey = read_rsa_private_key(private_key_path)
    
        # decipher AES key w/ RSA private key   
        print("Decrypting AES key with RSA private key...")
        noteKey = rsa_decrypt(decode_base64(jsonDict['ciphered_note_key']), privKey)
    
        # verify content integrity 
        print("Decrypting note with AES GCM...")
        note_content = decode_base64(jsonDict['encrypted_note'])
        note_tag = decode_base64(jsonDict['note_tag'])
        note_content = aes_gcm_decrypt(note_content, note_tag, noteKey, iv)
    except Exception as e:
        raise e
        
    return True