from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User, Task
from .forms import LoginForm, TaskForm
from django.db.models import Q


# Логика входа
def login_user(request):
    if request.method == 'POST' and 'login' in request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = User.objects.filter(email=cd['email']).first()
            if username is None:
                messages.error(request, "Логин или пароль указаны не корректно")

            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
            else:
                messages.error(request, "Логин или пароль указаны не корректно")
        else:
            messages.error(request, "Логин или пароль указаны не корректно")
    return redirect('main')


def logout_user(request):
    logout(request)
    request.session.clear_expired()
    request.session.flush()
    return redirect('main')


def main(request):
    if request.user.is_authenticated:
        all_task = Task.objects.all()
        my_task = all_task.filter(creator=request.user)
        available_to_me = all_task.filter(~Q(creator=request.user), executor=None)
        execute = all_task.filter(executor=request.user)
    else:
        my_task = None
        available_to_me = None
        execute = None

    data = {
        'login_form': LoginForm(),
        'task_form': TaskForm(),
        'my_task': my_task,
        'available_to_me': available_to_me,
        'execute': execute,
    }
    return render(request, 'tasks.html', data)


def create_task(request):
    if request.method == 'POST' and 'create' in request.POST:
        form = TaskForm(request.POST)
        if form.is_valid():
            save_creator = form.save(commit=False)
            save_creator.creator = request.user
            save_creator.save()
        else:
            print(form.errors)
    return redirect('main')
