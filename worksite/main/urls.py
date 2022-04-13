from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path('login', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout'),
    path('create', views.create_task, name='create_task'),
    path('give_task=<int:task_id>', views.give_task, name='give_task'),
    path('complete_task=<int:task_id>', views.complete_task, name='complete_task'),
    path('cancel_task=<int:task_id>', views.cancel_task, name='cancel_task'),
    path('refusal_task=<int:task_id>', views.refusal_task, name='refusal_task'),
    path('delete_task=<int:task_id>', views.delete_task, name='delete_task'),
    path('profile', views.profile, name='profile')
]
