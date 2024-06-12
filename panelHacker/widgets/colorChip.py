from PySide2 import QtWidgets, QtGui, QtCore

from widgets import baseWidget


class ColorChip(baseWidget.BaseWidget):

    colorChanged = QtCore.Signal(list)

    def __init__(self, label=None, color=None):
        super(ColorChip, self).__init__()

        self.defaultColor = color or (255, 255, 255)
        self.label = label or ''
        self.color = color
        self.masterLayout = QtWidgets.QHBoxLayout()
        self.colorChip = QtWidgets.QPushButton()
        self.colorLabel = QtWidgets.QLabel(self.label)

    def initializeInterface(self):
        """
        This is used to add all the widgets to the main layout and set all interface items.
        """
        self.masterLayout.addWidget(self.colorChip)
        self.masterLayout.addWidget(self.colorLabel)
        self.setLayout(self.masterLayout)
        self.masterLayout.setContentsMargins(0, 0, 0, 0)

    def initializeDefaults(self):
        """
        This will set all the initial values for all the widgets and self.
        """
        self.colorChip.setFixedHeight(20)
        self.colorChip.setFixedWidth(20)

        if self.color:
            self.setColor(self.color)

    def initializeSignals(self):
        """
        This will connect all the signals for all widgets and self.
        """
        self.colorChip.pressed.connect(self.getColor)

    def getColor(self):
        """
        This will open the color picker dialog and set the color of the chip
        """
        colorPicker = QtWidgets.QColorDialog()
        colorPicker.colorSelected.connect(self.setColor)
        colorPicker.exec_()

    def setColor(self, color):
        """
        This will set the color of the chip to the given color
        Args:
            color (tuple(int, int, int)): RGB values to set the color to
        """
        if isinstance(color, QtGui.QColor):
            color = [color.red(), color.green(), color.blue()]

        elif len(color) != 3:
            raise AttributeError('RGB values must be passed to set the color, ie: (255, 255, 255)')

        if not isinstance(color, list):
            color = list(color)

        self.color = color
        self.colorChip.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.color))
        self.colorChanged.emit(self.color)

    def mousePressEvent(self, event):
        """
        This will set the color of the chip to the default color if the right mouse button is pressed
        Args:
            event (QtGui.QMouseEvent):  Mouse event that triggered the function
        """
        if event.button() == QtCore.Qt.RightButton:
            self.setColor(self.defaultColor)
        else:
            super(ColorChip, self).mousePressEvent(event)

