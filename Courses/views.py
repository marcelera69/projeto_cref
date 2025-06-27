from django.shortcuts import render
from Courses.models import Course
from unidecode import unidecode
from Courses.forms import CourseModelForm
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

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
    
    
class NewCourseView(View):

    def get(self, request):
        # Exibe o formulário vazio
        new_course_form = CourseModelForm()
        return render(request, 'new_course.html', {'form': new_course_form})
    
    def post(self, request):
        new_course_form = CourseModelForm(request.POST)
        if new_course_form.is_valid():
            new_course_form.save()
            return redirect('courses_list')
        else:
            # Se o formulário não for válido, exibe novamente com erros
            return render(request, 'new_course.html', {'form': new_course_form})


