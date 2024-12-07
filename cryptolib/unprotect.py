from utils.file import *
from utils.cryptoutils import *
from utils.noteparser import *
import argparse
import json
    
def unprotect_user_note(note_file_path: str, private_key_path: str):
    """ Deciphers note content"""
    """ Deciphers AES key with RSA private key """

    jsonDict = read_user_json(note_file_path, 'CIPHERED')
    
    iv = decode_base64(jsonDict['iv'])
    privKey = read_rsa_private_key(private_key_path)
    
    # decipher AES key w/ RSA private key
    secretKey = rsa_decrypt(decode_base64(jsonDict['note_key']), privKey)
    
    # decipher note content
    note_content = decode_base64(jsonDict['note'])
    note_tag = decode_base64(jsonDict['note_tag'])
    note = aes_gcm_decrypt(note_content, note_tag, secretKey, iv)
    
    unprotected_json = json.loads(note.decode())

    write_user_json(note_file_path, unprotected_json, 'PLAIN')
    return f"unprotect.py: File {note_file_path} unprotected successfully"
    
def unprotect_server_note(note_file_path: str, private_key_path: str):
    """ Deciphers only server metadata """
    """ Deciphers AES key with RSA private key """

    jsonDict = read_user_json(note_file_path, 'CIPHERED')
    
    iv = decode_base64(jsonDict['iv'])
    privKey = read_rsa_private_key(private_key_path)
    
    # decipher AES key w/ RSA private key
    secretKey = rsa_decrypt(decode_base64(jsonDict['server_metadata_key']), privKey)
    
    # decipher server metadata
    server_metadata = decode_base64(jsonDict['server_metadata'])
    server_metadata_tag = decode_base64(jsonDict['server_metadata_tag'])    
    server_metadata = aes_gcm_decrypt(server_metadata, server_metadata_tag, secretKey, iv)
    server_metadata = json.loads(server_metadata.decode())
    
    # get fields from ciphered json and build final unprotected json
    note = jsonDict['note']
    note_tag = decode_base64(jsonDict['note_tag'])
    note_key = decode_base64(jsonDict['note_key'])
    server_metadata_key = decode_base64(jsonDict['server_metadata_key'])
    
    unprotected_json = build_unprotected_json_server(iv, note, note_tag, note_key,
                                server_metadata, server_metadata_tag, server_metadata_key)
    
    write_server_json(note_file_path, unprotected_json, 'PLAIN')
    return f"unprotect.py: File {note_file_path} unprotected successfully"
    