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
        """
        Returns:
            tuple(int, int, int): The default value of the preference.
        """
        return self._default

    @default.setter
    def default(self, value):
        """
        This ensures that the default value is set to the color chip widget
        Args:
            value (tuple(int, int, int)): tuple of the rgb values for the color chip
        """

        self.colorChip.defaultColor = value
        self._default = value

    @property
    def preferenceType(self):
        """
        Returns:
            str: The type of the preference.
        """
        return Globals.scriptEditorType

    def initialize(self):
        """
        Initialize the preference.  This will set the value of the preference to the value stored
        in the preferences if one is found otherwise it will set the value to the default value.
        Additionally, this will set up the UI elements for the preference and connect any signals.
        """
        previousValue = Globals.preferences.get(self.key, None)
        if previousValue:
            if isinstance(previousValue, dict):
                previousValue = ColorPreference(**previousValue)

            previousValue = previousValue.value
        self.colorChip.setColor(previousValue or self.default)
        if self.callable:
            self.colorChip.colorChanged.connect(self.update)

    def update(self, value):
        """
        Update the value of the preference and call the callable function
        Args:
            value (tuple(int, int, int)): tuple of the rgb values for the color chip
        """
        self.value = value
        self.callable(self)
