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


class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control me-2',
        'placeholder': 'Повторите пароль',
    }))

    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'email': forms.TextInput(attrs={
                'class': 'form-control me-2',
                'placeholder': 'Email'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control me-2',
                'placeholder': 'Имя пользователя'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control me-2',
                'placeholder': 'Пароль'
            }),
        }

    def clean_password2(self):
        print('Я тут был, мед да пиво пил')
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']


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
        
