from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from .models import Course, Enrollment
from openai_api import client

#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

def course_inventory_update():
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
    from .models import CourseInventory  
    CourseInventory.objects.create(
        courses_count=courses_count,
        average_students_per_course=average_students,
    )


@receiver(pre_save, sender=Course)
def course_pre_save(sender, instance, **kwargs):
    if not instance.description:
        ia_description = client.generate_course_description(instance.name)
        instance.description = ia_description


@receiver(post_save, sender=Course)
def course_post_save(sender, instance, **kwargs):
    # Atualiza o inventário de cursos após a criação ou atualização de um curso
    course_inventory_update()


@receiver(post_delete, sender=Course)
def course_post_delete(sender, instance, **kwargs):
    # Atualiza o inventário de cursos após a exclusão de um curso
    course_inventory_update()