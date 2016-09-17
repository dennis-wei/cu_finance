from models.models import Initiative, FTF, Revenue, db

def enter_new_initiative(form):
    form_dict = form.data
    init = Initiative(**form_dict)
    db.session.add(init)
    db.session.commit()
    return init.name

def enter_new_ftf(form):
    ftf_dict = form.data
    ftf = FTF(**ftf_dict)
    db.session.add(ftf)
    db.session.commit()
    return ftf.id

def enter_revenue(form):
    rev_dict = form.data
    rev_dict.pop('f')
    rev_dict['filename'] = form.f.data.filename
    rev = Revenue(**rev_dict)
    db.session.add(rev)
    update_initiative_revenue(form.program.data, form.amount.data)
    db.session.commit()
    return rev.program

def update_initiative_revenue(init_name, amt):
    init = Initiative.query.filter_by(name=init_name).first()
    init.revenue += amt
    overall = Initiative.query.filter_by(name='overall').first()
    overall.revenue += amt
