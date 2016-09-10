from models.models import db, Initiative, FTF, Revenue
import datetime as dt

def get_overall_data():
    db_pull = Initiative.query.filter_by(name='overall').first()
    ret_dict = db_pull.__dict__.copy()
    ret_dict['remaining_funds'] = _get_remaining_budget(ret_dict)

    ret_dict['allocated_budget'] = _get_allocated_budget()

    app_ftf_list = FTF.query.filter_by(status='approved')
    ret_dict['past_7'] = _get_expenditure(app_ftf_list, 7)
    ret_dict['past_30'] = _get_expenditure(app_ftf_list, 30)
    ret_dict['past_90'] = _get_expenditure(app_ftf_list, 90)

    pending_ftf_count = db.session.query(FTF).filter_by(status='pending').count()
    ret_dict['num_pending'] = pending_ftf_count

    most_recent_transactions = sorted(app_ftf_list, key=lambda f: f.event_date, reverse=True)[:5]
    ret_dict['most_recent_transactions'] = [
        {'name': m.name, 'amount': m.amount, 'description': m.description}
        for m in most_recent_transactions
    ]

    return ret_dict

def get_initiative_data(initiative_name):
    db_pull = Initiative.query.filter_by(name=initiative_name).first()
    ret_dict = db_pull.__dict__.copy()
    ret_dict['remaining_budget'] = _get_remaining_budget(ret_dict)

    ftf_list = FTF.query.filter_by(program=initiative_name)
    ret_dict['ftf_list'] = sorted([_get_ftf_dict_data(ftf) for ftf in ftf_list], \
                                    key=lambda f: f['event_date'], reverse=True)
    return ret_dict

def get_specific_ftf(ftf_id):
    ftf = FTF.query.filter_by(id=ftf_id).first()
    ftf_dict = ftf.__dict__.copy()
    return ftf_dict

def get_ftf_data():
    ftf_list = FTF.query.all()
    return sorted([_get_ftf_dict_data(ftf) for ftf in ftf_list], \
                    key=lambda f: f['event_date'], reverse=True)

def get_all_initiatives():
    active_list = db.session.query(Initiative).filter_by(status='active').all()
    inactive_list = Initiative.query.filter_by(status='inactive').all()
    ret_dict = {
        'active': [_pop_status(i.__dict__) for i in active_list],
        'inactive': [_pop_status(i.__dict__) for i in inactive_list]
    }
    return ret_dict

def get_revenue_data():
    revenue_list = Revenue.query.all()
    rev_dict_list = [_pop_id_revenue(r) for r in revenue_list]
    print rev_dict_list
    return sorted(rev_dict_list, key=lambda r: r['date'], reverse=True)

def get_initiative_name_list():
    name_tuples = db.session.query(Initiative.name).all()
    return [n[0] for n in name_tuples]

def _pop_status(init_dict):
    copy_dict = init_dict.copy()
    copy_dict.pop('status')
    return copy_dict

def _pop_id_revenue(rev):
    ret_dict = rev.__dict__.copy()
    ret_dict.pop('receipt_received')
    return ret_dict

def _get_ftf_dict_data(ftf):
    res = {
        'name': ftf.name,
        'amount': ftf.amount,
        'event_date': ftf.event_date,
        'description': ftf.description,
        'status': ftf.status
    }
    return res

def _get_remaining_budget(ret_dict):
    return ret_dict['base_budget'] + ret_dict['revenue'] - ret_dict['expended_budget']

def _get_allocated_budget():
    inits = db.session.query(Initiative).filter(Initiative.name!='overall')
    return sum(i.base_budget for i in inits)

def _get_expenditure(ftf_list, num_days):
    today = dt.date.today()
    date_range = today - dt.timedelta(days=num_days)
    return sum(ftf.amount for ftf in ftf_list if date_range <= ftf.event_date <= today)
