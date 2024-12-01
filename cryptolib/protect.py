from utils.file import *
from utils.cryptoutils import *
from utils.noteparser import *
import argparse
import json

def protect_file(note_file_path: str, secret_key_path: str, public_key_path: str) -> str:
    """ Ciphers note content and metadata with AES GCM """
    """ Ciphers AES key with RSA public key """

    jsonDict = read_json(note_file_path, 'PLAIN')
    
    iv = generate_random_iv()
    secretkey = read_file_bytes(secret_key_path)
    pubKey = read_rsa_public_key(public_key_path)
    
    # cipher note content
    note_content = jsonDict['note']
    ciphered_note, note_tag = aes_gcm_encrypt(note_content.encode(), secretkey, iv)
    
    # cipher metadata
    metadata = jsonDict['metadata']
    metadata_bytes = json.dumps(metadata).encode()
    ciphered_metadata, metadata_tag = aes_gcm_encrypt(metadata_bytes, secretkey, iv)
    
    # cipher AES key w/ RSA public key
    rsa_pub_key = read_rsa_public_key(public_key_path)
    ciphered_key = rsa_encrypt(secretkey, rsa_pub_key)
    
    protected_json = build_ciphred_json_note(ciphered_note, note_tag, ciphered_metadata, 
                                                        metadata_tag, iv, ciphered_key)
    write_json(note_file_path, protected_json, 'CIPHERED')
    return f"protect.py: File {note_file_path} protected successfully"
    
def parse_args():
    """ Parse command-line arguments """
    parser = argparse.ArgumentParser(description="Protect a note file with encryption.")
    parser.add_argument('note_file_path', help="The name of the note file to protect")
    parser.add_argument('secret_key_path', help="Path to the AES secret key file")
    parser.add_argument('public_key_path', help="Path to the RSA public key file")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    result = protect_file(args.note_file_path, args.secret_key_path, args.public_key_path)
    print(result)