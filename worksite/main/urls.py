from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path('login', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout'),
    path('create', views.create_task, name='create_task')

]
