from globals import Globals
from .base import Preference
from widgets import colourCheck


class ColourPreference(Preference):

    def __init__(self, key, name=None, value=None, **kwargs):
        super(ColourPreference, self).__init__(key, name, value, **kwargs)

        self.default = kwargs.get('default')
        self.callable = kwargs.get('callable', None)
        self.colourChip = colourCheck.ColourChip(self.name)
        self.colourChip.setToolTip(kwargs.get('toolTip', self.key))

    @property
    def preferenceType(self):
        return Globals.scriptEditorType

    def initialize(self):

        previousValue = Globals.preferences.get(self.key, None)
        if previousValue:
            if isinstance(previousValue, dict):
                previousValue = ColourPreference(**previousValue)

            previousValue = previousValue.value
        self.colourChip.setColour(previousValue or self.default)
        if self.callable:
            self.colourChip.colourChanged.connect(self.update)

    def update(self, value):

        self.value = value
        self.callable(self)
