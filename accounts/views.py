from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationRequestForm
import smtplib

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            '''
            Enviar email de notificação
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
            '''
            return redirect('login')
    else:
        user_form = UserCreationForm()

    return render(request, 'register.html', {'form': user_form})


def login_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('courses_list')
    else:
        login_form = AuthenticationForm()

    return render(request, 'login.html', {'form': login_form})


def logout_view(request):
    logout(request)
    return redirect('login')


def solicitar_registro(request):
    if request.method == 'POST':
        form = RegistrationRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses_list')
    else:
        form = RegistrationRequestForm()
    return render(request, 'solicitacao_registro.html', {'form': form})
