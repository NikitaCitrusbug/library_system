from ast import Return
from email import message
import http
from multiprocessing import context
from pyexpat.errors import messages
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
from librarysystem.models import Author, Category, User, AbstractUser, Book, IssuedBooks
from librarysystem.forms import AddForm, CustomMemberCreationForm, CustomUserCreationForm, LoginForm, AddCategoryForm, AddAuthorForm, UpdateBookForm, UpdateAuthorForm, UpdateCategoryForm, IssuedBooksForm, UpdateIssueBookForm
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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.messages import constants as messages
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import logout
from django.contrib.auth.models import auth


class Home(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)


class Dashboard(LoginRequiredMixin,SuccessMessageMixin, View):
    template_name = 'dashboard.html'
    login_url = '/Login'
    redirect_field_name = 'login'

    def get(self,request):
        # messages.success(request, 'Thank you for the Login ')
        # return redirect('/Dashboard/')
        return render(request, self.template_name)

# @login_required(login_url="/")
# def dashboard1(request):
#     return render(request, 'dashboard1.html')

class AdminDashboard(LoginRequiredMixin,SuccessMessageMixin, View):
    template_name = 'dashboard1.html'
    login_url = '/Login'
    redirect_field_name = 'login'

    def get(self,request):
        # messages.success(request, 'Thank you for the Login ')
        # return redirect('/Dashboard/')
        return render(request, self.template_name)


class BookView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'book/book.html'
    login_url = 'Login'
    redirect_field_name = 'login'


