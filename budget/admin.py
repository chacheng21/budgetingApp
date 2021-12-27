from django.contrib import admin
from .models import Group, Expense, Category
# Register your models here.

admin.site.register(Group)
admin.site.register(Expense)
admin.site.register(Category)