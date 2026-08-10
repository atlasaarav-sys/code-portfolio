import argparse
import getpass
import sys

from vault import Vault, DecryptionError


def get_master_password():
    return getpass.getpass("Master password: ")


def cmd_init(args):
    password = get_master_password()
    confirm = getpass.getpass("Confirm master password: ")
    if password != confirm:
        print("Passwords don't match.")
        sys.exit(1)
    Vault(password)
    print("Vault initialized.")


def open_vault():
    password = get_master_password()
    try:
        return Vault(password)
    except DecryptionError as e:
        print(f"Error: {e}")
        sys.exit(1)


def cmd_add(args):
    vault = open_vault()
    password = args.password or getpass.getpass(f"Password for {args.name}: ")
    vault.add(args.name, args.username, password)
    print(f"Added entry: {args.name}")


def cmd_get(args):
    vault = open_vault()
    try:
        entry = vault.get(args.name)
    except KeyError:
        print(f"No entry named '{args.name}'")
        sys.exit(1)
    print(f"username: {entry['username']}")
    print(f"password: {entry['password']}")


def cmd_list(args):
    vault = open_vault()
    names = vault.list_names()
    if not names:
        print("Vault is empty.")
        return
    for name in names:
        print(name)


def cmd_delete(args):
    vault = open_vault()
    if vault.delete(args.name):
        print(f"Deleted entry: {args.name}")
    else:
        print(f"No entry named '{args.name}'")


def main():
    parser = argparse.ArgumentParser(description="Local encrypted password vault")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init").set_defaults(func=cmd_init)

    p_add = sub.add_parser("add")
    p_add.add_argument("name")
    p_add.add_argument("username")
    p_add.add_argument("password", nargs="?", help="omit to be prompted (hidden input)")
    p_add.set_defaults(func=cmd_add)

    p_get = sub.add_parser("get")
    p_get.add_argument("name")
    p_get.set_defaults(func=cmd_get)

    sub.add_parser("list").set_defaults(func=cmd_list)

    p_delete = sub.add_parser("delete")
    p_delete.add_argument("name")
    p_delete.set_defaults(func=cmd_delete)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
