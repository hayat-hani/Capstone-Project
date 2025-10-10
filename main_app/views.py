from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SkillForm, ProjectForm

from .models import Skill, Project, Task, Reflection

def home(request):
      if request.user.is_authenticated:
          skills = Skill.objects.filter(user=request.user)
          projects = Project.objects.filter(user=request.user)
          return render(request, 'main_app/home.html', {'skills': skills, 'projects': projects})
      else:
            return render(request, 'main_app/home.html')

def skills_list(request):
      if request.user.is_authenticated:
            skills = Skill.objects.filter(user=request.user)
            return render(request, 'main_app/skills_list.html', {'skills': skills})
      else:
            return redirect('main_app:login')

def projects_list(request):
      if request.user.is_authenticated:
            projects = Project.objects.filter(user=request.user)
            return render(request, 'main_app/projects_list.html', {'projects': projects})
      else:
            return redirect('main_app:login')

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


def user_signup(request):
      if request.method == 'POST':
          form = UserCreationForm(request.POST)
          if form.is_valid():
              user = form.save()
              login(request, user)
              return redirect('main_app:home')
      else:
          form = UserCreationForm()
      return render(request, 'main_app/signup.html', {'form': form})


def skill_create(request):
      if request.user.is_authenticated:
          if request.method == 'POST':
              form = SkillForm(request.POST)
              if form.is_valid():
                  skill = form.save(commit=False)
                  skill.user = request.user
                  skill.save()
                  return redirect('main_app:skills_list')
          else:
              form = SkillForm()
          return render(request, 'main_app/skill_form.html',{'form': form, 'action': 'Add'})
      else:
          return redirect('main_app:login')
      

def skill_edit(request, skill_id):
      if request.user.is_authenticated:
          skill = Skill.objects.get(id=skill_id, user=request.user)
          if request.method == 'POST':
              form = SkillForm(request.POST, instance=skill)
              if form.is_valid():
                  form.save()
                  return redirect('main_app:skills_list')
          else:
              form = SkillForm(instance=skill)
          return render(request, 'main_app/skill_form.html',
  {'form': form, 'action': 'Edit'})
      else:
          return redirect('main_app:login')

def skill_delete(request, skill_id):
      if request.user.is_authenticated:
          skill = Skill.objects.get(id=skill_id, user=request.user)
          if request.method == 'POST':
              skill.delete()
              return redirect('main_app:skills_list')
          return render(request, 'main_app/skill_confirm_delete.html', {'skill': skill})
      else:
          return redirect('main_app:login')
      

def project_create(request):
      if request.user.is_authenticated:
          if request.method == 'POST':
              form = ProjectForm(request.POST)
              if form.is_valid():
                  project = form.save(commit=False)
                  project.user = request.user
                  project.save()
                  return redirect('main_app:projects_list')
          else:
              form = ProjectForm()
          return render(request, 'main_app/project_form.html', {'form': form, 'action': 'Add'})
      else:
          return redirect('main_app:login')

def project_edit(request, project_id):
      if request.user.is_authenticated:
          project = Project.objects.get(id=project_id, user=request.user)
          if request.method == 'POST':
              form = ProjectForm(request.POST, instance=project)
              if form.is_valid():
                  form.save()
                  return redirect('main_app:projects_list')
          else:
              form = ProjectForm(instance=project)
          return render(request, 'main_app/project_form.html', {'form': form, 'action': 'Edit'})
      else:
          return redirect('main_app:login')

def project_delete(request, project_id):
      if request.user.is_authenticated:
          project = Project.objects.get(id=project_id, user=request.user)
          if request.method == 'POST':
              project.delete()
              return redirect('main_app:projects_list')
          return render(request, 'main_app/project_confirm_delete.html', {'project': project})
      else:
          return redirect('main_app:login')