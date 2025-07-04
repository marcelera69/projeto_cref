from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from .models import Course



@receiver(pre_save, sender=Course)
def course_pre_save(sender, instance, **kwargs):
    ...