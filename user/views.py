from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.http import HttpResponse
def index(request):
    pass

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Вход выполнен')
                else:
                    return HttpResponse('Не верный пароль или логин')
            else:
                return render(request, 'user/loginWPS.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})
