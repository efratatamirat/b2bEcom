from django.db import models
from django.contrib.auth.models import User #it is the default django user model

#the code bellow is for the admin side

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

#the code is till here


# Create your models here.
#when you are building the admin side so that the admin can see everything 
#come here and see the code and the second video of the video list of making the store
#YOU ALSO FORGOT TO CUSTOMER IN THE ERD MODEL SO DO THAT!!! 
# The user and customer have a one to one relationship
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200)
    def __str__(self):

        return self.name
    


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    digital = models.BooleanField(default=False,null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    #the requirments for adding an image field are 
# explained in the second video of the store how install pillow and evrything
    def __str__(self):
        return self.name



    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

 
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

#the code bellow is for if the product that was added to the cart is digital 
#and not phisycal it makes the shiping address form field invisible in the chekout page
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()

        for i in orderitems:
            if i.product.digital == False:
                shipping = True
                break  
        return shipping  


    #the code is till here

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

#the code bellow is for the admin side


#class Products(models.Model):
 #   name = models.CharField(max_length=100)
  #  image = models.ImageField(upload_to='product_images/')
   # price = models.DecimalField(max_digits=10, decimal_places=2)

#the code is till here