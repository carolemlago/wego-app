
"""Server for Wego app."""

from urllib.parse import _ResultMixinStr
from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db
from passlib.hash import argon2
import crud
from jinja2 import StrictUndefined
from pprint import pformat
import os
import requests
import time
import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail




# API keys

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

MAPS_API_KEY = os.environ['GOOGLE_MAPS_KEY']
YELP_API_KEY = os.environ['YELP_API_KEY']
TWILIO_API_KEY = os.environ['TWILIO_API_KEY']


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

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    user_password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    
    # Hashing password
    hashed = argon2.hash(user_password)
    
    del user_password

    user = crud.get_user_by_email(email)

    # Check if user already have an account
    if user:
        flash("User email already exists.")
        return redirect("/")

    elif not argon2.verify(confirm_password, hashed):
        flash("Passwords don't match. Try again.")

    # Create new user in the database with user's info from the html form
    else:
        user = crud.create_user(fname, lname, email, hashed)
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

    email = request.form.get("email")
    password_attempt = request.form.get("password")

    user_info = crud.get_user_by_email(email=email)
   
    
    # Check if user's email and password match info in the database

    if user_info and argon2.verify(password_attempt, user_info.hashed):
        flash("Logged in!")
        session['user_id'] = user_info.user_id
        return redirect(f"/users/{session['user_id']}")

    else:
        flash("User email or password don't match. Try again.")

    return redirect('/')
  

@app.route('/users/<user_id>')
def show_user(user_id):
    """Show users dashboard."""


    if "user_id" in session:
        
        # Create user in the database
        user = crud.get_user_by_id(user_id)

        return render_template("user_profile.html", user=user)
        

    else:
        flash("You must be logged in to view user dashboard page")
        return redirect("/login")

   

@app.route('/logout')
def logout():
    """ Logout user from session """
    session.pop('user_id',None)
    flash("Logged Out.")
    return redirect('/')

        
@app.route('/user/search')
def search_itinerary():
    """Search for itineraries ideas"""

    # Get data from my search form
    num_people = request.args.get("num_people")
    location = request.args.get("location")
    budget = request.args.get("budget")
    date = request.args.get("date")
    types = request.args.getlist("type")
    event_results = {}
    bar_results = {}
    activity_results = {}
    date_unix = time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())
    
    # Headers for Yelp Fusion API
    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}

    for item in types:

        # API search for event date ideas
        if "event" in types:
            url_events = 'https://api.yelp.com/v3/events'
            querystring = {
            "attending_count": num_people, 
            "cost_max": int(budget), 
            "location": location,
            "start_date": int(date_unix)
            }
            response_events = requests.request("GET", url_events, headers=headers, params=querystring)
            event_results = response_events.json()['events']
            
        
        # API search for bar date ideas
        if "bar" in types:
            url_bars = 'https://api.yelp.com/v3/businesses/search'
            querystring = {
            "location": location,
            "categories": ["nightlife", "bars", "restaurants"]
            }

            response_bars = requests.request("GET", url_bars, headers=headers, params=querystring)
            bar_results = response_bars.json()['businesses']
           

        # API search for activity date ideas
        if "activity" in types:
            url_business = 'https://api.yelp.com/v3/businesses/search'   
            querystring = {
            "location": location, 
            "categories" : "active"
            }
    
            response_active = requests.request("GET", url_business, headers=headers, params=querystring)
            activity_results = response_active.json()['businesses']
    
    return render_template('user_search.html', date=date, events=event_results, bars=bar_results, activities=activity_results, user_id=session['user_id'])



@app.route('/save_plan', methods=['POST'])
def save_plan():
    """ Save in the database user's itinerary plan """

    # Data from selected date idea
    plan_type = request.form.get("type")
    photo = request.form.get("photo")
    name = request.form.get("name")
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")
    location = request.form.get("location")
    link = request.form.get("link")
    date = request.form.get("date")


    # Getting data from user in session
    user = crud.get_user_by_id(user_id=session['user_id'])

    # If selected plan is a bar or activity, there's no specific time
    if not start_time or start_time == "None":
        start_time = date
    if not end_time or end_time == "None":
        end_time = date


    # If event category was selected, create event date plan
    plan = crud.create_plan(
        user_id=session['user_id'],
        image_url=photo,
        plan_name=name,
        plan_type=plan_type,
        start_time=start_time,
        end_time=end_time,
        location=location,
        url=link
        ) 
    db.session.add(plan) 
   
    db.session.commit()   
    return render_template('save_plan.html', plan=plan, user=user)

@app.route('/delete_plan', methods=['POST'])
def delete_plan():
    """ Delete plan from view and database """

    plan_id = request.json.get("planId")
    
    crud.delete_plan(plan_id=plan_id) 
    return ("Success!")

@app.route('/send_email', methods=['POST'])
def send_email():
    """ Share chosen event via email """

    # Get recipient's email and plan id from modal form
    to_email = request.json.get('toEmail')
    date_id = request.json.get('planId')
    
    # Get plan from database
    date_plan = crud.get_plan_by_id(plan_id=date_id)

    # Getting data from user in session
    user = crud.get_user_by_id(user_id=session['user_id'])

    # Data from selected plan
    name = date_plan.plan_name
    location = date_plan.location
    start_time = date_plan.start_time
    end_time = date_plan.end_time
    url = date_plan.url
    image = date_plan.image_url

    print("Hello")
    
    # Email data
    message = Mail(from_email='carolemlago@gmail.com',
                    to_emails=to_email,
                    subject='Your Date Itinerary by Wego',
                    plain_text_content=f'You are going to {date_plan} event',
                    html_content=f'<div style="background-color: rgba(0,0,0,0.6); color: white;"> <center> <img id="app-logo" src="https://boxylife.sirv.com/CAROLE/newego-logo.png" width=200px></center> <br> <center> <strong> </strong> </center> <center> <img src="{image}" /> <br> <div> {user.fname} is inviting you to go to {name} <br> <div> Time: { start_time } to {end_time} </div> <br> <div> Address: {location } </div> <br> <a href="{url}" style="color:#d63384;"> Learn more</a> <br> </center> </div></div>')
                    
    try: 
        sg = SendGridAPIClient(os.environ['TWILIO_API_KEY'])
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)

    except Exception as e:
        print(e.message)

    return ("Success!")


@app.route('/get_calendar_events')
def get_calendar_events():
    """ Get all events from user and add to calendar """

    # Get all plans from logged in user in database
    plans = crud.Plan.query.filter_by(user_id=session['user_id']).all()
    
    # Adding each itinerary as a dictionary to a list of user's events
    events = []
    for plan in plans:
        plan_dict ={'title': plan.plan_name,
        'start': plan.start_time.strftime("%Y-%m-%d")
        }
        events.append(plan_dict)


    return jsonify(events)



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)