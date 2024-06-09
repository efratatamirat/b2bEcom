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





]

 

