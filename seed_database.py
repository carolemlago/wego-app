
"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb plans")
os.system('createdb plans')
model.connect_to_db(server.app)
model.db.create_all()




for n in range(10):
    email = f'user{n}@test.com'  
    password = 'test'

    user = crud.create_user(email, password)
    model.db.session.add(user)

for _ in range(10):
    user_id = user_id
    plan_type = plan_type
    location = location

    plan = crud.create_plan(user_id, plan_type, location)
    model.db.session.add(plan)

model.db.session.commit()