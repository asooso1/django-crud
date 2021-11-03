from django import forms
from django.forms import widgets
from .models import Article, Comment

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'content', 'image',)
        # fields = '__all__'

class CommentForm(forms.ModelForm):
    content = forms.CharField(max_length=200, label="내용")
    class Meta:
        model = Comment
        fields = ('content', )