import re
from PySide2 import QtCore, QtWidgets

import panelCollector
from panels.preferences.base import Preference

import panels.basePanel


class _PanelHacker(QtCore.QObject):

    _globalInstance = None
    _initialized = False
    preferenceUpdated = QtCore.Signal(Preference)

    def __init__(self):
        super(_PanelHacker, self).__init__()

        self.registeredPanelTypes = dict()
        self.registeredPanels = dict()

    def registerPanel(self, panelWrapper: panels.basePanel.BasePanel):
        """
        Registers a custom panel with the hacker, so it can be loaded whenever the panel is opened
        inside of nuke
        Args:
            panelWrapper (panels.basePanel.BasePanel):  Panel wrapper that will be registered
        """
        regex = panelWrapper.regex()
        self.registeredPanelTypes[regex] = panelWrapper

        for panel in QtWidgets.QApplication.allWidgets():
            panelName = panel.objectName()
            if not panelName:
                continue

            self.linkPanel(panel)

    def linkPanel(self, panel: panels.basePanel.BasePanel) -> panels.basePanel.BasePanel:
        """
        This will link the wrapper panel with the nuke panel it is to be associated with.  This
        handles iterating over all nukes current panels, finds the panel that meets the requirements
        of the wrapper and links it
        Args:
            panel (panels.basePanel.BasePanel):

        Returns:
            panels.basePanel.BasePanel:  The wrapper panel after it has been linked or the panel that has
                              already been registered
        """
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
        """
        Checks to see if there is an active instance of the panel hacker and returns that.  If one
        is not yet present then a new instance will be collected and registered
        Returns:
            _PanelHacker: Current active instance of the Panel Hacker
        """
        instance = cls._globalInstance
        if not instance:
            instance = cls()
            cls._globalInstance = instance
            cls._initialized = True

        return instance

    @classmethod
    def initialized(cls):

        return cls._initialized


PanelHacker = _PanelHacker.globalInstance


def start():
    """
    Starts the panel hacker by initializing the panel collector and installing an event filter
    """
    if _PanelHacker.initialized() is False:

        panelCollector.PanelCollector().panelCollected.connect(PanelHacker().linkPanel)
        app = QtWidgets.QApplication.instance()
        app.installEventFilter(panelCollector.PanelCollector())


