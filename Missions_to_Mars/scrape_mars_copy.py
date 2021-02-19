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
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

#Define scrape function to scrape all data from jupyter notebook and store in python dictionary
def scrape():
        browser = init_browser()
        mars_dict = {}
        return    
        
def news():
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
        mars_dict['news_title'] = news_title
        mars_dict['news_p'] = news_p
        return mars_dict