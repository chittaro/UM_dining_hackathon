from flask import Flask, jsonify
import pandas as pd

from scraping.data import scrape_and_send

app = Flask(__name__)

@app.route("/home")
def home():
    return "hi"

def handle_scraping():
    data = scrape_and_send()
    return jsonify(data)

if __name__ == '__main__':
    app.run()



