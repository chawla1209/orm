import uuid
from orm.database.base import BaseDatabase

class NoSQLDatabase(BaseDatabase):
    _db = {}

    def connect(self):
        return self._db

    def create_table(self, model):
        if model.__name__.lower() not in self._db:
            self._db[model.__name__.lower()] = {}

    def insert(self, model):
        table = self._db[model.__class__.__name__.lower()]
        record_id = str(uuid.uuid4())
        table[record_id] = {key: getattr(model, key) for key in model._meta.keys()}
        model.id = record_id

    def select(self, model, **conditions):
        table = self._db[model.__name__.lower()]
        results = [
            {key: value for key, value in record.items() if all(record[k] == v for k, v in conditions.items())}
            for record in table.values()
        ]
        return results, list(model._meta.keys())

    def delete(self, model, **conditions):
        table = self._db[model.__name__.lower()]
        keys_to_delete = [
            key for key, record in table.items()
            if all(record[k] == v for k, v in conditions.items())
        ]
        for key in keys_to_delete:
            del table[key]

    def update(self, model, **conditions):
        table = self._db[model.__name__.lower()]
        for key, record in table.items():
            if all(record[k] == v for k, v in conditions.items()):
                for field, value in conditions.items():
                    record[field] = value

    def execute_script(self, script):
        # NoSQL databases do not use SQL scripts, but this method is required for compatibility
        pass
