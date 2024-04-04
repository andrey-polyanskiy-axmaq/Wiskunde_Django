from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm

def logout_CustomUser(request):
    logout(request)
    return redirect('home')

def index(request):
    context = {
        'username': request.CustomUser.CustomUsername,
        'first_name': request.CustomUser.first_name,
        'last_name': request.CustomUser.last_name,
        'email': request.CustomUser.email,
        'date_joined': request.CustomUser.date_joined,
        'last_login': request.CustomUser.last_login,
    }
    return render(request, 'CustomUser/index.html', context)

def CustomUser_login(request):
    if request.CustomUser.is_authenticated:
        return redirect('CustomUserinfo')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            CustomUser = authenticate(CustomUsername=cd['CustomUsername'], password=cd['password'])
            if CustomUser is not None:
                if CustomUser.is_active:
                    login(request, CustomUser)
                    if request.CustomUser.is_superCustomUser:
                        return redirect('/admin/')
                    else:
                        return redirect('CustomUserinfo')
                else:
                    return render(request, 'CustomUser/loginWPS.html', {'form': form})
            else:
                return render(request, 'CustomUser/loginWPS.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'CustomUser/login.html', {'form': form})
