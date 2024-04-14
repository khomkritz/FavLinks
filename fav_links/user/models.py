from django.db import models

# Create your models here.
class User(models.Model):
    class Meta:
        db_table = 'user'
    username = models.CharField(max_length=150,  unique=True)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    tel = models.CharField(max_length=9, null=True)
    email = models.CharField(max_length=55, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(null=True, blank=True)

class Token(models.Model):
    class Meta:
        db_table = 'token'
    user_id = models.IntegerField()
    access_token = models.TextField()
    refresh_token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)