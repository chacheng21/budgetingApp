from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .models import Group, Category, Expense
from django.views.generic import CreateView
from django.utils.text import slugify
from django.contrib.auth.models import User
from .forms import ExpenseForm
from django.core.mail import send_mail
from budgeting_app.settings import EMAIL_HOST_USER
from datetime import datetime


# Create your views here.

# Render homepage to view all groups
def group_list(req):
    group_list = Group.objects.all()
    return render(req, 'budget/group_list.html', {'groups': group_list})


''' Render page to view a single group.  If spending exceeds 
your budget, or your budget goes down to less than the 
specified warning amount (default 10), the 
user will be sent an email to warn them of this.
'''
def group_details(req, group_slug):
    # Get the group object by searching the slug
    group = get_object_or_404(Group, slug = group_slug)

    # Runs user adds an expense
    if req.method == 'POST' and 'expense_name' in req.POST:
        form = ExpenseForm(req.POST)
        if form.is_valid():
            print('reached')
            expense_name = form.cleaned_data['expense_name']
            amount = form.cleaned_data['amount']
            category_name = form.cleaned_data['category']

            # Sends email to the superuser (user of the budget web app)
            superuser_email = list(User.objects.filter(is_superuser=True).values_list('email', flat=True))

            # Get date string to add to email for sending to user
            current_time = datetime.now()
            dt_string = current_time.strftime("%d/%m/%Y %H:%M:%S")

            # Send email anytime user goes over budget, even after going over budget multiple times
            if (group.budget_remaining() - amount) < 0:
                send_mail(
                    dt_string + '// WARNING: You are spending over budget for ' + group.group_name,
                    'Hello User, \nWith your new spending on ' + expense_name + ', you will be over budget by: ' + str(abs(group.budget_remaining() - amount)),
                    EMAIL_HOST_USER,
                    superuser_email,
                    fail_silently = False
                )
            # Send email anytime user's budget is low
            elif (group.budget_remaining() - amount) < group.warning_amount:
                send_mail(
                    dt_string + '// WARNING: You are on course to spend over budget for ' + group.group_name,
                    'Hello User, \nYou are on course to spend over budget for ' + expense_name +
                    '.  You currently have ' + str(abs(group.budget_remaining() - amount)) + ' remaining.',
                    EMAIL_HOST_USER,
                    superuser_email,
                    fail_silently=False
                )

            category = get_object_or_404(Category, group = group, category_name = category_name)

            Expense.objects.create(
                group = group,
                expense_name = expense_name,
                amount = amount,
                category = category,
            ).save()
        else:
            print(form.errors)
    # Runs user adds a category
    elif req.method == 'POST' and 'categories' in req.POST:
        print(req.POST)
        categories = [x.strip() for x in ((req.POST['categories']).split(','))]
        for category in categories:
            Category.objects.create(
                group=Group.objects.get(id=group.id),
                category_name=category
            ).save()
    # Runs otherwise to render page
    elif req.method == 'GET':
        category_list = Category.objects.filter(group = group)
        expense_list = (group.expenses.all().order_by('created')).reverse()

        return render(req, 'budget/group_detail.html', {'group': group, 'expense_list': expense_list, 'category_list': category_list})

    return HttpResponseRedirect(group_slug)
    

# Render page to create a new group
class GroupView(CreateView):
    model = Group
    template_name = 'budget/add_group.html'
    fields = ['group_name', 'budget', 'warning_amount']

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.save()

        categories = [x.strip() for x in ((self.request.POST['categories']).split(','))]
        for category in categories:
            Category.objects.create(
                group = Group.objects.get(id = self.object.id),
                category_name = category
            ).save()
        
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return slugify(self.request.POST['group_name'])
