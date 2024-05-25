from orm.models import Model
from orm.fields import IntegerField, CharField
from orm.database.sqlite import SQLiteDatabase
from orm.database.nosql import NoSQLDatabase
from orm.migrations import Migration

class User(Model):
    id = IntegerField()
    name = CharField(max_length=100)
    age = IntegerField()

if __name__ == "__main__":
    # Choose database (SQLite or NoSQL)
    db = SQLiteDatabase()
    # db = NoSQLDatabase()
    Model.set_db(db)

    # Create migrations
    migration = Migration(db)
    migration.make_migration('001_initial')
    migration.apply_migrations()

    # Example usage
    user = User.create(id=1, name="John Doe", age=30)
    fetched_user = User.get(id=1)
    print(fetched_user.to_dict())

    # Filter users
    users = User.filter(age=30)
    for user in users:
        print(user.to_dict())

    # Update user
    user.update(name="Jane Doe")
    updated_user = User.get(id=1)
    print(updated_user.to_dict())

    # Delete user
    user.delete()
    deleted_user = User.get(id=1)
    print(deleted_user)