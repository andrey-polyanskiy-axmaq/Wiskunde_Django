from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser
from .models import Themes

class ThemeFilterForm(forms.Form):
    theme = forms.ModelChoiceField(
        queryset=Themes.objects.all(),
        required=False,
        label='Тема',
        empty_label="Нет темы"
    )

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileEditForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'birth_date')

class LessonFeedbackForm(forms.Form):
    file = forms.FileField(label='Прикрепить файл с домашним заданием')

