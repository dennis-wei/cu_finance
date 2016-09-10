from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date, String, Integer, Boolean, Numeric

import datetime as dt

db = SQLAlchemy()

class Initiative(db.Model):
    __tablename__ = 'initiatives'

    name = db.Column(String, primary_key=True)
    base_budget = db.Column(Numeric)
    revenue = db.Column(Numeric)
    expended_budget = db.Column(Numeric)
    status = db.Column(String)

    def __init__(self, name, base_budget):
        self.name = name
        self.base_budget = base_budget
        self.revenue = 0
        self.expended_budget = 0
        self.status = 'active'

    def __repr__(self):
        return '<name {}>'.format(self.name)

    pass

class FTF(db.Model):
    __tablename__ = 'ftf_forms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(String)
    program = db.Column(String)
    location = db.Column(String)
    event_date = db.Column(Date)
    estimated_attendance = db.Column(Integer)
    description = db.Column(String)
    vendor = db.Column(String)
    amount = db.Column(Numeric)
    receipt_received = db.Column(Boolean)
    status = db.Column(String)

    def __init__(self, name, program, location, event_date, \
                    estimated_attendance, description, vendor, amount):
        self.name = name
        self.program = program
        self.location = location
        self.event_date = event_date
        self.estimated_attendance = estimated_attendance
        self.description = description
        self.vendor = vendor
        self.amount = amount
        self.receipt_received = False
        self.status = 'pending'

    def __repr__(self):
        return '<id {}>'.format(self.id)

    pass

class Revenue(db.Model):
    __tablename__ = 'revenue'

    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(String)
    description = db.Column(String)
    amount = db.Column(Numeric)
    date = db.Column(Date)
    receipt_received = db.Column(Boolean)

    def __init__(self, program, description, amount):
        self.program = program
        self.description = description
        self.amount = amount
        self.date = dt.date.today()
        self.receipt_received = False

    def __repr__(self):
        return '<id {}>'.format(self.id)

    pass

class User(db.Model):
    __tablename__ = 'users'

    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<email {}>'.format(self.email)

    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False
