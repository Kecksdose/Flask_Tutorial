from flask import render_template, flash, redirect, g, url_for, session, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from .forms import UsernamePasswordForm
from .models import User

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/index/')
@login_required
def index():
    user = g.user
    posts = [
        {
            'author': {'nickname': 'Timon'},
            'body': 'Alles Gute, Jana!'
        },
    ]
    return render_template('index.html',
        title='Home',
        user=user,
        posts=posts)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = UsernamePasswordForm()
    if form.validate_on_submit():
        user = \
            User.query.filter_by(nickname=form.nickname.data).first()
        if user is None:
            user = User(nickname=form.nickname.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Success!')
            return redirect('/index/')
        else:
            flash('Nickname ist bereits vergeben!')
    return render_template('register.html',
        title='Registrierung',
        form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = UsernamePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(nickname=form.nickname.data).first()
        if user is not None:
            if user.is_correct_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                flash('Du bist drin! Das war ja einfach...')
            else:
                flash('Da ist wohl was schiefgelaufen!')
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash('Nickname nicht gefunden!')
    return render_template('login.html',
        title='Anmeldung',
        form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
