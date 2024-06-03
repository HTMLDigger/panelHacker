from PySide2 import QtCore


class _PanelCollector(QtCore.QObject):

    _globalInstance = None
    _initialized = False
    panelCollected = QtCore.Signal(object)

    def __init__(self):

        super(_PanelCollector, self).__init__()

    def eventFilter(self, widget, event):

        success = super(_PanelCollector, self).eventFilter(widget, event)
        if event.type() == QtCore.QEvent.ShowToParent:
            if widget.objectName():
                self.panelCollected.emit(widget)

        return success

    @classmethod
    def globalInstance(cls) :
        """
        Checks to see if there is an active instance of the panel collector and returns that.  If
        one is not yet present then a new instance will be collected and registered
        Returns:
            _PanelCollector: Current active instance of the Panel Hacker
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


PanelCollector = _PanelCollector.globalInstance
