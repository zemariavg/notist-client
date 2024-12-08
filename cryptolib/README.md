## **Notist note protection library**
NotIST employs AES-GCM encryption to encrypt and decrypt notes, relying on RSA to encrypt and decrypt the AES key used to encrypt the note.  

##### Requirements:
- Python 3.6 or higher
- python cryptography library (install with `pip install cryptography`)

### **Usage example**
Run the tool with
```bash
python3 notist.py
```
#### To protect a note (output will be in note_path_protected.json):
```bash
python3 notist.py protect <note_path> <aes_key_path> <rsa_pub_key_path>
```
#### To unprotect a note:
```bash
python3 notist.py unprotect <note_path> <rsa_priv_key_path>
```

#### To check note integrity:
```bash
python3 notist.py check <note_path> <rsa_priv_key_path>
```

***
## RSA key and padding decisions
• **Key size (2048 bits)** and **public exponent (65537)** are industry standards, providing an optimal balance between security and performance (2048bit is safe until 2030, according to NIST)

**PKCS8** (Public-Key Cryptography Standards #8):
• Essential for securely storing and transporting private keys.
• Ensures compatibility across cryptographic systems.
• Allows future-proofing for different key algorithms.

**SPKI** (SubjectPublicKeyInfo):
• Facilitates secure transmission and storage of public keys in a standardized way.
• Required by many cryptographic protocols and certificates.

## RSA padding
RSA is inherently deterministic, meaning encrypting the same message with the same key always produces the same ciphertext. 
This predictability makes it vulnerable to chosen plaintext and replay attacks. 
Padding schemes introduce randomness, ensuring different outputs for identical inputs. This randomness prevents attackers from guessing the plaintext or reusing encrypted messages, thus enhancing the security of RSA-based cryptographic systems.

## Used padding
**1. OAEP (Optimal Asymmetric Encryption Padding)**
OAEP is used in RSA encryption to randomize plaintext before encryption, ensuring the same message produces different ciphertexts each time. It uses MGF1 (Mask Generation Function) to generate a mask from the message using SHA-256 to ensure randomization.
OAEP is a widely adopted standard (part of PKCS#1).

**2. PSS (Probabilistic Signature Scheme)**
PSS adds randomness to the signing process, ensuring each signature is unique for the same message. It employs MGF1 and a salt (random value) combined with the message hash (SHA-256) to generate a non-deterministic signature.
PSS is the recommended standard for RSA signatures (specified in PKCS#1 v2.2).