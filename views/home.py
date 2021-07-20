from flask import Flask, session, render_template, redirect, Blueprint, url_for

home = Blueprint('home', __name__)

@home.route('/')
def home_page():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('home.html')
