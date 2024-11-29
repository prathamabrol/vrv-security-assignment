# tasks/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404
from .models import Task, CustomUser
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from .utils import is_ceo,is_manager,is_employee
# from django.utils.timezone import now
from .forms import TaskUpdateForm






User = get_user_model()




def manage_roles(request):
    is_ceo(request.user)  # Ensure only CEOs can access this view
    users = CustomUser.objects.exclude(user_type='CEO')  # Exclude the CEO themselves

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('new_role')
        user = CustomUser.objects.get(id=user_id)
        user.user_type = new_role
        user.save()

    return render(request, 'manage_roles.html', {'users': users})





def assign_task(request):
    if request.user.user_type != 'Manager':
        messages.error(request, "You do not have permission to assign tasks.")
        return redirect('task_list')

    employees = CustomUser.objects.filter(user_type='Employee')
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to_id = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date')

        try:
            assigned_to = CustomUser.objects.get(id=assigned_to_id, user_type='Employee')
            Task.objects.create(
                title=title,
                description=description,
                assigned_to=assigned_to,
                due_date=due_date,
            )
            messages.success(request, "Task assigned successfully!")
            return redirect('task_list')
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid employee selected.")

    return render(request, 'assign_task.html', {'employees': employees})


@login_required
def task_list(request):
    if request.user.is_staff:  # For managers
        tasks = Task.objects.all()
    else:  # For employees
        tasks = Task.objects.filter(assigned_to=request.user)

    return render(request, 'task_list.html', {'tasks': tasks})





@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Redirect to the task list after update
    else:
        form = TaskUpdateForm(instance=task)

    return render(request, 'task_detail.html', {'task': task, 'form': form})





# Register View
# Registration view
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validate passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        # Log the user in after successful registration
        login(request, user)
        return redirect('task_list')  # Redirect to the task list or dashboard

    return render(request, 'register.html')



# Login View
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('task_list')  # Redirect to the task list or dashboard
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
            return redirect('login')

    return render(request, 'login.html')




# Logout View
def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')













# For creating tasks
@login_required
def create_task(request):
    if request.user.user_type != 'manager':
        return redirect('task_list')  # Redirect employees

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to_id = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date')
        
        assigned_user = CustomUser.objects.get(id=assigned_to_id)
        Task.objects.create(
            title=title,
            description=description,
            assigned_to=assigned_user,
            due_date=due_date,
        )
        return redirect('task_list')

    users = CustomUser.objects.filter(user_type='employee')  # Managers assign tasks to employees only
    return render(request, 'create_task.html', {'users': users})


#  TO task list
@login_required
def task_list(request):
    # Get the tasks based on user role (Managers see all tasks, Employees see their tasks)
    if request.user.user_type == 'manager':
        tasks = Task.objects.all()  # Managers see all tasks
    else:
        tasks = Task.objects.filter(assigned_to=request.user)  # Employees see their tasks only

    # Handle the task update for both employees and managers
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        task = Task.objects.get(id=task_id)

        # Check if the task exists
        if not task:
            messages.error(request, "Task not found.")
            return redirect('task_list')

        # Update the task based on the user role
        if request.user.user_type == 'manager':
            # Managers can update all task details
            task.title = request.POST.get('title', task.title)
            task.description = request.POST.get('description', task.description)
            task.due_date = request.POST.get('due_date', task.due_date)
            task.completed = 'completed' in request.POST
            task.comments = request.POST.get('comments', task.comments)

        elif request.user.user_type == 'employee':
            # Employees can only update the 'completed' status and comments
            task.completed = 'completed' in request.POST
            task.comments = request.POST.get('comments', task.comments)

        # Save the updated task
        task.save()
        messages.success(request, "Task updated successfully.")
        return redirect('task_list')  # Redirect to the task list after update

    return render(request, 'task_list.html', {'tasks': tasks})




# For updating task
@login_required
def update_task(request, task_id):
    task = Task.objects.get(id=task_id)
    
    # Ensure the user has the right permissions
    if request.user.user_type == 'manager':
        # Managers can update the title, description, due date, assigned user
        if request.method == 'POST':
            task.name = request.POST['name']
            task.description = request.POST['description']
            task.due_date = request.POST['due_date']
            task.comments = request.POST['comments']
            task.assigned_to = User.objects.get(id=request.POST['assigned_to'])
            
            # Handle completion status
            task.completed = 'completed' in request.POST
            task.save()
            messages.success(request, "Task updated successfully!")
            return redirect('task_list')  # Redirect to task list after update
    elif request.user.user_type == 'employee':
        # Employees can only update status and comments
        if request.method == 'POST':
            task.completed = 'completed' in request.POST
            task.comments = request.POST['comments']
            task.save()
            messages.success(request, "Task status updated!")
            return redirect('task_list')

    return render(request, 'update_task.html', {'task': task, 'users': User.objects.all()})



# For deleting a task
# @login_required
# @permission_required('tasks.delete_task', raise_exception=True)
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')
