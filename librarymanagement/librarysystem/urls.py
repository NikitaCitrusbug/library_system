from django.urls import path,include
from django.views.generic import TemplateView
from . import views
from .views import  AddAuthor, BookRetrieve, Home , SignupAdmin , SignupMember , Login , Dashboard , CategoryView, BookView, AddIssue, AuthorView ,AddBook , AddCategory , AddAuthor , AuthorRetrieve , CategoryRetrieve , IssueBookRetrieve 
from .models import *
from django import forms
from django.contrib.auth import views as auth_views 


urlpatterns = [
    path('',Home.as_view() , name = "home"),
    
    path('Adminsignup',SignupAdmin.as_view(), name = 'adminsignup'),
    path('Usersignup',SignupMember.as_view(), name = 'membersignup'),
    path('Login',Login.as_view(),name='login'),
    path('Dashboard/',Dashboard.as_view() , name = "dashboard"),
    
    path('Issuedbook/',AddIssue.as_view() , name = "issuedbook"),
    path('Author/',AuthorView.as_view() , name = "author"),
    # path('ContactUs',Contact.as_view() , name = "contactus"),
    path('Book/',BookView.as_view() , name = "book"),
    path('Category/',CategoryView.as_view() , name = "category"),

    path('Addbook/',AddBook.as_view() , name = "addbook"),
    path('Addcategory/',AddCategory.as_view() , name = "addcategory"),
    path('Addauthor/',AddAuthor.as_view() , name = "addauthor"),
 


    path('retrievebook/',BookRetrieve.as_view() , name = "bookretrieve"),
    path('retrieveauthor/',AuthorRetrieve.as_view() , name = "authorretrieve"),
    path('retrievecategory/',CategoryRetrieve.as_view() , name = "categoryretrieve"),
    path('retrieveissue/',IssueBookRetrieve.as_view(),name="issueretrieve"),

    path('bookdetail/<int:pk>', views.BookDetail.as_view(), name = 'bookdetail'),
    path('authordetail/<int:pk>', views.AuthorDetail.as_view(), name = 'authordetail'),
    path('categorydetail/<int:pk>', views.CategoryDetail.as_view(), name = 'categorydetail'),
    path('issuedetail/<int:pk>', views.IssueBookDetail.as_view() , name = 'issuebookdetail'),

    path('<int:pk>/bookupdate/', views.BookUpdate.as_view(), name = 'bookupdate'),
    path('<int:pk>/authorupdate/', views.AuthorUpdate.as_view(), name = 'authorupdate'),
    path('<int:pk>/categoryupdate/', views.CategoryUpdate.as_view(), name = 'categoryupdate'),
    path('<int:pk>/issueupdate/', views.IssueBookUpdate.as_view(), name = 'issuebookupdate'),


    
    path('<int:pk>/bookdelete/', views.BookDelete.as_view(), name = 'bookdelete'),
    path('<int:pk>/authordelete/', views.AuthorDelete.as_view(), name = 'authordelete'),
    path('<int:pk>/categorydelete/', views.CategoryDelete.as_view(), name = 'categorydelete'),
    path('<int:pk>/issuedelete/', views.IssueBookDelete.as_view(), name = 'issuebookdelete'),


    path('Searchbook/', views.SearchBook, name = 'book_search'),
    path('Searchauthor/', views.SearchAuthor, name = 'author_search'),
    path('Searchcategory/', views.SearchCategory, name = 'category_search'),
 

    
    
    path('Dashboard1/' ,views.dashboard1, name = 'dashboard1'),
    path('Logout/',views.logout, name = 'logout'),
    # path('ContactUs/',views.contact, name = 'contactus'),
    
    
]
