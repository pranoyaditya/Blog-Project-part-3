from django.shortcuts import render,redirect
from .forms import RegisterForm,UserLoginForm,ChangeUserDataForm,ChangePassWordForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from posts.models import Post

# Create your views here.
def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully.')
            return redirect('user_login')
    return render(request, 'author/register.html', {'form' : form, 'type': 'Register'})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            userName = form.cleaned_data['username']
            userPass = form.cleaned_data['password']
            user = authenticate(username = userName, password = userPass)
            if user is not None:
                login(request,user)
                messages.success(request, 'Logged in successfully.')
                return redirect('profile')
            else:
                messages.warning(request, "Login information incorrect.")
                return redirect('register')
    else:
        form = UserLoginForm()
    return render(request, 'author/register.html', {'form' : form, 'type': 'Login'})

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('homePage')
    return redirect('user_login')

@login_required
def profile(request):
    data = Post.objects.filter(author = request.user)
    return render(request, 'author/profile.html', {'data' : data})

@login_required
def user_profile_update(request):
    form = ChangeUserDataForm(instance = request.user)
    if request.method == 'POST':
        form = ChangeUserDataForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    return render(request, 'author/update_profile.html', {'form' : form})

@login_required
def password_change(request):
    form = ChangePassWordForm(request.user)
    if request.method == 'POST':
        form = ChangePassWordForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password reset was successfull.')
            update_session_auth_hash(request, request.user)
            return redirect('profile')
    return render(request, 'author/password_change.html', {'form' : form})