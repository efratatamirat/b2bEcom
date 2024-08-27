from django import forms
from .models import Product

#the code bellow is for the displayigng email writing place in the signup page
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from.models import Customer #for considering new users as customers
#the code is till here


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'image', 'price', 'digital', 'quantity')


#the code bellow is for the displayigng email writing place in the signup page

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    tin = forms.CharField(max_length=200, required=True)  # TIN field in the form

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create a Customer object linked to the new User
            customer = Customer(user=user, name=user.username, email=user.email, tin=self.cleaned_data['tin'])
            customer.save()
        return user

#the code is till here













