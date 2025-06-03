from lib.db.connection import CURSOR, CONN

class Pet:
    VALID_TYPES = ['dog', 'cat', 'bird', 'fish', 'lizard', 'hamster']

    def __init__(self, name, pet_type, owner_id=None, id=None):
        self.id = id
        self.name = name
        self.pet_type = pet_type
        self.owner_id = owner_id

    @property
    def pet_type(self):
        return self._pet_type

    @pet_type.setter
    def pet_type(self, value):
        if value.lower() not in Pet.VALID_TYPES:
            raise ValueError(f"{value} is not a valid pet type.")
        self._pet_type = value.lower()

    def save(self):
        if self.id:
            CURSOR.execute(
                "UPDATE pets SET name = ?, pet_type = ?, owner_id = ? WHERE id = ?",
                (self.name, self.pet_type, self.owner_id, self.id)
            )
        else:
            CURSOR.execute(
                "INSERT INTO pets (name, pet_type, owner_id) VALUES (?, ?, ?)",
                (self.name, self.pet_type, self.owner_id)
            )
            self.id = CURSOR.lastrowid
        CONN.commit()

    def delete(self):
        CURSOR.execute("DELETE FROM pets WHERE id = ?", (self.id,))
        CONN.commit()

    def get_owner(self):
        from lib.db.models.owner import Owner
        return Owner.find_by_id(self.owner_id)

    @classmethod
    def instance_from_db(cls, row):
        id, name, pet_type, owner_id = row
        return cls(name, pet_type, owner_id, id)

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM pets")
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute("SELECT * FROM pets WHERE id = ?", (id,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_owner_id(cls, owner_id):
        CURSOR.execute("SELECT * FROM pets WHERE owner_id = ?", (owner_id,))
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    def __repr__(self):
        return f"<Pet {self.id}: {self.name} the {self.pet_type}>"
