__Installation Instruction__:
1. Create a superuser for yourself.  This is needed for sending a warning email
2. run 
   ```.sh
   python manage.py runserver 
   ```
__Code Structure__:

Budget directory stores all relevant code:
1. templates store HTML for the webpages 
2. forms.py store the forms required for user to fill in
3. models.py creates the models we need to store user's information
4. urls.py creates the routes to view different budgeting group
5. views.py renders the page and handles all requests

__Requirements__:

First Party Packages: sqlite (Django Database), datetime (Email), math (Simple calculations) 

Third Party Packages: Django, Django Mail

Classes: 3 classes in Models.py, magic methods: __str__, __getattribute__

__Video Demo__:

https://youtu.be/525QegCyPvw
