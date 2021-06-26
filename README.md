# ORM Encrypt Decrypt Fields
 
A Django and SQLAlchemy model field that encrypts your data based SHA256 algorithm and Fernet (symmetric encryption) when saving to the model field.  The fernet module guarantees that data encrypted using it cannot be further manipulated or read without the key.  It keeps data always encrypted in the database.

Also, possible to use it directly with the Crypto class.

[![Project Check](https://github.com/alpden550/django-encrypt-decrypt/actions/workflows/python-package.yml/badge.svg)](https://github.com/alpden550/django-encrypt-decrypt/actions/workflows/python-package.yml)

## How install

```
pip install encrypt-decrypt-fields
```

## Usage

For Django use project secret key or own:

```
from django.conf import settings
from django.db import Model
from django_encrypt_decrypt import EncryptedBinaryField


class DemoModel(models.Models):
    password = EncryptedBinaryField(blank=True, null=True)
```

```
DemoModel.objects.create(password='password')
```

```
obj = DemoModel.objects.get(id=1)
obj.password.to_bytes()  # b'gAAAAABgxGVVeTPV9i1nPNl91Ss4XVH0rD6eJCgOWIOeRwtagp12gBJg9DL_HXODTDW0WKsqc8Z9vsuHUiAr3qQVE9YQmTd3pg=='
```

To read bytes in postgres, use to_bytes() method of memoryview

```
obj.password.to_bytes()
```

or

```
bytes(obj.password, 'utf-8')
```

To decrypt value use Crypto class:

```
from django.conf import settings
from django_encrypt_decrypt import Crypto

obj = DemoModel.objects.get(id=1)

decrypted = Crypto(settings.SECRET_KEY).decrypt_token(obj.password.to_bytes())
decrypted  # 'password'
```

For SQLAlchemy, it is similar:

```
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Demo(Base):
    __tablename__ = 'demo'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(EncryptedAlchemyBinaryField(key='secret), nullable=True)
```

```
object = session.query(Demo).first()
Crypto('secret').decrypt_token(object.password)  
```
