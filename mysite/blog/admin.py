from django.contrib import admin
from .models import Post

# Register your models here.

admin.site.register(Post)

# Create your models here.
# class Post(models.Model):
#    title = models.CharField(max_length=200)
#   content = models.TextField()