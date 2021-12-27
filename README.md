Installation Instruction:
1. Create a superuser for yourself.  This is needed for sending a warning email
2. run python manage.py runserver 

Code Structure:
Budget stores all relevant code
a. Templates store HTML for the webpages
b. forms.py store the forms required for user to fill in
c. models.py creates the models we need to store user's information
d. urls.py creates the routes to view different budgeting group
e. views.py renders the page and handles all requests

Requirements:
First Party Packages: sqlite (Django Database), datetime (Email), math (Simple calculations)
Third Party Packages: Django, Django Mail
Classes: 3 classes in Models.py, magic methods: __str__, __getattribute__

Video Demo:
https://youtu.be/525QegCyPvw
