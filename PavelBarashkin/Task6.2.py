# #### Task 4.2
# Implement custom dictionary that will memorize 10 latest changed keys.
# Using method "get_history" return this keys.


class HistoryDict:
    def __init__(self, dct=None):
        self.history_dict = dct or {}
        self.history_list = []

    def set_value(self, key, value):
        self.history_dict[key] = value
        if key in self.history_list:
            self.history_list.remove(key)
        if len(self.history_list) < 10:
            self.history_list.insert(0, key)
        else:
            self.history_list.pop()
            self.history_list.insert(0, key)

    def get_history(self):
        print(self.history_list)


d = HistoryDict({'foo': 42})
d.set_value('bar', 36)
d.get_history()
