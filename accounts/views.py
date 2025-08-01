from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import View, ListView, UpdateView
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationRequestForm
from django.core.mail import send_mail
from django.utils import timezone
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


from django.utils.timezone import localtime
def registration_request_view(request):
    if request.method == 'POST':
        form = RegistrationRequestForm(request.POST)
        if form.is_valid():
            form.save()
            #Enviar email de solicitação de cadastro
            sender = 'centrodereferencia.iff@gmail.com'
            recipient = 'ceeloalves.curso@gmail.com'
            message = f"""
            Olá,

            Uma nova solicitação de cadastro foi registrada no sistema.

            📌 Detalhes da solicitação:
            - Nome completo: {form.cleaned_data.get("name")}
            - Matrícula: {form.cleaned_data.get("registration")}
            - E-mail informado: {form.cleaned_data.get("email")}
            - Data/Hora da solicitação: {localtime(timezone.now()).strftime('%d/%m/%Y %H:%M')}

            Por favor, acesse o painel de administração para aprovar ou recusar esta solicitação.

            Atenciosamente,  
            Sistema de Controle de Evasão do CREF.
            """

            
            send_mail('Novo Cadastro Solicitado',
                      message,
                      sender,
                      [recipient],
                     )

            return redirect('courses_list')

    else:
        form = RegistrationRequestForm()
    return render(request, 'registration_request.html', {'form': form})


from .models import RegistrationRequest
from django.contrib import messages
def approve_registration_request_view(request):
    

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')

        if action == 'approve':
            registration_request = RegistrationRequest.objects.get(id=request_id)
            registration_request.is_approved = True
            registration_request.save()
            messages.success(request, f"Solicitação de {registration_request.name} aprovada.")
        else:
            registration_request = RegistrationRequest.objects.get(id=request_id)
            registration_request.is_rejected = True
            registration_request.save()
            messages.error(request, f"Solicitação de {registration_request.name} rejeitada.")

    requests_not_rejected = RegistrationRequest.objects.filter(is_approved=False, is_rejected=False).order_by('-created_at')
    return render(request, 'approve_registration_requests.html', {'registration_requests': requests_not_rejected})
