from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm

def signup_view(request):
    """
    Handles user registration.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.username}.')
            return redirect('users:accounts')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()

    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    """
    Handles user login.
    """
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Welcome back, {username}!')
                return redirect('users:accounts')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    """
    Handles user logout.
    """
    logout(request)
    messages.info(request, 'You have been successfully logged out.')
    return redirect('core:home')

@login_required
def accounts_view(request):
    """
    The main accounts page for a logged-in user.
    Handles profile updates.
    """
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('users:accounts')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        profile_form = UserProfileForm(instance=request.user.profile)

    context = {
        'profile_form': profile_form
    }
    return render(request, 'users/accounts.html', context)
