from orm.database.sqlite import SQLiteDatabase
from orm.database.nosql import NoSQLDatabase

def migrate(db):
    if isinstance(db, SQLiteDatabase):
        db.execute_script('''
            CREATE TABLE user (
                id INTEGER PRIMARY KEY,
                name TEXT(100),
                age INTEGER
            );
        ''')
    elif isinstance(db, NoSQLDatabase):
        db.create_table(User)
