from django.db import models

# Create your models here.

class Participant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=50) 
    email = models.EmailField(max_length=100, unique=True)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='participant')

class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    tutor = models.CharField(max_length=100)
