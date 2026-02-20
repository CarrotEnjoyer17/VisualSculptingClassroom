from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
# Create your views here.

def index(request):
    context = {
        'title': 'VisualSculptingClassroom',
    }
    return render(request, 'users/index.html', context)

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username = username, password = password)
            if user:
                auth.login(request,user)
                return HttpResponseRedirect(reverse('classrooms:classrooms_list'))
    else:
        form = UserLoginForm()
    context = {
        'title': 'Вход',
        'form': form,
    }
    return render(request, 'users/login.html', context)
def registration(request):
    if request.method == 'POST':
        i_d = {'last_name':'ddd'}
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Поздравляем! Вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {
        'form' : form,
        'title': 'Регистрация'
    }
    return render(request, 'users/registration.html', context)
@login_required

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

def profile(request, user_id):
    if request.method == "POST":
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)


    context ={
        'title':'Профиль',
        'form':form,
        'user': request.user
    }
    return render(request, 'users/profile.html', context)