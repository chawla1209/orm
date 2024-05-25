class BaseDatabase:
    def connect(self):
        raise NotImplementedError

    def create_table(self, model):
        raise NotImplementedError

    def insert(self, model):
        raise NotImplementedError

    def select(self, model, **conditions):
        raise NotImplementedError

    def delete(self, model, **conditions):
        raise NotImplementedError

    def update(self, model, **conditions):
        raise NotImplementedError

    def execute_script(self, script):
        raise NotImplementedError