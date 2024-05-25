import sqlite3
from orm.database.base import BaseDatabase
from orm.fields import IntegerField, CharField

class SQLiteDatabase(BaseDatabase):
    _conn = None

    def connect(self):
        if self._conn is None:
            self._conn = sqlite3.connect(':memory:')
        return self._conn

    def create_table(self, model):
        conn = self.connect()
        cursor = conn.cursor()
        columns = []
        for field_name, field in model._meta.items():
            if isinstance(field, IntegerField):
                columns.append(f"{field_name} INTEGER")
            elif isinstance(field, CharField):
                columns.append(f"{field_name} TEXT({field.max_length})")
        columns_sql = ", ".join(columns)
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {model.__name__.lower()} ({columns_sql})")
        conn.commit()

    def insert(self, model):
        conn = self.connect()
        cursor = conn.cursor()
        columns = ', '.join(model._meta.keys())
        placeholders = ', '.join(['?' for _ in model._meta.keys()])
        values = [getattr(model, key) for key in model._meta.keys()]
        query = f"INSERT INTO {model.__class__.__name__.lower()} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, values)
        conn.commit()

    def select(self, model, **conditions):
        conn = self.connect()
        cursor = conn.cursor()
        query = f"SELECT * FROM {model.__name__.lower()} WHERE " + " AND ".join(f"{k} = ?" for k in conditions.keys())
        cursor.execute(query, tuple(conditions.values()))
        result = cursor.fetchall()
        return result, [col[0] for col in cursor.description]

    def delete(self, model, **conditions):
        conn = self.connect()
        cursor = conn.cursor()
        query = f"DELETE FROM {model.__name__.lower()} WHERE " + " AND ".join(f"{k} = ?" for k in conditions.keys())
        cursor.execute(query, tuple(conditions.values()))
        conn.commit()

    def update(self, model, **conditions):
        conn = self.connect()
        cursor = conn.cursor()
        set_clause = ", ".join([f"{key} = ?" for key in conditions.keys()])
        query = f"UPDATE {model.__class__.__name__.lower()} SET {set_clause} WHERE id = ?"
        values = [conditions[key] for key in conditions.keys()] + [model.id]
        cursor.execute(query, values)
        conn.commit()

    def execute_script(self, script):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.executescript(script)
        conn.commit()