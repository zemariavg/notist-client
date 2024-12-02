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
