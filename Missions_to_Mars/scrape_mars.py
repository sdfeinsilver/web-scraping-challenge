#Import dependencies
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import time

#Setup init_browser function
def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

#Define scrape function to scrape all data from jupyter notebook and store in python dictionary
def scrape():
    try:
        browser = init_browser()
        mars_facts = {}
        
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

        #Add News Article and Paragraph to mars facts dictionary
        mars_facts['news_title'] = news_title
        mars_facts['news_p'] = news_p

        #Use pandas to read in table of Mars facts
        facts_url = 'https://space-facts.com/mars/'
        facts_table = pd.read_html(facts_url)

        #Convert table to a DataFrame, rename column hearders
        df = facts_table[0]
        df.columns = ['Interesting Mars Facts', 'Values']

        #Use Pandas to convert the data to a HTML table string    
        html_table = df.to_html()

        #Strip unwanted new lines (/n)
        html_table.replace('\n', '')

        #Add Mars table to Mars facts dictionary
        mars_facts['mars_facts_table'] = html_table

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

        #Add Mars table to Mars facts dictionary
        mars_facts['hemisphere_image_urls'] = hemisphere_image_urls

    #Close the browser
    finally:
        browser.quit()
    
    #Return the Mars Facts Dictionary
    return mars_facts