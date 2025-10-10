from django import forms
from .models import Skill, Project

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