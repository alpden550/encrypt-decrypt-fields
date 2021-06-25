from sqlalchemy.types import TypeDecorator, Text

from encrypt_decrypt_fields import Crypto


class EncryptedAlchemyTextField(TypeDecorator):
    impl = Text

    def __init__(self, key: str, *arg, **kwargs):
        TypeDecorator.__init__(self, *arg, **kwargs)
        self.key = key
        self.crypto = Crypto(key=self.key)

    def process_bind_param(self, value, dialect):
        if not value or isinstance(value, bytes) or isinstance(value, memoryview):
            return value

        return self.crypto.encrypt(value)
