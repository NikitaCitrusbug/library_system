from dataclasses import fields
from multiprocessing.sharedctypes import Value
from tkinter import Widget
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Author, Category, User , Book , IssuedBooks
from django.forms import CharField, TextInput



# class CustomUserCreationForm(forms.ModelForm):
   

#     class Meta():
#         model = User
#         fields = ['username', 'first_name', 'last_name','email']
        
#     def __init__(self, args, *kwargs):
#         super(self).__init__(*args, **kwargs)

#     def clean(self):
#         cleaned_data = super(CustomUserCreationForm, self).clean()
#         username = cleaned_data.get("username")
#         first_name = cleaned_data.get("first_name")
#         last_name = cleaned_data.get("last_name")
#         email = cleaned_data.get("email")
#         password = cleaned_data.get("password")
        
        

#         if not email :
#             raise forms.ValidationError(
#                 "Please add email."
#             )
#         if not password :
#             raise forms.ValidationError(
#                 "Please add Password."
#             )
#         if not last_name :
#             raise forms.ValidationError(
#                 "Please add last name."
#             )
#         if not first_name :
#             raise forms.ValidationError(
#                 "Please add first name."
#             )
#         if not username :
#             raise forms.ValidationError(
#                 "Please add user name."
#             )
#     def save(self, commit=True):
#         instance = super().save(commit=False)

#         if commit:
#             instance.save()

#         return instance



class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name','email']
    
    def save(self,commit=True):
        user = super().save(commit=False)
        user.is_librarian = True
        if commit:
            user.save()
        return user


class CustomMemberCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name','email']

    def save(self,commit=True):
        user = super().save(commit=False)
        user.is_member = True
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

# class LoginForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ['username' , 'password']



class AddForm(forms.ModelForm):
    authorname = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple ,queryset=Author.objects.all(), required=False)
    
    
    class Meta:
        model = Book
        fields = ['name' , 'discription' , 'quantity' , 'category' , 'authorname']
        
                
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}),
            'discription':forms.TextInput(attrs={'class':'form-control','placeholder':'Discription'}),
            'quantity':forms.NumberInput(attrs={'class':'form-control','placeholder':'quantity'}),
            'category':forms.Select(attrs={'class':'form-control form-select','placeholder':'select category'}),
            'authorname':forms.Select(attrs={'class':'form-control form-select','placeholder':'select author'}),
            
           
        }


class UpdateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class UpdateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name' , 'discription']

class UpdateAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name' , 'discription']

# class DateInput(forms.DateInput):
#     input_type = 'date'

# class IssuedBooksForm(forms.ModelForm):
#     class Meta:
#         model = IssuedBooks
#         fields = '__all__'
#     widgets = {
#         'return_date' : DateInput(),
#         'issued_date': DateInput(),
#         'issued_date' : forms.HiddenInput(),

#     }
class IssuedBooksForm(forms.ModelForm):
    
    return_date = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=['%d/%m/%Y']
    )
    
    charge_per_day = CharField( widget=TextInput(attrs={'type': 'number'}))
    class Meta():
    
        model = IssuedBooks
        fields = ['book' , 'user_name','user_email' , 'user_address' , 'return_date' , 'charge_per_day']
       


class UpdateIssueBookForm(forms.ModelForm):
    class Meta:
        model = IssuedBooks
        fields = ['book' , 'user_name','user_email' , 'user_address' , 'return_date' , 'charge_per_day']
        
