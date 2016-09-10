from models.models import Initiative, FTF, Revenue, db

def enter_new_initiative(form):
    form_dict = form.data
    init = Initiative(**form_dict)
    db.session.add(init)
    db.session.commit()

def enter_new_ftf(form):
    ftf_dict = form.data
    ftf = FTF(**ftf_dict)
    db.session.add(ftf)
    db.session.commit()

def enter_revenue(form):
    rev_dict = form.data
    rev = Revenue(**rev_dict)
    db.session.add(rev)
    db.session.commit()

    update_initiative_revenue(form.program.data, form.amount.data)

def update_initiative_revenue(init_name, amt):
    init = Initiative.query.filter_by(name=init_name).first()
    init.revenue += amt
