import random
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
from django.http import JsonResponse
from django.conf import settings
import os
from django.http import FileResponse

from classrooms.forms import ClassroomCreationForm, EnterClassroom, WorkUploadForm, MarkPuttingForm
from users.models import User
from classrooms.models import Classroom, ClassroomList, Work, Mark
# Create your views here.
@login_required

def cube(request):
    context= {
        "model_path" : static("img/scene.gltf")
    }

    return render(request, 'classrooms/index.html',context)

def classrooms_list(request):
    context = {
        'title': 'Список классов',
        'user': request.user,
        'classes': list(ClassroomList.objects.all())
    }
    return render(request, 'classrooms/classrooms_list.html', context)

def classroom_creation(request):
    if request.method == 'POST':
        form = ClassroomCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            real_key = form.cleaned_data['key']
            ClassroomList.objects.create(member=request.user, classroom=Classroom.objects.get(key=real_key))
            return HttpResponseRedirect(reverse('classrooms:classrooms_list'))
    else:
        keys = Classroom.objects.values_list("key")
        keys_list = list(keys)
        random_key = random.randint(10000000, 99999999)
        while random_key in keys_list:
            random_key = random.randint(10000000, 99999999)
        initial_data = {'key': random_key, 'creator': request.user.username}
        form = ClassroomCreationForm(initial=initial_data)
    context = {
        'form': form,
        'title': 'Создание класса'
    }
    return render(request, 'classrooms/classroom_creation.html', context)

def class_list(request, classroom_key):
    if request.user.username == Classroom.objects.get(key=classroom_key).creator:
        f = 1
    else:
        f = 0
    students = []
    for cl in ClassroomList.objects.all():
        if cl.classroom.key == classroom_key:
            students.append(cl)
    context = {
        'title': 'Список класса',
        'members': students,
        'is_admin':f,
        'name_of_admin':Classroom.objects.get(key=classroom_key).creator,
        'classroom_key': classroom_key,
        'marks':Mark.objects.all()
    }
    return render(request, 'classrooms/class_list.html', context)

def enter_classroom(request, user_login):
    if request.method == "POST":
        form = EnterClassroom(request.POST)
        if form.is_valid():
            key_user = form.cleaned_data['key']
            for real_key_n in Classroom.objects.values_list('key'):
                real_key = real_key_n[0]
                if key_user == real_key:
                    new_member = User.objects.get(username=user_login)
                    members = ClassroomList.objects.filter(member=request.user, classroom=Classroom.objects.get(key=real_key))
                    if not members.exists():
                        ClassroomList.objects.create(member=new_member, classroom=Classroom.objects.get(key=real_key))
                        return HttpResponseRedirect(reverse('classrooms:classrooms_list'))
                    break
                else:
                    pass
                        #Действие если пользователь уже в классе
    else:
        form = EnterClassroom()
    context = {
        'title': 'Вход в класс',
        'form': form,
        'user': request.user,
    }
    return render(request, 'classrooms/enter_classroom.html', context)

def leave_classroom(request, classroom_key):
    class_to_del = Classroom.objects.get(key=classroom_key)
    if class_to_del.creator == request.user.username:
        Classroom.objects.filter(key=classroom_key).delete()
    else:
        ClassroomList.objects.filter(classroom=class_to_del, member=request.user).delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def delete_user(request, delete_key,deleted_username):
    classroom_d = Classroom.objects.get(key=delete_key)
    member_d = User.objects.get(username=deleted_username)
    ClassroomList.objects.filter(classroom = classroom_d, member = member_d).delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def works(request, user_login, class_key):
    user = User.objects.get(username=user_login)
    context = {
        'title': 'Работы ученика',
        'user': user,
        'role': request.user.roles,
        'class_key': class_key,
        'looking': request.user.username,
        'all_works':Work.objects.filter(author=user, classroom=Classroom.objects.get(key=class_key))
    }
    return render(request, 'classrooms/works.html', context)

