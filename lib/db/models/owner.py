from lib.db.connection import CONN, CURSOR
from lib.db.models.pet import Pet

class Owner:
    def __init__(self, name, id=None):
        self.name = name
        self.id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Owner name must be a non-empty string.")
        self._name = value.strip()

    def save(self):
        if self.id:
            CURSOR.execute("UPDATE owners SET name = ? WHERE id = ?", (self.name, self.id))
            CONN.commit()
        else:
            CURSOR.execute("INSERT INTO owners (name) VALUES (?)", (self.name,))
            self.id = CURSOR.lastrowid
            CONN.commit()

    def pets(self):
        CURSOR.execute("SELECT * FROM pets WHERE owner_id = ?", (self.id,))
        rows = CURSOR.fetchall()
        return [Pet.instance_from_db(row) for row in rows]

    def add_pet(self, pet):
        if not isinstance(pet, Pet):
            raise TypeError("Expected a Pet instance.")
        pet.owner_id = self.id
        pet.save()

    @classmethod
    def find_by_id(cls, owner_id):
        CURSOR.execute("SELECT * FROM owners WHERE id = ?", (owner_id,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM owners")
        return [cls.instance_from_db(row) for row in CURSOR.fetchall()]

    @classmethod
    def instance_from_db(cls, row):
        id, name = row
        return cls(name=name, id=id)

    def __repr__(self):
        return f"<Owner {self.id}: {self.name}>"
