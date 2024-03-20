from django.shortcuts import render,redirect
from.models import Product,Category,Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,UpdateUserForm,ChangePasswordForm,UserInfoForm
from django import forms
# Create your views here.




def filter_products(request):
    # Obtener los parámetros del filtro del request GET
    color = request.GET.get('color')
    alcohol = request.GET.getlist('alcohol')
    amargor = request.GET.getlist('amargor')
    
    # Filtrar productos basados en los parámetros
    filtered_products = Product.objects.all()
    if color:
        filtered_products = filtered_products.filter(color=color)
    if alcohol:
        filtered_products = filtered_products.filter(alcohol__in=alcohol)
    if amargor:
        filtered_products = filtered_products.filter(amargor__in=amargor)
    
    # Renderizar el template con los productos filtrados
    return render(request, 'filtered_products.html', {'products': filtered_products})



def search(request):
    # Determine if they submitted the form
    if 'searched' in request.GET:
        searched = request.GET['searched']
        # Query the Products DB Model
        searched_results = Product.objects.filter(name__icontains=searched)
        # Test for empty query results
        if not searched_results:
            messages.success(request, "Ese producto no existe. Por favor, inténtelo de nuevo.")
            return render(request, "search.html", {})
        else:
            return render(request, "search.html", {'searched': searched_results})
    else:
        return render(request, "search.html", {})


def update_info(request):
	if request.user.is_authenticated:
		# Get Current User
		current_user = Profile.objects.get(user__id=request.user.id)
		# Get Current User's Shipping Info
		#shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		
		# Get original User Form
		form = UserInfoForm(request.POST or None, instance=current_user)
		# Get User's Shipping Form
		#shipping_form = ShippingForm(request.POST or None, instance=shipping_user)		
		if form.is_valid(): #or shipping_form.is_valid():
			# Save original form
			form.save()
			# Save shipping form
			#shipping_form.save()

			messages.success(request, "Your Info Has Been Updated!!")
			return redirect('home')
		return render(request, "update_info.html", {})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')


def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated...")
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')



def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request, current_user)
			messages.success(request, "User Has Been Updated!!")
			return redirect('home')
		return render(request, "update_user.html", {'user_form':user_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')

def category_summary(request):
	categories = Category.objects.all()
	return render(request, 'category_summary.html', {"categories":categories})	



def category(request, foo):
	# Replace Hyphens with Spaces
	foo = foo.replace('-', ' ')
	# Grab the category from the url
	try:
		# Look Up The Category
		category = Category.objects.get(name=foo)
		products = Product.objects.filter(category=category)
		return render(request, 'category.html', {'products':products, 'category':category})
	except:
		messages.success(request, ("That Category Doesn't Exist..."))
		return redirect('home')


def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})



def home(request):
    products=Product.objects.all()
    return render(request, 'home.html',{'products':products})

def about(request):
    return render(request, 'about.html', )


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Has sido logeado")
            return redirect('home')
        else:
            messages.success(request, "Hubo un error")
            return redirect('login')
    else:
        return render(request, 'login.html', {})



def logout_user(request):
    logout(request)
    messages.success(request, (" Has salido de la pagina"))
    return redirect('home')


def register_user(request):
    form=SignUpForm()
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            
            user=authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, (" Ha sido registrado con extio"))
            return redirect('update_info')

    else:
        return render(request, 'register.html',{'form':form} )
    

