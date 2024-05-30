from panels import basePanel
from globals import Globals
from panels.preferences.scriptEditor import ColourPreference
from highlighters import syntaxPython


class Preferences(basePanel.BasePanel):
    requiredAttributes = ['scriptEditorLayout']
    cacheWrapper = False

    def __init__(self, panel=None, hackerParent=None):
        super(Preferences, self).__init__(panel, hackerParent=hackerParent)

        self.panel = panel

        self.initialized = False
        self._scriptEditorLayout = None
        self.keywordPreference = ColourPreference('highlighter.keywordHighlighter',
                                                  name='Keyword Highlighter',
                                                  toolTip='Highlighter color for Python keywords')
        self.classNamePreference = ColourPreference('highlighter.classNameHighlighter',
                                                    name='Class Name Highlighter',
                                                    toolTip='Highlighter color for Python class names')
        self.commentPreference = ColourPreference('highlighter.commentHighlighter',
                                                  name='Comment Highlighter',
                                                  toolTip='Highlighter color for Python comments')
        self.bracketPreference = ColourPreference('highlighter.bracketHighlighter',
                                                  name='Bracket Highlighter',
                                                  toolTip='Highlighter color for Python brackets')
        self.methodPreference = ColourPreference('highlighter.methodHighlighter',
                                                 name='Method Highlighter',
                                                 toolTip='Highlighter color for Python methods')
        self.stringPreference = ColourPreference('highlighter.stringHighlighter',
                                                 name='String Highlighter',
                                                 toolTip='Highlighter color for Python strings')
        self.dunderPreference = ColourPreference('highlighter.dunderHighlighter',
                                                 name='Dunder Highlighter',
                                                 toolTip='Highlighter color for Python dunder methods')
        self.selfPreference = ColourPreference('highlighter.selfHighlighter',
                                               name='Self Highlighter',
                                               toolTip='Highlighter color for Python self')
        self.builtInPreference = ColourPreference('highlighter.builtInHighlighter',
                                                  name='Built In Highlighter',
                                                  toolTip='Highlighter color for Python built in functions')
        self.numberPreference = ColourPreference('highlighter.numberHighlighter',
                                                 name='Number Highlighter',
                                                 toolTip='Highlighter color for Python numbers')

        self.preferences = [self.keywordPreference,
                            self.classNamePreference,
                            self.commentPreference,
                            self.bracketPreference,
                            self.methodPreference,
                            self.stringPreference,
                            self.dunderPreference,
                            self.selfPreference,
                            self.builtInPreference,
                            self.numberPreference]

        self._preferencePath = None

    def initialize(self):

        if self.initialized:
            return

        for preference in self.preferences:
            defaultKey = preference.key.split('.')[-1] + 'Default'
            preference.default = getattr(syntaxPython.PythonHighlighter, defaultKey)
            preference.callable = self.preferenceUpdated
            preference.initialize()
            if self.panel:
                self.scriptEditorLayout.addWidget(preference.colourChip)

        self.initialized = True

    def preferenceUpdated(self, preference):

        Globals.savePreference(preference)
        self.hackerParent.preferenceUpdated.emit(preference)

    @property
    def preferenceType(self):
        return Globals.preferencesType

    @property
    def scriptEditorLayout(self):

        if self._scriptEditorLayout is None:
            stackedLayout = self.panel.layout().itemAt(0).widget().layout()
            stackedWidget = stackedLayout.itemAt(1).widget()
            self._scriptEditorLayout = stackedWidget.layout().itemAt(21).widget().layout()
            
        return self._scriptEditorLayout

    def eventFilter(self, widget, event):

        return super(Preferences, self).eventFilter(widget, event)

    @classmethod
    def regex(cls):
        return str('.*preferencesdialog')

    @classmethod
    def reloadPreferences(cls, parentInstance=None):

        instance = cls()
        parentInstance = parentInstance or instance
        instance.initialize()
        for preference in instance.preferences:
            parentInstance.updatePreferences(preference)
