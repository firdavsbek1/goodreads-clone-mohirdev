from django import forms
from django.conf import settings
from django.core.mail import send_mail

from .models import CustomUser


class UserForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    password = forms.CharField(max_length=188, widget=forms.PasswordInput())

    def save(self):
        user = CustomUser.objects.create(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
        )
        user.set_password(self.cleaned_data['password'])
        return user


class UserModelForm(forms.ModelForm):
    password = forms.CharField(max_length=188, widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(user.password)
        user.save()


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username','first_name','last_name','email','profile_image')