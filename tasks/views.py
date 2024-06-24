from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from .models import Task

def home(request):
    return render(request, "home.html")


@login_required
def signout(request):
    logout(request)
    return redirect("home")

def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {
            "form": AuthenticationForm()
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, "signin.html", {
                "form": AuthenticationForm(),
                "error": "El usuario o contraseña no son correctos"
            })
        else:
            login(request, user)
            return redirect("tasks")


def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                return render(request, "signup.html", {
                    "form": UserCreationForm(),
                    "error": "El usuario ya existe"
                })
        else:
            return render(request, "signup.html", {
                "form": UserCreationForm(),
                "error": "Las contraseñas no coinciden"
            })
    else:
        return render(request, "signup.html", {
            "form": UserCreationForm()
        })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=True).order_by('-date_completed')
    return render(request, "task.html", {
        "tasks": tasks
    })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    return render(request, "task.html", {
        "tasks": tasks
    })

@login_required
def task_detail(request, id):
    task = get_object_or_404(Task, pk=id, user=request.user)
    if request.method == "GET":
        form = TaskForm(instance=task)
        return render(request, "task_detail.html", {
            "task": task,
            "form": form
        })
    else:
        try:
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect("tasks")
            else:
                return render(request, "task_detail.html", {
                    "task": task,
                    "form": form,
                    "error": "Error al actualizar la tarea"
                })
        except ValueError:
            return render(request, "task_detail.html", {
                "task": task,
                "form": TaskForm(instance=task),
                "error": "Error al actualizar la tarea"
            })

@login_required
def complete_task(request, id):
    task = get_object_or_404(Task, pk=id, user=request.user)
    if request.method == "POST":
        task.date_completed = timezone.now()
        task.save()
        return redirect("tasks")

@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, pk=id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("tasks")

@login_required
def createTask(request):
    if request.method == "GET":
        return render(request, "create_task.html", {
            "form": TaskForm()
        })
    else:
        try:
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                return redirect("tasks")
            else:
                return render(request, "create_task.html", {
                    "form": form,
                    "error": "Error al crear la tarea"
                })
        except ValueError:
            return render(request, "create_task.html", {
                "form": TaskForm(),
                "error": "Error al crear la tarea"
            })

