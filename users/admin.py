from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Referral, Reward

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'referral_code', 'referred_by', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'referral_code')
    
admin.site.register(User, UserAdmin)
admin.site.register(Referral)
admin.site.register(Reward)
