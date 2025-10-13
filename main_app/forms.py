from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Skill, Project, Task, Reflection

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['title', 'description', 'category']
        widgets = {'description': forms.Textarea(attrs={'rows': 4}),
                   }


class ProjectForm(forms.ModelForm):
      class Meta:
          model = Project
          fields = ['title', 'description']
          widgets = {
              'description': forms.Textarea(attrs={'rows': 4}),
            }
          
class TaskForm(forms.ModelForm):
      class Meta:
          model = Task
          fields = ['title', 'description']
          widgets = {
              'description': forms.Textarea(attrs={'rows': 3}),
          }

class ReflectionForm(forms.ModelForm):
      class Meta:
          model = Reflection
          fields = ['content']
          widgets = {
              'content': forms.Textarea(attrs={
                  'rows': 5,
                  'placeholder': 'Share your thoughts, lessons learned, or progress notes...'
              }),
          }
          labels = {
              'content': 'Your Reflection'
          }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user