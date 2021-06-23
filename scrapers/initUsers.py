# This file is for filling up a SQLite database with open source project data

# Import Modules
import sqlite3

# Connect to a local database
db = sqlite3.connect('projects.db')
cur = db.cursor()
#cur.execute('DROP TABLE IF EXISTS Users')

# Create the user database
cur.execute('''CREATE TABLE IF NOT EXISTS Users(
               id INT PRIMARY KEY, email TEXT UNIQUE, 
               password TEXT, name TEXT
               )''')
