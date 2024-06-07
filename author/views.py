from typing import Any
from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from posts.models import Post

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

def register(request):
    if request.method == 'POST':
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('user_login')
    else:
        register_form = forms.RegistrationForm()
        
    return render(request, 'register.html', {'form': register_form, 'type': 'Register'})


# def user_login(request):
#     form = AuthenticationForm()
    
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         user = authenticate(request, username=username, password=password)

#         print(user)

#         if user is None:
#             messages.error(request, "Username and password do not match")
#             return render(request, 'register.html', {'form': form, 'type': 'Login'})

#         login(request, user)
#         messages.success(request, f'Welcome {username} login successfull')
#         return redirect('add_post')
    
#     return render(request, 'register.html', {'form': form, 'type': 'Login'})

@login_required
def profile(request):
    posts = Post.objects.filter(author = request.user)
    return render(request, 'profile.html', {'posts': posts})



@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = forms.ChangeUserData(request.POST, instance=request.user)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile Updated Successfully!')
            return redirect('profile')
    else:
        profile_form = forms.ChangeUserData(instance=request.user)
    
    return render(request, 'update_profile.html', {'form': profile_form})

@login_required
def pass_change(request):
    if request.method == 'POST':
            form = PasswordChangeForm(request.user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Password updated successfully!')
                update_session_auth_hash(request, form.user)
                return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
            
    return render(request, 'pass_change.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('user_login')


# implementing authentication using class based view

class UserLoginView(LoginView):
    template_name = 'register.html'

    def get_success_url(self):
        return reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, 'Login successful!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request, 'Login information incorrect!')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['type'] = 'login'
        return context
    

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('homepage')  

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)





















