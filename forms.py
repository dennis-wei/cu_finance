from flask_wtf import Form
from wtforms import TextField, TextAreaField, DecimalField, IntegerField, SelectField, DateField, PasswordField, FileField
from wtforms.validators import DataRequired, Email, Optional

from services.read_db import get_initiative_name_list

def _check_valid_initiative(form, field):
    if field.data not in get_initiative_name_list():
        raise ValidationError('Inititiative Not Found')

class InitiativeForm(Form):
    name = TextField('Initiative Name', validators=[DataRequired()])
    base_budget = DecimalField('Initial Budget', validators=[DataRequired()])

class FTFForm(Form):
    name = TextField('Event Name', validators=[DataRequired()])
    program = TextField('Initiative', validators=[DataRequired(), _check_valid_initiative])
    location = TextField('Event Location', validators=[DataRequired()])
    event_date = DateField('Event Date', validators=[DataRequired()], format='%m-%d-%Y')
    estimated_attendance = IntegerField('Estimated Attendance', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    vendor = TextField('Vendor', validators=[DataRequired()])
    amount = DecimalField('Transaction Amount', validators=[DataRequired()])

class RevenueForm(Form):
    program = TextField('Initiative', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    amount = DecimalField('Transaction Amount', validators=[DataRequired()])
    f = FileField('Receipt File', validators=[DataRequired()])

class LoginForm(Form):
    email = TextField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class UpdateInitiativeForm(Form):
    budget = DecimalField('Change Budget', validators=[Optional()])
    status = SelectField('Change Status', choices=[('active', 'Active'), ('inactive', 'Inactive')])

class UploadForm(Form):
    f = FileField()
