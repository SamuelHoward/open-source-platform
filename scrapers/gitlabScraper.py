# This file is used to retrieve data about open source projects from gitlab

# Import Modules
import requests
from bs4 import BeautifulSoup

# Function for 'scraping' gitlab for open source projects, returns list of dictionaries
def gitlabScrape():

    # Initialize empty list
    ret = []
    
    # Use requests module to access gitlab open source page and save it
    result = requests.get("https://about.gitlab.com/solutions/open-source/projects/")

    # store site content
    src = result.content

    # Use BeautifulSoup to parse and process a webpage
    soup = BeautifulSoup(src, 'lxml')

    # Use find_all to find all rows on the page
    pcs = soup.find_all("tr")

    # Loop through rows
    for pc in pcs:

        # Find all cells in row
        cells = pc.find_all("td")

        # Find links in cell
        for a in cells:

            # If link is present, save it
            link = a.find_all("a")

            # Form disctionary representing JSON object
            if (len(link) > 0):
                name = a.text.strip()
                url = link[0].get('href')
            else:
                description = a.text.strip()
                objDict = {
                    "name": name,
                    "url": url,
                    "description": description,
                    "source": "gitlab"
                }

                # Append JSON dictionary to list
                ret.append(objDict)

    # Return list of dictionaries
    return ret
