from django import forms
from .models import Skill

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['title', 'description', 'category']
        widgets = {'description': forms.Textarea(attrs={'rows': 4}),}