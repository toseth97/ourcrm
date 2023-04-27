from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from django.contrib import messages
from .decorator import unauthenticated, allowedUsers, redirection
from .filter import *
from .models import *
from .forms import *


# Create your views here.

@unauthenticated
@redirection
@allowedUsers(allowed_role=['admin'])
def home(request):
    user = None
    if request.user.is_authenticated:
        user = request.user
    order_count = Order.objects.all().count()
    orders = Order.objects.all().order_by('-id')[:5]
    delivered = Order.objects.filter(status="Delivered").count()
    pending = Order.objects.filter(status="Pending").count
    customers = Customer.objects.all()
    context = {"title": "Dashboard", "pending": pending, "orders": orders,
               "order_count": order_count, "delivered": delivered, "user": user, "customers": customers}
    return render(request, 'account/dashboard.html', context)


@unauthenticated
@allowedUsers(allowed_role=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    filters = OrderFilter(request.GET, queryset=orders)
    orders = filters.qs

    order_count = orders.count()

    context = {"customer": customer, "orders": orders,
               "title": "Customer", "title": "Customer", "order_count": order_count, "filters": filters}

    return render(request, 'account/customer.html', context)


@unauthenticated
@allowedUsers(allowed_role=['admin'])
def product(request):
    products = Product.objects.all()

    context = {"title": "Product", "products": products, "title": "Products"}
    return render(request, 'account/product.html', context)


@unauthenticated
@allowedUsers(allowed_role=['admin'])
def create_customer(request):
    customerForm = CustomerForm()
    context = {"customerForm": customerForm, "title": "Create Customer"}
    if request.method == "POST":
        customerForm = CustomerForm(request.POST)
        if customerForm.is_valid():
            customerForm.save()
            return redirect("/")

    return render(request, 'account/customerform.html', context)


@unauthenticated
@allowedUsers(allowed_role=['admin'])
def update_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == "POST":
        customerForm = CustomerForm(request.POST, instance=customer)
        if customerForm.is_valid():
            customerForm.save()
            return redirect("/")
    else:
        customerForm = CustomerForm(instance=customer)
        context = {"customerForm": customerForm,
                   "customer": customer, "title": "Update Customer"}

    return render(request, 'account/update_customer.html', context)


@unauthenticated
@allowedUsers(allowed_role=['admin'])
def create_order(request):
    orderForm = OrderForm()
    context = {"orderForm": orderForm, "title": "Create Order"}
    if request.method == "POST":
        orderForm = OrderForm(request.POST)
        if orderForm.is_valid():
            orderForm.save()
            return redirect("/")

    return render(request, 'account/orderform.html', context)


@unauthenticated
@allowedUsers(allowed_role=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect("/")
    context = {"order": order, "title": "Delete Order"}

    return render(request, 'account/delete_order.html', context)


@unauthenticated
@allowedUsers(allowed_role=['admin'])
def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == "POST":
        customer.delete()
        return redirect("/")
    context = {"customer": customer, "title": "Create Customer"}

    return render(request, 'account/delete_customer.html', context)


@unauthenticated
@allowedUsers(allowed_role=['admin'])
def update_order(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == "POST":
        orderForm = OrderForm(request.POST, instance=order)
        if orderForm.is_valid():
            order.save()
            return redirect("/")
    else:
        orderForm = OrderForm(instance=order)
        context = {"orderForm": orderForm,
                   "order": order, "title": "Update Order"}

    return render(request, 'account/update_order.html', context)


@unauthenticated
def place_order(request, pk):
    customer = Customer.objects.get(id=pk)
    orderForm = OrderForm(initial={"customer": customer})

    if request.method == "POST":
        orderForm = OrderForm(request.POST)
        if OrderForm.is_valid():
            orderForm.save()
            return redirect("/")

    context = {"orderForm": orderForm, "title": "Place Order"}

    return render(request, 'account/orderform.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        userLogin = authenticate(
            request, username=username.lower(), password=password)
        if userLogin is not None:
            login(request, userLogin)
            return redirect("home")
        else:
            messages.info(request, "Username or Password incorrect.")
    context = {"title": "User Login"}
    return render(request, "account/login.html", context)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect("home")

    registerForm = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get("username")
            messages.success(request, "Account created for " + user)

            registerForm = form.save(commit=False)
            registerForm.username = registerForm.username.lower()
            registerForm.save()
            return redirect("loginPage")

    context = {"title": "User Registration", "registerForm": registerForm}
    return render(request, "account/register.html", context)


@unauthenticated
def logoutUser(request):
    logout(request)
    return redirect("loginPage")


@unauthenticated
@allowedUsers(allowed_role=['customer'])
def userPage(request):
    user = request.user
    username = (request.user.username).title()
    order_count = user.customer.order_set.all().count()
    delivered = user.customer.order_set.filter(status="Delivered").count()
    pending = user.customer.order_set.filter(status="Pending").count
    orders = user.customer.order_set.all()

    context = {"title": "Welcome " + username, "pending": pending, "orders": orders,
               "order_count": order_count, "delivered": delivered, "user": user}

    return render(request, 'account/user.html', context)
