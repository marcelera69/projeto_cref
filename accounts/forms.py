from django import forms
from .models import RegistrationRequest
from datetime import datetime, timedelta

class RegistrationRequestForm(forms.ModelForm):
    class Meta:
        model = RegistrationRequest
        fields = ['name', 'email', 'registration']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Digite seu nome'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Digite seu email'}),
            'registration': forms.NumberInput(attrs={'placeholder': 'Digite seu número de matrícula'}),
        }

    def clean_registration(self):
        registration = self.cleaned_data.get('registration')
        created_date = self.cleaned_data.get('created_at')

        #Pega o limite de um dia
        limite = datetime.now() - timedelta(days=1)
        # Verifica se já existe uma requisição com o mesmo número de matrícula nos últimos 24 horas
        if RegistrationRequest.objects.filter(
            registration=registration, 
            created_at__gte=limite
        ).exists():
            raise forms.ValidationError("Você já fez uma requisição nas últimas 24 horas com este número de matrícula.")

        if registration and not registration.isdigit():
            raise forms.ValidationError("O número de matrícula deve conter apenas dígitos.")
        
        if registration and len(str(registration)) > 12:
            raise forms.ValidationError("O número de matrícula não pode ter mais de 12 dígitos.")

        return registration
    
