from django.shortcuts import render, redirect
#the code below is when you did the login page and signup page
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
#till here
from .models import * 
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder

#the code bellow are the imports for the admin side

from .forms import ProductForm
from django.urls import reverse
#from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

#the code is till here
#the code bellow is for the admin side customer data displaying
from.models import Customer, Order, OrderItem, Product, ShippingAddress
#the is till here

#the code bellow is for the displayigng email writing place in the signup page
from.forms import CustomUserCreationForm  # Import the custom form

#the code is till here

# Create your views here.

#the code below is when you did the login page and signup page

'''
@login_required
def home(request):
    return render(request, "registration/login.html", {})
'''
#the function bellow handels the signup page and
#the code below is when you did the login page and signup page

#the code bellow is for the displayigng email writing place in the signup page

def authView(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("store:login")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})

#the code is till here


'''
def authView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("store:login")
    else:
        form = UserCreationForm()
    
    return render(request, "registration/signup.html", {"form": form})
'''
#till here



def store(request):

    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()
    context = {'products':products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    # Prepare a list to hold items marked as out of stock
    out_of_stock_items = []

    # Iterate over items in the cart
    for item in items:
        product = item.product
        # Check if the item quantity exceeds the product quantity
        if item.quantity > product.quantity:
            # Mark the item as out of stock
            item.out_of_stock = True
            out_of_stock_items.append(item)

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'out_of_stock_items': out_of_stock_items  # Pass the out of stock items to the template
    }
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    quantity = data.get('quantity', 100)  # Default to 1 if quantity is not provided
    print('Action:', action)
    print('productId:', productId)

    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += quantity  # Increase by 1
    elif action == 'remove':
        orderItem.quantity -= quantity  # Decrease by 1
        

    orderItem.save()


    if orderItem.quantity <= 99:
	    orderItem.delete()

    return JsonResponse('Item was added', safe=False)


#from django.views.decorators.csrf import csrf_exempt

#@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        

    else:
       customer, order = guestOrder(request, data)

    	#customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
        )

    #the code bellow is for printing the datas that are in chekout.html on line 141
    #print('Data:', request.body)
    #the code is till here 
    
    return JsonResponse('Payment submitted..', safe=False)


#the code bellow fo when you added the admin side 

#def addProduct(request):
 #   return render(request, 'admin/home.html')

'''
def addProduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            # Assuming you have a way to determine the current order
            order = determine_current_order(request)  # You need to implement this function
            quantity = 1  # Default quantity, adjust as needed
            
            # Create and save the OrderItem instance
            order_item = OrderItem(product=product, order=order, quantity=quantity)
            order_item.save()
            
            return redirect('store:home')
    else:
        form = ProductForm()

    #data = cartData(request)
    products = Product.objects.all()
    context = {'products': products, 'form': form}
    return render(request, 'admin/home.html', context)
'''
#data = cartData(request)
#code bellow you took from AI that allows ypu access the quantity in the product 
#class int e models.py 
#THE ORIGINAL CODE IS BELLOW

def addProduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)  # Don't save yet to modify quantity
            quantity = form.cleaned_data['quantity']  # Get the quantity from the form
            product.quantity = quantity  # Set the quantity on the product
            product.save()  # Save the product with the specified quantity
            return redirect('store:home')
    else:
        form = ProductForm()



    products = Product.objects.all()
    context = {'products': products, 'form': form,}
    return render(request, 'admin/home.html', context)


#the code is till here

def product_delete(request, pk):
    
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('store:home')
    context = {
        'product': product
    }
    return render(request, 'admin/product_delete.html', context)#context


'''
    try:
        product = Product.objects.get(id=pk)
    except ObjectDoesNotExist:
        # Handle the case where the Product does not exist
        return HttpResponse("Product not found")

    if request.method == 'POST':
        product.delete()
        return redirect('store:home')
'''
    
    


'''  
    product = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('admin/home.html')
    context = {
        'product': product
    }
'''
    #return render(request, 'admin/product_delete.html')#context

'''
from django.shortcuts import get_object_or_404

def addProduct(request):
    if request.method == 'POST':
        if 'delete-btn' in request.POST:
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            product.delete()
            return redirect('store:home')
        else:
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('store:home')
    else:
        form = ProductForm()

    data = cartData(request)
    products = Product.objects.all()
    context = {'products': products, 'form': form}
    return render(request, 'admin/home.html', context)
'''
    
'''
def addProduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('store:home')
    else:
        form = ProductForm()
    
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems, 'form': form}
    return render(request, 'store/store.html', context)
'''
'''
def delete_product(request, product_id):
    # Retrieve the product instance
    product = Product.objects.get(id=product_id)

    # Delete the product
    product.delete()

    # Redirect to a success page or perform any other desired logic
    return redirect('product_list')
'''

#the code is till here

#the code bellow is for the admin side customer data displaying

def data_table(request):
    users = User.objects.all()  # Fetch all users
    customers = Customer.objects.all()
    orders = Order.objects.all()
    order_items = OrderItem.objects.all()
    products = Product.objects.all()
    shipping_addresses = ShippingAddress.objects.all()

    return render(request, 'admin/data_table.html', {
        'users': users,
        'customers': customers,
        'orders': orders,
        'order_items': order_items,
        'products': products,
        'shipping_addresses': shipping_addresses,
    })

#the code is till here
























