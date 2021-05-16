# This file is for filling up a SQLite database with open source project data

# Import Modules
import sqlite3
import githubScraper
import gitlabScraper
import openSourceGoogleScraper
import codeTriageScraper
import upForGrabsScraper

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
               description TEXT, source TEXT
               )''')

# Scrape for projects
print("Begin scraping")
projs = githubScraper.githubScrape(3)
projs += gitlabScraper.gitlabScrape()
projs += openSourceGoogleScraper.openSourceGoogleScrape()
projs += codeTriageScraper.codeTriageScrape(4)
projs += upForGrabsScraper.upForGrabsScrape()

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