class BookRetrieve(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'book/book_list.html'
    login_url = '/Login'
    redirect_field_name = 'login'


class AddBook(LoginRequiredMixin, CreateView):
    model = Book
    form_class = AddForm
    template_name = 'book/add_book.html'
    login_url = '/Login'
    redirect_field_name = 'login'

    def post(self, request):
        data = request.POST.copy()
        authors = data.pop('authorname')
        form = self.form_class(data)
        if form.is_valid():
            book = form.save()
            for a in authors:
                print(a)
                authors = Author.objects.get(id=a)
                authors.book.add(book)

            # print(authors)
            # print('msg')
            return redirect('bookretrieve')
        else:
            return redirect('login')


class BookDetail(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'book/details_book.html'
    login_url = '/Login'
    redirect_field_name = 'login'

    def get(self, request, pk):
        context = {}
        context['detail'] = Book.objects.get(id=pk)
        context['author'] = Author.objects.filter(book__pk=pk)

        return render(request, self.template_name, context)


class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = UpdateBookForm
    template_name = 'book/update_book.html'
    login_url = '/Login'
    redirect_field_name = 'login'

    def get_success_url(self):
        return reverse('bookretrieve')

    # def post(self,request , pk):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('bookupdate' , pk)
    #     else:
    #         return HttpResponse('error')


class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'book/delete_book.html'
    success_url = "/AdminDashboard/"
    login_url = '/Login'
    redirect_field_name = 'login'


class CategoryView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category/Category.html'
    login_url = 'Login'
    redirect_field_name = 'login'


class CategoryRetrieve(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category/list_category.html'
    login_url = '/Login'
    redirect_field_name = 'login'


class CategoryDetail(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'category/details_category.html'
    login_url = '/Login'
    redirect_field_name = 'login'


class AddCategory(LoginRequiredMixin, CreateView):
    model = Category
    form_class = AddCategoryForm
    template_name = 'category/add_category.html'
    login_url = '/Login'
    redirect_field_name = 'login'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoryretrieve')
        else:
            return redirect('login')


class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = UpdateCategoryForm
    template_name = 'category/update_category.html'
    login_url = '/Login'
    redirect_field_name = 'login'

    def get_success_url(self):
        return reverse('categoryretrieve')
    # def post(self , request , pk):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect('/' , pk)
    #     else:
    #         return HttpResponse('error')


class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'category/delete_category.html'
    success_url = "/AdminDashboard/"
    login_url = '/Login'
    redirect_field_name = 'login'


class AuthorView(LoginRequiredMixin, ListView):
    model = Author
    template_name = 'author/author.html'
    login_url = '/Login'
    redirect_field_name = 'login'


class AuthorRetrieve(LoginRequiredMixin, ListView):
    model = Author
    template_name = 'author/list_author.html'
    login_url = '/Login'
    redirect_field_name = 'login'


class AuthorDetail(LoginRequiredMixin, DetailView):
    model = Author
    template_name = 'author/details_author.html'
    login_url = '/Login'
    redirect_field_name = 'login'

    def get(self, request, pk):
        context = {}
        context['object'] = Author.objects.get(id=pk)
        context['book'] = Book.objects.filter(author__pk=pk)

        return render(request, self.template_name, context)


class AddAuthor(LoginRequiredMixin, CreateView):
    model = Author
    form_class = AddAuthorForm
    template_name = 'author/add_author.html'
    login_url = '/Login'
    redirect_field_name = 'login'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('authorretrieve')
        else:
            return redirect('login')


class AuthorUpdate(LoginRequiredMixin, UpdateView):
    model = Author
    form_class = UpdateAuthorForm
    template_name = 'author/update_author.html'
    login_url = '/Login'
    redirect_field_name = 'login'

    def get_success_url(self):
        return reverse('authorretrieve')

    # def post(self , request , pk):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect('/' , pk)
    #     else:
    #         return HttpResponse('error')


class AuthorDelete(LoginRequiredMixin, DeleteView):
    model = Author
    template_name = 'author/delete_author.html'
    success_url = "/AdminDashboard/"
    login_url = '/Login'
    redirect_field_name = 'login'


class AddIssue(LoginRequiredMixin, CreateView):
    model = IssuedBooks
    form_class = IssuedBooksForm
    template_name = 'issuebook/issue.html'
    login_url = '/Login'
    redirect_field_name = 'login'

    # def get(self ,request , pk):
    #         context = {}
    #         context['charges'] = IssuedBooks.objects.get(id = pk)

    #         return render(request , self.template_name , context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('issueretrieve')
        else:
            return redirect('login')


class IssueBookRetrieve(LoginRequiredMixin, ListView):
    model = IssuedBooks
    template_name = 'issuebook/list_issue.html'
    login_url = '/Login'
    redirect_field_name = 'login'

    # permission_classes = [isAuthenticated]
    # queryset = Post.objects.all()
    # serializer_class = PostSerializer

    # def get(self ,request , pk):
    #     context = {}
    #     context['name'] = IssuedBooks.objects.get(book= pk)

    #     return render(request , self.template_name , context)


class IssueBookDetail(LoginRequiredMixin, DetailView):
    model = IssuedBooks
    template_name = 'issuebook/details_issue.html'
    login_url = '/Login'
    redirect_field_name = 'login'

    def get(self, request, pk):
        context = {}
        context['object'] = IssuedBooks.objects.get(id=pk)
        return render(request, self.template_name, context)


class IssueBookUpdate(LoginRequiredMixin, UpdateView):
    model = IssuedBooks
    form_class = UpdateIssueBookForm
    template_name = 'issuebook/update_issue.html'
    login_url = '/Login'
    redirect_field_name = 'login'

    def get_success_url(self):
        return reverse('issueretrieve')


class IssueBookDelete(LoginRequiredMixin, DeleteView):
    model = IssuedBooks
    template_name = 'issuebook/delete_issue.html'
    success_url = "/Dashboard/"
    login_url = '/Login'
    redirect_field_name = 'login'

# class Contact(View):
#     template_name = 'contact.html'

# def contact(request):
#     return render(request, 'contact.html')

# def logout_view(request):
#     logout(request)
    
#     return HttpResponseRedirect('/Login')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/Login')



# class SignupAdmin(CreateView):
#     """View to create User"""

#     model = User
#     form_class = CustomUserCreationForm
#     template_name = 'signup_admin.html'
#     # permission_required = ("customadmin.add_user",)

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         # kwargs["user"] = self.request.user

#         return kwargs

#     def get_success_url(self):
#         # opts = self.model._meta
#         return redirect('/Adminsignup')

class SignupAdmin(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'signup_admin.html'

    def post(self, request):
        print(request.POST)
        form = self.form_class(request.POST)
        print(form, '[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[')
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            messages.success(
                request, 'Thank you for the registration   ' + username)

            return redirect('/Adminsignup')

            # msg = 'Thank you for the registration'
            # return HttpResponse(msg)
        else:
            messages.success(request, 'This account is already exist...')

            return redirect('/Adminsignup')


class SignupMember(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomMemberCreationForm
    template_name = 'signup_member.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, 'Thank you for the registration   ' + username)

            return redirect('/Usersignup')
        else:
            messages.success(request, 'PLEASE TRY AGAIN...')

            return redirect('/Usersignup')


class Login(SuccessMessageMixin ,View):
    model = User
    template_name = 'login.html'   
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        
        
        if request.method == "POST" and form.is_valid():
            uname = form.cleaned_data['username']
            password = form.cleaned_data['password']
            una = request.POST['username']
            ps = request.POST['password']
            user =  auth.authenticate(username=uname,password=password)
            if user is not None:
                if user.is_librarian == True:
                    auth.login(request,user)
                    return HttpResponseRedirect('/AdminDashboard/')
                else:
                    auth.login(request,user)
                    return HttpResponseRedirect('/Dashboard/')
                
            else:
                messages.success(request, 'PLEASE TRY AGAIN...')
                return redirect('/Login')
                
                
        else:
            messages.success(request, 'TRY AGAIN...')
            return redirect('/Login')






# class Login(SuccessMessageMixin, View):
#     model = User
#     form_class = LoginForm
#     template_name = 'login.html'

#     def get(self, request):
#         form = self.form_class(request.POST)
#         return render(request, self.template_name, {'form': form})

#     def post(self, request):
#         username = request.POST['username']
#         passw = request.POST['password']
#     # print(username,passw)
#         pwd = User.objects.get(username=username)
#     # a = User.objects.all()
#         print('data', pwd)
#         password = pwd.password
#         valid = check_password(passw, password)

#         if valid:
#             user = User.objects.get(username=username)
            

#             if user.is_librarian == True:
#                     login(request, user)
#                     return HttpResponseRedirect('/AdminDashboard/')
#             else:
#                     login(request, user)
#                     return HttpResponseRedirect('/Dashboard/')
            
#         else:
#             messages.success(request, 'PLEASE TRY AGAIN...')
#             return redirect('/Login')


class SearchBook(LoginRequiredMixin, TemplateView):
    model = Book
    template_name = 'book/search_book.html'
    login_url = '/Login'
    redirect_field_name = 'login'

    def get(self ,request):
        query = None
        results = []
        if request.method == "GET":
            query = request.GET.get("search")
            results = Book.objects.filter(Q(name__icontains=query))
        return render(request, self.template_name, {'query': query, 'results': results})


class SearchAuthor(LoginRequiredMixin, TemplateView):
    model = Book
    template_name = 'author/search_author.html'
    login_url = '/Login'
    redirect_field_name = 'login'

    def get(self ,request):
        query = None
        results = []
        if request.method == "GET":
            query = request.GET.get("search")
            results = Author.objects.filter(Q(name__icontains=query))
        return render(request, self.template_name, {'query': query, 'results': results})

class SearchCategory(LoginRequiredMixin, TemplateView):
    model = Category
    template_name = 'category/search_category.html'
    login_url = '/Login'
    redirect_field_name = 'login'

    def get(self ,request):
        query = None
        results = []
        if request.method == "GET":
            query = request.GET.get("search")
            results = Category.objects.filter(Q(name__icontains=query))
        return render(request, self.template_name, {'query': query, 'results': results})

# @login_required(login_url="/")
# def SearchBook(request):
#     query = None
#     results = []
#     if request.method == "GET":
#         query = request.GET.get("search")
#         results = Book.objects.filter(Q(name__icontains=query))
#     return render(request, 'book/search_book.html', {'query': query, 'results': results})


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


# @login_required(login_url="/")
# def SearchAuthor(request):
#     query = None
#     results = []
#     if request.method == "GET":
#         query = request.GET.get("search")
#         results = Author.objects.filter(Q(name__icontains=query))
#     return render(request, 'author/search_author.html', {'query': query, 'results': results})


# @login_required(login_url="/")
# def SearchCategory(request):
#     query = None
#     results = []
#     if request.method == "GET":
#         query = request.GET.get("search")
#         results = Category.objects.filter(Q(name__icontains=query))
#     return render(request, 'category/search_category.html', {'query': query, 'results': results})
