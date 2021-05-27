# This file is used to retrieve data about open source projects from github

# Import Modules
import sys
import requests

# Function for 'scraping' github for open source projects, returns list of dictionaries
def githubScrape(pageLimit):

    # Initialize empty list
    ret = []
    
    # Use function argument to determine the number of pages to access
    for i in range(pageLimit):

        # Use github api to access projects tagged as open source
        result = requests.get(
            "https://api.github.com/search/repositories?q=topic:open-source" +
            "&per_page=100&page=" + str(i+1))

        # Store the projects' information within a JSON object
        for item in result.json()["items"]:
            objDict = {
                "name": item["name"],
                "url": item["html_url"],
                "description": item["description"],
                "source": "github",
                "owner": item["owner"]["login"],
                "owner_avatar": item["owner"]["avatar_url"],
                "language": item["language"],
            }

            # Append JSON dictionary to list
            ret.append(objDict)

    # Return list of dictionaries
    return ret
