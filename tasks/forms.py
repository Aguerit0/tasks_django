from .models import Task
from django import forms

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task # modelo que se va a usar para validar los campos
        fields = ['title', 'description', 'important'] # mecanismo de validacion de campos
        widgets = {
            'tittle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba una tarea'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escriba una descripcion'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input text-center m-auto'}),
            
        }