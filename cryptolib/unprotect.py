from utils.file import *
from utils.cryptoutils import *
from utils.noteparser import *
import argparse
import json

def unprotect_file(note_file_path: str, private_key_path: str):
    """ Dciphers note content and metadata with AES GCM """
    """ Diphers AES key with RSA private key """

    jsonDict = read_json(note_file_path, 'CIPHERED')
    
    iv = decode_base64(jsonDict['iv'])
    privKey = read_rsa_private_key(private_key_path)
    
    # decipher AES key w/ RSA private key
    secretKey = rsa_decrypt(decode_base64(jsonDict['key']), privKey)
    
    # decipher note content
    note_content = jsonDict['note']
    note_tag = decode_base64(jsonDict['note_tag'])
    note_content = aes_gcm_decrypt(decode_base64(note_content), note_tag, secretKey, iv)
    
    # decipher metadata
    metadata = jsonDict['metadata']
    metadata_tag = decode_base64(jsonDict['metadata_tag'])
    metadata = aes_gcm_decrypt(decode_base64(metadata), metadata_tag, secretKey, iv)
    
    unprotected_json = build_json_note(note_content.decode(), json.loads(metadata.decode()))
    write_json(note_file_path, unprotected_json, 'PLAIN')
    return f"unprotect.py: File {note_file_path} unprotected successfully"
    
def parse_args():
    """ Parse command-line arguments """
    parser = argparse.ArgumentParser(description="Unprotect a note file with decryption.")
    parser.add_argument('note_file_path', help="The name of the note file to unprotect")
    parser.add_argument('private_key_path', help="Path to the RSA private key file")
    return parser.parse_args()
    
if __name__ == "__main__":
    args = parse_args()

    result = unprotect_file(args.note_file_path, args.private_key_path)
    print(result)