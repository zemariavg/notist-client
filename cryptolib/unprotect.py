import argparse
import json
from .utils.file import *
from .utils.cryptoutils import *
from .utils.noteparser import *
   
def unprotect_note_path(note_path: str, priv_key_path: str) -> None:
    try:
        json_content = read_note(note_path, 'PROTECTED')
        unprotected = unprotect_note(json_content, priv_key_path)[0] # get only the json
        write_note(note_path, unprotected, 'UNPROTECTED')
    except Exception as e:
        raise e
 
def unprotect_note(note_json: dict, priv_key_path: str) -> tuple[dict, bytes]: # json and aes key
    """ Deciphers note content"""
    """ Deciphers AES key with RSA private key """
    
    try:
        iv = decode_base64(note_json['iv'])
        priv_key = read_rsa_private_key(priv_key_path)
        
        # decipher AES key w/ RSA private key
        note_key = rsa_decrypt(decode_base64(note_json['note_key']), priv_key)
        
        # decipher note content
        note_content = decode_base64(note_json['note'])
        note_tag = decode_base64(note_json['note_tag'])
        note = aes_gcm_decrypt(note_content, note_tag, note_key, iv)
        return json.loads(note), note_key
    except Exception as e:
        raise e