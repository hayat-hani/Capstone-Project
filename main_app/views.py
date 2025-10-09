from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Skill, Project, Task, Reflection

def home(request):
      return render(request, 'main_app/home.html')

def skills_list(request):
      return render(request, 'main_app/skills_list.html')

def projects_list(request):
      return render(request, 'main_app/projects_list.html')

def user_login(request):
      if request.method == 'POST':
          username = request.POST['username']
          password = request.POST['password']
          user = authenticate(request, username=username, password=password)        
          if user is not None:
              login(request, user)
              return redirect('main_app:home')
      return render(request, 'main_app/login.html')


def user_logout(request):
      logout(request)
      return redirect('main_app:home')