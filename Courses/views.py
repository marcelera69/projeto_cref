from django.shortcuts import render, redirect
from Courses.models import Course
from unidecode import unidecode
from Courses.forms import CourseModelForm
from django.shortcuts import redirect, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from Courses.models import *
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()

        # Todos os enrollments relacionados ao curso, com student e group
        enrollments = Enrollment.objects.filter(course=course).select_related('student__group')

        # Contar quantos alunos não têm grupo associado
        context['students_without_group_count'] = enrollments.filter(group__isnull=True).count()

        return context



@method_decorator(login_required(login_url='login'), name='dispatch')
class NewCourseView(CreateView):
    model = Course
    form_class = CourseModelForm
    template_name = 'new_course.html'

    def get_success_url(self):
        return reverse_lazy('course_add_student', kwargs={'pk': self.object.pk})



@method_decorator(login_required(login_url='login'), name='dispatch')
class AddStudentsView(View):
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        
        # Base: alunos ainda não matriculados no curso
        students = Student.objects.exclude(
            Enrollments_student__course=course
        )

        # 🔍 Filtro por nome ou matrícula, se houver busca
        query = request.GET.get('q')
        if query:
            students = students.filter(
                Q(name__icontains=query) | Q(registration__icontains=query)
            )

        return render(request, 'course_add_students.html', {
            'course': course,
            'students': students,
        })

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        alunos_ids = request.POST.getlist('alunos')
        for aluno_id in alunos_ids:
            Enrollment.objects.create(course=course, student_id=aluno_id)
        return redirect('course_detail', pk=course.pk)



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



@login_required(login_url='login')
def course_dashboard_view(request):
    total_courses = Course.objects.count()
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_tutors = Tutor.objects.count()
    context = {
        'total_courses': total_courses,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_tutors': total_tutors,
    }
    return render(request, 'course_dashboard.html', context)

    