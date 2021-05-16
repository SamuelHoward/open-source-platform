# Testing web scraping using requests and BeautifulSoup in Python

### https://github.com/topics/open-source ###

# Import requests and BeautifulSoup
import sys
import requests
from bs4 import BeautifulSoup

# Use requests module to access webpage and save it
result = requests.get("https://github.com/topics/open-source")

# Print status code for site, 200 means the site is accessible
print(result.status_code)

# Print HTTP header of site
print(result.headers)

# store site content
src = result.content
#print(src)

# Use BeautifulSoup to parse and process a webpage
soup = BeautifulSoup(src, 'lxml')

# Use find_all to find all links on the page
pcs = soup.find_all("article", {"class": "border rounded color-shadow-small color-bg-secondary my-4"})

# loop through links to filter them

for pc in pcs:

    # print(pc)
    '''
    print('{:16}'.format(pc.get('id')) +
          pc.find("span", {"class": "course-title"}).text.strip())
    '''
    aTags = pc.find_all("h1", {"class": "f3 color-text-secondary text-normal lh-condensed"})

    for a in aTags:

        print(a.text.strip())
    '''
    for sec in secs:

        print('{:16}'.format(sec.find("span", {"class": "section-id"}).text.strip()) +
              '{:32}'.format(sec.find("span", {"class": "section-instructor"}).text.strip()) +
              '{:3}'.format(sec.find("span", {"class": "open-seats-count"}).text.strip()) +
              " / " +
              '{:3}'.format(sec.find("span", {"class": "total-seats-count"}).text.strip())
        )

    print
    '''
