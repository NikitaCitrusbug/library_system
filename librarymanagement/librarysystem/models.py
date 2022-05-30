
from enum import auto
from tkinter import CASCADE
from unicodedata import category
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    is_librarian = models.BooleanField(default=False)
    is_member = models.BooleanField(default=True)



class Category(models.Model):
    name = models.CharField(max_length= 20)
    
    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length = 50)
    discription = models.TextField(max_length=500)
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category , on_delete= models.CASCADE)
    
    def __str__(self):
        return self.name




class Author(models.Model):
    name = models.CharField(max_length = 50)
    discription = models.TextField(max_length = 500)
    book = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

class IssuedBooks(models.Model):
    book = models.ForeignKey(Book , on_delete=models.CASCADE)
    user_name = models.CharField(max_length = 20)
    user_email = models.EmailField()
    user_address = models.TextField(max_length = 50)
    issued_date = models.DateTimeField(auto_now=True)
    return_date = models.DateTimeField()
    charge_per_day = models.PositiveIntegerField()
    total_charge = models.PositiveIntegerField()

    def __str__(self):
        return self.user_name
