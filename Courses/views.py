from django.shortcuts import render, redirect
from unidecode import unidecode
from django.shortcuts import redirect, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Course

#Importações de modelos e formulários dos meus próprios arquivos
from Courses.models import *
from Courses.forms import CourseModelForm, ModuleModelForm

#Importações necessárias Para o dashboard
from plotly.offline import plot
import plotly.graph_objects as go

@method_decorator(login_required(login_url='login'), name='dispatch')
class CoursesListView(LoginRequiredMixin, ListView):
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
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class CourseDetailView(LoginRequiredMixin, DetailView):
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
    success_url = '/cursos/lista_cursos/'


def graph_average_students_per_course():
    #Pegar dados ordenados da CourseInventory
    data = CourseInventory.objects.all().order_by('-created_at')

    #separer em listas para o campo x e y
    if not data:
        # Se não houver dados, retornar gráfico vazio
        return plot(go.Figure(), output_type='div', include_plotlyjs=False)
    else:
        dates = []
        averages = []
        for item in data:
            dates.append(item.created_at.strftime('%Y-%m-%d'))
            averages.append(item.average_students_per_course)

    # Criar o gráfico
    fig = go.Figure(data=go.Scatter(x=dates, y=averages, mode='markers+lines'))
    fig.update_layout(title='',
                      xaxis_title='Data',
                      yaxis_title='Média de Alunos',
                        xaxis=dict(tickangle=-45),
                        yaxis=dict(tickformat='d'),  # força a exibir números inteiros no eixo y
                        margin=dict(l=40, r=40, t=50, b=100)
                      )
    
    grafico_html = plot(fig, output_type='div', include_plotlyjs=False)
    
    return grafico_html

from django.db.models.functions import TruncDate

def grafico_barras_agrupadas():
    cursos = Course.objects.all()

    datas = (
        HistoryAmountStudents.objects
        .annotate(date_only=TruncDate('date'))
        .values('date_only')
        .distinct()
        .order_by('-date_only')[:2]
    )
    datas = sorted([d['date_only'] for d in datas])

    data_por_curso = {curso.name: {} for curso in cursos}

    for curso in cursos:
        for data in datas:
            obj = HistoryAmountStudents.objects.filter(
                course=curso,
                date__date=data
            ).first()
            data_por_curso[curso.name][data] = obj.amount_students if obj else 0

    cursos_nomes = [curso.name for curso in cursos]
    alunos_data1 = [data_por_curso[curso][datas[0]] for curso in cursos_nomes]
    alunos_data2 = [data_por_curso[curso][datas[1]] for curso in cursos_nomes]


    import re
    cursos_abreviados = []
    for curso in cursos_nomes:
        # Extrai o campus
        campus_match = re.search(r'\(Campus (.*?)\)', curso)
        cidade = campus_match.group(1) if campus_match else ""

        # Remove tudo antes de "em" ou "na"
        match = re.search(r'\b(?:em|na)\s+(.*)', curso, flags=re.IGNORECASE)
        if match:
            conteudo = match.group(1).strip()
        else:
            conteudo = curso  # fallback

        # Pega os primeiros `limite` caracteres do conteúdo
        truncado = conteudo[:15] + "..."

        curso = f"{truncado} ({cidade})" if cidade else truncado
        cursos_abreviados.append(curso)

    print(cursos_abreviados)

    trace1 = go.Bar(
        x=cursos_abreviados,
        y=alunos_data1,
        name=datas[0].strftime('%d/%m/%Y'),
        marker_color='blue'
    )
    trace2 = go.Bar(
        x=cursos_abreviados,
        y=alunos_data2,
        name=datas[1].strftime('%d/%m/%Y'),
        marker_color='orange'
    )

    data = [trace1, trace2]
    layout = go.Layout(
        title='Quantidade de Alunos por Curso em 2 Datas',
        barmode='group'
    )

    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div


@login_required(login_url='login')
def course_dashboard_view(request):
    total_courses = Course.objects.count()
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_tutors = Tutor.objects.count()
    all_courses = Course.objects.all().order_by('name')
    
    # Gerar o gráfico de alunos por curso
    graph_history_studants = graph_average_students_per_course()

    # Gráfico de barras agrupadas
    graph_bars = grafico_barras_agrupadas()

    latest_courses = Course.objects.order_by('-id')[:2]

    context = {
        'total_courses': total_courses,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_tutors': total_tutors,
        'graph_history_studants': graph_history_studants,
        'latest_courses': latest_courses,
        'all_courses': all_courses,
        'graph_bars': graph_bars
    }
    return render(request, 'course_dashboard.html', context)


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Course, HistoryAmountStudents

def course_specific_graph(request, pk):
    course = get_object_or_404(Course, pk=pk)
    data = HistoryAmountStudents.objects.filter(course=course).order_by('date')

    dates = [item.date.strftime('%Y-%m-%d') for item in data]
    amounts = [item.amount_students for item in data]

    return JsonResponse({
        'course_name': course.name,
        'x': dates,
        'y': amounts,
    })

@login_required(login_url='login')
def course_module_view(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        form = ModuleModelForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course  # vincula o módulo ao curso
            module.save()
            return redirect('course_modules', pk=pk)
    else:
        form = ModuleModelForm(initial={'course': course})

    modules = Module.objects.filter(course=course).order_by('name')

    context = {
        'course': course,
        'modules': modules if modules.exists() else None,
        'form': form,
    }
    return render(request, 'course_modules.html', context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class ModuleDetailView(DetailView):
    model = Module
    template_name = 'course_module_detail.html'

    def get_object(self, queryset=None):
        course_pk = self.kwargs.get('pk')
        module_pk = self.kwargs.get('module_pk')
        return get_object_or_404(Module, pk=module_pk, course__pk=course_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        module = self.get_object()
        course = module.course
        students = module.students.all()
        atividades = module.activities.all()

        alunos_com_atividades = []

        for aluno in students:
            status_atividades = []
            for atividade in atividades:
                relacao = ActivityHasStudents.objects.filter(activity=atividade, student=aluno).first()
                status_atividades.append({
                    'atividade': atividade,
                    'concluida': relacao.completed if relacao else False
                })
            alunos_com_atividades.append({
                'aluno': aluno,
                'atividades': status_atividades,
                'media_conclusao': (sum(1 for atv in status_atividades if atv['concluida']) / len(status_atividades) if status_atividades else 0) * 100,
            })

        context.update({
            'course': course,
            'module': module,
            'atividades': atividades,
            'alunos_com_atividades': alunos_com_atividades,
        })
        return context
    