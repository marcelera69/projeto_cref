from django.shortcuts import render
from alunos.models import Student, Enrollment

def alunos_view(request):
    students = Student.objects.all()
    enrollments_by_student = []

    for student in students:
        enrollments = Enrollment.objects.filter(student=student)

        # Cria uma lista com o nome de todos os cursos em que o aluno está matriculado
        course_list = [enrollment.course for enrollment in enrollments]

        enrollments_by_student.append({
            'name': student.name,
            'enrollments': course_list
        })

    return render(
        request,
        template_name='alunos.html',
        context={
            'enrollments_by_student': enrollments_by_student,
        }
    )