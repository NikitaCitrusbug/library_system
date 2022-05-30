
from django.contrib import admin
from .models import  Book , Category , Author , IssuedBooks , User
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User role',
            {
                'fields':(
                    'is_librarian',
                )
            }
        )
    )



admin.site.register(User , CustomUserAdmin)
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(IssuedBooks)