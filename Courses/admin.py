from django.contrib import admin
from Courses.models import Student, Teacher, Tutor, Group, Course, Module, Enrollment, Activity, ActivityHasStudents, HistoryAmountStudents

#Classe para usar o modelo MOdule como inline no admin do Course
class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0
    autocomplete_fields = ['teachers']
    fields = ('name', 'description', 'number_classes', 'teachers', 'students')
    readonly_fields = ('number_classes',)
    ordering = ('name',)

#Classe para usar o modelo Enrollment como inline no admin do Course
class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0
    autocomplete_fields = ['student']
    fields = ('student', 'group', 'status')
    ordering = ('student',)

class HistoryAmountStudentsInline(admin.TabularInline):
    model = HistoryAmountStudents
    extra = 0
    fields = ('course', 'amount_students')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    inlines = [EnrollmentInline, ModuleInline, HistoryAmountStudentsInline]


class ActivityHasStudentsInline(admin.TabularInline):
    model = ActivityHasStudents
    extra = 0
    autocomplete_fields = ['student']
    fields = ('activity', 'student', 'completed')
    ordering = ('student',)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'module',)
    search_fields = ('title',)
    list_filter = ('module', 'student',)
    ordering = ('module', 'title')
    inlines = [ActivityHasStudentsInline]


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


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'email')
    search_fields = ('name',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'tutor__name')
    search_fields = ('name', 'tutor',)






