from django import forms
from Courses.models import Course
    
class CourseModelForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'start_date', 'end_date']
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Enter course description'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }