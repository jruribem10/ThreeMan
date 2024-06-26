#models.py
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save



class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	date_modified = models.DateTimeField(User, auto_now=True)
	phone = models.CharField(max_length=20, blank=True)
	address1 = models.CharField(max_length=200, blank=True)
	address2 = models.CharField(max_length=200, blank=True)
	city = models.CharField(max_length=200, blank=True)
	state = models.CharField(max_length=200, blank=True)
	zipcode = models.CharField(max_length=200, blank=True)
	country = models.CharField(max_length=200, blank=True)
	old_cart = models.CharField(max_length=200, blank=True, null=True)

	def __str__(self):
		return self.user.username



# Create a user Profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile(user=instance)
		user_profile.save()

# Automate the profile thing
post_save.connect(create_profile, sender=User)





class Category(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'categories'

class Estilos (models.Model):
    estilo=models.CharField(max_length=50)

    def __str__(self):
        return self.estilo

class Customer (models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=15)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=100)
    

    
    def __str__(self):
        return f'{self.first_name}{self.last_name}'

class Product(models.Model):

    AMARGOR_CHOICES = [
        ('Bajo', 'Bajo'),
        ('Medio', 'Medio'),
        ('Alto', 'Alto'),
    ]
    name = models.CharField(max_length=255)
    categories =models.ForeignKey(Category,on_delete=models.CASCADE,default=1)  # Campo correspondiente a 'tipo' en el formulario
    alcohol = models.FloatField()  # Campo correspondiente a 'alcohol' en el formulario
    color = models.CharField(max_length=255)  # Campo correspondiente a 'color' en el formulario
    amargor = models.CharField(max_length=255, choices=AMARGOR_CHOICES)
    descripcion = models.TextField()  # Campo correspondiente a 'descripcion' en el formulario
    price = models.FloatField()  # Campo correspondiente a 'precio' en el formulario
    casa = models.CharField(max_length=255)  # Campo correspondiente a 'casa' en el formulario
    stock = models.FloatField()  # Campo correspondiente a 'stock' en el formulario
    image=models.ImageField(upload_to='uploads/product/')
    
    #add sale
    is_sale=models.BooleanField(default=False)
    sale_price=models.DecimalField(default=0,decimal_places=2,max_digits=6)


    def __str__(self):
        return self.name
    
    def get_discounted_price(self):
        """Returns the sale price if the product is on sale, otherwise returns the regular price."""
        if self.is_sale:
            return self.sale_price
        return self.price

class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    addres=models.CharField(max_length=100, default='', blank=False)
    phone=models.CharField(max_length=15)
    date=models.DateField(default=datetime.datetime.today)
    status=models.BooleanField(default=False)


    def __str__(self):
        return self.product


