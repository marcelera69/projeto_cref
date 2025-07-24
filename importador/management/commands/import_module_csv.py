from django.core.management.base import BaseCommand
import csv
import re
from datetime import datetime
from django.utils.timezone import make_aware
from Courses.models import Student, Module, Activity, ActivityHasStudents, Course, Enrollment


class Command(BaseCommand):
    help = 'Importa atividades e estudantes a partir de um CSV de módulo'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Caminho para o arquivo CSV')
        parser.add_argument('module_id', type=int, help='ID do módulo que será usado para importar as atividades')

    def handle(self, *args, **options):
        csv_path = options['csv_path']
        module_id = options['module_id']

        try:
            module = Module.objects.get(id=module_id)
        except Module.DoesNotExist:
            self.stderr.write(self.style.ERROR(f'Módulo com ID {module_id} não encontrado.'))
            return

        course = module.course  # curso relacionado ao módulo

        self.stdout.write(f'📘 Importando dados para o módulo "{module.name}" do curso "{course.name}"...')

        with open(csv_path, newline='', encoding='utf-16') as csvfile:
            # Lê o CSV com delimitador de tabulação
            reader = list(csv.reader(csvfile, delimiter='\t'))

            header = reader[0]
            atividade_headers = []
            for i in range(2, len(header), 2):
                atividade_nome = header[i].strip('"')
                if atividade_nome:
                    atividade_headers.append((i, atividade_nome))

            for row in reader[1:]:
                nome_completo = row[0].strip().strip('"')

                # extrair código entre colchetes
                match = re.search(r"(.*)\s(\[.*\])$", nome_completo)
                if match:
                    nome_limpo = match.group(1).strip()
                    codigo = match.group(2).strip()
                else:
                    nome_limpo = nome_completo
                    codigo = None

                # Buscar ou criar estudante
                student, created = Student.objects.get_or_create(
                    name=nome_limpo,
                    code=codigo
                )
                if created:
                    self.stdout.write(f"➕ Estudante criado: {student.name} | código: {student.code}")

                # Criar matrícula se ainda não existir
                enrollment, _ = Enrollment.objects.get_or_create(
                    student=student,
                    course=course,
                    defaults={"status": "active"}
                )

                # Vincular estudante ao módulo (se ainda não)
                module.students.add(student)

                # Importar atividades e status
                for i, atividade_nome in atividade_headers:
                    status = row[i].strip().lower()
                    data_str = row[i + 1].strip()

                    activity, _ = Activity.objects.get_or_create(
                        title=atividade_nome,
                        module=module
                    )

                    # Verificar se já existe relação estudante-atividade
                    ahs, created = ActivityHasStudents.objects.get_or_create(
                        activity=activity,
                        student=student,
                        defaults={
                            "completed": status == "concluído"
                        }
                    )

                    if not created:
                        ahs.completed = status == "concluído"
                        ahs.save()

        self.stdout.write(self.style.SUCCESS("\n✅ Importação concluída com sucesso!"))
