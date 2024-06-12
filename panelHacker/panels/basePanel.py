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
    def panelType(self):
        """
        Must be implemented by the child class and return the preference type
        """
        raise NotImplementedError()

    def updatePreferences(self, preference):
        """
        This will take the given preference and ensure that it is the correct type for the panel
        next we ensure that the panel has the required attributes, then we update the preference

        for example if the preference key is 'highlighter.dunderHighlighter' then we will check
        that the panel has the attribute 'highlighter' and that 'highlighter' has the attribute
        'dunderHighlighter'. If it does then we will set the value of 'dunderHighlighter' on the
        highlighter to the preference value or whatever the previous value was if the preference
        value is None

        Args:
            preference (Preference): The preference that will be used to update the panel
        """

        # If the preference is not the correct type for the panel then we return
        if preference.preferenceType != self.panelType or not preference.key:
            return

        attrs = preference.key.split('.')
        currentObject = self
        # Ensure that the panel has the required attributes
        for attr in attrs:
            if not hasattr(currentObject, attr):
                return
            if attr != attrs[-1]:
                currentObject = getattr(currentObject, attr)

        # If the last attribute is callable then we return
        if callable(getattr(currentObject, attrs[-1])):
            return

        # Update the preference
        setattr(currentObject, attrs[-1], preference.value or getattr(currentObject, attrs[-1]))

    @classmethod
    def regex(cls):
        """
        This is the regex that will be used to find the nuke panel that we want to interact with and
        must be implemented by the child class
        """
        raise NotImplementedError()
