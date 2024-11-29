# tasks/utils.py
from django.core.exceptions import PermissionDenied

def is_ceo(user):
    if user.user_type != 'CEO':
        raise PermissionDenied

def is_manager(user):
    if user.user_type != 'MANAGER':
        raise PermissionDenied

def is_employee(user):
    if user.user_type != 'EMPLOYEE':
        raise PermissionDenied
