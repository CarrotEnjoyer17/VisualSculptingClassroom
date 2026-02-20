from django.contrib import admin

from classrooms.models import Classroom, ClassroomList, Work, Mark

# Register your models here.
admin.site.register(Classroom)
admin.site.register(ClassroomList)
admin.site.register(Work)
admin.site.register(Mark)