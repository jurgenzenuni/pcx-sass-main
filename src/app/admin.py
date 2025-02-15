from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import EmailVerificationToken, Contact, SupportThread, ThreadMessage

class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'is_verified', 'created_at')
    list_filter = ('is_verified',)
    search_fields = ('user__username', 'user__email')
    actions = ['verify_emails']

    def email(self, obj):
        return obj.user.email

    def verify_emails(self, request, queryset):
        for token in queryset:
            token.user.is_active = True
            token.user.save()
            token.is_verified = True
            token.save()
        self.message_user(request, f"Successfully verified {queryset.count()} users.")
    verify_emails.short_description = "Verify selected users"

# Extend UserAdmin to show verification status
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('is_verified', 'verification_status')
    
    def is_verified(self, obj):
        try:
            return obj.emailverificationtoken.is_verified
        except EmailVerificationToken.DoesNotExist:
            return False
    is_verified.boolean = True
    
    def verification_status(self, obj):
        try:
            token = obj.emailverificationtoken
            return "Verified" if token.is_verified else "Pending"
        except EmailVerificationToken.DoesNotExist:
            return "No verification token"

# Unregister the default UserAdmin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(EmailVerificationToken, EmailVerificationTokenAdmin)
admin.site.register(Contact)
admin.site.register(SupportThread)
admin.site.register(ThreadMessage) 