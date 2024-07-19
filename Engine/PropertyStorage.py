from collections import defaultdict


class PropertyStorage:
    def __init__(self):
        self.properties = defaultdict(None)

    def update(self, property_id, value):
        self.properties[property_id] = value

    def remove(self, property_id):
        self.properties.pop(property_id)

    def check(self, property_id):
        return property_id in self.properties.keys()

    def get(self, property_id):
        return self.properties[property_id]
