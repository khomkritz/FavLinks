from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .utils import hash_password, check_password, generate_jwt_tokens, refresh_jwt_token, verify_jwt_token, strength_password
from .models import User, Token

# Create your views here.
class Register(APIView):
    def post(self, request):
        data = request.data
        if "username" not in data or data["username"] == None:
            return Response({"status" : False,"message": "require username"}, status=status.HTTP_400_BAD_REQUEST)
        if "password" not in data or data["password"] == None:
            return Response({"status" : False,"message": "require password"}, status=status.HTTP_400_BAD_REQUEST)
        existing_user = User.objects.filter(Q(username=data["username"]) | Q(email=data["email"]))
        if existing_user.exists():
            return Response({"status" : False,"message": "This username or email is already in use"}, status=status.HTTP_400_BAD_REQUEST)
        check_pass = strength_password(data["password"])
        if check_pass["status"] == False:
            return Response({"status" : False,"message": check_pass["message"]}, status=status.HTTP_400_BAD_REQUEST)
        hash_pass = hash_password(data["password"])
        data_user = {
            "password" : hash_pass,
            "username" : data["username"],
            "email" : data["email"],
            "username" : data["username"],
        }
        create_user = User.objects.create(**data_user)
        if create_user:
            return Response({"status" : True, "message" : "register success",}, status=status.HTTP_200_OK)

class Login(APIView):
    def post(self, request):
        data = request.data
        if "username" not in data or data["username"] == None:
            return Response({"status" : False,"message": "require username"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(username=data["username"])
        check = check_password(data["password"], user.password)
        if check == True:
            token = generate_jwt_tokens(user.id)
            Token.objects.create(user_id=user.id, access_token=token["access_token"], refresh_token=token["refresh_token"])
        else:
            return Response({"status" : False,"message": "Password is not true"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status" : True, "message" : "login success", "data" : token}, status=status.HTTP_200_OK)

class Refresh(APIView):
    def post(self, request):
        data = request.data
        refresh = refresh_jwt_token(data["refresh_token"])
        Token.objects.filter(user_id=refresh["user_id"]).update(access_token=refresh["access_token"], refresh_token=refresh["refresh_token"])
        return Response({"status" : True, "message" : "refresh success", "data" : refresh}, status=status.HTTP_200_OK)
    
class Logout(APIView):
    def post(self, request):
        payload = verify_jwt_token(request)
        if payload["status"] == False:
            return Response({"status" : False,"message": "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        Token.objects.filter(user_id=payload["user_id"]).delete()
        return Response({"status" : True, "message" : "logout success"}, status=status.HTTP_200_OK)