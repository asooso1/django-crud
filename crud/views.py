from django.shortcuts import redirect, render, get_object_or_404
from django.http.response import HttpResponse, JsonResponse
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.

@require_safe
def index(request):
    articles = Article.objects.order_by('-pk')
    paginator = Paginator(articles, 10)

    page_number = request.GET.get('page') or 1
    if int(page_number) > articles.count()//5+1:
        page_number = articles.count()//5+1
    page_obj = paginator.get_page(page_number)
    
    context = {
        'articles' : articles,
        'page_obj' : page_obj,
        'page_number' : page_number,
    }
    return render(request, 'crud/index.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
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
        form = ArticleForm(request.POST, request.FILES, instance=article)
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
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('crud:detail', article_pk)

@require_POST
def article_likes(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        if article.like_users.filter(pk=request.user.pk).exists():
            article.like_users.remove(request.user)
            liked = True
        else:
            article.like_users.add(request.user)
            liked = False
        # return redirect('crud:detail', article_pk)
        return JsonResponse({'liked':liked, 'count':article.like_users.count()})
    # return redirect('accounts:login')
    return HttpResponse(status=401)

@require_POST
def comment_likes(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.like_users.filter(pk=request.user.pk).exists():
            comment.like_users.remove(request.user)
            commentliked = True
        else:
            comment.like_users.add(request.user)
            commentliked = False
        # return redirect('crud:detail', article.pk)
        return JsonResponse({'commentliked':commentliked, 'count':comment.like_users.count()})
    # return redirect('accounts:login')
    return HttpResponse(status=401)

@require_POST
def comment_dislikes(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.dislike_users.filter(pk=request.user.pk).exists():
            comment.dislike_users.remove(request.user)
            commentdisliked = True
        else:
            comment.dislike_users.add(request.user)
            commentdisliked = False
        # return redirect('crud:detail', article.pk)
        return JsonResponse({'commentdisliked':commentdisliked, 'count':comment.dislike_users.count()})
    # return redirect('accounts:login')
    return HttpResponse(status=401)