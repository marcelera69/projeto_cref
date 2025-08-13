import csv
import os
import difflib
import re
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from datetime import datetime
from Courses.models import (
    Student, Teacher, Group, Course,
    Enrollment, HistoryAmountStudents, CourseInventory
)

class Command(BaseCommand):
    help = 'Importa alunos de um arquivo CSV para o banco de dados, sincronizando a base'

    def add_arguments(self, parser):
        parser.add_argument('csvfile', type=str, help='Arquivo CSV para importar')

    def handle(self, *args, **kwargs):
        csvfile = kwargs['csvfile']

        # 📁 Extrai nome do curso do nome do arquivo CSV
        filename = os.path.splitext(os.path.basename(csvfile))[0]

        # 🔍 Função para limpar nome
        def limpar_nome_curso(nome):
            nome = nome.lower()
            nome = re.sub(r'alunos? (da|do|de|das|dos)\s+', '', nome)
            nome = re.sub(r'[^\w\s\(\)\-]', '', nome)  # remove caracteres especiais
            nome = nome.strip()
            return nome

        nome_limpo = limpar_nome_curso(filename)

        # 🔍 Busca curso mais semelhante no banco
        todos_cursos = Course.objects.all()
        melhor_curso = None
        maior_similaridade = 0.0
        limiar_similaridade = 0.80

        for curso in todos_cursos:
            nome_db = limpar_nome_curso(curso.name)
            similaridade = difflib.SequenceMatcher(None, nome_limpo, nome_db).ratio()
            if similaridade > maior_similaridade:
                maior_similaridade = similaridade
                melhor_curso = curso

        if melhor_curso and maior_similaridade >= limiar_similaridade:
            course = melhor_curso
            self.stdout.write(self.style.SUCCESS(
                f'Curso semelhante encontrado: "{course.name}" (similaridade: {maior_similaridade:.2f}). Será utilizado.'
            ))
        else:
            course = Course.objects.create(name=filename)
            self.stdout.write(self.style.SUCCESS(f'Curso "{filename}" criado.'))

        csv_emails = set()

        with open(csvfile, encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)

            # Limpa os cabeçalhos para evitar problemas de BOM ou espaços
            reader.fieldnames = [field.strip().replace('\ufeff', '') for field in reader.fieldnames]

            def get_field(row, keys):
                for key in keys:
                    value = row.get(key)
                    if value:
                        return value.strip()
                return None

            for row_num, row in enumerate(reader, start=2):
                self.stdout.write(f'🔍 Processando linha {row_num}: {row}')

                nome = get_field(row, ['Nome'])
                code = get_field(row, ['Sobrenome'])
                email = get_field(row, ['Endereço de email', 'E-mail', 'Email'])
                grupo_nome = get_field(row, ['Grupos', 'Grupo'])

                if not email:
                    self.stdout.write(self.style.WARNING(f"Linha {row_num} ignorada: sem email"))
                    continue

                csv_emails.add(email)

                student, _ = Student.objects.get_or_create(
                    email=email,
                    defaults={'name': nome, 'code': code}
                )

                group = None
                if grupo_nome:
                    group, _ = Group.objects.get_or_create(
                        name=grupo_nome,
                        course=course,
                        defaults={'tutor': None}
                    )

                enrollment, created = Enrollment.objects.update_or_create(
                    student=student,
                    course=course,
                    defaults={'group': group, 'status': 'active'}
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Matriculado "{student.name}" no curso "{course.name}".'))
                else:
                    self.stdout.write(f'"{student.name}" já estava matriculado. Matrícula atualizada.')

        # 🔥 Remove alunos que saíram do CSV
        enrollments_db = Enrollment.objects.filter(course=course)
        for enrollment in enrollments_db:
            if enrollment.student.email not in csv_emails:
                enrollment.delete()
                self.stdout.write(self.style.WARNING(
                    f'Aluno "{enrollment.student.name}" removido da matrícula do curso "{course.name}".'
                ))

        # 📊 Atualiza histórico de quantidade de alunos
        total = Enrollment.objects.filter(course=course).count()

        # Você pode definir uma data fixa se quiser (descomente para isso):
        # data_fixa = make_aware(datetime(2025, 7, 24, 10, 0))
        # HistoryAmountStudents.objects.create(course=course, amount_students=total, date=data_fixa)

        HistoryAmountStudents.objects.create(course=course, amount_students=total)

        self.stdout.write(self.style.SUCCESS(
            f'Histórico atualizado: {total} alunos no curso "{course.name}".'
        ))

        # 📦 Atualiza o inventário de cursos
        courses = Course.objects.prefetch_related('students').all()
        courses_count = courses.count()
        total_alunos = sum(course.students.count() for course in courses)
        media_alunos = total_alunos / courses_count if courses_count > 0 else 0

        CourseInventory.objects.create(
            courses_count=courses_count,
            average_students_per_course=media_alunos,
        )

        self.stdout.write(self.style.SUCCESS('Inventário de cursos atualizado.'))
