#Import Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#Create an instance of Flask
app = Flask(__name__)

#Use pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    mars_dict = mongo.db.mars_info
    mars_dict_data = scrape_mars.scrape()
    mars_dict.replace_one({}, mars_dict_data, upsert=True)
    return redirect("/")

#Create Home Route
@app.route("/")
def home():
    mars_dict = mongo.db.mars_info.find_one()
    return render_template("index.html", dict=mars_dict)

#End Flask
if __name__ == "__main__":
    app.run(debug=True)
