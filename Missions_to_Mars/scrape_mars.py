#Import Dependencies
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import time

#Setup init_browser function
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

#Scrape function
def scrape():
    mars_dict = {}

    #Initiate Browser
    browser = init_browser()

    #Read in NASA Mars News Site into Python
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(5)
    html = browser.html

    #Create a BeautifulSoup Object
    soup = bs(html, 'html.parser')

    #Find the Latest News Title from NASA website and save in a variable
    news_title = soup.find_all('div', class_='content_title')[1].text

    #Find the Latest News Paragraph from NASA website and save in a variable
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    #Use pandas to read in table of Mars facts
    facts_url = 'https://space-facts.com/mars/'
    facts_table = pd.read_html(facts_url)

    #Convert table to a DataFrame, rename column hearders
    df = facts_table[0]
    df.columns = ['Interesting Mars Facts', 'Values']

    #Scrape Mars Hemispheres
    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hem_url)
    time.sleep(5)
    html = browser.html

    #Finding the main hemisphere links
    links = browser.find_by_css("a.product-item h3")

    #Create Empty List
    hemisphere_image_urls = []

    #Run a for loop to append dictionary
    for i in range(len(links)):
        hemisphere = {}
    
        #We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item h3")[i].click()
    
        #Next, we find the Sample image anchor tag and extract the href
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
    
        #Get Hemisphere title
        hemisphere['title'] = browser.find_by_css("h2.title").text
    
        #Append hemisphere object to list
        hemisphere_image_urls.append(hemisphere)

    #Close the browser
    browser.quit()

    #Create a dictionary with all your scraped information
    mars_dict={
        "news_title":news_title,
        'news_p':news_p,
        "fact_table": df,
        "mars_images":hemisphere_image_urls
        }
    
    #Return the Mars Facts Dictionary
    return mars_dict



