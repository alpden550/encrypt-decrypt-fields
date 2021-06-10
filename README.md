# Django Encrypt Decrypt
 
A Django model field that encrypts your data based SHA256 algorithm when saving to the model field. It keeps data always encrypted in the database.

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
obj.password  # 'bYijegsEDrmS1s7iuytt5TUgglnspA'
```

To decrypt value use Crypto class:

```
from django.conf import settings
from django_encrypt_decrypt import Crypto

obj = DemoModel.objects.get(id=1)

decrypted = Crypto(settings.SECRET_KEY).decrypt_token(obj.password)
decrypted  # 'password'
```
