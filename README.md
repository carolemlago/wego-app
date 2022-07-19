[![Carole's GitHub stats](https://github-readme-stats.vercel.app/api?username=carolemlago)](https://github.com/carolemlago/github-readme-stats)

# Wego <img src="/static/img/wego-black-logo.png" width="30">
Let us do the planning.

Life gets busy, but busy folks don't have to miss out on fun. Wego is an date plan generator app, available nationwide, that selects a curated list of events which users can save, add to the calendar, and share with friends.
## Table of Contents
* 🤖 [Technologies](#technologies-used)
* ⭐ [Features](#features)
* 🚀 [Future Improvements](#future-improvements)
* 📖 [Set Up](#set-up)
* 😸 [About Me](#about-me)
## Technologies Used
* Backend: Python, Flask, SQL, PostgreSQL, SQLAlchemy
* Frontend: Javascript, HTML, CSS, Bootstrap, AJAX, JSON, Jinja
* APIs: Google Maps, Yelp Fusion, Twilio's Sendgrid and FullCalendar
## Features
🎥 [See a full video walk-through](https://www.youtube.com/watch?v=5Qs-WGbvJzc)

### Homepage
* To begin, users can create an account or login
![Wego Homepage](/static/img/homepage.png)

### Sign Up
* Users can register to have access to the app.
![Wego Sign Up](/static/img/signup.png)

### Login
* If user already has an account, authentication is used to verify info.
* Passwords are first hashed using Argon2 and then saved to the database to maximize security
![Wego Login](/static/img/login.png)

### User Dashboard
* Users can create a new date plan based on category, number of people, date, location and budget.
* The map is interactive and allow users to select location using markers that retrieves info, updates the search form and save the coordinates in my database.
* User's dashboard also displays saved plans and an integrated calendar that's updated every time a plan is added or deleted.
![Wego User Dashboard](/static/img/user-profile1.png)
![Wego User Dashboard](/static/img/user-profile2.png)

### Search Results 
* Users can slide through events, bars, restaurants or activities and save them using the interested button.
![Wego Search Results](/static/img/search-results.png)

### Save Plan
* Once user selects a date plan, the itinerary is confirmed.
* All the info is saved in the database associated with that user's id.
* A event is created for that plan in user's calendar.
![Wego Save Plan](/static/img/save-plan.png)

### Share Event
* Users can share their plans via email using Twilio Sendgrid API.
![Wego Share Event](/static/img/modal-share.png)
![Wego Email](/static/img/email.png)

## Future Improvements
* Recreate the front end using React

## Set Up
To run this project, first clone or fork this repo:
```
git clone https://github.com/carolemlago/wego-app
```
Create and activate a virtual environment inside your directory
```
virtualenv env
source env/bin/activate
```
Install the dependencies:
```
pip install -r requirements.txt
```
Sign up to obtain keys for the Google Maps API, Yelp Fusion API, and Twilio SendGrid API

Save your Yelp and Google Maps API keys in a file called `secrets.sh` using this format:
```
export APP_KEY="YOUR_KEY_GOES_HERE"
```
Save your SendGrid API key in a file called `sendgrid.env` using this format:
```
export SENDGRID_API_KEY="YOUR_KEY_GOES_HERE"
```
Source your keys into your virtual environment:
```
source secrets.sh
source sendgrid.env
```
Set up the database:
```
python3 seed.py
```
Run the app:
```
python3 server.py
```
You can now navigate to 'localhost:5000/' to access the travel app

## About Me
😸 Hi, my name is Carole and I'm former journalist turn into a software engineer. This date plan app is my first full stack application which I created in four weeks as my final project at Hackbright, a 12-week accelerated software engineering fellowship. Feel free to connect on [LinkedIn](https://www.linkedin.com/in/carolelago/)!
