from django.conf import settings
from django.db import models

from .crypto import Crypto


class EncryptedBinaryField(models.BinaryField):
    """Store encrypted value as binary"""

    def __init__(self, *args, **kwargs):
        self.key = kwargs.pop('key', None)
        if self.key is None:
            self.key = settings.SECRET_KEY

        self.crypto = Crypto(self.key)
        super().__init__(*args, **kwargs)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not value or isinstance(value, (bytes, memoryview)):
            return value

        encrypted_text = self.crypto.encrypt(str(value))
        encrypted_value = super().get_db_prep_value(encrypted_text, connection, prepared)
        return encrypted_value
