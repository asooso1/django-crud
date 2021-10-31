from django.shortcuts import render, redirect
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required

# Create your views here.
@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'crud:index')
    else:
        form = AuthenticationForm(request)
    context = {
        'form' : form,
        'login' : True,
    }
    return render(request, 'accounts/form.html', context)

@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('crud:index')


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('crud:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form' : form,
        'signup' : True,
    }
    return render(request, 'accounts/form.html', context)


@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
    return redirect('crud:index')

@login_required
@require_http_methods(['GET', 'POST'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            auth_logout(request)
            return redirect('crud:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form' : form,
        'change_password' : True,
    }
    return render(request, 'accounts/form.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def change(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crud:index')
    else:
        form = CustomUserChangeForm()
    context = {
        'form' : form,
        'change' : True,
    }
    return render(request, 'accounts/form.html', context)