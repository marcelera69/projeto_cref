from django import forms
from Courses.models import Course, Module

class CourseModelForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'start_date', 'end_date', 'teachers', 'tutors']
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Enter course description'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'teachers': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'tutors': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')

        if end_date and start_date and end_date < start_date:
            raise forms.ValidationError("A data de início não pode ser posterior à data de término.")

        return end_date

class ModuleModelForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Enter module description'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("O nome do módulo é obrigatório.")
        return name