from utils.file import *
from utils.cryptoutils import *
from utils.noteparser import *
import argparse
import json
    
def unprotect_note(note_file_path: str, private_key_path: str) -> None:
    """ Deciphers note content"""
    """ Deciphers AES key with RSA private key """
    
    try:
        jsonDict = read_note(note_file_path, 'PROTECTED')
        iv = decode_base64(jsonDict['iv'])
        privKey = read_rsa_private_key(private_key_path)
        
        # decipher AES key w/ RSA private key
        noteKey = rsa_decrypt(decode_base64(jsonDict['note_key']), privKey)
        
        # decipher note content
        note_content = decode_base64(jsonDict['note'])
        note_tag = decode_base64(jsonDict['note_tag'])
        note = aes_gcm_decrypt(note_content, note_tag, noteKey, iv)
        
        write_note(note_file_path, json.loads(note), 'UNPROTECTED')
    except Exception as e:
        error(f"unprotect_user_note: {e}")