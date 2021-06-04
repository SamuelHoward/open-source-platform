# This file is for filling up a SQLite database with open source project data

# Import Modules
import sqlite3
import githubScraper
import gitlabScraper
import openSourceGoogleScraper
import codeTriageScraper
import upForGrabsScraper
import requests
import json

# Initialize some sounter variables
newRecords = 0
oldRecords = 0

# Connect to a local database
db = sqlite3.connect('projects.db')
cur = db.cursor()

# Temp: Drop the pre-existing database
#cur.execute('DROP TABLE IF EXISTS Projects')

# Create the database
cur.execute('''CREATE TABLE IF NOT EXISTS Projects(
               name TEXT PRIMARY KEY, url TEXT, 
               description TEXT, source TEXT,
               owner TEXT, language TEXT,
               owner_avatar TEXT, created_time TEXT,
               last_updated TEXT
               )''')

# Scrape for projects
print("Begin scraping")
print("Scrape github")
projs = githubScraper.githubScrape(6)
print("Scrape gitlab")
projs += gitlabScraper.gitlabScrape()
print("Scrape openSourceGoogle")
projs += openSourceGoogleScraper.openSourceGoogleScrape()
print("Scrape codeTriage")
projs += codeTriageScraper.codeTriageScrape(8)
print("Scrape upForGrabs")
projs += upForGrabsScraper.upForGrabsScrape()
print("Add records to Projects database")

# Add each project to the SQLite database
for proj in projs:

    # Check if record exists
    cur.execute("SELECT name FROM Projects WHERE name = ?", (proj['name'],))
    foundRecords = cur.fetchall()

    # If record does not exist, add it
    if len(foundRecords) == 0:
    
        # Dynamically form SQL command
        cols = ', '.join(proj.keys())
        placeHolders = ', '.join('?' * len(proj))
        sql = 'INSERT INTO Projects ({}) VALUES ({})'.format(cols, placeHolders)
        
        # Execute and commit the SQL command
        cur.execute(sql, [val for val in proj.values()])
        db.commit()

        # Increment new records
        newRecords += 1
        
    else:

        # Increment old records
        oldRecords += 1

print("Total new records added to database: " + str(newRecords))
print("Total existing records seen again: " + str(oldRecords))

cur.execute('DROP TABLE IF EXISTS Organizations')
cur.execute('''CREATE TABLE Organizations AS 
               SELECT DISTINCT owner AS "name", owner_avatar AS "avatar"
               FROM Projects
               ''')
cur.execute('''ALTER TABLE Organizations
               ADD COLUMN url TEXT''')
cur.execute('''UPDATE Organizations SET url = "https://github.com/" || name''')
db.commit()

#cur.execute("SELECT * FROM Organizations")
#foundOrgRecords = cur.fetchall()

#cur.execute('''ALTER TABLE Organizations
#               ADD COLUMN avatar TEXT''')

#for org in foundOrgRecords:

#    result = requests.get("https://api.github.com/search/users?q=" + org[0]).json()
#    print(org)
#    print(result)

#    if "items" in result:
#        sql = "UPDATE Organizations SET avatar = " + json.dumps(result["items"][0]["avatar_url"]) + "  WHERE name = '" + org[0] + "'"
#        print(sql)
#        cur.execute(sql)
#        db.commit()
