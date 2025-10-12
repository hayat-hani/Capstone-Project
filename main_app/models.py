from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):
      title = models.CharField(max_length=255)
      description = models.TextField(blank=True, null=True)
      category = models.CharField(max_length=100, blank=True, null=True)
      progress = models.FloatField(default=0.0)
      user = models.ForeignKey(User, on_delete=models.CASCADE)

      def __str__(self):
          return self.title
      
      def calculate_progress(self):
        tasks = self.task_set.all()
        if tasks.count() == 0:
            return 0.0
        completed_tasks = tasks.filter(is_completed=True).count()
        return round((completed_tasks / tasks.count()) * 100, 1)

      def save(self, *args, **kwargs):
        update_progress = kwargs.pop('update_progress', False)
        if not update_progress:
          super().save(*args, **kwargs)
          self.progress = self.calculate_progress()
          super().save(update_fields=['progress'])
        else:
          super().save(*args, **kwargs)
    

class Project(models.Model):
      title = models.CharField(max_length=255)
      description = models.TextField(blank=True, null=True)
      progress = models.FloatField(default=0.0)
      user = models.ForeignKey(User, on_delete=models.CASCADE)

      def __str__(self):
          return self.title
      
      def calculate_progress(self):
        tasks = self.task_set.all()
        if tasks.count() == 0:
            return 0.0
        completed_tasks = tasks.filter(is_completed=True).count()
        return round((completed_tasks / tasks.count()) * 100, 1)
      
      def save(self, *args, **kwargs):
        update_progress = kwargs.pop('update_progress', False)
        if not update_progress:
          super().save(*args, **kwargs)
          self.progress = self.calculate_progress()
          super().save(update_fields=['progress'])
        else:
          super().save(*args, **kwargs)


class Task(models.Model):
      title = models.CharField(max_length=255)
      description = models.TextField(blank=True, null=True)
      is_completed = models.BooleanField(default=False)
      skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True, blank=True)
      project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)

      def __str__(self):
          return self.title
      
      def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # update progress for parent skill or project
        if self.skill:
            self.skill.save(update_progress=True)
        elif self.project:
            self.project.save(update_progress=True)
        

class Reflection(models.Model):
      content = models.TextField()
      date = models.DateTimeField(auto_now_add=True)
      skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True, blank=True)
      project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)

      def __str__(self):
          return f"Reflection on {self.date}"
      

