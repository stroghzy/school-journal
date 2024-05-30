from django.contrib import admin
from .models import Teacher, Subjects, Class, TeacherByClass, CreditByStudent, Student

# Register your models here.
admin.site.register(Teacher)
admin.site.register(Subjects)
admin.site.register(Class)
admin.site.register(TeacherByClass)
admin.site.register(CreditByStudent)
admin.site.register(Student)