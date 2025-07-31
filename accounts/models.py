from django.db import models

# Create your models here.


class RegistrationRequest(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    registration = models.CharField(max_length=12, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email} - {self.registration} - {self.created_at}"