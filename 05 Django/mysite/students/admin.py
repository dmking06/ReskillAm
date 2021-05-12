from django.contrib import admin

from .models import Student, School, Department, Grade, Faculty, Certificate

admin.site.register(Student)
admin.site.register(School)
admin.site.register(Department)
admin.site.register(Grade)
admin.site.register(Faculty)
admin.site.register(Certificate)
