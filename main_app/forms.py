from django import forms
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
                  'placeholder': 'Share your thoughts, lessonslearned, or progress notes...'
              }),
          }
          labels = {
              'content': 'Your Reflection'
          }