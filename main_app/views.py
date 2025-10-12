from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SkillForm, ProjectForm, TaskForm, ReflectionForm

from .models import Skill, Project, Task, Reflection

def home(request):
      if request.user.is_authenticated:
          skills = Skill.objects.filter(user=request.user)
          projects = Project.objects.filter(user=request.user)
           # calculate statistics
          total_skills = skills.count()
          total_projects = projects.count()

          # calculate overall progress
          if total_skills > 0:
              avg_skill_progress = sum([skill.calculate_progress() for skill in skills]) / total_skills
          else:
              avg_skill_progress = 0

          if total_projects > 0:
              avg_project_progress = sum([project.calculate_progress() for project in projects]) / total_projects
          else:
              avg_project_progress = 0

          # calculate task statistics
          all_tasks = Task.objects.filter(skill__user=request.user) | Task.objects.filter(project__user=request.user)
          total_tasks = all_tasks.count()
          completed_tasks = all_tasks.filter(is_completed=True).count()
          pending_tasks = total_tasks - completed_tasks

          # calculate completion rate
          if total_tasks > 0:
              completion_rate = round((completed_tasks / total_tasks) * 100, 1)
          else:
              completion_rate = 0

          # recent reflections
          recent_reflections = Reflection.objects.filter(
              skill__user=request.user
          ).union( 
              Reflection.objects.filter(project__user=request.user)
          ).order_by('-date')[:3]

          context = {
              'skills': skills[:3],  # show only first 3 for preview
              'projects': projects[:3],  # show only first 3 for preview
              'total_skills': total_skills,
              'total_projects': total_projects,
              'avg_skill_progress': round(avg_skill_progress, 1),
              'avg_project_progress': round(avg_project_progress, 1),
              'total_tasks': total_tasks,
              'completed_tasks': completed_tasks,
              'pending_tasks': pending_tasks,
              'completion_rate': completion_rate,
              'recent_reflections': recent_reflections,
          }
          return render(request, 'main_app/home.html', context)
      else:
            return render(request, 'main_app/home.html')

def skills_list(request):
      if request.user.is_authenticated:
            skills = Skill.objects.filter(user=request.user)
            # to refresh the progress for all the skills 
            for skill in skills:
                  skill.save()
            return render(request, 'main_app/skills_list.html', {'skills': skills})
      else:
            return redirect('main_app:login')

def projects_list(request):
      if request.user.is_authenticated:
            projects = Project.objects.filter(user=request.user)
            # to refresh the progress for all the projects 
            for project in projects:
                  project.save()
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
      

def skill_detail(request, skill_id):
      if request.user.is_authenticated:
          skill = Skill.objects.get(id=skill_id, user=request.user)
          skill.save()
          tasks = Task.objects.filter(skill=skill)
          reflections = Reflection.objects.filter(skill=skill).order_by('-date')
          return render(request, 'main_app/skill_detail.html', {'skill': skill, 'tasks': tasks,  'reflections': reflections})
      else:
          return redirect('main_app:login')
      

def project_detail(request, project_id):
      if request.user.is_authenticated:
          project = Project.objects.get(id=project_id, user=request.user)
          project.save()
          tasks = Task.objects.filter(project=project)
          reflections = Reflection.objects.filter(project=project).order_by('-date')
          return render(request, 'main_app/project_detail.html', {'project': project, 'tasks': tasks, 'reflections': reflections})
      else:
          return redirect('main_app:login')
      

def task_create_for_skill(request, skill_id):
      if request.user.is_authenticated:
          skill = Skill.objects.get(id=skill_id, user=request.user)
          if request.method == 'POST':
              form = TaskForm(request.POST)
              if form.is_valid():
                  task = form.save(commit=False)
                  task.skill = skill
                  task.save()
                  return redirect('main_app:skill_detail', skill_id=skill_id)
          else:
              form = TaskForm()
          return render(request, 'main_app/task_form.html', {'form': form, 'skill': skill, 'action': 'Add'})
      else:
          return redirect('main_app:login')
      

def task_create_for_project(request, project_id):
      if request.user.is_authenticated:
          project = Project.objects.get(id=project_id, user=request.user)
          if request.method == 'POST':
              form = TaskForm(request.POST)
              if form.is_valid():
                  task = form.save(commit=False)
                  task.project = project
                  task.save()
                  return redirect('main_app:project_detail', project_id=project_id)
          else:
              form = TaskForm()
          return render(request, 'main_app/task_form.html', {'form': form, 'project': project, 'action': 'Add'})
      else:
          return redirect('main_app:login')
      

