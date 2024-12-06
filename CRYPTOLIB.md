# **ROADMAP** 
- [x] SR1 - Confidentiality
- [x] SR2 - Integrity 1
- [ ] SR3 - Integrity 2 - We need ideas on how to implement this!
- [ ] SR4 - Authentication - We need ideas on how to implement this!

# The NotIST notes app
* Security Requirements:
### *Confidentiality* - SR1
Only the *owner* of the notes can see their content. 
### *Integrity 1* - SR2
The *owner* of the notes can verify they were not tampered with.
### *Integrity 2* - SR3
The *owner* of the notes can verify if some note is missing.
### *Authentication* - SR4
Only the *owner* of the notes can access them.

***
# **Choice of Encryption**
#### Why AES/GCM?
AES GCM is one of the current standards for encrypting files. It features high performance due to its ability to be parallelized and it also allows for integrity to be checked with the authentication tag it generates during encryption. Using a random IV for each encryption, we can assure that it is always safe. We keep track of the IV to discard any repeated IVs and prevent replay attacks (not yet implemented!).
#### Why RSA?
RSA is a widely adopted public-key cryptosystem that provides secure key exchange and digital signatures. It is based on the computational difficulty of factoring large integers. We used RSA to encrypt the AES key used to encrypt the notes, ensuring that only the owner of the notes can access them. 

## **Cryptolib note protection library**
Cryptolib employs AES-GCM encryption to encrypt and decrypt notes, relying on RSA to encrypt and decrypt the AES key used to encrypt the note.  

##### Requirements:
- Python 3.6 or higher
- python cryptography library (install with `pip install cryptography`)

### **Usage example**
#### To protect a note:
```bash
python3 protect.py note rsa_pub_key
```

#### To unprotect a note:
```bash
python3 unprotect.py note rsa_priv_key
```

#### To check the integrity of a note:
```bash
python3 check.py note rsa_priv_key
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