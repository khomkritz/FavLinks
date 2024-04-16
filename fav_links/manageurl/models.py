from django.db import models

# Create your models here.
class Category(models.Model):
    class Meta:
        db_table = 'category'
    name = models.CharField(max_length=150)
    user_id = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(null=True, blank=True)

class Tag(models.Model):
    class Meta:
        db_table = 'tag'
    name = models.CharField(max_length=150)
    user_id = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(null=True, blank=True)

class Url(models.Model):
    class Meta:
        db_table = 'url'
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=255)
    link = models.CharField(max_length=150)
    user_id = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.IntegerField(default=1) #1 in process , 2 approve , 3 reject , 4 delete
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(null=True, blank=True)

class UrlTag(models.Model):
    class Meta:
        db_table = 'url_tag'
    url = models.ForeignKey(Url, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(null=True, blank=True)

class LogError(models.Model):
    class Meta:
        db_table = 'log_error'
    method = models.CharField(max_length=15)
    path = models.CharField(max_length=150)
    data = models.CharField(max_length=225)
    create_at = models.DateTimeField(auto_now_add=True)