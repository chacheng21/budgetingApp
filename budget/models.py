from django.db import models
from django.utils.text import slugify
from django.utils import timezone


# Create your models here.

'''
Group model stores a bunch of different expenses under one single group.  
It consists of 3 fields: group_name, budget, slug.  The slug is what's 
used to generate the link to a group's details.
'''
class Group(models.Model):
    group_name = models.CharField(max_length = 100)
    budget = models.IntegerField()
    warning_amount = models.IntegerField(default = 10)
    slug = models.SlugField(max_length = 100, unique = True, blank = True)

    # When group gets created, create the slug with slugify method
    def save(self, *args, **kwargs):
        self.slug = slugify(self.group_name)
        super(Group, self).save(*args, **kwargs)

    # calculate budget remaining 
    def budget_remaining(self):
        expenses = Expense.objects.filter(group = self)
        if expenses == None or len(expenses) == 0:
            return self.budget
        total_spent = 0
        for expense in expenses:
            total_spent += expense.amount

        return self.budget - total_spent

    # returns name of group (simpler for admin viewing)
    def __str__(self):
        return self.group_name

    # returns number of expenses made for a given group
    def __len__(self):
        return len(Expense.objects.filter(group = self))

    def __getattribute__(self, __name):
        return super().__getattribute__(__name)


'''
A user can break down their expenses into different categories 
within a same group.  Therefore, a category is attached to a group.  
There are 2 fields: the name of a category, and the group it is
attached to.

Example Relationships: School -> Stationery // School -> Books
'''
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.category_name

    def __getattribute__(self, __name):
        return super().__getattribute__(__name)


'''
An expense can be viewed as a single transaction.  It consists 
of the expense name, the amount, the group, the category, and 
the date of the expense.

'''
class Expense(models.Model):
    expense_name =  models.CharField(max_length = 100)
    amount = models.DecimalField(decimal_places=2, max_digits=6)
    group = models.ForeignKey(Group, on_delete = models.CASCADE, related_name = 'expenses')
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    created = models.DateTimeField(editable = False, default = timezone.now())

    def __str__(self):
        return self.expense_name

    def __getattribute__(self, __name):
        return super().__getattribute__(__name)

