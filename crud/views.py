from django.shortcuts import redirect, render, get_object_or_404
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
# Create your views here.

@require_safe
def index(request):
    articles = Article.objects.all()
    context = {
        'articles' : articles,
    }
    return render(request, 'crud/index.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            return redirect('crud:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form' : form,
        'create' : True,
    }
    return render(request, 'crud/form.html', context)

@require_safe
def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comments = article.comment_set.all()
    form = CommentForm()
    context = {
        'article' : article,
        'comments' : comments,
        'form' : form,
    }
    return render(request, 'crud/detail.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('crud:detail', article.pk)
    else:
        form = ArticleForm(instance=article)
    context = {
        'form' : form,
        'update' : True,
    }
    return render(request, 'crud/form.html', context)


@require_POST
def delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user.is_authenticated:
        article.delete()
        return redirect('crud:index')
    return redirect('crud:detail', article.pk)

@require_POST
def comment_create(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.article = article
            comment.save()
        return redirect('crud:detail', article.pk)
    return redirect('accounts:login')


@require_POST
def comment_delete(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    return redirect('crud:detail', article_pk)

@require_POST
def article_likes(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if article.like_users.filter(pk=request.user.pk).exists():
        article.like_users.remove()
    else:
        article.like_users.add(request.user)
    return redirect('crud:detail', article_pk)

@require_POST
def comment_likes(request, article_pk, comment_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.like_users.filter(pk=request.user.pk).exist():
        comment.like_users.remove()
    else:
        comment.like_users.add(request.user)
    return redirect('crud:detail', article.pk)

def comment_dislikes(request, article_pk, comment_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.like_users.filter(pk=request.user.pk).exist():
        comment.like_users.remove()
    else:
        comment.like_users.add(request.user)
    return redirect('crud:detail', article.pk)