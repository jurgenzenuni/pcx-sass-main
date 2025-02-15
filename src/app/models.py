from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

class SupportThread(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('open', 'Open'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed')
    ], default='open')
    category = models.CharField(max_length=50, choices=[
        ('technical', 'Technical Support'),
        ('order', 'Order Issues'),
        ('general', 'General Questions'),
        ('feedback', 'Feedback')
    ])

class ThreadMessage(models.Model):
    thread = models.ForeignKey(SupportThread, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_admin_reply = models.BooleanField(default=False)

# class Product(models.Model):
#     id = models.AutoField(primary_key=True)
#     product_name = models.CharField(max_length=200)
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     class Meta:
#         db_table = 'products'  

#     def __str__(self):
#         return self.product_name

# class Cart(models.Model):
#     id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     product_name = models.CharField(max_length=200)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     quantity = models.IntegerField(default=1)
#     added_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = 'cart'  

#     def __str__(self):
#         return f"{self.user.username}'s cart - {self.product_name}"

