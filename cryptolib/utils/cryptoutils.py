import os
import base64
from utils import file

from cryptography.hazmat.backends import default_backend # OpenSSL backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

""" Base64 Encoding/Decoding Functions """
def encode_base64(data: bytes) -> str:
    return base64.encodebytes(data).decode()
    
def decode_base64(data: str) -> bytes:
    return base64.decodebytes(data.encode())

""" Random Generation Functions """
def generate_random_iv() -> bytes:
    return os.urandom(16)

def generate_secret_key() -> bytes:
    return os.urandom(32)
    
""" AES Encryption/Decryption Functions """
def aes_gcm_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> tuple[bytes, bytes]:
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    tag = encryptor.tag
    return ciphertext, tag
    
def aes_gcm_decrypt(ciphertext: bytes, tag: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

""" RSA Handling Functions """
def generate_rsa_key_pair(public_key_path: str, private_key_path: str) -> None:
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    file.write_file_bytes(private_key_path, pem)

    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    file.write_file_bytes(public_key_path, pem)

def read_rsa_public_key(public_key_path: str) -> rsa.RSAPublicKey:
    pem = file.read_file_bytes(public_key_path)
    public_key = serialization.load_pem_public_key(pem, backend=default_backend())
    
    if not isinstance(public_key, rsa.RSAPublicKey):
        raise TypeError("The provided key is not an RSA public key.")
    
    return public_key
    
def read_rsa_private_key(private_key_path: str) -> rsa.RSAPrivateKey:
    pem = file.read_file_bytes(private_key_path)
    private_key = serialization.load_pem_private_key(pem, password=None, backend=default_backend())
    
    if not isinstance(private_key, rsa.RSAPrivateKey):
        raise TypeError("The provided key is not an RSA private key.")
    
    return private_key
    
""" RSA Encryption/Decryption Functions """
def rsa_encrypt(message: bytes, public_key: rsa.RSAPublicKey) -> bytes:
    return public_key.encrypt(
        message,
        padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
    )
    
def rsa_decrypt(ciphertext: bytes, private_key: rsa.RSAPrivateKey) -> bytes:
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
    )
    
def rsa_sign(message: bytes, private_key: rsa.RSAPrivateKey) -> bytes:
    return private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    
def rsa_verify(signature: bytes, message: bytes, public_key: rsa.RSAPublicKey) -> None:
    public_key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )