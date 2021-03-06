import requests
import os
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User, Task
from .forms import LoginForm, TaskForm, RegistrationForm
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from dotenv import load_dotenv

load_dotenv()

SERVER_FLASK = os.getenv('SERVER_FLASK')

def register(request):
    if request.method == "POST":

        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            # user_form.save()
            cd = user_form.cleaned_data
            User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password'])
            return redirect('main')
        else:
            print(user_form.errors)
    else:
        user_form = RegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


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
        available_to_me = all_task.filter(~Q(creator=request.user), executor=None, status='new')
        execute = all_task.filter(executor=request.user, status='in_work')
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


def give_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.executor = request.user
    task.status = 'in_work'
    task.save()
    return redirect('main')


def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.status = 'complete'
    task.save()
    return redirect('main')


def cancel_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.status = 'cancel'
    task.save()
    return redirect('main')


def refusal_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.status = 'refusal'
    task.save()
    return redirect('main')


def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('main')


def profile(request):
    refresh = RefreshToken.for_user(request.user)
    token = str(refresh.access_token)
    data = {
        'token': token
    }
    return render(request, 'profile.html', data)


def chats(request):
    url = f'{SERVER_FLASK}/chat_history'
    response = requests.get(url)
    data = {
        'chat_messages': response.json()
    }
    return render(request, 'chats.html', data)


def private_chat(request, customer_id, executor_id):
    url_history = f'{SERVER_FLASK}/chat_history/customer={customer_id}&executor={executor_id}'
    url_users = f'{SERVER_FLASK}/chat_users/customer={customer_id}&executor={executor_id}'
    response_history = requests.get(url_history)
    response_users = requests.get(url_users)
    data = {
        'users': response_users.json(),
        'chat_messages': response_history.json(),
        'customer': User.objects.get(pk=customer_id),
        'executor': User.objects.get(pk=executor_id),
    }
    return render(request, 'private_chat.html', data)
