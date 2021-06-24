#

# Import Modules
import sqlite3

# Connect to a local database
db = sqlite3.connect('projects.db')
cur = db.cursor()
#cur.execute('DROP TABLE IF EXISTS Users')

# Create the user database
cur.execute('''CREATE TABLE IF NOT EXISTS Favorites(
               id INT PRIMARY KEY, user_id INT, 
               fav_name TEXT, fav_type TEXT
               )''')
