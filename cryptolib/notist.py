import argparse
import sys
from .protect import protect_note_path
from .unprotect import unprotect_note_path
from .check import check_note

def display_help() -> None:
    print(
        "Usage: \n"
        "\tnotist [-h|help]\n"
        "\tnotist protect (plain_note) (aes-key) (public-key)\n"
        "\tnotist check (protected_note) (private-key)\n"
        "\tnotist unprotect (protected_note) (private-key)"
    )
    sys.exit(0)

def handle_protect(args) -> None:
    try:
        protect_note_path(args.note_file_path, args.aes_key, args.public_key) 
        print("Note protected successfully.")
    except Exception as e:
        print(f"Error during protect: {e}")
        sys.exit(1)

def handle_check(args) -> None:
    try:
        result = check_note(args.note_file_path, args.private_key_path)
        print("Note is valid." if result else "Note has been tampered with.")
    except Exception as e:
        print(f"Error during check: {e}")
        sys.exit(1)

def handle_unprotect(args) -> None:
    try:
        unprotect_note_path(args.note_file_path, args.private_key_path)
        print("Note unprotected successfully.")
    except Exception as e:
        print(f"Error during unprotect: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Notist Cryptographic Tool")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    protect_parser = subparsers.add_parser("protect", help="Protect a note file.")
    protect_parser.add_argument("note_file_path", help="The path to the note file")
    protect_parser.add_argument("aes_key", help="The AES key file path")
    protect_parser.add_argument("public_key", help="The public key file path")
    
    check_parser = subparsers.add_parser("check", help="Check the integrity of a note file")
    check_parser.add_argument("note_file_path", help="The path to the note file")
    check_parser.add_argument("private_key_path", help="Path to the RSA private key file")
    
    unprotect_parser = subparsers.add_parser("unprotect", help="Unprotect a note file")
    unprotect_parser.add_argument("note_file_path", help="The path to the note file")
    unprotect_parser.add_argument("private_key_path", help="Path to the RSA private key file")
    
    help_parser = subparsers.add_parser("help", help="Display help message")

    args = parser.parse_args()
    
    if args.command == "help" or not args.command:
        display_help()

    if args.command == "protect":
        handle_protect(args)
    elif args.command == "check":
        handle_check(args)
    elif args.command == "unprotect":
        handle_unprotect(args)