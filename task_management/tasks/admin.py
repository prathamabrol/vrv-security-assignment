from django.contrib import admin
from .models import CustomUser, Role, Permission, Task

# Task Admin
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'due_date', 'completed', 'comments')  # Add completion and comments fields
    list_filter = ('assigned_to', 'due_date', 'completed')  # Filter by task status
    search_fields = ('title', 'description')  # Search functionality for tasks

# Role Admin
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Key fields in admin list view
    search_fields = ('name',)  # Allow searching by role name

# Permission Admin
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Key fields in admin list view
    search_fields = ('name',)  # Allow searching permissions

# Custom User Admin
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff')  # Display key user fields
    search_fields = ('username', 'email')  # Allow searching users
    


# Registering models
admin.site.register(Task, TaskAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
