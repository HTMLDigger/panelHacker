from globals import Globals
from .base import Preference
from widgets import colorChip


class ColorPreference(Preference):

    def __init__(self, key, name=None, value=None, **kwargs):
        super(ColorPreference, self).__init__(key, name, value, **kwargs)

        self._default = kwargs.get('default')
        self.callable = kwargs.get('callable', None)
        self.colorChip = colorChip.ColorChip(self.name, color=self.default)
        self.colorChip.setToolTip(kwargs.get('toolTip', self.key))

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, value):

        self.colorChip.defaultColor = value
        self._default = value

    @property
    def preferenceType(self):
        return Globals.scriptEditorType

    def initialize(self):

        previousValue = Globals.sePreferences.get(self.key, None)
        if previousValue:
            if isinstance(previousValue, dict):
                previousValue = ColorPreference(**previousValue)

            previousValue = previousValue.value
        self.colorChip.setColor(previousValue or self.default)
        if self.callable:
            self.colorChip.colorChanged.connect(self.update)

    def update(self, value):

        self.value = value
        self.callable(self)
