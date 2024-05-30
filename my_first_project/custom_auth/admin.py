from django.contrib import admin
from .models import PseudoUser, Token
# Register your models here.

admin.site.register(PseudoUser)
admin.site.register(Token) 
