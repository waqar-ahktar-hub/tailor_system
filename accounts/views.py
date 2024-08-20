from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# def signup_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'accounts/signup.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('/')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')



@login_required
def profile(request):
    return render(request, 'profile.html')


from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    """Custom login view to redirect users based on their status."""

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('tailor_management_system:dashboard')  # Redirect to admin dashboard or appropriate URL
        return reverse_lazy('accounts:dashboard')  # Redirect to client dashboard
 

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from order.models import Order, Task  # Import your models

# class ClientDashboardView(LoginRequiredMixin, View):
#     """Client Dashboard View."""
#     def get(self, request):
#         client = request.user.client  # Assuming User model has a OneToOneField with Client
        
#         # Fetch data relevant to the client
#         recent_orders = Order.objects.filter(client=client).order_by('-created_at')[:5]
#         pending_tasks = Task.objects.filter(client=client, status='Pending')
        
#         context = {
#             'recent_orders': recent_orders,
#             'pending_tasks': pending_tasks,
#         }
#         return render(request, 'client/dashboard.html', context)

class ClientDashboardView(LoginRequiredMixin, View):
    """Client Dashboard View."""

    def get(self, request):
        client = request.user.client  # Get the client associated with the logged-in user
        orders = Order.objects.filter(client=client)
        tasks = Task.objects.filter(order__client=client)  # Adjust based on your task relationships

        context = {
            'orders': orders,
            'tasks': tasks
        }
        return render(request, 'client/dashboard.html', context)

from django.contrib.auth.decorators import login_required
@login_required
def client_dashboard(request):
    return render(request, 'client/dashboard.html')


@login_required
def activity_view(request):
    # Example context data; replace with your actual data source
    order_stats = {
        "D": 150,  # Delivered
        "I": 25,   # Pending
        "total": 200,  # Total Orders
        "C": 25    # Closed
    }
    
    context = {
        'order_stats': order_stats
    }
    
    return render(request, 'widgets/activity.html',context)
