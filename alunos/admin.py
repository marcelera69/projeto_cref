from django.contrib import admin
from alunos.models import Student, Teacher, Group, Course, Enrollment

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
admin.site.register(Course, CourseAdmin)


class StudentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'email')
    search_fields = ('name',)
admin.site.register(Student, StudentsAdmin)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'email')
    search_fields = ('name',)
admin.site.register(Teacher, TeacherAdmin)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'tutor')
    search_fields = ('name', 'tutor',)
admin.site.register(Group, GroupAdmin)


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status')
    search_fields = ('student__name', 'course__name')
admin.site.register(Enrollment, EnrollmentAdmin)