from orm.fields import Field, IntegerField, CharField
from orm.database.sqlite import SQLiteDatabase
from orm.database.nosql import NoSQLDatabase

class ModelMeta(type):
    def __new__(cls, name, bases, dct):
        new_class = super().__new__(cls, name, bases, dct)
        new_class._meta = {}
        for key, value in dct.items():
            if isinstance(value, Field):
                value.name = key
                new_class._meta[key] = value
        return new_class

class Model(metaclass=ModelMeta):
    _db = None

    @classmethod
    def set_db(cls, db_instance):
        cls._db = db_instance

    def __init__(self, **kwargs):
        for key in self._meta.keys():
            value = kwargs.get(key)
            self._meta[key].validate(value)
            setattr(self, key, value)

    @classmethod
    def create(cls, **kwargs):
        cls._db.create_table(cls)
        obj = cls(**kwargs)
        cls._db.insert(obj)
        return obj

    @classmethod
    def get(cls, **kwargs):
        cls._db.create_table(cls)
        result, columns = cls._db.select(cls, **kwargs)
        if result:
            return cls(**dict(zip(columns, result[0])))
        return None

    @classmethod
    def filter(cls, **kwargs):
        cls._db.create_table(cls)
        results, columns = cls._db.select(cls, **kwargs)
        return [cls(**dict(zip(columns, row))) for row in results]

    def save(self):
        self._db.create_table(self.__class__)
        self._db.insert(self)

    def delete(self):
        self._db.delete(self.__class__, id=self.id)

    def update(self, **kwargs):
        self._db.update(self, **kwargs)

    def to_dict(self):
        return {key: getattr(self, key) for key in self._meta.keys()}

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
