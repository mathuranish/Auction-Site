# Auction-Site
This is a simple Auctioning site designed using Django that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

Live: 
https://auction-django-app.herokuapp.com/


## Setup
Requires Python3 and the package installer for Python (pip) to run:

* Install requirements (Django4): `pip install -r requirements.txt`
* After cloning the repository, refer to the project folder and:
  1. Create new migrations based on the changes in models: `python3 manage.py makemigrations`
  2. Apply the migrations to the database: `python3 manage.py migrate`
  3. Create a superuser to be able to use Django Admin Interface: `python3 manage.py createsuperuser`
  4. Run the app locally: `python3 manage.py runserver`
  5. Visit the site: `http://localhost:8000`
  6. Enjoy!

## Topics
Built with [`Python`](https://www.python.org/downloads/), [`Django`](https://www.djangoproject.com/), and HTML/CSS.
