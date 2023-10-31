from unittest.mock import Mock

import pytest

from encrypt_decrypt_fields import EncryptedBinaryField, Crypto


class TestDjangoEncryptField:
    FIELD = EncryptedBinaryField(key="secret")

    @pytest.fixture
    def connection(self):
        yield Mock()

    def test_passed_empty_value(self, connection):
        value = self.FIELD.get_db_prep_value(None, connection)

        assert value is None
        connection.Database.Binary.assert_not_called()

    def test_passed_byte_value(self, connection):
        value = self.FIELD.get_db_prep_value(b"value", connection)

        assert value == b"value"
        connection.Database.Binary.assert_not_called()

    def test_passed_memoryview_value(self, connection):
        value = self.FIELD.get_db_prep_value(memoryview(b"value"), connection)

        assert value.tobytes() == b"value"
        connection.Database.Binary.assert_not_called()

    def test_passed_string_value(self, connection):
        connection.Database.Binary.return_value = (
            b"gAAAAABg1vz2rLbNvztnC8p2hQbBGzrnyuGN772bEY5"
            b"w9c1s6fVmqZm4bkjJPfr2PAWZZ3twsLcajxK5y6g-KpjjeMO5luh0fg=="
        )
        value = self.FIELD.get_db_prep_value("password", connection)

        connection.Database.Binary.assert_called_once()
        assert not isinstance(value, str)
        assert Crypto("secret").decrypt_token(value) == "password"

    @pytest.mark.parametrize(
        ("passed", "passed_type"),
        [(1, int), ({"value": 1}, dict), ([1, "value"], list)],
    )
    def test_passed_any_value(self, passed, passed_type, connection):
        connection.Database.Binary.return_value = b"value"
        value = self.FIELD.get_db_prep_value(passed, connection)

        connection.Database.Binary.assert_called_once()
        assert not isinstance(value, passed_type)
        assert value != passed
