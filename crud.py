"""CRUD operations."""

from model import Plan, db, User, connect_to_db


# Functions start here!

if __name__ == '__main__':
    from server import app
    connect_to_db(app)


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def create_plan(user_id, location, 
plan_name, start_time,end_time, url, image_url):

    """ Create and return new plan """
    
    
    plan = Plan(
        user_id=user_id,
        location=location,
        plan_name=plan_name,
        start_time=start_time,
        end_time=end_time,
        url=url,
        image_url=image_url

    )

    return plan


def get_plans():
    """Return all plans."""
    return Plan.query.all()

def get_plan_by_id(plan_id):
    """Get plan by its id"""
    return Plan.query.get(plan_id)

def get_user_by_id(user_id):
    """Get user by its id"""
    return User.query.get(user_id)

def get_user_by_email(email):
    """Return a user by email"""    
    return User.query.filter(User.email == email).first()

def delete_plan(plan_id):
    """Delete selected plan."""
    deleted_plan = Plan.query.get(plan_id)
    db.session.delete(deleted_plan)
    db.session.commit()
       