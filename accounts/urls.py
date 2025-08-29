from django.urls import path
from accounts.views import *

urlpatterns = [
    path('solicitar_registro/', registration_request_view, name='registration_request'),
    path('solicitar_registro/aprovar/', approve_registration_request_view, name='approve_registration_requests'),
    path('login/', login_view, name='login'),
    path('cadastro/',register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('trocar_senha/', PasswordChangeView.as_view(), name='password_change'), 
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        PasswordResetDoneView.as_view(),
        name='password_reset_complete'
    ),
]