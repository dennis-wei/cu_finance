from models.models import db, Initiative
from flask import current_app as app

def init_db():
    check = Initiative.query.filter_by(name='overall').first()
    if not check:
        init = Initiative('overall', app.config['BASE_ALLOCATION'])
        db.session.add(init)
        db.session.commit()
