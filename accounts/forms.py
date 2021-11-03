from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

class CustomUserChangeForm(UserChangeForm):
    profile_image = forms.ImageField(label='프로필사진(선택)', required=False)

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'last_name', 'first_name', 'profile_image')

class CustomUserCreationForm(UserCreationForm):
    profile_image = forms.ImageField(label='프로필사진(선택)', required=False)
    username = forms.CharField(min_length=6, max_length=16, label='ID', help_text='6자이상 16자이하의 ID를 입력해주세요')

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        # fields = UserCreationForm.Meta.fields + ( 'last_name', 'first_name', 'email', 'profile_image')
        fields = ('username', 'last_name', 'first_name', 'password1', 'password2',  'email', 'profile_image')
