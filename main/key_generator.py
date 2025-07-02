class KeyGenerator:
    def __init__(self, column1=None, column2=None):
        if not column1:
            raise ValueError("At least one column must be specified for key generation.")
        self.column1 = column1
        self.column2 = column2
        self.key_list = []

    def generate(self, record):
        if self.column2:
            key = (record[self.column1], record[self.column2])
        else:
            key = record[self.column1]
        self.key_list.append(key)
        return key

    def get_keys(self):
        return self.key_list
