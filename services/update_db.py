from models.models import db, Initiative, FTF, Revenue

def approve_ftf(ftf_id):
    ftf = FTF.query.filter_by(id=ftf_id).first()
    if ftf:
        if ftf.status == 'receipt_received':
            ftf.status = 'approved'
        else:
            ftf.status = 'approved_receipt_pending'
        update_initiative_expenditure(ftf.program, ftf.amount)
        db.session.commit()
        return (ftf.program, ftf.amount)
    else:
        return None

def reject_ftf(ftf_id):
    ftf = FTF.query.filter_by(id=ftf_id).first()
    if ftf:
        ftf.status = 'rejected'
        db.session.commit()
        return ftf.name
    else:
        return None

def update_ftf_receipt(ftf_id, filename):
    ftf = FTF.query.filter_by(id=ftf_id).first()
    if ftf:
        ftf.receipt_filename = filename
        if ftf.status == 'approved_receipt_pending':
            ftf.status = 'approved'
        else:
            ftf.status = 'receipt_received'
        db.session.commit()
        return ftf.name
    else:
        return None

def update_initiative_data(form, init_name):
    init = Initiative.query.filter_by(name=init_name).first()
    if init:
        budget = form.budget.data
        if budget:
            init.base_budget = budget
        status = form.status.data
        if status:
            init.status = status
    db.session.commit()

def update_init_ftf(init_name, amt):
    init = Initiative.query.filter_by(name=init_name).first()
    init.expended_budget += amt
    db.session.commit()
    return init.name

def update_initiative_expenditure(init_name, amt):
    init = Initiative.query.filter_by(name=init_name).first()
    init.expended_budget += amt
    overall = Initiative.query.filter_by(name='overall').first()
    overall.expended_budget += amt
