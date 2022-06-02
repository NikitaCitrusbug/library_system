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


class Home(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)


class Dashboard(LoginRequiredMixin,SuccessMessageMixin, View):
    template_name = 'dashboard.html'
    login_url = '/'
    redirect_field_name = 'home'

    def get(self,request):
        # messages.success(request, 'Thank you for the Login ')
        # return redirect('/Dashboard/')
        return render(request, self.template_name)


class BookView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'book/book.html'
    login_url = '/'
    redirect_field_name = 'home'


class BookRetrieve(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'book/book_list.html'
    login_url = '/'
    redirect_field_name = 'home'


class AddBook(LoginRequiredMixin, CreateView):
    model = Book
    form_class = AddForm
    template_name = 'book/add_book.html'
    login_url = '/'
    redirect_field_name = 'home'

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
            return HttpResponse('error')


class BookDetail(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'book/details_book.html'
    login_url = '/'
    redirect_field_name = 'home'

    def get(self, request, pk):
        context = {}
        context['detail'] = Book.objects.get(id=pk)
        context['author'] = Author.objects.filter(book__pk=pk)

        return render(request, self.template_name, context)


class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = UpdateBookForm
    template_name = 'book/update_book.html'
    login_url = '/'
    redirect_field_name = 'home'

    def get_success_url(self):
        return reverse('home')

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
    success_url = "/Dashboard1/"
    login_url = '/'
    redirect_field_name = 'home'


class CategoryView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category/Category.html'
    login_url = '/'
    redirect_field_name = 'home'


class CategoryRetrieve(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category/list_category.html'
    login_url = '/'
    redirect_field_name = 'home'


class CategoryDetail(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'category/details_category.html'
    login_url = '/'
    redirect_field_name = 'home'


class AddCategory(LoginRequiredMixin, CreateView):
    model = Category
    form_class = AddCategoryForm
    template_name = 'category/add_category.html'
    login_url = '/'
    redirect_field_name = 'home'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoryretrieve')
        else:
            return HttpResponse('error')


class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = UpdateCategoryForm
    template_name = 'category/update_category.html'
    login_url = '/'
    redirect_field_name = 'home'

    def get_success_url(self):
        return reverse('home')
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
    success_url = "/Dashboard1/"
    login_url = '/'
    redirect_field_name = 'home'


class AuthorView(LoginRequiredMixin, ListView):
    model = Author
    template_name = 'author/author.html'
    login_url = '/'
    redirect_field_name = 'home'


class AuthorRetrieve(LoginRequiredMixin, ListView):
    model = Author
    template_name = 'author/list_author.html'
    login_url = '/'
    redirect_field_name = 'home'


class AuthorDetail(LoginRequiredMixin, DetailView):
    model = Author
    template_name = 'author/details_author.html'
    login_url = '/'
    redirect_field_name = 'home'

    def get(self, request, pk):
        context = {}
        context['object'] = Author.objects.get(id=pk)
        context['book'] = Book.objects.filter(author__pk=pk)

        return render(request, self.template_name, context)


class AddAuthor(LoginRequiredMixin, CreateView):
    model = Author
    form_class = AddAuthorForm
    template_name = 'author/add_author.html'
    login_url = '/'
    redirect_field_name = 'home'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('authorretrieve')
        else:
            return HttpResponse('error')


class AuthorUpdate(LoginRequiredMixin, UpdateView):
    model = Author
    form_class = UpdateAuthorForm
    template_name = 'author/update_author.html'
    login_url = '/'
    redirect_field_name = 'home'

    def get_success_url(self):
        return reverse('home')

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
    success_url = "/Dashboard1/"
    login_url = '/'
    redirect_field_name = 'home'


class AddIssue(LoginRequiredMixin, CreateView):
    model = IssuedBooks
    form_class = IssuedBooksForm
    template_name = 'issuebook/issue.html'
    login_url = '/'
    redirect_field_name = 'home'

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
            return HttpResponse('error')


class IssueBookRetrieve(LoginRequiredMixin, ListView):
    model = IssuedBooks
    template_name = 'issuebook/list_issue.html'
    login_url = '/'
    redirect_field_name = 'home'

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
    login_url = '/'
    redirect_field_name = 'home'

    def get(self, request, pk):
        context = {}
        context['object'] = IssuedBooks.objects.get(id=pk)
        return render(request, self.template_name, context)


class IssueBookUpdate(LoginRequiredMixin, UpdateView):
    model = IssuedBooks
    form_class = UpdateIssueBookForm
    template_name = 'issuebook/update_issue.html'
    login_url = '/'
    redirect_field_name = 'home'

    def get_success_url(self):
        return reverse('home')


class IssueBookDelete(LoginRequiredMixin, DeleteView):
    model = IssuedBooks
    template_name = 'issuebook/delete_issue.html'
    success_url = "/Dashboard/"
    login_url = '/'
    redirect_field_name = 'home'

# class Contact(View):
#     template_name = 'contact.html'

# def contact(request):
#     return render(request, 'contact.html')


def logout(request):
    return HttpResponseRedirect('/')


@login_required(login_url="/")
def dashboard1(request):
    return render(request, 'dashboard1.html')


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

            messages.success(
                request, 'Thank you for the registration   ' + username)

            return redirect('/Adminsignup')

            # msg = 'Thank you for the registration'
            # return HttpResponse(msg)
        else:
            messages.success(request, 'PLEASE TRY AGAIN...')

            return redirect('/Usersignup')


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




class Login(SuccessMessageMixin, View):
    model = User
    form_class = LoginForm
    template_name = 'login.html'

    def get(self, request):
        form = self.form_class(request.POST)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        username = request.POST['username']
        passw = request.POST['password']
    # print(username,passw)
        pwd = User.objects.get(username=username)
    # a = User.objects.all()
        print('data', pwd)
        password = pwd.password
        valid = check_password(passw, password)

        # if not valid:
        #     return HttpResponse("incorrect password")
        # else:
        if valid:
            user = User.objects.get(username=username)
            

            if user.is_librarian == True:
                    login(request, user)
                    return HttpResponseRedirect('/Dashboard1/')
            else:
                    login(request, user)
                    return HttpResponseRedirect('/Dashboard/')
            
        else:
            messages.success(request, 'PLEASE TRY AGAIN...')
            return redirect('/Login')



@login_required(login_url="/")
def SearchBook(request):
    query = None
    results = []
    if request.method == "GET":
        query = request.GET.get("search")
        results = Book.objects.filter(Q(name__icontains=query))
    return render(request, 'book/search_book.html', {'query': query, 'results': results})


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


@login_required(login_url="/")
def SearchAuthor(request):
    query = None
    results = []
    if request.method == "GET":
        query = request.GET.get("search")
        results = Author.objects.filter(Q(name__icontains=query))
    return render(request, 'author/search_author.html', {'query': query, 'results': results})


@login_required(login_url="/")
def SearchCategory(request):
    query = None
    results = []
    if request.method == "GET":
        query = request.GET.get("search")
        results = Category.objects.filter(Q(name__icontains=query))
    return render(request, 'category/search_category.html', {'query': query, 'results': results})
