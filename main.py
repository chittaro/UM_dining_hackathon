from flask import Flask, redirect, url_for, render_template, request, session
from scraping.combined import *
import os

app = Flask(__name__)
app.secret_key = "testKey" # TODO: change

#TODO: find best method/time to scrape new menu
'''
menuDict = getStartDict()
halls = getDHalls()

html_path = "scraping/hall_HTML/"
html_dirs = os.listdir(html_path)
for hall in html_dirs:
    getDhallItems(path = html_path, dining_hall_file = hall, menu_dict = menuDict)

#place dictionary into pd dataframe
diningDf = pd.DataFrame(menuDict)
'''
diningDf = pd.read_csv("scraping/csvFile")


@app.route("/", methods = ["GET", "POST"])
def home():

    # create default session values
    menuItems = []

    # TODO: check how to identify specific button submission (if multiple needed)
    if request.method == "POST":

        # get dropdown values
        hall = request.form["hall"]
        meal = request.form["meal"]
        filter = request.form["filter"]
        count = int(request.form["count"])

        # index into menu dictionary w/ given values
        filterDf = getTopItems(diningDf, hall, meal, count, filter)
        menuItems = filterDf.to_dict('records')

        # save choices in session data
        session["hall"] = hall
        session["meal"] = meal
        session["filter"] = filter
        session["count"] = count
        session["menuItems"] = menuItems

    return render_template('home.html', session = session)

@app.route("/graphs")
def graphs():
    return render_template('graphs.html')

if __name__ == '__main__':
    app.run(debug = True)