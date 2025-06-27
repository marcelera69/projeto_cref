from django.shortcuts import render
from Courses.models import Course
from unidecode import unidecode
from Courses.forms import CourseModelForm
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

class CoursesListView(ListView):
    model = Course
    template_name = 'courses.html'
    context_object_name = 'courses'
    
    def get_queryset(self):
        search = self.request.GET.get('search', '')
        search_normalized = unidecode(search.strip().lower())

        if search_normalized:
            # Filtra manualmente, sem depender do banco
            courses = [
                course for course in Course.objects.all() if search_normalized in unidecode(course.name.lower())
            ]
        else:
            courses = Course.objects.all().order_by('name')

        return courses
    
    
class NewCourseView(CreateView):
    model = Course
    form_class = CourseModelForm
    template_name = 'new_course.html'
    success_url = '/cursos/'



