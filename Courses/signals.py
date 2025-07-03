from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

def course_pre_save(sender, instance, **kwargs):
    ...