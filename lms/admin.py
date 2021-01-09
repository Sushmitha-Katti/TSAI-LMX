from django.contrib import admin

# LMS application imports.
from .models.users_model import Staff, Student
from .models.course_model import Course


# Registers the student profile model at the admin backend.
class StudentAdmin(admin.ModelAdmin):
    list_filter = ('user',)
    search_fields = ('user__username',)
    ordering = ['user__username', ]


admin.site.register(Student, StudentAdmin)


# Registers the staff profile model at the admin backend.
class StaffAdmin(admin.ModelAdmin):
    list_filter = ('is_admin', 'is_teacher', 'is_teaching_assistant')
    search_fields = ('user__username',)
    ordering = ['user__username', 'is_admin', 'is_teacher', 'is_teaching_assistant']


admin.site.register(Staff, StaffAdmin)



class CourseAdmin(admin.ModelAdmin):

    list_display = ('title', 'student',)
    list_filter = ('student',)
    search_fields = ('title',)
    raw_id_fields = ('student',)


# Registers the article model at the admin backend.
admin.site.register(Course, CourseAdmin)