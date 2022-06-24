
"""Models for Wego Itinerary Planner app."""

from flask_sqlalchemy import SQLAlchemy

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
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)  

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
        return f"<Plan plan_id = {self.plan_id} plant_type={self.plan_type} user_id = {self.user_id} location = {self.location} >"


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)