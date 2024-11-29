# tasks/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_task, name='create_task'),
    path('update/<int:task_id>/', views.update_task, name='update_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('assign-task/', views.assign_task, name='assign_task'),
    path('tasks/', views.task_list, name='task_list'),
    # path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    
]
