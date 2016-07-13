from flask import (render_template, flash, redirect, g, url_for,
                   session, request)

from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from app import app, db
from .forms import (UsernameMailPasswordRegisterForm,
                    UsernamePasswordLoginForm,
                    EditForm)
from .models import User

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

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
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = UsernameMailPasswordRegisterForm()
    flash(form.validate_on_submit())
    if form.validate_on_submit():
        user = \
            User.query.filter_by(nickname=form.nickname.data).first()
        email = \
            User.query.filter_by(email=form.email.data).first()
        if user is not None and email is not None:
            flash('Nickname und E-Mail-Adresse sind bereits vergeben!')
        elif user is not None:
            flash('Nickname ist bereits vergeben!')
        elif email is not None:
            flash('E-Mail-Adresse ist bereits vergeben!')
        else:
            user = User(nickname=form.nickname.data,
                        password=form.password.data,
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            flash('Success!')
            return redirect('/index/')
    return render_template('register.html',
        title='Registrierung',
        form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = UsernamePasswordLoginForm()
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

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Mein erster Post!'},
        {'author': user, 'body': 'Und ein weiterer!'}
    ]
    return render_template('user.html',
                           user=user,
                           posts=posts)

@app.route('/edit/', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Deine Daten wurde aktualisiert.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)
