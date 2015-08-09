from flask import render_template

from triager import app


@app.route("/")
def homepage():
    return render_template("index.html")
