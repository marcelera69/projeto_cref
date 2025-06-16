import csv
import os
from django.core.management.base import BaseCommand
from Courses.models import Student, Teacher, Group, Course, Enrollment

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
                code = row.get('Code')
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
                group = None
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
                    defaults={'status': 'active'}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Matriculado "{student.name}" no curso "{course.name}".'))
                else:
                    self.stdout.write(f'"{student.name}" já está matriculado no curso "{course.name}".')
