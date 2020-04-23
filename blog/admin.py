from django.contrib import admin
from blog.models import Post, BlogComment

# Register your models here.
admin.site.register((Post, BlogComment))