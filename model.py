
"""Models for Wego Itinerary Planner app."""

from flask_sqlalchemy import SQLAlchemy
from passlib.hash import argon2
import datetime

db = SQLAlchemy()




def connect_to_db(flask_app, db_uri="postgresql:///plans", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


class User(db.Model):
    """User's information"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(25), nullable=False, unique=True)
    hashed = db.Column(db.String(100), nullable=False)  

    plans = db.relationship("Plan", back_populates="user")

    def __repr__(self):
        return f"<User user_id = {self.user_id} email = {self.email}>"


class Plan(db.Model):
    """Plans table"""

    __tablename__ = "plans"

    plan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    plan_name = db.Column(db.String)
    plan_type = db.Column(db.String)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    location = db.Column(db.String, nullable=False)
    url = db.Column(db.String)
    image_url = db.Column(db.String)
    

    user = db.relationship("User", back_populates="plans")

   

    def __repr__(self):
        return f"<Plan plan_id = {self.plan_id} plan_type={self.plan_type} user_id = {self.user_id} location = {self.location} >"

def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    Plan.query.delete()
    User.query.delete()
    

    # Add sample users and plans
    password_1 = "123"
    hashed1 = argon2.hash(password_1)
    user1 = User(fname='Jocelyn', lname='Tang', email='test1@test1.com', hashed=hashed1)
    password_2 = "123"
    hashed2 = argon2.hash(password_2)
    user2 = User(fname='Steve', lname='Chait', email='test2@test2.com', hashed=hashed2)
    password_3 = "123"
    hashed3 = argon2.hash(password_3)
    user3 = User(fname='Ione', lname='Axel', email='test3@test3.com', hashed=hashed3)
    
    db.session.add_all([user1, user2, user3])
    db.session.commit()

    plan1 = Plan(user_id=user1.user_id, plan_name='Zoo', plan_type='activity', start_time=datetime.date.today(), end_time=datetime.date.today(), location='San Diego, CA')
    plan2 = Plan(user_id=user2.user_id, plan_name='Bar', plan_type='bar', start_time=datetime.date.today(), end_time=datetime.date.today(), location='Los Angeles, CA')
    plan3 = Plan(user_id=user3.user_id, plan_name='Event', plan_type='event', start_time=datetime.date.today(), end_time=datetime.date.today(), location='San Francisco, CA')

    db.session.add_all([plan1, plan2, plan3])
    db.session.commit()

if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)