from flask import Blueprint
from flask import Flask, render_template
login_bp = Blueprint('login', __name__)

@login_bp.route('/login')
def login():
    return render_template("login.html")
