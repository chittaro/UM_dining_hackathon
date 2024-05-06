from flask import Flask, redirect, url_for, render_template, request
from scraping import *

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def home():
    return render_template('home.html')

@app.route("/graphs")
def graphs():
    return render_template('graphs.html')

if __name__ == '__main__':
    app.run(debug = True)