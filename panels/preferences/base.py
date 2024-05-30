import json
from PySide2 import QtCore


class Preference(QtCore.QObject):

    def __init__(self, key, name=None, value=None, **kwargs):
        super(Preference, self).__init__()

        self.key = key
        self.name = name or self.key
        self.value = value or None

    def __reduce__(self):
        return (Preference, (self.key, self.name, self.value,),)

    @property
    def preferenceType(self):
        raise NotImplementedError()

    def initialize(self):

        raise NotImplementedError()


class PreferenceEncoder(json.JSONEncoder):
    def default(self, instance):
        if isinstance(instance, Preference):
            data = {'key': instance.key, 'value': instance.value, 'name': instance.name}
            return data

        try:
            return json.JSONEncoder.default(self, instance)
        except TypeError:
            return None
