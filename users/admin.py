from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Address


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username','email','phone','is_staff')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user','label','city','pincode','is_default')