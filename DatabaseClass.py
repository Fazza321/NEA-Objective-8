import sqlite3
from PlayerClass import player


class PlayerScore:
    def __init__(self):
        # Initialize a connection to the SQLite database file
        self.myDatabase = sqlite3.connect('database.db')

        # Set initial values for instance variables
        self.name = None
        self.username = None
        self.password = None

        # Create the 'players' and 'scores' tables if they don't exist yet
        cursor = self.myDatabase.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS players (
                            nameID      integer,
                            name        text,
                            username    text,
                            password    text,
                            PRIMARY KEY ("nameID" AUTOINCREMENT)
                        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS scores ( 
                            timeID      integer,
                            time        real,
                            nameID      integer,
                            PRIMARY KEY ("timeID" AUTOINCREMENT),
                            FOREIGN KEY ("nameID") REFERENCES players ("nameID")
                        )''')

    def newUser(self, username, name, password, function):
        # Set instance variables based on input
        self.username = username
        self.password = password
        self.name = name

        # Check if the username already exists in the database
        cursor = self.myDatabase.cursor()
        cursor.execute('SELECT * FROM players WHERE username = ?', [username])
        if cursor.fetchall():
            print('Username Taken')
            return

        # Add the new user to the database
        cursor.execute('''INSERT INTO players(username, name, password)
                          VALUES(?, ?, ?)''', [username, name, password])
        self.myDatabase.commit()

        # Set the player name to the username and call the input function
        player.name = username
        function()

    def login(self, username, password, function):
        # Check if the username and password match a user in the database
        cursor = self.myDatabase.cursor()
        cursor.execute('SELECT * FROM players WHERE username = ? AND password = ?', [username, password])
        results = cursor.fetchall()

        if results:
            # If a matching user is found, set the player name to the username and call the input function
            for i in results:
                player.name = username
                print('Welcome ' + i[2])
                function()
        else:
            # If no matching user is found, print an error message
            print("username or password not recognized")

    def insertScores(self, score, name):
        # Insert a new score for the given player name into the 'scores' table
        cursor = self.myDatabase.cursor()
        cursor.execute('SELECT nameID FROM players WHERE name = (?)', [name])
        cursor.execute('INSERT INTO scores (time, nameID) VALUES (?, ?)', [score, cursor.fetchone()])
        self.myDatabase.commit()

        # Print all scores in the 'scores' table
        cursor.execute('SELECT * FROM scores')
        for item in cursor.fetchall():
            print(item)

    def allScores(self):
        # Print all players and all scores in the database
        cursor = self.myDatabase.cursor()
        cursor.execute('SELECT * FROM players')
        print(cursor.fetchall())
        cursor.execute('SELECT * FROM scores')
        print(cursor.fetchall())

    def sortScores(self):
        # Print all scores in the 'scores' table, sorted by time in ascending order
        cursor = self.myDatabase.cursor()
        cursor.execute('SELECT * FROM scores ORDER BY time')
        print(cursor.fetchall())

    def changeUser(self, name, newname):
        # Update the name of a user in the 'players' table
        cursor = self.myDatabase.cursor()
        cursor.execute('UPDATE SET name = (?) WHERE name = (?)', (newname, name))
        self.myDatabase.commit()


db = PlayerScore()
