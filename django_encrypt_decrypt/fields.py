from django.db import models

from .crypto import Crypto


class EncryptedTextField(models.TextField):
    internal_type = "TextField"

    def __init__(self, *args, **kwargs):
        self.key = kwargs.pop('key', None)
        self.crypto = Crypto(self.key)
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return self.internal_type

    def get_db_prep_value(self, value, connection, prepared=False):
        value = super().get_db_prep_value(value, connection, prepared)
        if value is None:
            return None

        encrypted_text = self.crypto.encrypt(value)
        return encrypted_text
