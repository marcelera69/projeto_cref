from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from .models import Course, Enrollment




@receiver(post_save, sender=Course)
def course_post_save(sender, instance, **kwargs):
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



@receiver(post_delete, sender=Course)
def course_post_delete(sender, instance, **kwargs):
    ...