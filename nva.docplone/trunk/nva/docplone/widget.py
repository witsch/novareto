from Products.Archetypes.Widget import TypesWidget

class DocPloneWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update({
                'macro': "docplone"})
