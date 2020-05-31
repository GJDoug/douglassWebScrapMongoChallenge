from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scraping
# import os

app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app)

@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_data = mongo.db.mars.find_one()

    # Return template and data
    return render_template("/index.html", mars=mars_data)


# scrape function
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping()
    mars.update({}, mars_data, upsert=True)

    # back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)