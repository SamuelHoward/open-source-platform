# This file is used to retrieve data about open source projects from codeTriage

# Import Modules
import requests
from bs4 import BeautifulSoup

# Function for 'scraping' codeTriage for open source projects, returns list of dictionaries
def codeTriageScrape(pageLimit):

    # Initialize empty list
    ret = []

    # Use function argument to determine the number of pages to access
    for i in range(pageLimit):
            
        # Use requests module to access gitlab open source page and save it
        result = requests.get("https://www.codetriage.com/?page=" + str(i+1))

        # store site content
        src = result.content

        # Use BeautifulSoup to parse and process a webpage
        soup = BeautifulSoup(src, 'lxml')

        # Use find_all to find all cards on the page
        pcs = soup.find_all("li", {"class": "repo-item"})

        # Loop through rows
        for pc in pcs:

            # Extract the project name, description, and url
            name = pc.find_all("h3")[0].text.strip()
            description = pc.find_all("p")[0].text.strip()
            urlSuffix = pc.find_all("a")[0].get('href')
            url = "https://www.codetriage.com" + urlSuffix
            owner = urlSuffix[1:urlSuffix[1:].find('/')+1]
            language = pc.get('data-language')
            
            # Store those values in a dictionary
            objDict = {
                "name": name,
                "url": url,
                "description": description,
                "source": "codeTriage",
                "owner": owner,
                "language": language,
            }
        
            # Append JSON dictionary to list
            ret.append(objDict)
                    
    # Return list of dictionaries
    return ret
