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
]