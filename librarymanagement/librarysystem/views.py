from ast import Return
import http
from multiprocessing import context
from re import template
from unittest import result
from django.shortcuts import get_object_or_404, render

# Create your views here.
from urllib import request
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, TemplateView
from django.shortcuts import render, redirect, reverse
from django import forms
from librarysystem import forms
from django.http import HttpResponse, HttpResponseRedirect
from librarysystem.models import Author, Category, User, AbstractUser, Book , IssuedBooks
from librarysystem.forms import AddForm, CustomMemberCreationForm, CustomUserCreationForm, LoginForm, AddCategoryForm, AddAuthorForm, UpdateBookForm , UpdateAuthorForm , UpdateCategoryForm , IssuedBooksForm , UpdateIssueBookForm
from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.db.models import Q

class Home(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)


class Dashboard(View):
    template_name = 'dashboard.html'

    def get(self, request):
        return render(request, self.template_name)


class BookView(ListView):
    model = Book
    template_name = 'book/book.html'


class BookRetrieve(ListView):
    model = Book
    template_name = 'book/book_list.html'
    

class AddBook(CreateView):
    model = Book
    form_class = AddForm
    template_name = 'book/add_book.html'

    def post(self, request):
        data = request.POST.copy()
        authors = data.pop('authorname')
        form = self.form_class(data)
        if form.is_valid():
            book = form.save()
            for a in authors:
                print(a)
                authors = Author.objects.get(id = a)
                authors.book.add(book)
               
            

            # print(authors)
            # print('msg')
            return redirect('bookretrieve')
        else:
            return HttpResponse('error')

class BookDetail(DetailView):
    model = Book
    template_name = 'book/details_book.html'
   
    def get(self ,request , pk):
            context = {}
            context['detail'] = Book.objects.get(id = pk)
            context['author'] = Author.objects.filter(book__pk = pk )
            
            return render(request , self.template_name , context)
        




class BookUpdate(UpdateView):
    model = Book
    form_class = UpdateBookForm
    template_name = 'book/update_book.html'

    def get_success_url(self):
        return reverse('home')
    
    # def post(self,request , pk):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('bookupdate' , pk)
    #     else:
    #         return HttpResponse('error')


class BookDelete(DeleteView):
    model = Book
    template_name = 'book/delete_book.html'
    success_url = "/Dashboard1/"


class CategoryView(ListView):
    model = Category
    template_name = 'category/Category.html'


class CategoryRetrieve(ListView):
    model = Category
    template_name = 'category/list_category.html'

class CategoryDetail(DetailView):
    model = Category
    template_name = 'category/details_category.html'

class AddCategory(CreateView):
    model = Category
    form_class = AddCategoryForm
    template_name = 'category/add_category.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoryretrieve')
        else:
            return HttpResponse('error')


class CategoryUpdate(UpdateView):
    model = Category
    form_class = UpdateCategoryForm
    template_name = 'category/update_category.html'
    
    def get_success_url(self):
        return reverse('home')
    # def post(self , request , pk):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect('/' , pk)
    #     else:
    #         return HttpResponse('error')

class CategoryDelete(DeleteView):
    model = Category
    template_name = 'category/delete_category.html'
    success_url = "/Dashboard1/"

class AuthorView(ListView):
    model = Author
    template_name = 'author/author.html'



class AuthorRetrieve(ListView):
    model = Author
    template_name = 'author/list_author.html'


class AuthorDetail(DetailView):
    model = Author
    template_name = 'author/details_author.html'

    
    def get(self ,request , pk):
            context = {}
            context['object'] = Author.objects.get(id = pk)
            context['book'] = Book.objects.filter(author__pk = pk )
            
            return render(request , self.template_name , context)
    

class AddAuthor(CreateView):
    model = Author
    form_class = AddAuthorForm
    template_name = 'author/add_author.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('authorretrieve')
        else:
            return HttpResponse('error')



class AuthorUpdate(UpdateView):
    model = Author
    form_class = UpdateAuthorForm
    template_name = 'author/update_author.html'
    
    def get_success_url(self):
        return reverse('home')

    # def post(self , request , pk):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect('/' , pk)
    #     else:
    #         return HttpResponse('error')