def task_toggle(request, task_id):
      if request.user.is_authenticated:
          task = Task.objects.get(id=task_id)
          # make sure task belongs to user's skill or project
          if (task.skill and task.skill.user == request.user) or (task.project and task.project.user == request.user):
              task.is_completed = not task.is_completed
              task.save()

              # redirect back to the appropriate detail page
              if task.skill:
                  return redirect('main_app:skill_detail', skill_id=task.skill.id)
              elif task.project:
                  return redirect('main_app:project_detail', project_id=task.project.id)

          return redirect('main_app:home')
      else:
          return redirect('main_app:login')
      

def reflection_create_for_skill(request, skill_id):
      if request.user.is_authenticated:
          skill = Skill.objects.get(id=skill_id, user=request.user)
          if request.method == 'POST':
              form = ReflectionForm(request.POST)
              if form.is_valid():
                  reflection = form.save(commit=False)
                  reflection.skill = skill
                  reflection.save()
                  return redirect('main_app:skill_detail', skill_id=skill_id)
          else:
              form = ReflectionForm()
          return render(request, 'main_app/reflection_form.html', {'form': form, 'skill': skill, 'action': 'Add'})
      else:
          return redirect('main_app:login')
      

def reflection_create_for_project(request, project_id):
      if request.user.is_authenticated:
          project = Project.objects.get(id=project_id, user=request.user)
          if request.method == 'POST':
              form = ReflectionForm(request.POST)
              if form.is_valid():
                  reflection = form.save(commit=False)
                  reflection.project = project
                  reflection.save()
                  return redirect('main_app:project_detail', project_id=project_id)
          else:
              form = ReflectionForm()
          return render(request, 'main_app/reflection_form.html', {'form': form, 'project': project, 'action': 'Add'})
      else:
          return redirect('main_app:login')
      

def reflection_edit(request, reflection_id):
    if request.user.is_authenticated:
        reflection = Reflection.objects.get(id=reflection_id)
        # check if user owns this reflection through skill or project
        if (reflection.skill and reflection.skill.user == request.user) or (reflection.project and reflection.project.user == request.user):
            if request.method == 'POST':
                form = ReflectionForm(request.POST, instance=reflection)
                if form.is_valid():
                    form.save()
                    if reflection.skill:
                        return redirect('main_app:skill_detail', skill_id=reflection.skill.id)
                    elif reflection.project:
                        return redirect('main_app:project_detail', project_id=reflection.project.id)
            else:
                form = ReflectionForm(instance=reflection)
            return render(request, 'main_app/reflection_form.html', {'form': form, 'reflection': reflection, 'action': 'Edit'})

        return redirect('main_app:home')
    else:
        return redirect('main_app:login')

def reflection_delete(request, reflection_id):
      if request.user.is_authenticated:
          reflection = Reflection.objects.get(id=reflection_id)
          # check if user owns this reflection
          if (reflection.skill and reflection.skill.user == request.user) or (reflection.project and reflection.project.user == request.user):
              if request.method == 'POST':
                  skill_id = reflection.skill.id if reflection.skill else None
                  project_id = reflection.project.id if reflection.project else None
                  reflection.delete()

                  if skill_id:
                      return redirect('main_app:skill_detail', skill_id=skill_id)
                  elif project_id:
                      return redirect('main_app:project_detail', project_id=project_id)

              return render(request, 'main_app/reflection_confirm_delete.html', {'reflection': reflection})

          return redirect('main_app:home')
      else:
          return redirect('main_app:login')
      

def task_edit(request, task_id):
      if request.user.is_authenticated:
          task = Task.objects.get(id=task_id)
          # Check if user owns this task through skill or project
          if (task.skill and task.skill.user == request.user) or (task.project and task.project.user == request.user):
              if request.method == 'POST':
                  form = TaskForm(request.POST, instance=task)
                  if form.is_valid():
                      form.save()
                      if task.skill:
                          return redirect('main_app:skill_detail', skill_id=task.skill.id)
                      elif task.project:
                          return redirect('main_app:project_detail', project_id=task.project.id)
              else:
                  form = TaskForm(instance=task)
              return render(request, 'main_app/task_form.html', {'form': form, 'task': task, 'action': 'Edit'})

          return redirect('main_app:home')
      else:
          return redirect('main_app:login')


def task_delete(request, task_id):
      if request.user.is_authenticated:
          task = Task.objects.get(id=task_id)
          # Check if user owns this task
          if (task.skill and task.skill.user == request.user) or (task.project and task.project.user == request.user):
              if request.method == 'POST':
                  skill_id = task.skill.id if task.skill else None
                  project_id = task.project.id if task.project else None
                  task.delete()

                  if skill_id:
                      return redirect('main_app:skill_detail', skill_id=skill_id)
                  elif project_id:
                      return redirect('main_app:project_detail', project_id=project_id)

              return render(request, 'main_app/task_confirm_delete.html', {'task': task})

          return redirect('main_app:home')
      else:
          return redirect('main_app:login')