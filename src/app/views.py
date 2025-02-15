import os
from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact, SupportThread, ThreadMessage
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from django.db import connection
from django.db.models import Q
from django.core.paginator import Paginator

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

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        print("Received POST request")  # Debug print
        try:
            data = json.loads(request.body)
            product_name = data.get('product_name')
            print(f"Product name: {product_name}")  # Debug print
            
            # Get the product from your database
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, price FROM products WHERE product_name = %s",
                    [product_name]
                )
                product = cursor.fetchone()
                
                if product:
                    product_id, price = product
                    
                    # Check if item already in cart
                    cursor.execute(
                        """
                        SELECT id, quantity FROM cart 
                        WHERE user_id = %s AND product_id = %s
                        """,
                        [request.user.id, product_id]
                    )
                    cart_item = cursor.fetchone()
                    
                    if cart_item:
                        # Update quantity
                        cursor.execute(
                            """
                            UPDATE cart 
                            SET quantity = quantity + 1 
                            WHERE id = %s
                            """,
                            [cart_item[0]]
                        )
                    else:
                        # Insert new cart item
                        cursor.execute(
                            """
                            INSERT INTO cart 
                            (user_id, product_id, product_name, price, quantity, added_at) 
                            VALUES (%s, %s, %s, %s, 1, NOW())
                            """,
                            [request.user.id, product_id, product_name, price]
                        )
                    
                    return JsonResponse({
                        'success': True,
                        'message': 'Added to cart successfully'
                    })
                else:
                    print(f"Product not found: {product_name}")  # Debug print
                    return JsonResponse({
                        'success': False,
                        'message': 'Product not found'
                    })
                    
        except Exception as e:
            print(f"Error: {str(e)}")  # Debug print
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def get_cart(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT product_name, price, quantity 
            FROM cart 
            WHERE user_id = %s
        """, [request.user.id])
        
        cart_items = []
        total_items = 0
        total_price = 0
        
        for row in cursor.fetchall():
            product_name, price, quantity = row
            item_total = float(price) * quantity
            cart_items.append({
                'product_name': product_name,
                'price': float(price),
                'quantity': quantity,
                'total': item_total
            })
            total_items += quantity
            total_price += item_total

    cart_data = {
        'items': cart_items,
        'total_items': total_items,
        'total_price': total_price
    }
    return JsonResponse(cart_data)

@login_required
def update_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_name = data.get('product_name')
            change = int(data.get('change', 0))
            
            with connection.cursor() as cursor:
                # Get the cart item
                cursor.execute(
                    """
                    SELECT c.id, c.quantity 
                    FROM cart c
                    JOIN products p ON c.product_id = p.id
                    WHERE p.product_name = %s AND c.user_id = %s
                    """,
                    [product_name, request.user.id]
                )
                cart_item = cursor.fetchone()
                
                if cart_item:
                    cart_id, current_quantity = cart_item
                    new_quantity = current_quantity + change
                    
                    if new_quantity > 0:
                        # Update quantity
                        cursor.execute(
                            "UPDATE cart SET quantity = %s WHERE id = %s",
                            [new_quantity, cart_id]
                        )
                    else:
                        # Remove item if quantity would be 0 or less
                        cursor.execute(
                            "DELETE FROM cart WHERE id = %s",
                            [cart_id]
                        )
                    
                    return JsonResponse({
                        'success': True,
                        'message': 'Cart updated successfully'
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'message': 'Item not found in cart'
                    })
                    
        except Exception as e:
            print(f"Error: {str(e)}")  # Debug print
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def support(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')
    
    threads = SupportThread.objects.all().order_by('-created_at')
    
    # Apply filters
    if query:
        threads = threads.filter(
            Q(title__icontains=query) |
            Q(messages__content__icontains=query)
        ).distinct()
    if category:
        threads = threads.filter(category=category)
    if status:
        threads = threads.filter(status=status)
    
    # Pagination
    paginator = Paginator(threads, 10)
    page = request.GET.get('page')
    threads = paginator.get_page(page)
    
    return render(request, 'support.html', {
        'threads': threads,
        'query': query,
        'category': category,
        'status': status
    })

def thread_detail(request, thread_id):
    thread = get_object_or_404(SupportThread, id=thread_id)
    messages = thread.messages.all().order_by('created_at')
    
    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('content')
        if content:
            ThreadMessage.objects.create(
                thread=thread,
                author=request.user,
                content=content,
                is_admin_reply=request.user.is_staff
            )
            return redirect('thread_detail', thread_id=thread_id)
    
    return render(request, 'thread_detail.html', {
        'thread': thread,
        'messages': messages
    })

def create_thread(request):
    if request.method == 'POST' and request.user.is_authenticated:
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        
        thread = SupportThread.objects.create(
            title=title,
            author=request.user,
            category=category
        )
        ThreadMessage.objects.create(
            thread=thread,
            author=request.user,
            content=content
        )
        return redirect('thread_detail', thread_id=thread.id)
    
    return render(request, 'create_thread.html')

@login_required
def change_thread_status(request, thread_id, new_status):
    thread = get_object_or_404(SupportThread, id=thread_id)
    
    # Check if user is thread owner or admin
    if request.user == thread.author or request.user.is_staff:
        if new_status in ['open', 'resolved', 'closed']:
            thread.status = new_status
            thread.save()
            messages.success(request, f'Thread status updated to {new_status}')
    else:
        messages.error(request, "You don't have permission to change thread status.")
    
    return redirect('thread_detail', thread_id=thread_id)

