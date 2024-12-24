from django.shortcuts import render, get_object_or_404 ,redirect
from .models import Product,  Order 
from .forms import ProductForm 
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied 
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login  
from .forms import FakePaymentForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
def home(request):
    products = Product.objects.all() 
    return render(request, 'index.html', {'products': products})
 

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        order = Order.objects.create(customer_name=request.user.username, product=product, quantity=quantity, user=request.user)
        return render(request, 'order_success.html', {'order': order})

@login_required
def view_cart(request):
    orders = Order.objects.filter(user=request.user, completed=False)
    cart_count = sum(order.quantity for order in orders)
    return render(request, 'view_cart.html', {'orders': orders, 'cart_count': cart_count})

@login_required
def checkout(request):
    orders = Order.objects.filter(user=request.user, completed=False)  # Fetch the user's active cart items
    total = sum(order.product.price * order.quantity for order in orders)
    
    if request.method == "POST":
        payment_form = FakePaymentForm(request.POST)
        if payment_form.is_valid():
            # Here, you can simulate a successful payment
            # For now, just mark all orders as completed and save them
            orders.update(completed=True)
            # Redirect to the order confirmation page
            return redirect('order_confirmation')
    else:
        payment_form = FakePaymentForm()

    return render(request, 'checkout.html', {'orders': orders, 'total': total, 'payment_form': payment_form})


@login_required
def upload_product(request): 
    if not request.user.is_staff:
        raise PermissionDenied("You do not have permission to upload products.")

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product uploaded successfully!')
            return redirect('home') 
    else:
        form = ProductForm()

    return render(request, 'upload_product.html', {'form': form})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product_detail.html', {'product': product})
 

def remove_from_cart(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        return redirect('view_cart')
    
  
def order_confirmation(request):
    return render(request, 'order_confirmation.html')

# def register(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('product_list')  # Redirect to product list after registration
#     else:
#         form = RegisterForm()
#     return render(request, 'register.html', {'form': form})