from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import storage
from models.contact import Contact
from utils.filter import search_filter, sort
from math import ceil

views = Blueprint('views', __name__)
MAX_CONTACTS = 20

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
    contacts = current_user.contacts
    return render_template("profile.html", contacts=contacts)