from django.shortcuts import render
from .models import PseudoUser, Token
from datetime import datetime, timedelta
from hashlib import sha256, sha512
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST'])

def token_create(request):
    if request.method == 'POST':
        data = request.data
        if "email" not in data or "password" not in data:
            return Response({"status": "error","message": 'Передайте ключ email'})
        if Token.objects.filter(email=data["email"]).exists():
            return Response({"status": "error","message": "Токен уже существует"})
        user_obj = PseudoUser.objects.filter(email=data["email"])
        if not PseudoUser.objects.filter(email=data["email"]).exists():
            return Response({"status": "error","message": "Пользователя не существует"})
        if sha256(data["password"].encode()).hexdigest() != user_obj[0].password_hash:
            return Response({"status": "error","message": "Неверный пароль!"})
        date = datetime.now()
        token = f"{data['email']}.{user_obj[0].password_hash}.{date}"
        token = sha512(token.encode()).hexdigest()
        date = date + timedelta(days=3)
        Token.objects.create(email=data["email"], date_expired=date, token=token)
        return Response({'status': "success", "token": token})
    return Response({"message": 'Здесь вы можете создать токен'})


@api_view(["GET", "POST"])
def token_refresh(request):
    if request.method == 'POST':
        data = request.data
        if "email" not in data or "password" not in data:
            return Response({"status": "error","message": 'Передайте ключ email'})
        if not Token.objects.filter(email=data["email"]).exists():
            return Response({"status": "error","message": "Токена не существует"})
        user_obj = PseudoUser.objects.filter(email=data["email"])
        if sha256(data["password"].encode()).hexdigest() != user_obj[0].password_hash:
            return Response({"status": "error","message": "Неверный пароль!"})
        date = datetime.now()
        token = f"{data['email']}.{user_obj[0].password_hash}.{date}"
        token = sha512(token.encode()).hexdigest()
        date = date + timedelta(days=3)
        Token.objects.filter(email=data["email"]).update(date_expired=date, token=token)
        return Response({'status': "success", "token": token})
    return Response({"message": 'Здесь вы можете создать токен'})
