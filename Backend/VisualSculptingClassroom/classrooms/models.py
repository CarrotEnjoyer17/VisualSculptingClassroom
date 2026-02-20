from django.db import models
from random import randint
from django.templatetags.static import static
from users.models import User

# Create your models here.

class Classroom(models.Model):
    name = models.CharField(max_length=256)
    creator = models.CharField(max_length=256)
    key = models.IntegerField()

class ClassroomListQuerySet(models.QuerySet):
    pass

class ClassroomList(models.Model):
    classroom = models.ForeignKey(to=Classroom, on_delete=models.CASCADE)
    member = models.ForeignKey(to=User, on_delete=models.CASCADE)
    objects = ClassroomListQuerySet.as_manager()
    def medium_mark(self):
        classroom=self.classroom
        student=self.member
        mark_objects = Mark.objects.filter(student=student, classroom=classroom)
        marks = list(mark_objects.values_list("value", flat=True))
        summary = 0
        for mark in marks:
            summary += mark
        if marks:
            return summary / len(marks)
        else:
            return "нет оценок"
class Work(models.Model):
    name = models.CharField(max_length=256)
    classroom = models.ForeignKey(to=Classroom, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    file_model = models.FileField(null=False, upload_to='models', default=static('img/default.gltf'))
    file_sup = models.FileField(null=True, upload_to='models')
    file_textures = models.FileField(null=True, upload_to='models/textures')

class Mark(models.Model):
    values = ((5, '5'), (4, '4'), (3, '3'), (2, '2'), (1, '1'))
    value = models.IntegerField(choices=values, default=5)
    student = models.ForeignKey(to=User, on_delete=models.CASCADE)
    teacher = models.CharField(max_length=256)
    classroom = models.ForeignKey(to=Classroom, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Work, on_delete=models.CASCADE, default=0)
