import json
import os
import copy
import utilities
from panels.preferences.base import PreferenceEncoder


class _Globals(object):

    scriptEditorType = 'phScriptEditor'
    preferencesType = 'phPreferences'

    def __init__(self):
        super(_Globals, self).__init__()

        self._preferencePath = None
        self._preferences = None

    @property
    def preferencePath(self):

        if self._preferencePath is None:
            userDir = utilities.getUserDir()
            if not userDir:
                return None

            self._preferencePath = os.path.join(userDir, 'panelHacker.json').replace('\\', '/')

        return self._preferencePath

    @property
    def preferences(self):

        if self._preferences is None:
            if not os.path.exists(self.preferencePath):
                self._preferences = dict()

            else:
                with open(self.preferencePath, 'r') as preferenceFile:
                    self._preferences = json.load(preferenceFile)

            if not isinstance(self._preferences, dict):
                self._preferences = dict()

        return self._preferences

    def savePreference(self, preference):

        preferences = copy.deepcopy(self.preferences)
        preferences[preference.key] = preference
        with open(self.preferencePath, 'w') as preferenceFile:
            json.dump(preferences, preferenceFile, cls=PreferenceEncoder)

        self._preferences = preferences


Globals = _Globals()
