"""Key derivation + a simple authenticated stream cipher, stdlib only.

See the "Security note" in README.md -- this is a learning implementation,
not an audited primitive.
"""

import hashlib
import hmac
import secrets

PBKDF2_ITERATIONS = 200_000
KEY_LEN = 32  # bytes (256 bits)
SALT_LEN = 16
NONCE_LEN = 16


def derive_master_key(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS, dklen=KEY_LEN)


def _subkey(master_key: bytes, label: bytes) -> bytes:
    return hmac.new(master_key, label, hashlib.sha256).digest()


def _keystream(key: bytes, nonce: bytes, length: int) -> bytes:
    blocks = []
    counter = 0
    produced = 0
    while produced < length:
        block = hmac.new(key, nonce + counter.to_bytes(4, "big"), hashlib.sha256).digest()
        blocks.append(block)
        produced += len(block)
        counter += 1
    return b"".join(blocks)[:length]


def encrypt(master_key: bytes, plaintext: bytes) -> dict:
    enc_key = _subkey(master_key, b"encryption")
    mac_key = _subkey(master_key, b"authentication")

    nonce = secrets.token_bytes(NONCE_LEN)
    keystream = _keystream(enc_key, nonce, len(plaintext))
    ciphertext = bytes(p ^ k for p, k in zip(plaintext, keystream))

    tag = hmac.new(mac_key, nonce + ciphertext, hashlib.sha256).digest()

    return {
        "nonce": nonce.hex(),
        "ciphertext": ciphertext.hex(),
        "tag": tag.hex(),
    }


class DecryptionError(Exception):
    pass


def decrypt(master_key: bytes, payload: dict) -> bytes:
    enc_key = _subkey(master_key, b"encryption")
    mac_key = _subkey(master_key, b"authentication")

    nonce = bytes.fromhex(payload["nonce"])
    ciphertext = bytes.fromhex(payload["ciphertext"])
    tag = bytes.fromhex(payload["tag"])

    expected_tag = hmac.new(mac_key, nonce + ciphertext, hashlib.sha256).digest()
    if not hmac.compare_digest(tag, expected_tag):
        raise DecryptionError("authentication failed (wrong password or corrupted data)")

    keystream = _keystream(enc_key, nonce, len(ciphertext))
    plaintext = bytes(c ^ k for c, k in zip(ciphertext, keystream))
    return plaintext
