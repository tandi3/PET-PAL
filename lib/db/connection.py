import sqlite3

CONN = sqlite3.connect('lib/db/petpal.db')
CURSOR = CONN.cursor()

# Enable foreign key constraints
CURSOR.execute("PRAGMA foreign_keys = ON;")

# Drop tables safely
CURSOR.execute("PRAGMA foreign_keys = OFF;")
CURSOR.execute("DROP TABLE IF EXISTS pets;")
CURSOR.execute("DROP TABLE IF EXISTS owners;")
CURSOR.execute("PRAGMA foreign_keys = ON;")

# Create 'owners' table
CURSOR.execute("""
    CREATE TABLE IF NOT EXISTS owners (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
""")

# Create 'pets' table with foreign key to 'owners'
CURSOR.execute("""
    CREATE TABLE IF NOT EXISTS pets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        pet_type TEXT NOT NULL,
        owner_id INTEGER,
        FOREIGN KEY (owner_id) REFERENCES owners(id)
    );
""")

CONN.commit()
