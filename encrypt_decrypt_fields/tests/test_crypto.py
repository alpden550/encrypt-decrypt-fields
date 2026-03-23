import pytest

from encrypt_decrypt_fields import Crypto


class TestCrypt:
    def test_key_is_str(self):
        crypto = Crypto("secret")
        key = crypto.get_key()

        assert isinstance(key, bytes)
        assert key == b"K7gNU3sdo-OL0wNhqoVWhr3g6s1xYv72ol_pe_Unols="

    def test_key_not_str(self):
        crypto = Crypto(1)

        with pytest.raises(AttributeError):
            crypto.get_key()

    def test_encrypt_successfully(self):
        password = Crypto("secret").encrypt("password")

        assert isinstance(password, bytes)
        assert password != "password"

    @pytest.mark.parametrize("test_input", [int, tuple, list, dict])
    def test_encrypt_not_successfully(self, test_input):
        with pytest.raises(AttributeError):
            Crypto("secret").encrypt(test_input)

    def test_decrypt_empty_value(self):
        password = Crypto("secret").decrypt_token(b"")

        assert not password

    def test_decrypt_successfully(self):
        encrypted = Crypto("secret").encrypt("password")
        decrypted = Crypto("secret").decrypt_token(encrypted)

        assert decrypted == "password"
