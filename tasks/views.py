from django.shortcuts import render, redirect # para renderizar html y redireccionar
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User # para registrar usuarios
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
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
    return render(request, "task.html")


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