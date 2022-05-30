from dataclasses import fields
from multiprocessing.sharedctypes import Value
from tkinter import Widget
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Author, Category, User , Book , IssuedBooks
from django.forms import CharField, TextInput




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



class LoginForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username' , 'password']



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
        fields = '__all__'

class UpdateAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

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
        fields = '__all__'
        def __str__(self):
            return self.user_name
        def save(self, *args, **kwargs):
            self.user_name = self.user_name.book()
            if self.return_date != None:
                days = self.return_date - self.issued_date
                self.total_charge = days.days * self.charge_per_day
            return super(IssuedBooks, self).save(*args, **kwargs)


class UpdateIssueBookForm(forms.ModelForm):
    class Meta:
        model = IssuedBooks
        fields = '__all__'
