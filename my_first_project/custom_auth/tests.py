from django.test import TestCase

import hashlib
from datetime import datetime
hash_str = hashlib.sha256(b'qwerty123')
print(hash_str.hexdigest())
token_str = f'asdfgh{hash_str}.{str(datetime.now())}'
token = hashlib.sha512(token_str.encode())
print(token.hexdigest())
