# This file is used to retrieve data about open source projects from google's open source page

# Import Modules
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import FirefoxOptions

# Function for 'scraping' google's open source page for open source projects,
# returns list of dictionaries
def openSourceGoogleScrape():

    # Initialize empty list
    ret = []
    
    # Use selenium to access open source google webpage
    url = "https://opensource.google/projects/list/cloud?page=2"
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", "open-source-platform")
    browser = webdriver.Firefox(profile, firefox_options=opts)
    browser.get(url)
    src = browser.page_source
    
    # Use BeautifulSoup to parse and process a webpage
    soup = BeautifulSoup(src, 'lxml')

    # Use find_all to find all project cards
    pcs = soup.find_all("a", {"class": "project-card"})

    
    # Loop cards
    for pc in pcs:

        # Extract the project name, description, and url
        name = pc.find_all("h3")[0].text.strip()
        description = pc.find_all("p")[0].text.strip()
        url = "https://opensource.google" + pc.get('href')

        # Store those values in a dictionary
        objDict = {
            "name": name,
            "url": url,
            "description": description,
            "source": "open-source-google"
        }
        
        # Append JSON dictionary to list
        ret.append(objDict)

    # Return list of dictionaries
    return ret
