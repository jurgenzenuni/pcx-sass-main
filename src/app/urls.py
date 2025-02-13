from django.contrib import admin
from django.urls import path
from .views import home, about, submit_contact, contact, login_view, register_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('submit-contact/', submit_contact, name='submit_contact'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]
