from django.contrib import admin
from django.urls import path
from .views import home, about, submit_contact, contact, login_view, register_view, logout_view, add_to_cart, get_cart, update_cart, support, thread_detail, create_thread, change_thread_status

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('submit-contact/', submit_contact, name='submit_contact'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('api/cart/add/', add_to_cart, name='add_to_cart'),
    path('api/cart/', get_cart, name='get_cart'),
    path('api/cart/update/', update_cart, name='update_cart'),
    path('support/', support, name='support'),
    path('support/thread/<int:thread_id>/', thread_detail, name='thread_detail'),
    path('support/create/', create_thread, name='create_thread'),
    path('support/thread/<int:thread_id>/status/<str:new_status>/', change_thread_status, name='change_thread_status'),
]
