from django.shortcuts import render
from Courses.models import Student, Enrollment

def Courses_view(request):
    students = Student.objects.all()
    search = request.GET.get('search')
    if search:
        students = students.filter(name__icontains=search)  # case insensitive

    enrollments_by_student = []

    for student in students:
        enrollments = Enrollment.objects.filter(student=student)
        course_list = [enrollment.course.name for enrollment in enrollments]

        enrollments_by_student.append({
            'name': student.name,
            'enrollments': course_list
        })

    return render(
        request,
        template_name='courses.html',
        context={
            'enrollments_by_student': enrollments_by_student,
        }
    )
