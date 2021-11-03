from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)    # 제목
    content = models.TextField()    # 내용
    created_at = models.DateTimeField(auto_now_add=True)    # 생성시간
    updated_at = models.DateTimeField(auto_now=True)    # 수정시간
    image = models.ImageField(upload_to='origins/', blank=True, null=True)
    image_thumbnail = ImageSpecField(
        source='image',
        processors = [ResizeToFill(120, 120)],
        format='JPEG',
        options={'quality': 95},
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    # 작성유저
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_articles") # 게시글좋아요


    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.CharField(max_length=200)    # 내용
    created_at = models.DateTimeField(auto_now_add=True)    # 생성시간
    updated_at = models.DateTimeField(auto_now=True)    # 수정시간
    article = models.ForeignKey(Article, on_delete=models.CASCADE)  # 게시글
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    # 작성자
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_comments") # 댓글좋아요
    dislike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dislike_comments')   # 댓글 싫어요

    def __str__(self):
        return self.content
