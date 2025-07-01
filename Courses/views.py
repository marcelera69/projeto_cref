from django.shortcuts import render, redirect
from Courses.models import Course
from unidecode import unidecode
from Courses.forms import CourseModelForm
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from Courses.models import Enrollment
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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
    
class CourseDetailView(DetailView):
    model = Course
    template_name = 'course_detail.html'



@method_decorator(login_required(login_url='login'), name='dispatch')
class NewCourseView(CreateView):
    model = Course
    form_class = CourseModelForm
    template_name = 'new_course.html'
    success_url = '/cursos/'



@method_decorator(login_required(login_url='login'), name='dispatch')
class CourseupdateView(UpdateView):
    model = Course
    form_class = CourseModelForm
    template_name = 'course_update.html'
    success_url = '/cursos/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context['students'] = Enrollment.objects.filter(course=course).select_related('student', 'group')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            # Primeiro salva as alterações do curso
            form.save()

            # Em seguida, remove alunos se checkboxes estiverem marcados
            alunos_ids = request.POST.getlist('remover_alunos')
            if alunos_ids:
                Enrollment.objects.filter(course=self.object, student__id__in=alunos_ids).delete()

            return redirect(self.get_success_url())

        # Caso o formulário seja inválido
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
    
    def get_success_url(self):
        return reverse_lazy('course_detail', kwargs={'pk': self.object.pk})



@method_decorator(login_required(login_url='login'), name='dispatch')
class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'course_delete.html'
    success_url = '/cursos/'
