import logging
from PySide2 import QtWidgets, QtGui, QtCore

from widgets import baseWidget


class ColourChip(baseWidget.BaseWidget):

    colourChanged = QtCore.Signal(list)

    def __init__(self, label=None, colour=None):
        super(ColourChip, self).__init__()

        self.label = label or ''
        self.colour = colour
        self.masterLayout = QtWidgets.QHBoxLayout()
        self.colourChip = QtWidgets.QPushButton()
        self.colourLabel = QtWidgets.QLabel(self.label)

    def initializeInterface(self):
        self.masterLayout.addWidget(self.colourChip)
        self.masterLayout.addWidget(self.colourLabel)
        self.setLayout(self.masterLayout)
        self.masterLayout.setContentsMargins(0, 0, 0, 0)

    def initializeDefaults(self):
        self.colourChip.setFixedHeight(20)
        self.colourChip.setFixedWidth(20)

        if self.colour:
            self.setColour(self.colour)

    def initializeSignals(self):

        self.colourChip.pressed.connect(self.getColour)

    def getColour(self):

        colourPicker = QtWidgets.QColorDialog()
        colourPicker.colorSelected.connect(self.setColour)
        colourPicker.exec_()

    def setColour(self, colour):

        if isinstance(colour, QtGui.QColor):
            colour = [colour.red(), colour.green(), colour.blue()]

        elif len(colour) != 3:
            raise AttributeError('RGB values must be passed to set the colour, ie: (255, 255, 255)')

        if not isinstance(colour, list):
            colour = list(colour)

        self.colour = colour
        self.colourChip.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.colour))
        self.colourChanged.emit(self.colour)

