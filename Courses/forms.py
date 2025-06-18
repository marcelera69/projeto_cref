from django import forms
from Courses.models import Course

class CourseForm(forms.Form):
    name = forms.CharField(max_length=150)
    description = forms.TimeField(required=False, widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def save(self):
        course = Course(
            name= self.cleaned_data['name'],
            descripition=self.cleaned_data['descripition'],
            start_date=self.cleaned_data['start_date'],
            end_date=self.cleaned_data['end_date']
        )
        course.save()
        return course