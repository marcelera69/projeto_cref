from django.shortcuts import render
from Courses.models import Course, Enrollment
from unidecode import unidecode
from Courses.forms import CourseModelForm
from django.shortcuts import redirect


def courses_view(request):
    search = request.GET.get('search', '')
    search_normalized = unidecode(search.strip().lower())

    if search_normalized:
        # Filtra manualmente, sem depender do banco
        courses = [
            course for course in Course.objects.all()
            if search_normalized in unidecode(course.name.lower())
        ]
    else:
        courses = Course.objects.all().order_by('name')

    return render(request, 'courses.html', {'courses': courses})

def new_course_view(request):

    if request.method == 'POST':
        new_course_form = CourseModelForm(request.POST)
        if new_course_form.is_valid():
            new_course_form.save()
            return redirect('courses_list')
    else:
        # Exibe o formulário vazio
        new_course_form = CourseModelForm()

    return render(request, 'new_course.html', {'form': new_course_form})

