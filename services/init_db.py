from models.models import db, Initiative, User
from flask import current_app as app

def init_db():
    overall_check = Initiative.query.filter_by(name='overall').first()
    if not overall_check:
        init = Initiative('overall', app.config['BASE_ALLOCATION'])
        init.status = 'overall'
        db.session.add(init)
        db.session.commit()
    user_check = User.query.filter_by(email=app.config['USERNAME']).first()
    if not user_check:
        user = User(app.config['USERNAME'], app.config['PASSWORD'])
        db.session.add(user)
        db.session.commit()
