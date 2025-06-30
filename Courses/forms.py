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
    
    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')

        if end_date and start_date and end_date < start_date:
            raise forms.ValidationError("A data de início não pode ser posterior à data de término.")
        
        return end_date
