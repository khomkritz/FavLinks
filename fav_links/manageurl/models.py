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
    tag_id = models.ManyToManyField(Tag)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(null=True, blank=True)