from django.db import models

# Create your models here.

#Classe de especialização para pessoas, que será herdada por Student e Teacher
class Person(models.Model):  
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    phone = models.CharField(max_length=15, blank=True, null=True)
    registration = models.CharField(max_length=12, unique=True, blank=True, null=True)

    class Meta:
        abstract = True  # ✅ Isso evita que Django crie uma tabela para Person

class Student(Person):
    def __str__(self):
        return self.name

class Teacher(Person):
    def __str__(self):
        return self.name
    

class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    tutor = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name='Tutors')
    course = models.ForeignKey('Course', on_delete=models.PROTECT, related_name='Course')
    
    def __str__(self):
        return self.name


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    teachers = models.ManyToManyField(Teacher, related_name='Courses', blank=True, null=True)
    students = models.ManyToManyField('Student', through='Enrollment', blank=True, null=True)

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Ativo'),
        ('cancelled', 'Cancelado'),
        ('completed', 'Concluído'),
    ]

    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='Enrollments_student')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='Enrollments_course')
    status = models.CharField(max_length=20, choices= STATUS_CHOICES, default='active')	

    def __str__(self):
        return self.student.name + ' - ' + self.course.name
    