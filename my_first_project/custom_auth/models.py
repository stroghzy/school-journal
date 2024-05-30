from django.db import models
from hashlib import sha256

class PseudoUser(models.Model):
    email = models.CharField(max_length=50, primary_key=True)
    password_hash = models.CharField(max_length=32)
    role = models.CharField(max_length=10)
    role_id = models.PositiveBigIntegerField()

    def save(self, **kwargs):
        self.password_hash = sha256(self.password_hash.encode()).hexdigest()
        super().save(**kwargs)

class Token(models.Model):
    email = models.CharField(max_length=50, primary_key=True)
    date_expired = models.DateTimeField()
    token = models.CharField(max_length=128)