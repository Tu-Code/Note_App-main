from flask import Blueprint, render_template, redirect
from flask.helpers import url_for
from flask_login import  login_required, current_user
from werkzeug.wrappers import request
from flask import flash, request, jsonify
from .models import Note
from .forms import RequestResetForm, ResetPasswordForm
from . import db, mail
from flask_mail import Message
import json
#forgot pwd
from .forms import EmailForm
from .models import User
# from .util import send_email, ts
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        # return redirect(url_for('home.html'))
        note = request.form.get('note')
        Title = request.form.get('title')
        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(title=Title, data=note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            # flash('Note added!', category='success')
            # return render_template('views.html', data=)
    
    return render_template('home.html', user=current_user)


@views.route('/delete-note', methods=['DELETE'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='solarinsarah3@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('reset_token', token=token, _external=True)}
    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)

@views.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@views.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired token', 'warning')
        return redirect(url_for('reser_request'))
    form = ResetPasswordForm()
    if request.method == 'POST':
        # email = request.form.get('email')
        # first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # user = User.query.filter_by(email=email).first()
        # if user:
        #     flash('Email already exists.', category='error')
        # if len(email) < 4:
        #     flash('Email must be greater than 3 characters', category='error')
        # elif len(first_name) < 2:
        #     flash('Name must be greater than 1 character', category='error')
        if password1 != password2:
            flash('Password\'s dont match', category='error')
        elif len(password1) < 7:
            flash('Password is too short', category='error')
        else:
            # account created
            user.password = password1
            db.session.commit()
            # login_user(user)
            flash('Password updated!', category='success')
            # going back to views -> home
            return redirect(url_for('auth.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


