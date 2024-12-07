from check import *
from protect import *
from unprotect import *
import argparse
import sys

def display_help() -> None:
    """Display the help message and exit."""
    print(
        "Usage: \n"
        "\tnotist help\n"
        "\tnotist protect [-s] (note_file) (aes-key) (public-key)\n"
        "\tnotist check [-s] (note_file) (private-key)\n"
        "\tnotist unprotect [-s] (note_file) (private-key)"
    )
    sys.exit(0)

def handle_protect(args) -> None:
    """Handle the protect command."""
    try:
        result = protect_user_note(args.note_file_path, args.aes_key, args.public_key)
        print(result)
    except Exception as e:
        print(f"Error during protect: {e}")
        sys.exit(1)

def handle_check(args) -> None:
    """Handle the check command."""
    try:
        result = check_note(args.note_file_path, args.private_key_path)
        print("Note is valid." if result else "Note has been tampered with.")
    except Exception as e:
        print(f"Error during check: {e}")
        sys.exit(1)

def handle_unprotect(args) -> None:
    """Handle the unprotect command."""
    try:
        result = unprotect_user_note(args.note_file_path, args.private_key_path)
        print(result)
    except Exception as e:
        print(f"Error during unprotect: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Notist Cryptographic Tool")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # Subparser for 'protect'
    protect_parser = subparsers.add_parser("protect", help="Protect a note file.")
    protect_parser.add_argument("note_file_path", help="The path to the note file")
    protect_parser.add_argument("aes_key", help="The AES key file path")
    protect_parser.add_argument("public_key", help="The public key file path")
    protect_parser.add_argument("-s", "--server", action="store_true", help="Check server metadata")
    
    # Subparser for 'check'
    check_parser = subparsers.add_parser("check", help="Check the integrity of a note file")
    check_parser.add_argument("note_file_path", help="The path to the note file")
    check_parser.add_argument("private_key_path", help="Path to the RSA private key file")
    check_parser.add_argument("-s", "--server", action="store_true", help="Check server metadata")
    
    # Subparser for 'unprotect'
    unprotect_parser = subparsers.add_parser("unprotect", help="Unprotect a note file")
    unprotect_parser.add_argument("note_file_path", help="The path to the note file")
    unprotect_parser.add_argument("private_key_path", help="Path to the RSA private key file")
    unprotect_parser.add_argument("-s", "--server", action="store_true", help="Check server metadata")

    args = parser.parse_args()
    
    if args.command == "help" or not args.command:
        display_help()

    if args.command == "protect":
        handle_protect(args)
    elif args.command == "check":
        handle_check(args)
    elif args.command == "unprotect":
        handle_unprotect(args)