from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve

from classrooms.views import classrooms_list, classroom_creation, class_list, enter_classroom, leave_classroom, delete_user, cube, works, work_adding, work_big, putting_mark, download, delete

app_name = "classrooms"

urlpatterns = [
    path('classrooms_list/', classrooms_list, name="classrooms_list"),
    path('classroom_creation/', classroom_creation, name="classroom_creation"),
    path('class_list/<int:classroom_key>/', class_list, name="class_list"),
    path('enter_classroom/<str:user_login>/', enter_classroom, name="enter_classroom"),
    path('leave_classroom/<int:classroom_key>/', leave_classroom, name="leave_classroom"),
    path('delete_user/<int:delete_key>/<str:deleted_username>/', delete_user, name="delete_user"),
    path('cube/', cube, name="cube"),
    path('works/<str:user_login>/<int:class_key>/', works, name="works"),
    path('work_adding/<int:classroom_key>/', work_adding, name="work_adding"),
    path('work_big/<str:author_login>/<int:classroom_key>/<int:work_pk>/', work_big, name="work_big"),
    path('putting_mark/<str:student_login>/<int:class_k>/<int:work_pk>/', putting_mark, name="putting_mark"),
    path('download/<int:work_id>/', download, name="download"),
    path('delete/<int:work_id>/<int:cl_k>/', delete, name="delete"),
]
