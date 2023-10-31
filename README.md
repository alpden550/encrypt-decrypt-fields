# ORM Encrypt Decrypt Fields

A Django and SQLAlchemy model field that encrypts your data based SHA256 algorithm and Fernet (symmetric encryption)
when saving to the model field. The fernet module guarantees that data encrypted using it cannot be further manipulated
or read without the key. It keeps data always encrypted in the database.

Also, possible to use it directly with the Crypto class.

[![ProjectCheck](https://github.com/alpden550/encrypt-decrypt-fields/actions/workflows/check.yml/badge.svg)](https://github.com/alpden550/encrypt-decrypt-fields/actions/workflows/check.yml)

## How install

```
pip install encrypt-decrypt-fields
```

## Usage

For Django use project secret key or own:

```python
from django.db import models
from encrypt_decrypt_fields import EncryptedBinaryField


class DemoModel(models.Model):
    password = EncryptedBinaryField(blank=True, null=True)
```

```python
from .models import DemoModel

DemoModel.objects.create(password='password')

demo = DemoModel.objects.get(id=1)
print(demo.password.to_bytes()) 
# b'gAAAAABgxGVVeTPV9i1nPNl91Ss4XVH0rD6eJCgOWIOeRwtagp12gBJg9DL_HXODTDW0WKsqc8Z9vsuHUiAr3qQVE9YQmTd3pg=='
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

```python
from django.conf import settings
from encrypt_decrypt_fields import Crypto
from .models import DemoModel


obj = DemoModel.objects.get(id=1)

decrypted = Crypto(settings.SECRET_KEY).decrypt_token(obj.password.to_bytes())
print(decrypted) 
# 'password'
```

For SQLAlchemy, it is similar:

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from encrypt_decrypt_fields import Crypto, EncryptedAlchemyBinaryField

Base = declarative_base()
engine = create_engine("sqlite:///:memory:", echo=True)


class Demo(Base):
    __tablename__ = 'demo'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(EncryptedAlchemyBinaryField(key='secret'), nullable=True)


Session = sessionmaker(bind=engine)
session = Session()

demo = session.query(Demo).first()
Crypto('secret').decrypt_token(demo.password)  
```
