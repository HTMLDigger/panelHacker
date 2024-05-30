import re
from PySide2 import QtCore, QtWidgets

import panelCollector
from panels.preferences.base import Preference


HACKER = None
COLLECTOR = None


class _PanelHacker(QtCore.QObject):

    _globalInstance = None
    preferenceUpdated = QtCore.Signal(Preference)

    def __init__(self):
        super(_PanelHacker, self).__init__()

        self.registeredPanelTypes = dict()
        self.registeredPanels = dict()

    def registerPanelType(self, regex, panelWrapper):

        self.registeredPanelTypes[regex] = panelWrapper

        for panel in QtWidgets.QApplication.allWidgets():
            panelName = panel.objectName()
            if not panelName:
                continue

            self.registerPanel(panel)

    def registerPanel(self, panel):

        registered = self.registeredPanels.get(panel.winId(), None)
        if registered:
            return registered

        for regex, panelWrapper in self.registeredPanelTypes.items():
            if re.search(regex, panel.objectName()):
                wrapper = panelWrapper(panel, hackerParent=self)
                if hasattr(wrapper, 'requiredAttributes'):
                    skipWidget = False
                    for attr in wrapper.requiredAttributes:
                        if not hasattr(wrapper, attr):
                            skipWidget = True
                            break

                    if skipWidget:
                        continue

                if wrapper.cacheWrapper:
                    self.registeredPanels[panel.winId()] = wrapper
                if hasattr(wrapper, 'updatePreferences'):
                    self.preferenceUpdated.connect(wrapper.updatePreferences)

                wrapper.initialize()
                return wrapper

    @classmethod
    def globalInstance(cls):

        instance = cls._globalInstance
        if not instance:
            instance = cls()
            cls._globalInstance = instance

        return instance


PanelHacker = _PanelHacker.globalInstance


def start():

    global HACKER
    global COLLECTOR
    if HACKER is None:
        HACKER = PanelHacker()
        COLLECTOR = panelCollector.PanelCollector()
        COLLECTOR.panelCollected.connect(HACKER.registerPanel)

        app = QtWidgets.QApplication.instance()
        app.installEventFilter(COLLECTOR)


