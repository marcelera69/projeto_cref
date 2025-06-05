from django.db import models

# Create your models here.

class Participante(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=50) 
    email = models.EmailField(max_length=100, unique=True)
    group = models.CharField(max_length=50)