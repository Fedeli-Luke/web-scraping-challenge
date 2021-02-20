from flask import Flask, redirect, render_template

from flask_pymongo import PyMongo 

import Scrape_Mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route('/')
def index():
    mars_info = mongo.db.data.find_one()
    return render_template('index.html',data=mars_info)

@app.route('/scrape')
def scraper():
    data = mongo.db.data

    mars_info = Scrape_Mars.scrape()

    data.update({},mars_info,upsert=True)
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run(debug=True)