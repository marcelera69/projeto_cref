from django.contrib import admin
from alunos.models import Student, Teacher, Group, Course, Enrollment


#Classe para usar o modelo Enrollment como inline no admin do Course
class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0
    autocomplete_fields = ['student']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    inlines = [EnrollmentInline]
    
    
@admin.register(Student)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'email')
    search_fields = ('name',)
    list_filter = ('code',)
    ordering = ('name',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'email')
    search_fields = ('name',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'tutor__name')
    search_fields = ('name', 'tutor',)


