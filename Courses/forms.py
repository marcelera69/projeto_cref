from django import forms
from Courses.models import Student, Teacher, Tutor

class CourseForm(forms.Form):
    name = forms.CharField(max_length=150)
    descripition = forms.Textarea()
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    teachers = forms.ModelChoiceField(queryset=Teacher.objects.all())
    tutors = forms.ModelChoiceField(queryset=Tutor.objects.all())
    student = forms.ModelChoiceField(queryset=Student.objects.all())
