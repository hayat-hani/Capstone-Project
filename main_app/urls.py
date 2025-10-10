from django.urls import path
from . import views

app_name = 'main_app'
urlpatterns = [
    path('', views.home, name='home'),
    path('skills/', views.skills_list, name='skills_list'),    
    path('projects/', views.projects_list, name='projects_list'),
    path('login/', views.user_login, name='login'),  
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name='signup'),
    path('skills/add/', views.skill_create, name='skill_create'),
    path('skills/<int:skill_id>/edit/', views.skill_edit, name='skill_edit'),
    path('skills/<int:skill_id>/delete/', views.skill_delete, name='skill_delete'),
    path('projects/add/', views.project_create, name='project_create'),
    path('projects/<int:project_id>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:project_id>/delete/', views.project_delete, name='project_delete'),
    path('skills/<int:skill_id>/', views.skill_detail, name='skill_detail'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('skills/<int:skill_id>/add_task/', views.task_create_for_skill, name='task_create_for_skill'),
    path('projects/<int:project_id>/add_task/', views.task_create_for_project, name='task_create_for_project'),
    path('tasks/<int:task_id>/toggle/', views.task_toggle, name='task_toggle'),
]