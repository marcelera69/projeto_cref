"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Courses.views import *
from accounts.views import register_view, login_view, logout_view, registration_request_view, approve_registration_request_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cursos/', CoursesListView.as_view(), name='courses_list'),
    path('novo_curso/', NewCourseView.as_view(), name='new_course'),
    path('cursos/<int:pk>/adicionar_aluno/', AddStudentsView.as_view(), name='course_add_student'),
    path('cursos/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('cursos/<int:pk>/editar/', CourseupdateView.as_view(), name='course_update'),
    path('cursos/<int:pk>/deletear/', CourseDeleteView.as_view(), name='course_delete'),
    path('cadastro/',register_view, name='register'),
    path('solicitar_registro/', registration_request_view, name='registration_request'),
    path('solicitar_registro/aprovar/', approve_registration_request_view, name='approve_registration_requests'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', course_dashboard_view, name='course_dashboard'),
    path('cursos/<int:pk>/modulos/', course_module_view, name='course_modules'),
    path('cursos/<int:pk>/modulos/<int:module_pk>/', ModuleDetailView.as_view(), name='course_module_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
