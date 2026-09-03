from django.contrib import admin

from .models import Classroom, School, Student, Teacher


admin.site.register(School)
admin.site.register(Classroom)
admin.site.register(Teacher)
admin.site.register(Student)
