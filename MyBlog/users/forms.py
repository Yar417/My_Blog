from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='E-mail',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        required=True,
        label='Account Name',
        help_text='Don`t use "@, /, ?, !, \"',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Account login'
                                      })
    )
    # some = forms.ModelChoiceField(queryset= User.objects.all())
    password1 = forms.CharField(
        required=True,
        label='Insert password',
        help_text='Use at least 6 characters',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        required=True,
        label='The same password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        label='E-mail*',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        required=False,
        label='Account Name*',
        help_text='Don`t use "@, /, ?, !, \"',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Account login'
                                      })
    )

    class Meta:
        model = User
        fields = ['email', 'username']


class ProfileImageForm(forms.ModelForm):
    img = forms.ImageField(
        label='Download Photo',
        required=False,
        widget=forms.FileInput()
    )

    class Meta:
        model = Profile
        fields = ['img']


class ProfileUpdateForm(forms.ModelForm):
    gender = forms.CharField(
        required=True,
        label='Your gender* ',
        # choices=Profile.choice,
        widget=forms.Select(
            choices=Profile.choice,
            attrs={'class': 'form-select'})
    )

    notifications = forms.BooleanField(
        label=False,
        required=False,
        help_text='Получать уведомления на почту о новых статьях?'
    )

    class Meta:
        model = Profile
        fields = ['gender', 'notifications']
