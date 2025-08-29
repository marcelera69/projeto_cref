from django.urls import path
from Courses.views import *

urlpatterns = [
    path('lista_cursos', CoursesListView.as_view(), name='courses_list'),
    path('novo_curso/', NewCourseView.as_view(), name='new_course'),
    path('cursos/<int:pk>/adicionar_aluno/', AddStudentsView.as_view(), name='course_add_student'),
    path('cursos/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('cursos/<int:pk>/editar/', CourseupdateView.as_view(), name='course_update'),
    path('cursos/<int:pk>/deletear/', CourseDeleteView.as_view(), name='course_delete'),
    path('dashboard/', course_dashboard_view, name='course_dashboard'),
    path('dashboard/course-graph/<int:pk>/', course_specific_graph, name='course_specific_graph'),
    path('cursos/<int:pk>/modulos/', course_module_view, name='course_modules'),
    path('cursos/<int:pk>/modulos/<int:module_pk>/', ModuleDetailView.as_view(), name='course_module_detail'),
]