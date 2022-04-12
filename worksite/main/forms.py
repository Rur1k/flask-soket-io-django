from .models import User, Task
from django import forms


# Формы авторизации
class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control me-2',
        'placeholder': 'E-mail',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control me-2',
        'placeholder': 'Пароль',
    }))


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название задачи'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание задачи',
                'style': 'height: 100px; resize:none'
            }),
        }
        
