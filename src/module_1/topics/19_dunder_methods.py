class Some:
    def __init__(self):
        self.field = "Some field"

    def __str__(self):
        return "str-" + self.field

    def __repr__(self):
        return "repr-" + self.field


print(Some())
