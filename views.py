from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.contact import Contact
from utils.filter import search_filter, sort
from math import ceil
from werkzeug.security import generate_password_hash, check_password_hash

views = Blueprint('views', __name__)
MAX_CONTACTS = 30

# the route for the home page
@views.route('/')
@login_required
def home():
    field = request.args.get("sortby", None)
    contacts = sort(current_user.contacts, field)
    q = request.args.get("search")
    res = search_filter(contacts, q)
    pages = ceil(len(res) / MAX_CONTACTS)
    try:
        p = int(request.args.get("page"))
        if p < 1:
            p = 1
        if p > pages:
            p = pages
    except:
        p = 1
    contacts = res[MAX_CONTACTS * (p - 1):MAX_CONTACTS * p]
    pagination = {"pages": pages, "index": p, "sort_option": field}
    return render_template("index.html", contacts=contacts, pagination=pagination, home_active=True)

@views.route('/new-contact', methods=["GET", "POST"])
@login_required
def add_contact():
    values = {"first_name": "", "last_name": "", "email": ""}
    if request.method == "POST":
        email = request.form.get('email')
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        values = {"first_name": first_name, "last_name": last_name, "email": email}
        if len(first_name) < 4:
            flash('First name must be greater than 4 characters!', category="error")
        elif len(last_name) < 4:
            flash('Last name must be greater than 4 characters!', category="error")
        elif len(email) < 5:
            flash('Email must be greater than 5 characters!', category="error")
        else:
            flash('Contact created!', category="success")
            new_contact = Contact()
            new_contact.first_name = first_name
            new_contact.last_name = last_name
            new_contact.email = email
            new_contact.user_id = current_user.id
            new_contact.save()
            return redirect(url_for('views.home'))
    return render_template("new-contact.html", values=values, add_active=True)

@views.route('/profile')
@login_required
def profile():
    contacts = len(current_user.contacts)
    return render_template("profile.html", contacts=contacts, user=current_user)

@views.route('/edit-name', methods=["POST"])
@login_required
def edit_name():
    name = request.form.get('name')
    if len(name) < 4:
        flash('Name must be greater than 4 characters!', category="error")
    else:
        current_user.name = name
        current_user.save()
        flash('Your name has been changed!', category="success")
    return redirect(url_for("views.profile"))

@views.route('/edit-email', methods=["POST"])
@login_required
def edit_email():
    email = request.form.get('email')
    if len(email) < 5:
        flash('Your email must be greater than 5 characters!', category="error")
    else:
        current_user.email = email
        current_user.save()
        flash('Your email has been changed!', category="success")
    return redirect(url_for("views.profile"))

@views.route('/edit-password', methods=["POST"])
@login_required
def edit_password():
    password = request.form.get('old_password')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    if check_password_hash(current_user.password, password) is False:
        flash('Incorrect password, Try again!', category="error")
    elif len(password1) < 8:
        flash('Password must be greater than 8 characters!', category="error")
    elif password1 != password2:
        flash('Passwords don\'t match', category="error")
    else:
        current_user.password = generate_password_hash(password1, method="scrypt")
        current_user.save()
        flash('Password has been changed!', category="success")
    return redirect(url_for("views.profile"))