from django.shortcuts import render


def index(request):

    return render(request, 'main/index.html')


def info(request):
    return render(request, 'main/info.html')


def contacts(request):
    return render(request, 'main/contacts.html')


def year_course(request):
    return render(request, 'main/year_course.html')

def summer_course(request):
    return render(request, 'main/summer_course.html')

