from django.db import models

# Create your models here.
class Skill(models.Model):
    skill=models.CharField(max_length=60)
    experience=models.IntegerField()
    
    
    def __str__(self):
        return self.skill
class Profile(models.Model):
    username=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=60)
    skills=models.ForeignKey('Skill',on_delete=models.CASCADE)
    
    