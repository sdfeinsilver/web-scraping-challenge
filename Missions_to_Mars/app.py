#Import Dependencies
from flask import Flask, render_template, redirect
from pymongo import MongoClient
import scrape_mars

#Create an instance of Flask
app = Flask(__name__)

#Use pymongo to set up mongo connection
mongo_url = "mongodb://localhost:27017"
client = MongoClient(mongo_url)
db = client.mars_db

#Create Home Route
@app.route("/")
def home():
    mars_dict = db.mars_info.find_one()
    return render_template("index.html", dictionary=mars_dict)

#Route that will trigger the scrape function
@app.route("/scrape")
def scraper():
    mars_dict = db.mars_info
    mars_dict_data = scrape_mars.scrape()
    mars_dict.update({}, mars_dict_data, upsert=True)
    return redirect("/", code=302)

#End Flask
if __name__ == "__main__":
    app.run(debug=True)