class AuthorDelete(DeleteView):
    model = Author
    template_name = 'author/delete_author.html'
    success_url = "/Dashboard1/"


class AddIssue(CreateView):
    model = IssuedBooks
    form_class = IssuedBooksForm
    template_name = 'issuebook/issue.html'
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('issueretrieve')
        else:
            return HttpResponse('error')

class IssueBookRetrieve(ListView):
    model = IssuedBooks
    template_name = 'issuebook/list_issue.html'

    # permission_classes = [isAuthenticated]
    # queryset = Post.objects.all()
    # serializer_class = PostSerializer

    # def get(self ,request , pk):
    #     context = {}
    #     context['name'] = IssuedBooks.objects.get(book= pk)
            
    #     return render(request , self.template_name , context)

class IssueBookDetail(DetailView):
    model = IssuedBooks
    template_name = 'issuebook/details_issue.html'

    def get(self ,request , pk):
            context = {}
            context['object'] = IssuedBooks.objects.get(id = pk)
            
            
            return render(request , self.template_name , context)

class IssueBookUpdate(UpdateView):
    model = IssuedBooks
    form_class = UpdateIssueBookForm
    template_name = 'issuebook/update_issue.html'
    
    def get_success_url(self):
        return reverse('home')

class IssueBookDelete(DeleteView):
    model = IssuedBooks
    template_name = 'issuebook/delete_issue.html'
    success_url = "/Dashboard/"

class Contact(View):
    template_name = 'contact.html'

    def get(self, request):
        return render(request, self.template_name)


def logout(request):
    return HttpResponseRedirect('/')


def dashboard1(request):
    return render(request, 'dashboard1.html')


class SignupAdmin(CreateView):
    model = AbstractUser
    form_class = CustomUserCreationForm
    template_name = 'signup_admin.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/Dashboard1/')
        else:
            msg = 'This account is already exist'
            return HttpResponse(msg)


class SignupMember(CreateView):
    model = User
    form_class = CustomMemberCreationForm
    template_name = 'signup_member.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/Dashboard/')
        else:
            msg = 'This account is already exist'
            return HttpResponse(msg)


class Login(View):
        model = User
        form_class = LoginForm
        template_name = 'login.html'

        def get(self, request):
            form = self.form_class(request.POST)
            return render(request, self.template_name, {'form': form})


        def post(self,request):
            username = request.POST['username']
            passw =request.POST['password']
        # print(username,passw)
            pwd = User.objects.get(username=username)
        # a = User.objects.all()
            print('data',pwd)
            password=pwd.password
            valid = check_password(passw,password)
        
            if not valid:
                return  HttpResponse("incorrect password")

            user=User.objects.get(username=username)
            if user.is_authenticated:

                if user.is_librarian == True:
                    login(request, user)
                    return  HttpResponseRedirect('/Dashboard1/')
                else:
                    login(request,user)
                    return  HttpResponseRedirect('/Dashboard/')
            else:
                msg = "invalid login"
                return HttpResponse(msg)


def SearchBook(request):
    query = None
    results = []
    if request.method == "GET":
        query = request.GET.get("search")
        results = Book.objects.filter(Q(name__icontains = query))
    return render(request , 'book/search_book.html', {'query' : query , 'results' : results})


# class SearchAuthor(View):
#     model = Author
#     template_name = 'author/search_author.html'

    
#     def get(self ,request , name):
#         query = None
#         results = []
#         if request.method == "GET":
#             query = request.GET.get("search")
#             results = Author.objects.filter(Q(name__icontains = query))
#             context = {}
#             context['book'] = Book.objects.filter(author__name = name)
            
#         return render(request , self.template_name , context , {'query' : query , 'results' : results})



def SearchAuthor(request):
    query = None
    results = []
    if request.method == "GET":
        query = request.GET.get("search")
        results = Author.objects.filter(Q(name__icontains = query))
    return render(request , 'author/search_author.html', {'query' : query , 'results' : results})

def SearchCategory(request):
    query = None
    results = []
    if request.method == "GET":
        query = request.GET.get("search")
        results = Category.objects.filter(Q(name__icontains = query))
    return render(request , 'category/search_category.html', {'query' : query , 'results' : results})
