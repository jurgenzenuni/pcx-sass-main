from django.contrib import admin
from django.urls import path
from .views import home, about, submit_contact, contact

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('submit-contact/', submit_contact, name='submit_contact'),
]
