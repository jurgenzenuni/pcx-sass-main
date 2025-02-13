import os
from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse

def home(request):
    print(request.user)
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    # Get all contacts
    contacts = Contact.objects.all()
    # Pass to template
    context = {
        'contacts': contacts
    }
    return render(request, 'contact.html', context)

def submit_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        Contact.objects.create(
            name=name,
            email=email,
            message=message
        )
        messages.success(request, 'Thank you for your message!')
        return redirect('contact')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({
                'success': False, 
                'message': 'Invalid username or password'
            })
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'success': False,
                'message': 'Username already exists'
            })
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'message': 'Email already exists'
            })
            
        user = User.objects.create_user(username=username, email=email, password=password)
        return JsonResponse({
            'success': True,
            'message': 'Registration successful! Please login.'
        })
    return render(request, 'register.html', {})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')
