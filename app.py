from flask import Flask, redirect, url_for, render_template, flash
from flask_login import login_required, current_user, LoginManager, login_user
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os

from models.models import db, User, Revenue, FTF, Initiative
from forms import InitiativeForm, FTFForm, RevenueForm, LoginForm, UpdateInitiativeForm
from services.parse import enter_new_initiative, enter_new_ftf, enter_revenue
from services.read_db import get_overall_data, get_initiative_data, \
                                get_all_initiatives, get_ftf_data, \
                                get_specific_ftf, get_revenue_data
from services.update_db import approve_ftf, reject_ftf, update_ftf_receipt, \
                                update_revenue_receipt, update_initiative_data, \
                                update_init_ftf
from services.init_db import init_db

app = Flask(__name__)
app.config.from_pyfile('settings.py')

db.init_app(app)

with app.app_context():
    db.create_all()
    db.session.commit()

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def index():
    return render_template('index.html', data=get_overall_data())

@app.route('/initiatives')
@app.route('/initiatives/<initiative_name>')
def initiatives(initiative_name=None):
    if initiative_name == 'overall':
        return redirect(url_for('index'))
    elif initiative_name:
        data = get_initiative_data(initiative_name)
        if current_user.is_authenticated():
            return render_template('admin_initiative.html', data=data)
        else:
            return render_template('initiative.html', data=data)
    else:
        return render_template('all_initiatives.html', data=get_all_initiatives())

@app.route('/initiatives/submit', methods=['GET', 'POST'])
@login_required
def submit_intiative():
    form = InitiativeForm()
    if form.validate_on_submit():
        initiative_name = enter_new_initiative(form)
        return redirect(url_for('initiatives', initiative_name=initiative_name))
    return render_template('submit_initiative.html', form=form)

@app.route('/initiatives/update/<initiative_name>', methods=['GET', 'POST'])
@login_required
def update_initiative(initiative_name=None):
    form = UpdateInitiativeForm()
    if form.validate_on_submit():
        update_initiative_data(form, initiative_name)
        return redirect(url_for('initiatives', initiative_name=initiative_name))
    return render_template('update_initiative.html', data=get_initiative_data(initiative_name), form=form)

@app.route('/ftf')
@app.route('/ftf/<ftf_id>')
def ftf(ftf_id=None):
    if ftf_id:
        return render_template('specific_ftf.html', data=get_specific_ftf(ftf_id))
    else:
        if current_user.is_authenticated:
            return render_template('admin_ftf.html', data=get_ftf_data())
        else:
            return render_template('ftf.html', data=get_ftf_data())

@app.route('/ftf/submit', methods=['GET', 'POST'])
def submit_ftf():
    form = FTFForm()
    if form.validate_on_submit():
        ftf_id = enter_new_ftf(form)
        return redirect(url_for('ftf', ftf_id=ftf_id))
    return render_template('submit_ftf.html', form=form)

@app.route('/revenue')
def revenue():
    if current_user.is_authenticated:
        return render_template('admin_revenue.html', data=get_revenue_data())
    else:
        return render_template('revenue.html', data=get_revenue_data())

@app.route('/revenue/submit', methods=['GET', 'POST'])
@login_required
def submit_revenue():
    form = RevenueForm()
    if form.validate_on_submit():
        initiative_name = enter_revenue(form)
        return redirect(url_for('initiatives', initiative_name=initiative_name))
    return render_template('submit_revenue.html', form=form)

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload_receipt/<source_type>/<source_id>', methods=['GET', 'POST'])
def upload_receipt(source_type=None, source_id=None):
    if source_type and source_id:
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                if source_type == 'ftf':
                    success = update_ftf_receipt(source_id)
                    if success:
                        flash('Receipt successfully uploaded')
                    else:
                        flash('FTF not found')
                    return redirect(url_for('ftf'))
                elif source_type == 'revenue':
                    success = update_revenue_receipt(source_id)
                    if success:
                        flash('Receipt successfully uploaded')
                    else:
                        flash('Revenue item not found')
                return redirect(url_for('index'))
        return render_template('upload_receipt.html')
    else:
        redirect(url_for('index'))

@app.route('/ftf_status/<update>/<ftf_id>')
@login_required
def update_ftf_status(update='confirm', ftf_id=None):
    if update == 'confirm' and ftf_id:
        ftf_data = approve_ftf(ftf_id)
        if ftf_data:
            update_init_ftf(*ftf_data)
            flash('Confirmed FTF: ' + ftf_name)
            return redirect(url_for('ftf'), ftf_id=ftf_id)
        else:
            flash('FTF not found')
    elif update == 'reject' and ftf_id:
        ftf_name = reject_ftf(ftf_id)
        if ftf_name:
            flash('Rejected FTF: ' + ftf_name)
            return redirect(url_for('ftf'), ftf_id=ftf_id)
        else:
            flash('FTF not found')
    return redirect(url_for('ftf'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.email.data)
        if user.password == form.password.data:
            user.authenticated = True
            login_user(user, remember=True)
            flash('Logged in successfully.')
            return redirect(url_for('index'))
        else:
            flash('Incorrect login credentials')
            return redirect(url_for('login'))

    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Successfully logged out')
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@login_manager.user_loader
def user_loader(user_id):
    return User.query.filter_by(email=user_id).first()

with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=5000)

application = app
