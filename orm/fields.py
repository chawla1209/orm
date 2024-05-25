class Field:
    def __init__(self):
        self.name = None  # Will be set dynamically by the metaclass

    def validate(self, value):
        pass

class IntegerField(Field):
    def __init__(self):
        super().__init__()

    def validate(self, value):
        if not isinstance(value, int):
            raise ValueError(f"Expected int, got {type(value).__name__}")

class CharField(Field):
    def __init__(self, max_length):
        super().__init__()
        self.max_length = max_length

    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError(f"Expected str, got {type(value).__name__}")
        if len(value) > self.max_length:
            raise ValueError(f"String too long, maximum length is {self.max_length}")
