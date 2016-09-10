from models.models import db, Initiative, FTF, Revenue

def approve_ftf(ftf_id):
    ftf = FTF.query.filter_by(id=ftf_id).first()
    if ftf:
        ftf.status = 'approved_receipt_pending'
        return (ftf.program, ftf.amount)
    else:
        return None

def reject_ftf(ftf_id):
    ftf = FTF.query.filter_by(id=ftf_id).first()
    if ftf:
        ftf.status = 'rejected'
        return ftf.name
    else:
        return None

def update_ftf_receipt(ftf_id):
    ftf = FTF.query.filter_by(id=ftf_id).first()
    if ftf:
        ftf.receipt_received = True
        ftf.status = 'approved'
        return ftf.name
    else:
        return None

def update_revenue_receipt(rev_id):
    rev = FTF.query.filter_by(id=rev_id).first()
    if rev:
        rev.receipt_received = True
        return rev.program
    else:
        return None

def update_initiative(form, init_name):
    init = Initiative.query.filter_by(name=init_name).first()
    if init:
        budget = form.budget.data
        if budget:
            init.total_budget = budget
        status = form.status.data
        if status:
            init.status = status

def update_init_ftf(init_name, amt):
    init = Initiative.query.filter_by(name=init_name).first()
    init.expenditure += amt
