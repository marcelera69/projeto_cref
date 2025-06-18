from django.db import models

# Create your models here.

#Classe de especialização para pessoas, que será herdada por Student e Teacher
class Person(models.Model):  
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
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

class Tutor(Person):
    def __str__(self):
        return self.name
    

class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    tutor = models.ForeignKey(Tutor, on_delete=models.PROTECT, related_name='tutors_groups', null=True, blank=False)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='courses', null=True, blank=False)
    
    class Meta:
        unique_together = ('name', 'course')

    def __str__(self):
        return self.name


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    teachers = models.ManyToManyField(Teacher, related_name='teacher_courses', blank=True)
    tutors = models.ManyToManyField(Tutor, related_name='teacher_courses', null=True, blank=True)
    students = models.ManyToManyField('Student', through='Enrollment', blank=True )

    def __str__(self):
        return self.name


class Module(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    number_classes = models.IntegerField(default=0, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    teachers = models.ManyToManyField(Teacher, related_name='teacher_modules', blank=True, null=True)


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Ativo'),
        ('approved', 'Aprovado'),
        ('failed', 'Reprovado'),
        ('locked', 'Trancado'),
        ('dropped', 'Evadido'),
    ]

    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='Enrollments_student')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='Enrollments_course')
    status = models.CharField(max_length=20, choices= STATUS_CHOICES, default='active')	

    def __str__(self):
        return f'{self.course}'
    