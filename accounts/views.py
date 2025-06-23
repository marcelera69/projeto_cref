from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
import smtplib

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            sender = 'centrodereferencia.iff@gmail.com'
            recipient = 'ceeloalves.curso@gmail.com'
            message = f'Novo cadastro solicitado:\nUsuario: {user_form.cleaned_data["username"]}\nSenha: {user_form.cleaned_data["password1"]}'

            servidor_email = smtplib.SMTP('smtp.gmail.com', 587)
            servidor_email.starttls()
            servidor_email.login('centrodereferencia.iff@gmail.com', 'bdgp aern bmbj qgiv')
            servidor_email.sendmail(
                sender,
                [recipient],
                message
            )
            return redirect('courses_list')
        
    user_form = UserCreationForm()
    return render(request, 'register.html', {'form': user_form})