from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm

def logout_user(request):
    logout(request)
    return redirect('home')

def index(request):
    context = {
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'date_joined': request.user.date_joined,
        'last_login': request.user.last_login,
    }
    return render(request, 'user/index.html', context)

def user_login(request):
    if request.user.is_authenticated:
        return redirect('userinfo')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if request.user.is_superuser:
                        return redirect('/admin/')
                    else:
                        return redirect('userinfo')
                else:
                    return render(request, 'user/loginWPS.html', {'form': form})
            else:
                return render(request, 'user/loginWPS.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})
