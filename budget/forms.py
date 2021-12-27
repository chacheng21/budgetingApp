from django import forms

# Expense fields required for user to fill in
class ExpenseForm(forms.Form):
    expense_name = forms.CharField()
    amount = forms.DecimalField()
    category = forms.CharField()

# Group fields required for user to fill in.  Slug gets generated from group_name
class GroupForm(forms.Form):
    group_name = forms.CharField()
    budget = forms.IntegerField()
