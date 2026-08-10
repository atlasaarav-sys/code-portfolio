# Password Manager CLI

**Stack:** Python 3, stdlib only (`hashlib`, `hmac`, `secrets`)

A local encrypted credential vault: entries are encrypted with a key
derived from a master password via PBKDF2-HMAC-SHA256, stored in a JSON
file on disk. Add/get/list/delete entries; the master password is never
stored, only used to re-derive the key each run.

## Files

- `crypto_utils.py` — key derivation (PBKDF2, 200k iterations, random
  salt) and a simple authenticated stream cipher: XOR against an
  HMAC-SHA256-based keystream, with an HMAC tag over the ciphertext so
  tampering/wrong-password is detected before returning garbage plaintext
- `vault.py` — `Vault` class: load/save the encrypted JSON store, add/get/
  list/delete entries
- `main.py` — CLI (`init`, `add`, `get`, `list`, `delete`)
- `test_vault.py` — round-trip encryption tests + wrong-password rejection

## How to run

```bash
python main.py init                                  # creates vault.json, prompts for master password
python main.py add github myusername 'sup3r$ecret'
python main.py get github
python main.py list
python main.py delete github
```

Run tests:

```bash
python -m unittest test_vault.py
```

## Security note (read this before using it for real)

**This is a portfolio/learning implementation, not something to store real
credentials in.** The cipher here (HMAC-SHA256 keystream XOR) is a
hand-rolled construction to demonstrate key derivation + authenticated
encryption concepts using only the standard library — it has not been
audited and stdlib has no constant-time-verified, peer-reviewed AEAD
primitive to lean on. For anything real, use `cryptography`'s `Fernet` (AES
under the hood) or a maintained password manager. `vault.json` and any
`.key`/salt file are gitignored regardless.
