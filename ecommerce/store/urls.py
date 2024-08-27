from django.urls import path, include
from django.contrib.auth import views as auth_views
#from .views import home, authView
from .views import authView
from . import views


urlpatterns = [
    #the function bellow handels the signup page
    path("store/", views.store, name="store"),
    #path("home/", views.home, name="home"),
    path("", authView, name="authView"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),
    #till here

    #code bellow is the store and everything else, from here
    
    #Leave as empty string for base url
	#path('store/', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),

	path('process_order/', views.processOrder, name="process_order"),
    #the code it till here
   
    #the code bellow is for making the admin side
     path('home/', views.addProduct, name='home'),
     path('product_delete/<int:pk>', views.product_delete, name='product-delete'),
     #the code is till here

     #the code bellow is for the admin side customer data displaying

     path('data_table/', views.data_table, name='data_table'),


     #the code is till here

     ############################################################################################################################################################3
     #THIS IS THE HOME PAGE OF THE WHOLE COMPANY

     path('company_home_page/', views.company_home_page, name='company_home_page'),





]

 


#first superuser
#lauda
#efratatamirat@gmail.com
#password:  
'''
THIS IS YOUR MAIN SUPERUSER

the one after forgeting the above password
niki
efratatamirat@gmail.com
passniki£$%
'''

#this is the second user for an example
#username
#userpass123

#lookbelmar
#
#poss)3984h

#bomer
#nommer@gmail.com
#voodooshit@£123

'''
superuser:maashi
email:mashit@gmail.com
password:mahti:2341@
'''

#milki
#milki3@gmail.com
#milipassqword@

'''
malli
maloshoud@gmail.com
mollidoss@345$
'''
'''
when i logout in the admin page the default one and login with the super user 
i created in the application i am building it gets in but it considered as a guest user
but wehn i let it and then login in the admin page it gets in but ehrn i get back to my application ad refresh
it gives an erorr that says user has no customer.
but all of this go away when i login with the super user that i made early in the begining of making the application
'''

