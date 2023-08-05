from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserModelForm,UserUpdateForm


class RegisterView(View):

    def get(self,request):
        form=UserModelForm()
        context={
            'form':form
        }
        return render(request,'users/register.html',context)

    def post(self,request):
        form=UserModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
        return render(request,'users/register.html',context={'form':form})


class LoginView(View):

    def get(self,request):
        form=AuthenticationForm()
        return render(request,'users/login.html',{'form':form})

    def post(self,request):
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request,form.get_user())
            messages.success(request,'You have successfully logged in.')
            return redirect('books:list')
        return render(request,'users/login.html',{"form":form})


class ProfilePageView(LoginRequiredMixin,View):

    def get(self,request):
        return render(request,'users/profile.html',{'user':request.user})


class LogoutView(View):

    def get(self,request):
        logout(request)
        messages.info(request,'You have successfully logged out.')
        return redirect('home')


class UserUpdateView(LoginRequiredMixin,View):

    def get(self,request):
        form=UserUpdateForm(instance=request.user)
        return render(request,'users/profile-edit.html',{'form':form})

    def post(self,request):
        form=UserUpdateForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES
        )
        if form.is_valid():
            form.save()
            messages.success(request,'You have successfully updated your profile.')
            return redirect('users:profile')
        return render(request, 'users/profile-edit.html', {'form': form})
