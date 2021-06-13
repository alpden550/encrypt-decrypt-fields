# Django Encrypt Decrypt
 
A Django model field that encrypts your data based SHA256 algorithm and Fernet (symmetric encryption) when saving to the model field.  The fernet module guarantees that data encrypted using it cannot be further manipulated or read without the key.  It keeps data always encrypted in the database.

[![Project Check](https://github.com/alpden550/django-encrypt-decrypt/actions/workflows/python-package.yml/badge.svg)](https://github.com/alpden550/django-encrypt-decrypt/actions/workflows/python-package.yml)

## How install

```
pip install django-encrypt-decrypt
```

## Usage

Use project secret key or own:

```
from django.conf import settings
from django.db import Model
from django_encrypt_decrypt import EncryptedTextField


class DemoModel(models.Models):
    password = EncryptedTextField(blank=True)
```

```
DemoModel.objects.create(password='password')
```

```
obj = DemoModel.objects.get(id=1)
obj.password  # 'gAAAAABgxGVVeTPV9i1nPNl91Ss4XVH0rD6eJCgOWIOeRwtagp12gBJg9DL_HXODTDW0WKsqc8Z9vsuHUiAr3qQVE9YQmTd3pg=='
```

To decrypt value use Crypto class:

```
from django.conf import settings
from django_encrypt_decrypt import Crypto

obj = DemoModel.objects.get(id=1)

decrypted = Crypto(settings.SECRET_KEY).decrypt_token(obj.password)
decrypted  # 'password'
```
