
from enum import auto
from tkinter import CASCADE
from unicodedata import category
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.forms import CharField, TextInput
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
    return_date = models.DateField()
    charge_per_day = models.PositiveIntegerField()
    total_charge = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.user_name

    @property
    def Total_charges(self):
        
        # days = self.return_date.date()
        
        # return days
        cpd = self.charge_per_day
        days = self.return_date - self.issued_date
        print(days.days)
        total_charge = days.days * cpd
        return total_charge


    # def save(self, *args, **kwargs):
    #     self.user_name = self.user_name.title()
    #     if self.return_date != None:
    #         days = self.return_date - self.issued_date
    #         self.total_charge = days.days * self.charge_per_day
    #     return super(IssuedBooks, self).save(*args, **kwargs)
