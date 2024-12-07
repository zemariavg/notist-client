import os
import subprocess
import json

# Colors for the output
GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'

def test_protect_check_unprotect_user_note():
    note_file = os.path.join('cryptolib', 'test', 'notes', 'test1.json')
    protected_note = os.path.join('cryptolib', 'test', 'notes', 'test1_protected.json')
    aes_key = os.path.join('cryptolib', 'test', 'keys', 'aes.key')
    pub_key = os.path.join('cryptolib', 'test', 'keys', 'pub.pem')
    private_key = os.path.join('cryptolib', 'test', 'keys', 'priv.pem')
    
    print(f"{RESET}1. Running test: Protect, Check Integrity, and Unprotect{RED}")

    protect_command = [
        'python3', os.path.join('cryptolib', 'notist.py'), 'protect', note_file, aes_key, pub_key
    ]
    result = subprocess.run(protect_command, capture_output=True, text=True)
    assert result.returncode == 0, f"Protect failed: {result.stderr}\n{result.stdout}"
    
    check_command = [
        'python3', os.path.join('cryptolib', 'notist.py'), 'check', protected_note, private_key
    ]
    result = subprocess.run(check_command, capture_output=True, text=True)
    assert result.returncode == 0, f"Check failed: {result.stderr}"
    assert "Note is valid." in result.stdout, f"Integrity check failed: {result.stdout}"

    unprotect_command = [
        'python3', os.path.join('cryptolib', 'notist.py'), 'unprotect', protected_note, private_key
    ]
    result = subprocess.run(unprotect_command, capture_output=True, text=True)
    assert result.returncode == 0, f"Unprotect failed: {result.stderr}"
    
    with open(note_file, 'r') as f:
        original_note = f.read()
    with open(protected_note, 'r') as f:
        unprotected_note = f.read()
        
    assert original_note == unprotected_note, f"Original note and unprotected note are different."
    
    os.remove(protected_note)

    print(f"{GREEN}Test passed: Protect, Check Integrity, and Unprotect worked correctly.{RED}\n")

def test_protect_tamper_tag_check():
    note_file = os.path.join('cryptolib', 'test', 'notes', 'test2.json')
    protected_note = os.path.join('cryptolib', 'test', 'notes', 'test2_protected.json')
    aes_key = os.path.join('cryptolib', 'test', 'keys', 'aes.key')
    pub_key = os.path.join('cryptolib', 'test', 'keys', 'pub.pem')
    private_key = os.path.join('cryptolib', 'test', 'keys', 'priv.pem')
    
    print(f"{RESET}2. Running test: Protect, Tamper, and Check Integrity{RED}")

    protect_command = [
        'python3', os.path.join('cryptolib', 'notist.py'), 'protect', note_file, aes_key, pub_key
    ]
    result = subprocess.run(protect_command, capture_output=True, text=True)
    assert result.returncode == 0, f"Protect failed: {result.stderr}\n{result.stdout}"
    
    # change note tag 
    with open(protected_note, 'r') as f:
        note = f.read()
    json_note = json.loads(note)
    note_tag = json_note['note_tag']
    json_note['note_tag'] = note_tag[::-1] 
    with open(protected_note, 'w') as f:
        f.write(json.dumps(json_note))
    
    check_command = [
        'python3', os.path.join('cryptolib', 'notist.py'), 'check', protected_note, private_key
    ]
    result = subprocess.run(check_command, capture_output=True, text=True)
    assert result.returncode != 0, f"Check should have failed: {result.stdout}"
    assert "Note is valid." not in result.stdout, f"Integrity check should have failed: {result.stdout}"

    os.remove(protected_note)

    print(f"{GREEN}Test passed: Protect, Tamper, and Check Integrity worked correctly.{RED}\n")

def test_protect_tamper_note_check():
    note_file = os.path.join('cryptolib', 'test', 'notes', 'test3.json')
    protected_note = os.path.join('cryptolib', 'test', 'notes', 'test3_protected.json')
    aes_key = os.path.join('cryptolib', 'test', 'keys', 'aes.key')
    pub_key = os.path.join('cryptolib', 'test', 'keys', 'pub.pem')
    private_key = os.path.join('cryptolib', 'test', 'keys', 'priv.pem')
    
    print(f"{RESET}3. Running test: Protect, Tamper, and Check Note{RED}")

    protect_command = [
        'python3', os.path.join('cryptolib', 'notist.py'), 'protect', note_file, aes_key, pub_key
    ]
    result = subprocess.run(protect_command, capture_output=True, text=True)
    assert result.returncode == 0, f"Protect failed: {result.stderr}\n{result.stdout}"
    
    # change note tag 
    with open(protected_note, 'r') as f:
        note = f.read()
    json_note = json.loads(note)
    note_text = json_note['note']
    json_note['note'] = note_text[::-1] 
    with open(protected_note, 'w') as f:
        f.write(json.dumps(json_note))
    
    check_command = [
        'python3', os.path.join('cryptolib', 'notist.py'), 'check', protected_note, private_key
    ]
    result = subprocess.run(check_command, capture_output=True, text=True)
    assert result.returncode != 0, f"Check should have failed: {result.stdout}"
    assert "Note is valid." not in result.stdout, f"Integrity check should have failed: {result.stdout}"

    os.remove(protected_note)

    print(f"{GREEN}Test passed: Protect, Tamper, and Check Note worked correctly.{RED}\n")

def test_check_unprotect_server_note():
    note_file = os.path.join('cryptolib', 'test', 'notes', 'test4.json')
    aes_key = os.path.join('cryptolib', 'test', 'keys', 'aes.key')
    private_key = os.path.join('cryptolib', 'test', 'keys', 'priv.pem')
    
    print(f"{RESET}4. Running test: Check Integrity and Unprotect{RED}")

    check_command = [ # with server flag
        'python3', os.path.join('cryptolib', 'notist.py'), 'check', note_file, private_key, '--server'
    ]
    result = subprocess.run(check_command, capture_output=True, text=True)
    assert result.returncode == 0, f"Check failed: {result.stderr}"
    assert "Note is valid." in result.stdout, f"Integrity check failed: {result.stdout}"

    unprotect_command = [
        'python3', os.path.join('cryptolib', 'notist.py'), 'unprotect', note_file, private_key, '--server'
    ]
    result = subprocess.run(unprotect_command, capture_output=True, text=True)
    assert result.returncode == 0, f"Unprotect failed: {result.stderr}"

    print(f"{GREEN}Test passed: Check Integrity and Unprotect worked correctly.{RED}\n")

# Run the tests
test_protect_check_unprotect_user_note()
test_protect_tamper_tag_check()
test_protect_tamper_note_check()
test_check_unprotect_server_note()
