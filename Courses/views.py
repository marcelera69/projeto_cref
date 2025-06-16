from django.shortcuts import render
from Courses.models import Course, Enrollment
from unidecode import unidecode

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

