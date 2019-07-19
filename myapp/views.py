from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def index(request):
    # если мы залогинены
    if request.user.is_authenticated:
        return render(request, "index.html")
    else:
        return redirect('/login')


def login_page(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('login', '')
        password = request.POST.get('password', '')

        if username == '' or password == '':
            return HttpResponse("Заполните все поля")

        # проверяем правильность логина и пароля
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return HttpResponse("Логин неверен")


def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'register.html')
    if request.method == 'POST':
        username = request.POST.get('login', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')

        if username == '' or password == '' or email == '':
            return HttpResponse("Заполните все поля")

        if User.objects.filter(username=username).exists():
            return HttpResponse("Логин занят")

        # создаем пользователя
        user = User.objects.create_user(username, email, password)
        user.save()

        # "входим" пользователя
        login(request, user)

        return redirect('/')

def logout_page(request):
    if request.method == 'POST':
        logout(request)
    return redirect('/login')
