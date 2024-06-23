from django.shortcuts import render, redirect # para renderizar html y redireccionar
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User # para registrar usuarios
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task
# Create your views here.

def home(request):
    return render(request, "home.html")

def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                #registrar usuario en base de datos
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                #Guardar cookies para que el usuario pueda acceder a la pagina de tasks
                login(request, user)
                
                #redireccionar a la pagina de tasks
                return redirect("tasks")
            except IntegrityError:
                return render(request, "signup.html",{
                    "form": UserCreationForm,
                    "error": "El usuario ya existe"
                })


            
        else:
            #el usuario ya existe o las contraseñas no coincide
            return render(request, "signup.html",{
                    "form": UserCreationForm,
                    "error": "El usuario ya existe"
                })
        
    elif request.method == "GET":
        return render(request, "signup.html",{
        "form": UserCreationForm,
        "error": "El usuario ya existe"
    })
    



def tasks(request):
    Task.objects.all().filter(user=request.user)
    return render(request, "task.html", {
        "tasks": Task.objects.all().order_by('-date_completed')
    })
    

def createTask(request):
    if request.method == "GET":
        return render(request, "create_task.html",{
        "form": TaskForm
    })
    else:
        try:
            form = TaskForm(request.POST) # crear un form con los datos ingresados por el usuario
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.save()
                return redirect("tasks")
        except ValueError:
            return render(request, "create_task.html",{
                "form": TaskForm,
                "error": "Error al crear la tarea"
            })

def signout(request):
    logout(request)
    return redirect("home")

def signin(request, form_class=AuthenticationForm):
    if request.method == "GET":
        form = form_class()
        return render(request, "signin.html",{
            "form": form,
        })
    else:
        user =authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, "signin.html",{
                "form": form_class,
                "error": "El usuario o contraseña no son correctos"
            })
        else:
            login(request, user)
            return redirect("tasks")