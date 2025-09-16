from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from cart.models import Order # Add this import
from django.db.models import Sum # Add this import

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

# Add the new view function below
@login_required
def subscription(request):
    # Calculate the total amount of money the user has spent.
    # We filter Orders by the current user, then use aggregate and Sum to add up the 'total' field.
    # The 'or 0' handles the case where a user has no orders yet.
    total_spent = Order.objects.filter(user=request.user).aggregate(total=Sum('total'))['total'] or 0

    # Determine the subscription level based on the total spent.
    if total_spent < 15:
        subscription_level = 'Basic'
    elif 15 <= total_spent < 30:
        subscription_level = 'Medium'
    else:
        subscription_level = 'Premium'

    # Prepare the data for the template, following your established pattern.
    template_data = {
        'title': 'My Subscription',
        'total_spent': total_spent,
        'subscription_level': subscription_level,
    }

    return render(request, 'accounts/subscription.html', {'template_data': template_data})

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET': 
        return render(request, 'accounts/login.html', {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(request, username = request.POST['username'],
                            password = request.POST['password']
                            )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                          {'template_data': template_data})
        else: 
            auth_login(request, user)
            return redirect('home.index')
        
def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})
        
@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html', {'template_data': template_data})