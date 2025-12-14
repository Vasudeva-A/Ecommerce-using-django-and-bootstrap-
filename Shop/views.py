from django.shortcuts import render,redirect
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import*
from django.contrib import messages
from .forms import CustomUserForm  
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages




def home(request):
    
    context = {

        'home'  : Products.objects.filter(trending=1)
    }


    return render(request,'home.html',context)

def Register(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful")
            return redirect('login')
    else:
        form = CustomUserForm()

    context = {"form": form}
    return render(request, 'registration/register.html', context)

def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:

        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('username')
                pwd = form.cleaned_data.get('password')
                user = authenticate(request, username=name, password=pwd)
                if user is not None:
                    login(request, user)
                    return redirect('home')
            messages.error(request, "Invalid username or password")
        else:
            form = AuthenticationForm()

        return render(request, 'registration/login.html', {'form': form})

def LogoutPage(request):
    # if request.user.is_authenticated:
        logout(request)
        return redirect('home')

def Collections(request):

    context = {

        'collections' : Category.objects.filter(status=0)

    }

    return render(request,'collection.html',context)

def CollectionsView(request,name):

    if(Category.objects.filter(name=name,status=0)):

        context = {

            'products' : Products.objects.filter(category__name=name),
            "category_name":name

        }

        return render(request,'products.html',context)
    else:
        messages.warning(request,'no such category found')
        return redirect('collection')

def ProductDetails(request, cname, pname):
    if Category.objects.filter(name=cname, status=0).exists():
        if Products.objects.filter(category__name=cname, name=pname, status=0).exists():
            context = {
                'products_details': Products.objects.filter(category__name=cname, name=pname, status=0).first()
            }
            return render(request, 'productsdetail.html', context)
        else:
            messages.error(request, 'No such product found')
            return redirect('collection')
    else:
        messages.error(request, 'No such category found')
        return redirect('collection')

@login_required
def AddToCart(request, id):
    product = Products.objects.get(id=id)

    if request.method == "POST":
        qty = request.POST.get("qty", "1")
        qty = int(qty)    

        item, created = Carts.objects.get_or_create(user=request.user,products=product)

        if not created:
            item.product_quantity = item.product_quantity + int(qty)
        else:
            item.product_quantity = qty
            
        item.total = item.product_quantity * product.selling_price
        item.save()
        messages.success(request, f"{product.name} added to cart!")

    return redirect('cart_view')

def CartView(request):
    cart_items = Carts.objects.filter(user=request.user)
    return render(request, "cart.html", {"cart_items": cart_items})

@login_required
def CancelOrder(request,id):
    cart = get_object_or_404(Carts, id=id, user=request.user)
    cart.delete()
    messages.success(request, " removed from cart!")

    return redirect('cart_view')

@login_required
def PlaceOrder(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        qty = int(request.POST.get("qty", 1))
        print("DEBUG product_id:", product_id)  # Debug

        product = get_object_or_404(Products, id=product_id)
        print("DEBUG product:", product.name)  

        order = OrderProducts.objects.create(
            user=request.user,
            order_products=product,
            order_quantity=qty,
            total_price=qty * product.selling_price
        )

        messages.success(request, f"{product.name} ordered successfully!")
        return redirect("order_view")
    return redirect("cart_view")

@login_required
def Orderview(request):
    context = {
            
            "orders" : OrderProducts.objects.filter(user=request.user).order_by('-created_at')

    }

    return render(request,'orders.html',context)

@login_required
def ClearHistory(request,id):
    order = get_object_or_404(OrderProducts, id=id, user=request.user)
    order.delete()
    messages.warning(request, " Removed from Orders ")

    return redirect('order_view')

@login_required
def ClearAll(request):
    orders = OrderProducts.objects.filter(user_id=request.user)  # use your actual user field
    if orders.exists():
        orders.delete()
        messages.warning(request, "History cleared Successfully!")
    else:
        messages.info(request, "No orders to clear.")
    return redirect('order_view')