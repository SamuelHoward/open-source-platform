# This file is used to retrieve data about open source projects from up for grabs

# Import Modules
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
import time


# Function for 'scraping' up for grabs for open source projects, returns list of dictionaries
def upForGrabsScrape():

    # Initialize empty list
    ret = []

    # Use selenium to access up for grabs webpage
    url = "https://up-for-grabs.net/#"
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", "open-source-platform")
    browser = webdriver.Firefox(profile, firefox_options=opts)
    browser.get(url)
    time.sleep(5)
    src = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    
    # Use BeautifulSoup to parse and process a webpage
    soup = BeautifulSoup(src, 'lxml')
        
    # Use find_all to find all rows on the page
    pcs = soup.find_all("tbody", {"class": "counted"})
        
    # Loop through rows
    for pc in pcs:
            
        # Extract dict components
        nameAndURL = pc.find_all("span", {"class": "proj"})[0].find_all("a")[0]
        name = nameAndURL.text.strip()
        url = nameAndURL.get('href')
        description = pc.find_all("span", {"class": "desc"})[0].text.strip()
            
        # Form disctionary representing JSON object
        objDict = {
            "name": name,
            "url": url,
            "description": description,
            "source": "up-for-grabs"
        }
        
        # Append JSON dictionary to list
        ret.append(objDict)
            
    # Return list of dictionaries
    return ret
