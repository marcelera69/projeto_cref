import csv
import os
from django.core.management.base import BaseCommand
from Courses.models import Student, Teacher, Group, Course, Enrollment, HistoryAmountStudents, CourseInventory

class Command(BaseCommand):
    help = 'Importa alunos de um arquivo CSV para o banco de dados'

    def add_arguments(self, parser):
        parser.add_argument('csvfile', type=str, help='Arquivo CSV para importar')

    def handle(self, *args, **kwargs):
        csvfile = kwargs['csvfile']

        # Nome do curso será o nome do arquivo (sem extensão)
        course_name = os.path.splitext(os.path.basename(csvfile))[0]

        # Cria ou pega o curso
        course, created = Course.objects.get_or_create(name=course_name)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Curso "{course_name}" criado.'))
        else:
            self.stdout.write(f'Curso "{course_name}" já existe.')

        with open(csvfile, encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.stdout.write(str(row))  # Para depurar os dados lidos

                # Pegando dados do CSV (ajuste nomes das colunas conforme seu CSV)
                nome = row.get('Nome') or row.get('\ufeffNome')  # Caso tenha BOM
                code = row.get('Sobrenome')
                email = row.get('Endereço de email')
                grupo_nome = row.get('Grupos')

                # Cria ou pega o estudante
                student, created = Student.objects.get_or_create(
                    email=email,
                    defaults={'name': nome, 'code': code}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Estudante "{nome}" criado.'))
                else:
                    self.stdout.write(f'Estudante "{nome}" já existe.')

                # Procura o grupo com mesmo nome E ligado a esse curso
                if grupo_nome:
                    group = Group.objects.filter(name=grupo_nome, course=course).first()
                    if not group:
                        # Se não existir, cria com tutor None (ou defina um tutor padrão)
                        group = Group.objects.create(name=grupo_nome, course=course, tutor=None)
                        self.stdout.write(self.style.SUCCESS(f'Grupo "{grupo_nome}" criado para o curso "{course_name}".'))
                    else:
                        self.stdout.write(f'Grupo "{grupo_nome}" já existe para o curso "{course_name}".')

                # Cria o Enrollment para vincular aluno ao curso
                enrollment, created = Enrollment.objects.get_or_create(
                    student=student,
                    course=course,
                    group=group if grupo_nome else None,
                    defaults={'status': 'active'}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Matriculado "{student.name}" no curso "{course.name}".'))
                else:
                    self.stdout.write(f'"{student.name}" já está matriculado no curso "{course.name}".')

        # Atualiza a quantidade de alunos no curso
        total = Enrollment.objects.filter(course=course).count()
        history = HistoryAmountStudents(
        course=course,
        amount_students=total,
        )
        history.save()
        self.stdout.write(self.style.SUCCESS(f'Quantidade de alunos atualizada para o curso "{course.name}".'))
        
        # Atualiza o inventário de cursos
        courses_count = Course.objects.all().count()
        # Pegando o número de alunos por curso
        sum_alunos_per_course = 0
        for course in Course.objects.all():
            sum_alunos_per_course += course.students.count()
            if courses_count > 0:
                average_students = sum_alunos_per_course / courses_count
            else:
                average_students = 0

        # Atualizando os regisstros no modelo CourseInventory
        CourseInventory.objects.create(
            courses_count=courses_count,
            average_students_per_course=average_students,
        )
