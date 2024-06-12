import json
from PySide2 import QtCore


class Preference(QtCore.QObject):

    def __init__(self, key, name=None, value=None, **kwargs):
        super(Preference, self).__init__()

        self.key = key
        self.name = name or self.key
        self.value = value or None

    def __reduce__(self):
        """
        Returns:
            tuple: A tuple containing the class and the arguments to be passed to the class
            constructor.
        """
        return (Preference, (self.key, self.name, self.value,),)

    @property
    def preferenceType(self):
        """
        Returns:
            str: The type of the preference.
        """
        raise NotImplementedError()

    def initialize(self):
        """
        Initializes the preference.  Since the preference will be added to the preference panel,
        this is where you will set up the UI elements for the preference along with any signals
        """
        raise NotImplementedError()


class PreferenceEncoder(json.JSONEncoder):
    def default(self, instance):
        """
        This ensures that the preference object is serialized correctly when it is saved to disk
        Args:
            instance (Preference):  The prefence object to be serialized

        Returns:
            dict|None:  The serialized preference object or None if the object is not a preference
        """
        if isinstance(instance, Preference):
            data = {'key': instance.key, 'value': instance.value, 'name': instance.name}
            return data

        try:
            return json.JSONEncoder.default(self, instance)
        except TypeError:
            return None
