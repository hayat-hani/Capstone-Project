from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Skill(models.Model):
      title = models.CharField(max_length=255)
      description = models.TextField(blank=True, null=True)
      category = models.CharField(max_length=100, blank=True, null=True)
      progress = models.FloatField(default=0.0)
      user = models.ForeignKey(User, on_delete=models.CASCADE)

      def __str__(self):
          return self.title
    

class Project(models.Model):
      title = models.CharField(max_length=255)
      description = models.TextField(blank=True, null=True)
      progress = models.FloatField(default=0.0)
      user = models.ForeignKey(User, on_delete=models.CASCADE)

      def __str__(self):
          return self.title
      
class Task(models.Model):
      title = models.CharField(max_length=255)
      description = models.TextField(blank=True, null=True)
      is_completed = models.BooleanField(default=False)
      skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True, blank=True)
      project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)

      def __str__(self):
          return self.title
      

class Reflection(models.Model):
      content = models.TextField()
      date = models.DateTimeField(auto_now_add=True)
      skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True, blank=True)
      project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)

      def __str__(self):
          return f"Reflection on {self.date}"