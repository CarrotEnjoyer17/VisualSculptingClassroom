from django.forms import ModelForm
from django import forms
from random import randint

from classrooms.models import Classroom, Work, Mark

class ClassroomCreationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'type':'text',
        'name':'text_name',
        'placeholder':'Название класса',
        'style':"width: 90%; line-height: 28px;"
    }))
    key = forms.IntegerField(widget=forms.TextInput(attrs={
        'style':"display:none;",
        "readonly": "true"
    }))
    creator = forms.CharField(widget=forms.TextInput(attrs={
        'style':"display:none;",
        "readonly": "true"
    }))
    class Meta:
        model = Classroom
        fields = ('name','key','creator')
class EnterClassroom(forms.Form):
    key = forms.IntegerField(max_value= 100000000, widget=forms.TextInput(attrs={
        "type": "text",
        "name": "text_name",
        "placeholder": "Код класса",
        "style": "width: 50%; line-height: 28px;"
    }))

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class FileFieldForm(forms.Form):
    file_field = MultipleFileField()

class WorkUploadForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'type':'text',
        'name':'text_name',
        'placeholder':'Название работы',
        'style':"width: 50%; line-height: 28px;"
    }))
    file_model = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'type':'file',
    }))
    file_sup = MultipleFileField(required=False, widget=MultipleFileInput(attrs={
        'type':'file',
        'multiple': True
    }))
    file_textures = MultipleFileField(required=False, widget=MultipleFileInput(attrs={
        'type': 'file',
        'multiple': True
    }))
    class Meta:
        model = Work
        fields = ('name', 'file_model', 'file_textures', 'file_sup')
class MarkPuttingForm(forms.ModelForm):
    value = forms.Select(attrs={
        "font-size": "15px",
    })
    class Meta:
        model = Mark
        fields = ('value',)
