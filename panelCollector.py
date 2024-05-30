from PySide2 import QtCore


class PanelCollector(QtCore.QObject):

    panelCollected = QtCore.Signal(object)

    def eventFilter(self, widget, event):

        success = super(PanelCollector, self).eventFilter(widget, event)
        if event.type() == QtCore.QEvent.ShowToParent:
            if widget.objectName():
                self.panelCollected.emit(widget)

        return success
