import os
from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages

def home(request):
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


