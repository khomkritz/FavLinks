from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Tag, Url, UrlTag
from user.utils import verify_jwt_token
from datetime import datetime

# Create your views here.
class CreateCategory(APIView):
    def post(self, request):
        data = request.data
        payload = verify_jwt_token(request)
        print(payload)
        if payload["status"] == False:
            return Response({"status" : False,"message": "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        if "name" not in data or data["name"] == None:
            return Response({"status" : False,"message": "require name"}, status=status.HTTP_400_BAD_REQUEST)
        user_id = payload["user_id"]
        data_create = {
            "name" : data["name"],
            "user_id" : user_id,
        }
        create_category = Category.objects.create(**data_create)
        if create_category:
            return Response({"status" : True, "message" : "create category success"}, status=status.HTTP_200_OK)
        else:
            return Response({"status" : False,"message": "create category fail"}, status=status.HTTP_400_BAD_REQUEST)
        
class GetCategoryList(APIView):
    def get(self, request):
        collect_categories = []
        payload = verify_jwt_token(request)
        if payload["status"] == False:
            return Response({"status" : False,"message": "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        user_id = payload["user_id"]
        categories = Category.objects.filter(user_id=user_id)
        for category in categories:
            if category.delete_at == None:
                data_category = {
                    "id" : category.id,
                    "name" : category.name
                }
                collect_categories.append(data_category)
        return Response({"status" : True, "message" : "get category list success", "data" : collect_categories}, status=status.HTTP_200_OK)
        
class GetCatagoryID(APIView):
    def get(self, request, category_id):
        payload = verify_jwt_token(request)
        if payload["status"] == False:
            return Response({"status" : False,"message": "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        user_id = payload["user_id"]
        category = Category.objects.get(id=category_id)
        if category.user_id != user_id:
            return Response({"status" : False,"message": "category id isn't true"}, status=status.HTTP_400_BAD_REQUEST)
        data_category = {
            "id" : category.id,
            "name" : category.name,
            "create_at" : category.create_at,
            "update_at" : category.update_at,
            "delete_at" : category.delete_at
        }
        return Response({"status" : True, "message" : "get category success", "data" : data_category}, status=status.HTTP_200_OK)
    
class UpdateCategory(APIView):
    def put(self, request, category_id):
        data = request.data
        payload = verify_jwt_token(request)
        if payload["status"] == False:
            return Response({"status" : False,"message": "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        user_id = payload["user_id"]
        try:
            category = Category.objects.get(id=category_id)
        except:
            return Response({"status" : False,"message": "category id isn't found"}, status=status.HTTP_400_BAD_REQUEST)
        if category.user_id != user_id:
            return Response({"status" : False,"message": "category id isn't found"}, status=status.HTTP_400_BAD_REQUEST)
        if "name" not in data or data["name"] == None:
            return Response({"status" : False,"message": "require name"}, status=status.HTTP_400_BAD_REQUEST)
        category.name = data["name"]
        category.update_at = datetime.now()
        category.save()
        data_category = {
            "id" : category.id,
            "name" : category.name,
            "create_at" : category.create_at,
            "update_at" : category.update_at,
            "delete_at" : category.delete_at
        }
        return Response({"status" : True, "message" : "update category success", "data" : data_category}, status=status.HTTP_200_OK)
    
class DeleteCategory(APIView):
    def delete(self, request, category_id):
        payload = verify_jwt_token(request)
        if payload["status"] == False:
            return Response({"status" : False,"message": "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        user_id = payload["user_id"]
        try:
            category = Category.objects.get(id=category_id)
        except:
            return Response({"status" : False,"message": "category id isn't found"}, status=status.HTTP_400_BAD_REQUEST)
        if category.user_id != user_id:
            return Response({"status" : False,"message": "category id isn't found"}, status=status.HTTP_400_BAD_REQUEST)
        category.delete_at = datetime.now()
        category.save()
        return Response({"status" : True, "message" : "delete category success"}, status=status.HTTP_200_OK)

class CreateTag(APIView):
    def post(self, request):
        data = request.data
        payload = verify_jwt_token(request)
        print(payload)
        if payload["status"] == False:
            return Response({"status" : False,"message": "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        if "name" not in data or data["name"] == None:
            return Response({"status" : False,"message": "require name"}, status=status.HTTP_400_BAD_REQUEST)
        user_id = payload["user_id"]
        data_create = {
            "name" : data["name"],
            "user_id" : user_id,
        }
        create_tag = Tag.objects.create(**data_create)
        if create_tag:
            return Response({"status" : True, "message" : "create tag success"}, status=status.HTTP_200_OK)
        else:
            return Response({"status" : False,"message": "create tag fail"}, status=status.HTTP_400_BAD_REQUEST)
        
class GetTagList(APIView):
    def get(self, request):
        collect_tags = []
        payload = verify_jwt_token(request)
        if payload["status"] == False:
            return Response({"status" : False,"message": "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        user_id = payload["user_id"]
        tags = Tag.objects.filter(user_id=user_id, delete_at=None).order_by('id')
        for tag in tags:
            data_tag = {
                "id" : tag.id,
                "name" : tag.name
            }
            collect_tags.append(data_tag)
        return Response({"status" : True, "message" : "get tag list success", "data" : collect_tags}, status=status.HTTP_200_OK)
    
class GetTagID(APIView):
    def get(self, request, tag_id):
        payload = verify_jwt_token(request)
        if payload["status"] == False:
            return Response({"status" : False,"message": "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        user_id = payload["user_id"]
        tag = Tag.objects.get(id=tag_id)
        if tag.user_id != user_id:
            return Response({"status" : False,"message": "tag id isn't true"}, status=status.HTTP_400_BAD_REQUEST)
        data_tag = {
            "id" : tag.id,
            "name" : tag.name,
            "create_at" : tag.create_at,
            "update_at" : tag.update_at,
            "delete_at" : tag.delete_at
        }
        return Response({"status" : True, "message" : "get tag list success", "data" : data_tag}, status=status.HTTP_200_OK)
    
class UpdateTag(APIView):
    def put(self, request, tag_id):
        data = request.data
        payload = verify_jwt_token(request)
        if payload["status"] == False:
            return Response({"status" : False,"message": "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        user_id = payload["user_id"]
        try:
            tag = Tag.objects.get(id=tag_id)
        except:
            return Response({"status" : False,"message": "tag id isn't found"}, status=status.HTTP_400_BAD_REQUEST)
        if tag.user_id != user_id:
            return Response({"status" : False,"message": "tag id isn't found"}, status=status.HTTP_400_BAD_REQUEST)
        if "name" not in data or data["name"] == None:
            return Response({"status" : False,"message": "require name"}, status=status.HTTP_400_BAD_REQUEST)
        tag.name = data["name"]
        tag.update_at = datetime.now()
        tag.save()
        data_tag = {
            "id" : tag.id,
            "name" : tag.name,
            "create_at" : tag.create_at,
            "update_at" : tag.update_at,
            "delete_at" : tag.delete_at
        }
        return Response({"status" : True, "message" : "update tag success", "data" : data_tag}, status=status.HTTP_200_OK)
    
class DeleteTag(APIView):
    def delete(self, request, tag_id):
        payload = verify_jwt_token(request)
        if payload["status"] == False:
            return Response({"status" : False,"message": "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        user_id = payload["user_id"]
        try:
            tag = Tag.objects.get(id=tag_id)
        except:
            return Response({"status" : False,"message": "tag id isn't found"}, status=status.HTTP_400_BAD_REQUEST)
        if tag.user_id != user_id:
            return Response({"status" : False,"message": "tag id isn't found"}, status=status.HTTP_400_BAD_REQUEST)
        tag.delete_at = datetime.now()
        tag.save()
        return Response({"status" : True, "message" : "delete tag success"}, status=status.HTTP_200_OK)
    
class CreateUrl(APIView):
    def post(self, request):
        data = request.data
        payload = verify_jwt_token(request)
        if payload["status"] == False:
            return Response({"status" : False,"message": "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        user_id = payload["user_id"]
        data_create = {
            "name" : data["name"],
            "description" : data["description"],
            "link" : data["link"],
            "user_id" : user_id,
            "category_id" : data["category_id"],
        }
        create_url = Url.objects.create(**data_create)
        if create_url:
            for tag_id in data["tag"]:
                UrlTag.objects.create(url=create_url, tag_id=tag_id)
            return Response({"status" : True, "message" : "create url success"}, status=status.HTTP_200_OK)
        else:
            return Response({"status" : False,"message": "create url fial"}, status=status.HTTP_400_BAD_REQUEST)

class GetUrlList(APIView):
    def get(self, request):
        collect_urls = []
        payload = verify_jwt_token(request)
        if payload["status"] == False:
            return Response({"status" : False,"message": "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        user_id = payload["user_id"]
        urls = Url.objects.filter(user_id=user_id, delete_at=None).order_by("id")
        for url in urls:
            urltags = UrlTag.objects.filter(url=url.id)
            collect_tags = []
            for urltag in urltags:
                data_urltag = {
                    "id" : urltag.tag.id,
                    "name" : urltag.tag.name
                }
                collect_tags.append(data_urltag)
            data_url = {
                "id" : url.id,
                "name" : url.name,
                "description" : url.description,
                "link" : url.link,
                "category" : {
                    "id" : url.category.id,
                    "name" : url.category.name
                },
                "tag" : collect_tags
            }
            collect_urls.append(data_url)
        return Response({"status" : True, "message" : "get url list success", "data" : collect_urls}, status=status.HTTP_200_OK)

class GetUrlID(APIView):
    def get(self, request, url_id):
        payload = verify_jwt_token(request)
        if payload["status"] == False:
            return Response({"status" : False,"message": "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        user_id = payload["user_id"]
        url = Url.objects.get(id=url_id)
        urltags = UrlTag.objects.filter(url=url.id)
        if url.user_id != user_id:
            return Response({"status" : False,"message": "tag id isn't true"}, status=status.HTTP_400_BAD_REQUEST)
        collect_tags = []
        for urltag in urltags:
            data_urltag = {
                "id" : urltag.tag.id,
                "name" : urltag.tag.name
            }
            collect_tags.append(data_urltag)
        data_url = {
            "id" : url.id,
            "name" : url.name,
            "description" : url.description,
            "link" : url.link,
            "category" : {
                "id" : url.category.id,
                "name" : url.category.name
            },
            "tag" : collect_tags,
            "create_at" : url.create_at,
            "update_at" : url.update_at,
            "delete_at" : url.delete_at
        }
        return Response({"status" : True, "message" : "get url id success", "data" : data_url}, status=status.HTTP_200_OK)
    
class UpdateUrl(APIView):
    def put(self, request, url_id):
        data = request.data
        payload = verify_jwt_token(request)
        if payload["status"] == False:
            return Response({"status" : False,"message": "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        user_id = payload["user_id"]
        url = Url.objects.get(id=url_id)
        if url.user_id != user_id:
            return Response({"status" : False,"message": "tag id isn't true"}, status=status.HTTP_400_BAD_REQUEST)
        if "tag" in data and len(data["tag"]) > 0:
            delete_old_tags = UrlTag.objects.filter(url=url.id).delete()
            for tag in data["tag"]:
                UrlTag.objects.create(url=url, tag_id=tag)
        if "name" in data and data["name"] != None:
            url.name = data["name"]
        if "description" in data and data["description"] != None:
            url.description = data["description"]
        if "link" in data and data["link"] != None:
            url.link = data["link"]
        if "category_id" in data and data["category_id"] != None:
            url.category = data["category_id"]
        url.save()

        urltags = UrlTag.objects.filter(url=url.id)
        collect_tags = []
        for urltag in urltags:
            data_urltag = {
                "id" : urltag.tag.id,
                "name" : urltag.tag.name
            }
            collect_tags.append(data_urltag)
        data_url = {
            "id" : url.id,
            "name" : url.name,
            "description" : url.description,
            "link" : url.link,
            "category" : {
                "id" : url.category.id,
                "name" : url.category.name
            },
            "tag" : collect_tags,
            "create_at" : url.create_at,
            "update_at" : url.update_at,
            "delete_at" : url.delete_at
        }
        return Response({"status" : True, "message" : "update url success", "data" : data_url}, status=status.HTTP_200_OK)
    
class DeleteUrl(APIView):
    def delete(self, request, url_id):
        payload = verify_jwt_token(request)
        if payload["status"] == False:
            return Response({"status" : False,"message": "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        user_id = payload["user_id"]
        try:
            url = Url.objects.get(id=url_id)
        except:
            return Response({"status" : False,"message": "url id isn't found"}, status=status.HTTP_400_BAD_REQUEST)
        if url.user_id != user_id:
            return Response({"status" : False,"message": "url id isn't found"}, status=status.HTTP_400_BAD_REQUEST)
        url.delete_at = datetime.now()
        url.save()
        UrlTag.objects.filter(url=url.id).delete()
        return Response({"status" : True, "message" : "delete url success"}, status=status.HTTP_200_OK)