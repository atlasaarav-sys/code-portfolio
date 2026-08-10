import tempfile
import unittest
from pathlib import Path

from vault import Vault, DecryptionError
from crypto_utils import derive_master_key, encrypt, decrypt


class TestCryptoUtils(unittest.TestCase):
    def test_encrypt_decrypt_round_trip(self):
        key = derive_master_key("correct horse battery staple", b"0" * 16)
        plaintext = b"a secret message"
        payload = encrypt(key, plaintext)
        recovered = decrypt(key, payload)
        self.assertEqual(recovered, plaintext)

    def test_wrong_key_fails_authentication(self):
        key1 = derive_master_key("password1", b"0" * 16)
        key2 = derive_master_key("password2", b"0" * 16)
        payload = encrypt(key1, b"secret")
        with self.assertRaises(Exception):
            decrypt(key2, payload)

    def test_tampered_ciphertext_detected(self):
        key = derive_master_key("password", b"0" * 16)
        payload = encrypt(key, b"secret data")
        tampered = dict(payload)
        # Flip a byte in the ciphertext.
        raw = bytearray(bytes.fromhex(tampered["ciphertext"]))
        raw[0] ^= 0xFF
        tampered["ciphertext"] = bytes(raw).hex()
        with self.assertRaises(Exception):
            decrypt(key, tampered)


class TestVault(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.vault_path = Path(self.tmpdir.name) / "vault.json"

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_add_get_delete(self):
        vault = Vault("master-pw", path=self.vault_path)
        vault.add("github", "alice", "hunter2")
        entry = vault.get("github")
        self.assertEqual(entry["username"], "alice")
        self.assertEqual(entry["password"], "hunter2")

        self.assertEqual(vault.list_names(), ["github"])

        self.assertTrue(vault.delete("github"))
        self.assertEqual(vault.list_names(), [])

    def test_reopen_with_correct_password(self):
        vault1 = Vault("master-pw", path=self.vault_path)
        vault1.add("site", "bob", "pw123")
        del vault1

        vault2 = Vault("master-pw", path=self.vault_path)
        entry = vault2.get("site")
        self.assertEqual(entry["username"], "bob")

    def test_reopen_with_wrong_password_rejected(self):
        vault1 = Vault("correct-pw", path=self.vault_path)
        vault1.add("site", "bob", "pw123")
        del vault1

        with self.assertRaises(DecryptionError):
            Vault("wrong-pw", path=self.vault_path)


if __name__ == "__main__":
    unittest.main()
