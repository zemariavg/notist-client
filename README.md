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

# **Choice of Encryption**
#### Why AES/GCM?
AES GCM is one of the current standards for encrypting files. It features high performance due to its ability to be parallelized and it also allows for integrity to be checked with the authentication tag it generates during encryption. Using a random IV for each encryption, we can assure that it is always safe. We keep track of the IV to discard any repeated IVs and prevent replay attacks (not yet implemented!).
#### Why RSA?
RSA is a widely adopted public-key cryptosystem that provides secure key exchange and digital signatures. It is based on the computational difficulty of factoring large integers. We used RSA to encrypt the AES key used to encrypt the notes, ensuring that only the owner of the notes can access them. 

***
# **Project Guide**
We'll choose Security Challenge A.
# User Note Powers (Server side enforcement)
Any edit (title, content, collaborators) is a note modification.
Dates and last modified by are modified automatically on write.
## Owner
Can view everything.
Can edit note content and title.
Can add or remove editors/viewers.
Can delete note.
Can check integrity.
## Editor
Can view everything.
Can edit note content and title.
## Viewer
Can view note content and title.

**IMPORTANT:** With Security challenge A, anyone can check integrity!
# **Assumptions** (important!)
1. DB is previously populated with all user info
2. Entities have each others certificates(i.e. public keys), so TLS setup is easy
3. TLS ensures safety against replay attacks!
4. Authentication: user and password, returns session token that is used to validate every action requested by user.
5. Adding editors/viewers: Owner requests server to add editor/viewer. If editor/viewer is a legitimate user, server returns to client its public key. With this editor/viewer public key, client can cipher the symmetric key used to cipher note and send to server.

# Client side Features
- [ ] Create note
- [ ] Edit note
- [ ] Save note
- [ ] Send notes (push to server our local notes)
- [ ] Request notes (checks if any note is missing from server, **RUNS ALWAYS AT STARTUP**, and, if client requests)
- [ ] Edit editors and viewers (if owner)
- [ ] Check note integrity (when client requests)