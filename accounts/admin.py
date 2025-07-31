from django.contrib import admin
from .models import RegistrationRequest

@admin.register(RegistrationRequest)
class RegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'registration', 'is_approved', 'is_rejected', 'created_at')
    search_fields = ('name', 'email', 'registration')
    list_filter = ('is_approved', 'is_rejected', 'created_at')
    ordering = ('-created_at',)
