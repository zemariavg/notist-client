import os
import subprocess
import json

from cryptography.hazmat.primitives.serialization import PrivateFormat

# colors for output
RESET = "\033[0m"
GREEN = "\033[32m"
RED = "\033[31m"

# Run from test directory!
note = os.path.abspath("test_notes/test1.json")
note_key = os.path.abspath("test_keys/aes.key")
protected_note = os.path.abspath("test_notes/test1_protected.json")
pub_key = os.path.abspath("test_keys/pub.pem")
priv_key = os.path.abspath("test_keys/priv.pem")

protect_command = ["python3",  "../notist.py", "protect", note, note_key, pub_key]
unprotect_command = ["python3",  "../notist.py", "unprotect", protected_note, priv_key] 
check_command = ["python3",  "../notist.py", "check", protected_note, pub_key]

def protect_unprotect() -> None:
    print(f"{RESET}Testing protect and unprotect commands...")
    
    assert subprocess.run(protect_command).returncode == 0
    assert subprocess.run(unprotect_command).returncode == 0
    
    with open(note, "r") as f:
        note_content = f.read()
    with open(protected_note, "r") as f:
        protected_note_content = f.read()
    
    assert note_content == protected_note_content
    os.remove(protected_note)
    print(f"{GREEN}Protect and unprotect commands passed!")

def protect_check() -> None:
    print(f"{RESET}Testing protect and check commands...")
    
    assert subprocess.run(protect_command).returncode == 0 
    assert subprocess.run(check_command).returncode == 0
    os.remove(protected_note)
    print(f"{GREEN}Protect and check commands passed!")
    
def protect_tamper_check() -> None:
    print(f"{RESET}Testing protect, tamper and check commands...")
    
    assert subprocess.run(protect_command).returncode == 0 
    
    with open(protected_note, "r") as f:
        note_content = f.read()
        
    # change note_tag key's value
    with open(protected_note, "w") as f:
        note_content = json.loads(note_content)
        note_content["note_tag"] = note_content["note_tag"][::-2]
        f.write(json.dumps(note_content))
    
    result = subprocess.run(check_command, stdout=subprocess.PIPE, text=True)
    assert result.stdout.strip() == "Note has been tampered with."
    os.remove(protected_note)
    print(f"{GREEN}Protect, tamper and check commands passed!")
    
def test_all() -> None:
    protect_unprotect()
    protect_check()
    protect_tamper_check()
    print(f"{GREEN}All tests passed!")

if __name__ == "__main__":
    test_all()