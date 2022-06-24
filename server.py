
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

MAPS_API_KEY = os.environ['GOOGLE_MAPS_KEY']
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
    event_plan = crud.get_plans_by_user_and_plan_type(user_id, plan_type="events")
    bar_plan = crud.get_plans_by_user_and_plan_type(user_id, plan_type="bars")
    active_plan = crud.get_plans_by_user_and_plan_type(user_id, plan_type="activities")
    
    
    return render_template("user_profile.html", user=user, event_plan=event_plan, bar_plan=bar_plan, active_plan=active_plan)

@app.route('/logout')
def logout():
    session.pop('user_id',None)
    return redirect('/')

        
@app.route('/user/search')
def search_itinerary():
    """Search for itineraries ideas"""

    # Getting data from my HTML form
    num_people = request.args.get("num_people")
    location = request.args.get("location")
    budget = request.args.get("budget")
    date = request.args.get("date")
    types = request.args.getlist("type")
    event_results = {}
    bar_results = {}
    activity_results = {}


    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}

    for item in types:

        # Check for event in date types
        if "event" in types:
            url_events = 'https://api.yelp.com/v3/events'
            querystring = {
            "attending_count": num_people, 
            "cost_max": int(budget), 
            "location": location,
            }
            response_events = requests.request("GET", url_events, headers=headers, params=querystring)
            event_results = response_events.json()['events']
            
        
        # Check for bar in date types
        if "bar" in types:
            url_bars = 'https://api.yelp.com/v3/businesses/search'
            querystring = {
            "location": location,
            "categories": ["nightlife", "bars", "restaurants"]
            }

            response_bars = requests.request("GET", url_bars, headers=headers, params=querystring)
            bar_results = response_bars.json()['businesses']
            print(bar_results)

        # Check for active in date types
        if "activity" in types:
            url_business = 'https://api.yelp.com/v3/businesses/search'   
            querystring = {
            "location": location, 
            "categories" : "active"
            }
    
            response_active = requests.request("GET", url_business, headers=headers, params=querystring)
            activity_results = response_active.json()['businesses']
    
    return render_template('user_search.html', events=event_results, bars=bar_results, activities=activity_results, user_id=session['user_id'])



@app.route('/save_plan', methods=['POST'])
def save_plan():
    """ Save in the database user's itinerary plan """

    # variables for my event category plan
    event_type = request.form.get("events")
    event_photo = request.form.get("event_photo")
    event_name = request.form.get("event_name")
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")
    event_location = request.form.get("event_location")
    event_link = request.form.get("event_link")

    # variables for my bar category plan
    bars_type = request.form.get("bars")
    bar_photo = request.form.get("bar_photo")
    bar_name = request.form.get("bar_name")
    bar_location = request.form.get("bar_location")
    bar_link = request.form.get("bar_link")

    # variables for my activity category plan
    activities_type = request.form.get("activities")
    activity_photo = request.form.get("activity_photo")
    activity_name = request.form.get("activity_name")
    activity_location = request.form.get("activity_location")
    activity_link = request.form.get("activity_link")

    event_plan = {}
    bar_plan = {}
    activity_plan = {}
    
    # If event category was selected, create event date plan
    if event_type:
        event_plan = crud.create_plan(
        user_id=session['user_id'],
        image_url=event_photo,
        plan_name=event_name,
        plan_type=event_type,
        start_time=start_time,
        end_time=end_time,
        location=event_location,
        url=event_link
        ) 
        db.session.add(event_plan)

    # If bar category was selected, create bar date plan
    if bars_type:
        bar_plan = crud.create_plan(
        user_id=session['user_id'],
        image_url=bar_photo,
        plan_name=bar_name,
        plan_type=bars_type,
        start_time=None,
        end_time=None,
        location=bar_location,
        url=bar_link
        ) 
        db.session.add(bar_plan)

    # If activity category was selected, create activity date plan
    if activities_type:
        activity_plan = crud.create_plan(
        user_id=session['user_id'],
        image_url=activity_photo,
        plan_name=activity_name,
        plan_type=activities_type,
        start_time=None,
        end_time=None,
        location=activity_location,
        url=activity_link
        ) 
        db.session.add(activity_plan)

    
    print(bar_plan)
    db.session.commit()   
    return render_template('save_plan.html', event_plan=event_plan, bar_plan=bar_plan, activity_plan=activity_plan, user_id=session['user_id'])

@app.route('/delete_plan', methods=['POST'])
def delete_plan():
    """ Delete plan from view and database """

    plan_id = request.json.get("planId")
    
    crud.delete_plan(plan_id=plan_id) 
    return ("Event deleted succesfully!")



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)