#Import Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars_copy

#Create an instance of Flask
app = Flask(__name__)

#use PyMongo to establish Mongo Connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():

    #Find one record of data from mongo database
    mars = mongo.db.mars.find_one()

    #Return template and data
    return render_template("index.html", mars=mars)

#Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    print('Scripting')

    #Run the scrape function
    mars_data = scrape_mars_copy.scrape()

    #Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)
    
    #Redirect back to home page
    return redirect("/")

#End Flask
if __name__ == "__main__":
    app.run(debug=True)
