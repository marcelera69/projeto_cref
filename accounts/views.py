from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from .forms import RegistrationRequestForm
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.timezone import localtime
from django.contrib.auth.decorators import user_passes_test



# Função que verifica se o usuário é superusuário
def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def register_view(request):
    
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('login')
    else:
        user_form = UserCreationForm()

    return render(request, 'register.html', {'form': user_form})


def login_view(request):
    if not request.user.is_anonymous:
        return redirect('courses_list')
    
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

class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'password_change.html'
    success_url = '/cursos/lista_cursos'

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
            Sistema de Controle de Matrículas na EAD do Centro de Referência em Tecnologia, Informação e Comunicação na Educação.
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
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse

@user_passes_test(is_superuser)
def approve_registration_request_view(request):

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')

        if action == 'approve':
            registration_request = RegistrationRequest.objects.get(id=request_id)
            registration_request.is_approved = True
            registration_request.save()

            # Gerar senha aleatória para o usuário
            random_password = get_random_string(length=10)

            # Criar usuário com os dados da solicitação
            new_user = User.objects.create_user(
                username=registration_request.registration,
                email=registration_request.email,
                password=random_password
            )

            # Gerar token e uid para o NOVO usuário
            uid = urlsafe_base64_encode(force_bytes(new_user.pk))
            token = default_token_generator.make_token(new_user)


            # Montar URL absoluta
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )

            # Enviar email de aprovação
            sender = 'centrodereferencia.iff@gmail.com'
            recipient = registration_request.email
            message = f"""
            Olá {registration_request.name},

            Sua solicitação de cadastro foi aprovada com sucesso!

            📌 Detalhes do cadastro:
            - Login: {registration_request.registration}
            - Senha: {random_password}

            Por favor, faça login em nossa plataforma usando suas credenciais ou clique no link abaixo para definir sua senha:
            {reset_url}.

            Atenciosamente,
            Sistema de Controle de Evasão do CREF.
            """

            send_mail('Cadastro Aprovado',
                      message,
                      sender,
                      [recipient],
                     )

            messages.success(request, f"Solicitação de {registration_request.name} aprovada.")
            
        else:
            registration_request = RegistrationRequest.objects.get(id=request_id)
            registration_request.is_rejected = True
            registration_request.save()
            messages.error(request, f"Solicitação de {registration_request.name} rejeitada.")

    requests_not_rejected = RegistrationRequest.objects.filter(is_approved=False, is_rejected=False).order_by('-created_at')
    return render(request, 'approve_registration_requests.html', {'registration_requests': requests_not_rejected})
