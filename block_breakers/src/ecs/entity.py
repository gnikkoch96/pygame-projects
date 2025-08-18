class Entity:
    _id_counter = 1
    def __init__(self):
        self.id = Entity._id_counter
        Entity._id_counter += 1
        self.components = {}
    def add_component(self, component):
        self.components[type(component)] = component
    def get_component(self, component_type):
        return self.components.get(component_type)
