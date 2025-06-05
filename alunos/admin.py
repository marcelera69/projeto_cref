from django.contrib import admin
from alunos.models import Participante


class AlunosAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'last_name', 'email', 'group')
    search_fields = ('name',)

admin.site.register(Participante, AlunosAdmin)