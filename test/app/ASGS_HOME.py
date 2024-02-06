from flask import Blueprint
from flask import Flask, render_template
ASGS_HOME = Blueprint('ASGS', __name__)



@ASGS_HOME.route("/ASGS")
def ASGS():
    return render_template("ASGS.html")