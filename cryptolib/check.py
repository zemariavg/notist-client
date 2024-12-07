from utils.file import *
from utils.cryptoutils import *
from utils.noteparser import *
import argparse
import json

def check_note(note_file_path: str, private_key_path: str) -> bool:
    """ Checks integrity of note content """
    jsonDict = read_user_json(note_file_path, 'CIPHERED')
    
    iv = decode_base64(jsonDict['iv'])
    privKey = read_rsa_private_key(private_key_path)

    # decipher AES key w/ RSA private key   
    noteKey = rsa_decrypt(decode_base64(jsonDict['note_key']), privKey)
    
    # verify note content
    note_content = decode_base64(jsonDict['note'])
    note_tag = decode_base64(jsonDict['note_tag'])
    
    try:
        note_content = aes_gcm_decrypt(note_content, note_tag, noteKey, iv)
    except Exception as e:
        return False
        
    return True

def check_server_metadata(note_file_path: str, private_key_path: str) -> bool:
    """ Checks integrity of server metadata """
    jsonDict = read_server_json(note_file_path, 'CIPHERED')
    
    iv = decode_base64(jsonDict['iv'])
    privKey = read_rsa_private_key(private_key_path)
    
    # decipher AES key w/ RSA private key
    serverKey = rsa_decrypt(decode_base64(jsonDict['server_metadata_key']), privKey)
    
    # verify server metadata
    server_metadata = decode_base64(jsonDict['server_metadata'])
    server_metadata_tag = decode_base64(jsonDict['server_metadata_tag'])
    
    try:
        server_metadata = aes_gcm_decrypt(server_metadata, server_metadata_tag, serverKey, iv)
    except Exception as e:
        return False
        
    return True
 