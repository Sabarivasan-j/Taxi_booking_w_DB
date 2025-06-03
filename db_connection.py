import sqlite3

def get_connection():
    conn = sqlite3.connect('taxibooking.db')
    return conn

def setup_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Taxi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        currentSpot TEXT NOT NULL,
        freeTime INTEGER NOT NULL,
        totalEarning INTEGER NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Trip (
        tripId INTEGER PRIMARY KEY AUTOINCREMENT,
        taxiId INTEGER,
        customerId INTEGER,
        pickup TEXT,
        dropLoc TEXT,
        pickupTime INTEGER,
        dropTime INTEGER,
        amount INTEGER,
        FOREIGN KEY (taxiId) REFERENCES Taxi(id)
    )
    ''')
    conn.commit()
    conn.close()

# Call this once to setup tables
setup_database()
