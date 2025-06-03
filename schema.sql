DROP TABLE IF EXISTS owners;
DROP TABLE IF EXISTS pets;

CREATE TABLE owners (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE pets (
    id INTEGER PRIMARY KEY,
    name TEXT,
    pet_type TEXT,
    owner_id INTEGER,
    FOREIGN KEY (owner_id) REFERENCES owners(id)
);
