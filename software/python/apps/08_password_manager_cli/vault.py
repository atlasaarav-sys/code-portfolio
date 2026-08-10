"""Encrypted JSON credential vault."""

import json
import secrets
from pathlib import Path

from crypto_utils import derive_master_key, encrypt, decrypt, DecryptionError, SALT_LEN

DEFAULT_VAULT_PATH = Path(__file__).parent / "vault.json"


class Vault:
    def __init__(self, master_password: str, path: Path = DEFAULT_VAULT_PATH):
        self.path = path
        if path.exists():
            with open(path) as f:
                store = json.load(f)
            self.salt = bytes.fromhex(store["salt"])
            self.master_key = derive_master_key(master_password, self.salt)
            self.entries = store["entries"]  # name -> {nonce, ciphertext, tag}
            # Verify the password is correct by trying to decrypt a canary entry.
            if "__canary__" in self.entries:
                try:
                    decrypt(self.master_key, self.entries["__canary__"])
                except DecryptionError:
                    raise DecryptionError("wrong master password")
        else:
            self.salt = secrets.token_bytes(SALT_LEN)
            self.master_key = derive_master_key(master_password, self.salt)
            self.entries = {"__canary__": encrypt(self.master_key, b"vault-ok")}
            self.save()

    def save(self):
        with open(self.path, "w") as f:
            json.dump({"salt": self.salt.hex(), "entries": self.entries}, f, indent=2)

    def add(self, name: str, username: str, password: str):
        payload = json.dumps({"username": username, "password": password}).encode("utf-8")
        self.entries[name] = encrypt(self.master_key, payload)
        self.save()

    def get(self, name: str) -> dict:
        if name not in self.entries:
            raise KeyError(name)
        plaintext = decrypt(self.master_key, self.entries[name])
        return json.loads(plaintext)

    def delete(self, name: str) -> bool:
        if name in self.entries:
            del self.entries[name]
            self.save()
            return True
        return False

    def list_names(self):
        return sorted(n for n in self.entries if n != "__canary__")
