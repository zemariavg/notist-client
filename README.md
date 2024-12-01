***
### **Cryptolib note protection library**
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