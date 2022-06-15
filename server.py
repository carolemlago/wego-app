
"""Server for Wego app."""

from urllib.parse import _ResultMixinStr
from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
from pprint import pformat
import os
import requests



app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# API_KEY = os.environ['GOOGLE_MAPS_KEY']
TRAVEL_API_KEY = os.environ['BOOKING_API_KEY']
YELP_API_KEY = os.environ['YELP_API_KEY']


@app.route('/')
def homepage():
    """ Homepage view function"""

    return render_template('homepage.html')


@app.route('/signup')
def register_user():
    """ New user registration page"""

    return render_template('signup.html')

@app.route('/create_user', methods=["POST"])
def create_user():
    """ Create new user """


    user_email = request.form.get("email")
    user_password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    

    user = crud.get_user_by_email(user_email)

    # Check if user already have an account
    if user:
        flash("User email already exists.")
        return redirect("/")
    
    elif confirm_password != user_password:
        flash("Passwords don't match. Try again")
        return redirect("/signup")

    # Create new user in the database with user's info from the html form
    else:
        user = crud.create_user(user_email, user_password)
        db.session.add(user)    
        db.session.commit()
        user_id = user.user_id
        flash('Account created!')
        session['user_id'] = user.user_id
        return redirect(f"/users/{user_id}")



@app.route('/login')
def log_in():

    """ Show log in page """
    return render_template("login.html")

@app.route('/check_userinfo', methods=['POST'])
def get_user_by_email():
    """ Check if user's email and password match """

    user_email = request.form.get("email")
    user_password = request.form.get("password")

    user_info = crud.get_user_by_email(email=user_email)
   
    
    # Check if user's email and password match info in the database

    if user_info and (user_info.password == user_password):
        flash("Logged in!")
        session['user_id'] = user_info.user_id
        return redirect(f"/users/{session['user_id']}")

    else:
        flash("User email or password don't match. Try again.")

    return redirect('/')
  

@app.route('/users/<user_id>')
def show_user(user_id):
    """Show users dashboard."""
    user = crud.get_user_by_id(user_id)
   
    return render_template("user_profile.html", user=user)
        

@app.route('/user/search')
def search_itinerary():
    """Search for itineraries ideas"""

    # Getting data from my HTML form
    num_people = request.args.get('num_people', '')
    location = request.args.get('location', '')
    budget = request.args.get('budget', '')
    date = request.args.get('date', '')
    plan_type = request.args.get('plan_type')
   

    if plan_type == "travel":
        url_travel = 'https://booking-com.p.rapidapi.com/v1/hotels/search-filters'
        querystring = {"num_people": num_people , "location": location,
        "budget": int(budget),
        "date": date}

        headers = {
            "X-RapidAPI-Key": TRAVEL_API_KEY,
            "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
            }


        response = requests.request("GET", url_travel, headers=headers, params=querystring)
        print(response)
        results = response.json()
        
        

    else:
        url_date = 'https://api.yelp.com/v3/events'
        querystring = {"attending_count": num_people, 
        "cost_max": int(budget), 
        "location": location}

        headers = {"Authorization": f"Bearer {YELP_API_KEY}"}

        response = requests.request("GET", url_date, headers=headers, params=querystring)
        print(response.json())
        results = response.json()
        
    return render_template('user_search.html', results=results)


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)