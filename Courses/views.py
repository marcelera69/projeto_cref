from django.shortcuts import render
from Courses.models import Course, Enrollment
from unidecode import unidecode
from Courses.forms import CourseForm

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
    new_course_form = CourseForm()
    return render(request, 'new_course.html', {'form': new_course_form})

