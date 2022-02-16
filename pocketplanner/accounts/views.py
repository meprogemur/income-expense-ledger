from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.contrib import messages
from client.models import Client
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.


class SignUp(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('statement')
        form = SignUpForm()
        return render(request, 'accounts/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password1']
            client = Client.objects.create(user=User.objects.get(
                username=uname), name=uname, schema_name=uname, domain_url=request.META['HTTP_HOST'])
            client.save()
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                return redirect('statement')
        messages.error(request, 'Invalid Credentials')
        return redirect('signup')


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('statement')
        else:
            form = AuthenticationForm()
            return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get('username')
            upass = form.cleaned_data.get('password')
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                return redirect('statement')
        messages.error(request, 'Invalid username or password')
        return redirect('login')


@login_required(login_url='login')
def Logout(request):
    logout(request)
    return redirect('login')
