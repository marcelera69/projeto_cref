from django.contrib import admin
from alunos.models import Participant, Group


class AlunosAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'last_name', 'email', 'group')
    search_fields = ('name',)
admin.site.register(Participant, AlunosAdmin)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'tutor')
    search_fields = ('name', 'tutor',)
admin.site.register(Group, GroupAdmin)