def work_big(request, author_login, classroom_key, work_pk):
    author = User.objects.get(username=author_login)
    cl_list = ClassroomList.objects.filter(classroom=Classroom.objects.get(key=classroom_key))
    members = list(cl_list.values_list('member'))
    for i in range(len(members)):
        members[i] = members[i][0]
    teachers = []
    for teacher in User.objects.filter(roles='teacher'):
        if teacher.pk in members:
            teachers.append(teacher)
    work = Work.objects.get(pk=work_pk)
    loge = User.objects.get(username=author_login)
    cl = Classroom.objects.get(key=classroom_key)
    m = Mark.objects.filter(teacher=request.user.username, student=loge, classroom=cl, project=Work.objects.get(pk=work_pk))
    m1 = Mark.objects.filter(student=loge, classroom=cl, project=Work.objects.get(pk=work_pk))
    if m.exists():
        m = True
    else:
        m = False
    if request.method == "POST":
        form = MarkPuttingForm(data=request.POST)
        if form.is_valid():
            mark = form.cleaned_data['value']
            Mark.objects.create(value=mark, student = loge, teacher = request.user.username, classroom = cl, project = Work.objects.get(pk=work_pk))
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            print(form.errors)
    else:
        form = MarkPuttingForm()
    marks_objects = Mark.objects.filter(project=work)
    marks = list(marks_objects.values_list("value", flat=True))
    summary = 0
    for mark in marks:
        summary += mark
    if marks:
        work_medium_mark = summary / len(marks)
    else:
        work_medium_mark = "нет оценок"
    context = {
        'title': 'Работы ученика',
        'author': author,
        'user': request.user,
        'teachers':teachers,
        'work': work,
        'format': work.file_model.name[-4:],
        'cl': Classroom.objects.get(key=classroom_key),
        'm1':m1,
        'm':m,
        'form':form,
        'a_l':author_login,
        'c_k':classroom_key,
        'work_pk':work_pk,
        'work_medium_mark':work_medium_mark,
    }
    return render(request, 'classrooms/work_big.html', context)


def work_adding(request, classroom_key):
    if request.method == "POST":
        user = request.user
        place = Classroom.objects.get(key=classroom_key)
        form = WorkUploadForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            title = form.cleaned_data['name']
            obj = form.cleaned_data['file_model']
            Work.objects.create(name=title, classroom=place, author=user, file_model=obj)
            return HttpResponseRedirect(reverse('classrooms:works', kwargs={'user_login':user.username, 'class_key':classroom_key}))
        else:
            print(form.errors)
    else:
        form = WorkUploadForm()
    context = {
        'form': form,
        'title': 'Добавление работы',
        'key':classroom_key
    }
    return render(request, 'classrooms/work_adding.html', context)

def putting_mark(request, student_login, class_k, work_pk):
    if request.method == "POST":
        form = MarkPuttingForm(data=request.POST)
        loge = User.objects.get(username=student_login)
        cl = Classroom.objects.get(key=class_k)
        m = Mark.objects.filter(teacher=request.user.username, student=loge, classroom=cl)
        m1 = m
        if m.exists():
            m = True
        else:
            m = False
        if form.is_valid():
            mark = form.cleaned_data['value']
            Mark.objects.create(value=mark, student = loge, teacher = request.user.username, classroom = cl, project = Work.objects.get(pk=work_pk))
            return HttpResponseRedirect(reverse('classrooms:work_big', kwargs={'author_login':loge.username, 'classroom_key':class_k, "work_pk":work_pk}))
        else:
            print(form.errors)
    else:
        form = MarkPuttingForm()
    context = {
        'form':form,
        'user':request.user,
        'm':m,
        'm1':m1
    }
    return render(request, 'classrooms/work_big.html', context)

def download(request, work_id):
    response = FileResponse(open(Work.objects.get(pk=work_id).file_model.path, "rb"))
    return response
def delete(request, work_id, cl_k):
    Work.objects.filter(pk = work_id).delete()
    return HttpResponseRedirect(reverse('classrooms:works', kwargs={'user_login':request.user.username, 'class_key':cl_k}))