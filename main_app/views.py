from django.http import HttpResponse
from django.shortcuts import render

from .models import Skill, Project, Task, Reflection

def home(request):
      return render(request, 'main_app/home.html')

def skills_list(request):
      return render(request, 'main_app/skills_list.html')

def projects_list(request):
      return render(request, 'main_app/projects_list.html')