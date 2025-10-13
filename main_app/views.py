from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .forms import SkillForm, ProjectForm, TaskForm, ReflectionForm, ProfileForm, CustomUserCreationForm
from .models import Skill, Project, Task, Reflection
from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

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

          # calculate project task statistics
          project_tasks = Task.objects.filter(project__user=request.user)
          total_project_tasks = project_tasks.count()
          completed_project_tasks = project_tasks.filter(is_completed=True).count()
          
          # calculate skill task statistics  
          skill_tasks = Task.objects.filter(skill__user=request.user)
          total_skill_tasks = skill_tasks.count()
          completed_skill_tasks = skill_tasks.filter(is_completed=True).count()
          
          # calculate overall task statistics (for backward compatibility)
          total_tasks = total_project_tasks + total_skill_tasks
          completed_tasks = completed_project_tasks + completed_skill_tasks
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
              # Project-specific statistics
              'total_project_tasks': total_project_tasks,
              'completed_project_tasks': completed_project_tasks,
              # Skill-specific statistics
              'total_skill_tasks': total_skill_tasks,
              'completed_skill_tasks': completed_skill_tasks,
          }
          return render(request, 'main_app/home.html', context)
      else:
            return render(request, 'main_app/home.html')

def skills_list(request):
      if request.user.is_authenticated:
            skills = Skill.objects.filter(user=request.user)
            # get search parameters
            search_query = request.GET.get('search', '')
            category_filter = request.GET.get('category', '')

            # apply search filter
            if search_query:
                skills = skills.filter(
                    models.Q(title__icontains=search_query) |
                    models.Q(description__icontains=search_query)
                )

            # apply category filter
            if category_filter:
                skills = skills.filter(category=category_filter)

            # get unique categories for filter dropdown
            categories = Skill.objects.filter(user=request.user).exclude(category__isnull=True).exclude(category='').values_list('category', flat=True).distinct()
                
            # to refresh the progress for all the skills 
            for skill in skills:
                  skill.save()
            context = {
              'skills': skills,
              'categories': categories,
              'search_query': search_query,
              'category_filter': category_filter,
            }
            return render(request, 'main_app/skills_list.html', context)
      else:
            return redirect('main_app:login')

def projects_list(request):
      if request.user.is_authenticated:
            projects = Project.objects.filter(user=request.user)
            # get search parameters
            search_query = request.GET.get('search', '')

            # apply search filter
            if search_query:
                projects = projects.filter(
                    models.Q(title__icontains=search_query) |
                    models.Q(description__icontains=search_query)
                )
            # to refresh the progress for all the projects 
            for project in projects:
                  project.save()
            context = {
              'projects': projects,
              'search_query': search_query,
            }
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
          form = CustomUserCreationForm(request.POST)
          if form.is_valid():
              user = form.save()
              login(request, user)
              return redirect('main_app:home')
      else:
          form = CustomUserCreationForm()
      return render(request, 'main_app/signup.html', {'form': form})


def skill_create(request):
      if request.user.is_authenticated:
          if request.method == 'POST':
              form = SkillForm(request.POST)
              if form.is_valid():
                  skill = form.save(commit=False)
                  skill.user = request.user
                  skill.save()
                  messages.success(request, f'Skill "{skill.title}" created successfully!')
                  return redirect('main_app:skills_list')
          else:
              form = SkillForm()
          return render(request, 'main_app/skill_form.html',{'form': form, 'action': 'Add'})
      else:
          return redirect('main_app:login')
      

def skill_edit(request, skill_id):
      if request.user.is_authenticated:
          skill = get_object_or_404(Skill, id=skill_id, user=request.user)
          if request.method == 'POST':
              form = SkillForm(request.POST, instance=skill)
              if form.is_valid():
                  form.save()
                  messages.success(request, f'Skill "{skill.title}" updated successfully!')
                  return redirect('main_app:skills_list')
          else:
              form = SkillForm(instance=skill)
          return render(request, 'main_app/skill_form.html',
  {'form': form, 'action': 'Edit', 'skill': skill})
      else:
          return redirect('main_app:login')

def skill_delete(request, skill_id):
      if request.user.is_authenticated:
          skill = get_object_or_404(Skill, id=skill_id, user=request.user)
          if request.method == 'POST':
              skill_title = skill.title
              skill.delete()
              messages.success(request, f'Skill "{skill_title}" deleted successfully!')
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
                  messages.success(request, f'Project "{project.title}" created successfully!')
                  return redirect('main_app:projects_list')
          else:
              form = ProjectForm()
          return render(request, 'main_app/project_form.html', {'form': form, 'action': 'Add'})
      else:
          return redirect('main_app:login')

def project_edit(request, project_id):
      if request.user.is_authenticated:
          project = get_object_or_404(Project, id=project_id, user=request.user)
          if request.method == 'POST':
              form = ProjectForm(request.POST, instance=project)
              if form.is_valid():
                  form.save()
                  messages.success(request, f'Project "{project.title}" updated successfully!')
                  return redirect('main_app:projects_list')
          else:
              form = ProjectForm(instance=project)
          return render(request, 'main_app/project_form.html', {'form': form, 'action': 'Edit', 'project': project})
      else:
          return redirect('main_app:login')

