## **Notist note protection library**
NotIST employs AES-GCM encryption to encrypt and decrypt notes, relying on RSA to encrypt and decrypt the AES key used to encrypt the note.  

### To install cryptolib:
From the root directory, notist-client/, run:
```bash
pip install .
```
This will run the setup.py script and install the cryptolib as well as the required dependencies.

### **Usage example**
Run the tool with
```bash
python3 -m cryptolib.notist
```
#### To protect a note (output will be in note_path_protected.json):
```bash
python3 -m cryptolib.notist protect <note_path> <aes_key_path> <rsa_pub_key_path>
```
#### To unprotect a note:
```bash
python3 -m cryptolib.notist unprotect <note_path> <rsa_priv_key_path>
```

#### To check note integrity:
```bash
python3 -m cryptolib.notist check <note_path> <rsa_priv_key_path>
```
