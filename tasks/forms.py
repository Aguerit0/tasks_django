from django.forms import ModelForm
from .models import Task

class TaskForm(ModelForm):
    class Meta:
        model = Task # modelo que se va a usar para validar los campos
        fields = ['title', 'description', 'important'] # mecanismo de validacion de campos