def project_delete(request, project_id):
      if request.user.is_authenticated:
          project = get_object_or_404(Project, id=project_id, user=request.user)
          if request.method == 'POST':
              project_title = project.title
              project.delete()
              messages.success(request, f'Project "{project_title}" deleted successfully!')
              return redirect('main_app:projects_list')
          return render(request, 'main_app/project_confirm_delete.html', {'project': project})
      else:
          return redirect('main_app:login')
      

def skill_detail(request, skill_id):
      if request.user.is_authenticated:
          skill = get_object_or_404(Skill, id=skill_id, user=request.user)
          skill.save()
          tasks = Task.objects.filter(skill=skill)
          reflections = Reflection.objects.filter(skill=skill).order_by('-date')
          return render(request, 'main_app/skill_detail.html', {'skill': skill, 'tasks': tasks,  'reflections': reflections})
      else:
          return redirect('main_app:login')
      

def project_detail(request, project_id):
      if request.user.is_authenticated:
          project = get_object_or_404(Project, id=project_id, user=request.user)
          project.save()
          tasks = Task.objects.filter(project=project)
          reflections = Reflection.objects.filter(project=project).order_by('-date')
          return render(request, 'main_app/project_detail.html', {'project': project, 'tasks': tasks, 'reflections': reflections})
      else:
          return redirect('main_app:login')
      

def task_create_for_skill(request, skill_id):
      if request.user.is_authenticated:
          skill = get_object_or_404(Skill, id=skill_id, user=request.user)
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
          project = get_object_or_404(Project, id=project_id, user=request.user)
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
          task = get_object_or_404(Task, id=task_id)
          # make sure task belongs to user's skill or project
          if (task.skill and task.skill.user == request.user) or (task.project and task.project.user == request.user):
              task.is_completed = not task.is_completed
              task.save()
              status = "completed" if task.is_completed else "marked as incomplete" 
              messages.success(request, f'Task "{task.title}" {status}!')

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
          skill = get_object_or_404(Skill, id=skill_id, user=request.user)
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
          project = get_object_or_404(Project, id=project_id, user=request.user)
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
        reflection = get_object_or_404(Reflection, id=reflection_id)
        # check if user owns this reflection through skill or project
        if (reflection.skill and reflection.skill.user == request.user) or (reflection.project and reflection.project.user == request.user):
            if request.method == 'POST':
                form = ReflectionForm(request.POST, instance=reflection)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Reflection updated successfully!')
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
          reflection = get_object_or_404(Reflection, id=reflection_id)
          # check if user owns this reflection
          if (reflection.skill and reflection.skill.user == request.user) or (reflection.project and reflection.project.user == request.user):
              if request.method == 'POST':
                  skill_id = reflection.skill.id if reflection.skill else None
                  project_id = reflection.project.id if reflection.project else None
                  reflection.delete()
                  messages.success(request, 'Reflection deleted successfully!')

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
          task = get_object_or_404(Task, id=task_id)
          # Check if user owns this task through skill or project
          if (task.skill and task.skill.user == request.user) or (task.project and task.project.user == request.user):
              if request.method == 'POST':
                  form = TaskForm(request.POST, instance=task)
                  if form.is_valid():
                      form.save()
                      messages.success(request, f'Task "{task.title}" updated successfully!')
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
          task = get_object_or_404(Task, id=task_id)
          # Check if user owns this task
          if (task.skill and task.skill.user == request.user) or (task.project and task.project.user == request.user):
              if request.method == 'POST':
                  skill_id = task.skill.id if task.skill else None
                  project_id = task.project.id if task.project else None
                  task_title = task.title
                  task.delete()
                  messages.success(request, f'Task "{task_title}" deleted successfully!')

                  if skill_id:
                      return redirect('main_app:skill_detail', skill_id=skill_id)
                  elif project_id:
                      return redirect('main_app:project_detail', project_id=project_id)

              return render(request, 'main_app/task_confirm_delete.html', {'task': task})

          return redirect('main_app:home')
      else:
          return redirect('main_app:login')
      

@login_required
def profile_view(request):
    user = request.user

    # get user statistics
    total_skills = user.skill_set.count()
    total_projects = user.project_set.count()
    total_tasks = Task.objects.filter(
        models.Q(skill__user=user) | models.Q(project__user=user)).count() 
    completed_tasks = Task.objects.filter(
        models.Q(skill__user=user) | models.Q(project__user=user), is_completed=True ).count()

    context = {
        'user': user,
        'total_skills': total_skills,
        'total_projects': total_projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
    }
    return render(request, 'main_app/profile.html', context)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('main_app:profile')
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'main_app/profile_edit.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('main_app:profile')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'main_app/change_password.html', {'form': form})


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('main_app:home')
    return render(request, 'main_app/delete_account.html')
