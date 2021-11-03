from django.contrib import admin

from crud.models import Article, Comment

# Register your models here.
admin.site.register(Article)
admin.site.register(Comment)