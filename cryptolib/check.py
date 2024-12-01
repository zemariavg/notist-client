from utils.file import *
from utils.cryptoutils import *
from utils.noteparser import *
import argparse
import json

def check(note_file_path: str, private_key_path: str) -> str:
    """ Checks integrity of note content and metadata """
    jsonDict = read_json(note_file_path, 'CIPHERED')
    
    iv = decode_base64(jsonDict['iv'])
    privKey = read_rsa_private_key(private_key_path)

    # decipher AES key w/ RSA private key   
    secretKey = rsa_decrypt(decode_base64(jsonDict['key']), privKey)
    
    # verify note content
    note_content = decode_base64(jsonDict['note'])
    note_tag = decode_base64(jsonDict['note_tag'])
    
    try:
        note_content = aes_gcm_decrypt(note_content, note_tag, secretKey, iv)
    except Exception as e:
        return f"check.py: Note content has been tampered with"
        
    # verify metadata
    metadata = decode_base64(jsonDict['metadata'])
    metadata_tag = decode_base64(jsonDict['metadata_tag'])
    
    try:
        metadata = aes_gcm_decrypt(metadata, metadata_tag, secretKey, iv)
    except Exception as e:
        return f"check.py: Metadata has been tampered with"
    
    return f"check.py: File {note_file_path} is valid"
    
def parse_args():
    """ Parse command-line arguments """
    parser = argparse.ArgumentParser(description="Check a note file for integrity.")
    parser.add_argument('note_file_path', help="The name of the note file to check")
    parser.add_argument('public_key_path', help="Path to the RSA public key file")
    return parser.parse_args()
    
if __name__ == "__main__":
    args = parse_args()

    result = check(args.note_file_path, args.public_key_path)
    print(result)
