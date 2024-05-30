from PySide2 import QtCore


class BasePanel(QtCore.QObject):
    requiredAttributes = []
    cacheWrapper = True

    def __init__(self, panel, hackerParent=None):
        super(BasePanel, self).__init__()

        self.panel = panel
        self.hackerParent = hackerParent

    def initialize(self):
        """
        Used to initialize the panel and must be implemented by the child class
        """
        raise NotImplementedError()

    @property
    def preferenceType(self):
        """
        Must be implemented by the child class and return the preference type
        """
        raise NotImplementedError()

    def updatePreferences(self, preference):

        if preference.preferenceType != self.preferenceType or not preference.key:
            return

        attrs = preference.key.split('.')
        currentObject = self
        for attr in attrs:
            if not hasattr(currentObject, attr):
                return
            if attr != attrs[-1]:
                currentObject = getattr(currentObject, attr)

        if callable(getattr(currentObject, attrs[-1])):
            return

        setattr(currentObject, attrs[-1], preference.value or getattr(currentObject, attrs[-1]))

    @classmethod
    def regex(cls):
        """
        This is the regex that will be used to find the nuke panel that we want to interact with and
        must be implemented by the child class
        """
        raise NotImplementedError()
