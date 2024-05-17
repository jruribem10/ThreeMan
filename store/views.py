from django.shortcuts import render, redirect

from ecom import settings
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
from django.db.models import Q
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from django.utils.translation import gettext as _
from django.shortcuts import redirect
from django.utils import translation


def set_language(request):
    user_language = request.GET.get('language', 'es')
    translation.activate(user_language)
    response = redirect(request.META.get('HTTP_REFERER'))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)
    return response

# Vista para la API
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Vista de filtrado de productos
def filter_products(request):
    selected_color = request.GET.get('color')
    selected_amargor = request.GET.get('amargor')
    selected_in_discount = request.GET.get('is_sale') == 'true'
    
    filtered_products = Product.objects.all()
    
    if selected_color:
        filtered_products = filtered_products.filter(color=selected_color)
        
    if selected_amargor:
        filtered_products = filtered_products.filter(amargor=selected_amargor)
        
    if selected_in_discount:
        filtered_products = filtered_products.filter(is_sale=True)
    
    colors = Product.objects.values_list('color', flat=True).distinct()
    amargors = Product.objects.values_list('amargor', flat=True).distinct()
    
    context = {
        'products': filtered_products,
        'selected_color': selected_color,
        'selected_amargor': selected_amargor,
        'selected_in_discount': selected_in_discount,
        'colors': colors,
        'amargors': amargors
    }
    
    return render(request, 'filtered_products.html', context)

# Vista de búsqueda
def search(request):
    if 'searched' in request.GET:
        searched = request.GET['searched']
        searched_results = Product.objects.filter(name__icontains=searched)
        if not searched_results:
            messages.success(request, _("Ese producto no existe. Por favor, inténtelo de nuevo."))
            return render(request, "search.html", {})
        else:
            return render(request, "search.html", {'searched': searched_results})
    else:
        return render(request, "search.html", {})

# Vista para actualizar información del usuario
def update_info(request):
    if request.user.is_authenticated:
        try:
            current_user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            current_user_profile = Profile(user=request.user)
            current_user_profile.save()

        form = UserInfoForm(request.POST or None, instance=current_user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, _("Your Info Has Been Updated!!"))
            return redirect('home')
        return render(request, "update_info.html", {'form': form})
    else:
        messages.error(request, _("You Must Be Logged In To Access That Page!!"))
        return redirect('home')

# Vista para actualizar contraseña
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, _("Your Password Has Been Updated..."))
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form': form})
    else:
        messages.success(request, _("You Must Be Logged In To View That Page..."))
        return redirect('home')

# Vista para actualizar usuario
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, _("User Has Been Updated!!"))
            return redirect('home')
        return render(request, "update_user.html", {'user_form': user_form})
    else:
        messages.success(request, _("You Must Be Logged In To Access That Page!!"))
        return redirect('home')

# Vista para resumen de categorías
def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories": categories})

# Vista para categoría específica
def category(request, foo):
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except:
        messages.success(request, _("That Category Doesn't Exist..."))
        return redirect('home')

# Vista para producto específico
def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

# Vista de inicio
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

# Vista de "sobre nosotros"
def about(request):
    return render(request, 'about.html')

# Vista para login de usuario
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, _("You have been logged in!"))
            return redirect('home')
        else:
            messages.success(request, _("There was an error logging in"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

# Vista para logout de usuario
def logout_user(request):
    logout(request)
    messages.success(request, _("You have logged out!"))
    return redirect('home')

# Vista para registro de usuario
def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, _("You have been registered successfully!"))
            return redirect('update_info')
    else:
        return render(request, 'register.html', {'form': form})