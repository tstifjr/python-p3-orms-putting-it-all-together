import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    all = []
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)
    
    def save(self):
        sql="""
            INSERT INTO dogs (name, breed)
            VALUES (?,?)
        """
        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()
        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
    
    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM dogs
        """
        db_all = CURSOR.execute(sql).fetchall()
        cls.all = [cls.new_from_db(row) for row in db_all]
        return cls.all

    @classmethod
    def drop_table(cls):
        sql = """DROP TABLE IF EXISTS dogs"""

        CURSOR.execute(sql)

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM dogs
            WHERE name = ?
            LIMIT 1
        """
        dog = CURSOR.execute(sql, (name,)).fetchone()
        if dog == None:
            return None
        else:
            return cls.new_from_db(dog)

    @classmethod
    def find_by_id (cls, id):
        sql = """
            SELECT * FROM dogs
            WHERE id = ?
            LIMIT 1
        """
        dog = CURSOR.execute(sql, (id,)).fetchone()
        return cls.new_from_db(dog)
    
    @classmethod
    def find_or_create_by(cls, name, breed):
        if not cls.find_by_name(name):
            return cls.create(name, breed)
        else :
            return cls.find_by_name(name)
        
    
    def update(self) :
        sql = """
            UPDATE dogs
            SET name = ?
            WHERE id = ?
            """
        CURSOR.execute(sql, (self.name, self.id,))
        CONN.commit()