from utils.file import *
from utils.cryptoutils import *
from utils.noteparser import *
import argparse
import json

def check_note(note_file_path: str, private_key_path: str) -> bool:
    """ Checks integrity of note content """
    try: 
        jsonDict = read_note(note_file_path, 'PROTECTED')
        iv = decode_base64(jsonDict['iv'])
        privKey = read_rsa_private_key(private_key_path)
    
        # decipher AES key w/ RSA private key   
        noteKey = rsa_decrypt(decode_base64(jsonDict['note_key']), privKey)
    
        # verify content integrity 
        note_content = decode_base64(jsonDict['note'])
        note_tag = decode_base64(jsonDict['note_tag'])
        note_content = aes_gcm_decrypt(note_content, note_tag, noteKey, iv)
    except Exception as e:
        return False
        
    return True