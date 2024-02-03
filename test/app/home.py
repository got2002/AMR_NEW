from flask import Blueprint
from flask import Flask, render_template
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template("index.html")
