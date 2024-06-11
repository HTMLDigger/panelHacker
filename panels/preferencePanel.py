from panels import basePanel
from globals import Globals
from panels.preferences.scriptEditor import ColorPreference
from highlighters import syntaxPython


class Preferences(basePanel.BasePanel):
    # This should be updated with all the required attributes for the preferences panel that you
    # are wanting to hack
    requiredAttributes = ['scriptEditorLayout']
    # We set this to False so that the preferences are always reloaded when the panel is opened.
    # Since the preference panel is not persistent if we cached it we would run into problems with
    # certain widgets no longer being present
    cacheWrapper = False

    def __init__(self, panel=None, hackerParent=None):
        super(Preferences, self).__init__(panel, hackerParent=hackerParent)

        self.panel = panel

        self.initialized = False
        self._scriptEditorLayout = None

        # Prefixing anything related to the script editor with se
        self.seKeywordPreference = ColorPreference(
            'highlighter.keywordHighlighter',
            name='Keyword Highlighter',
            toolTip='Highlighter color for Python keywords')
        self.seClassNamePreference = ColorPreference(
            'highlighter.classNameHighlighter',
            name='Class Name Highlighter',
            toolTip='Highlighter color for Python class names')
        self.seOperatorPreference = ColorPreference(
            'highlighter.operatorHighlighter',
            name='Operator Highlighter',
            toolTip='Highlighter color for Python operators')
        self.seCommentPreference = ColorPreference(
            'highlighter.commentHighlighter',
            name='Comment Highlighter',
            toolTip='Highlighter color for Python comments')
        self.seBracketPreference = ColorPreference(
            'highlighter.bracketHighlighter',
            name='Bracket Highlighter',
            toolTip='Highlighter color for Python brackets')
        self.seMethodPreference = ColorPreference(
            'highlighter.methodHighlighter',
            name='Method Highlighter',
            toolTip='Highlighter color for Python methods')
        self.seStringPreference = ColorPreference(
            'highlighter.stringHighlighter',
            name='String Highlighter',
            toolTip='Highlighter color for Python strings')
        self.seDunderPreference = ColorPreference(
            'highlighter.dunderHighlighter',
            name='Dunder Highlighter',
            toolTip='Highlighter color for Python dunder methods')
        self.seSelfPreference = ColorPreference(
            'highlighter.selfHighlighter',
            name='Self Highlighter',
            toolTip='Highlighter color for Python self')
        self.seBuiltInPreference = ColorPreference(
            'highlighter.builtInHighlighter',
            name='Built In Highlighter',
            toolTip='Highlighter color for Python built in functions')
        self.seNumberPreference = ColorPreference(
            'highlighter.numberHighlighter',
            name='Number Highlighter',
            toolTip='Highlighter color for Python numbers')

        self.sePreferences = [self.seKeywordPreference,
                              self.seClassNamePreference,
                              self.seOperatorPreference,
                              self.seCommentPreference,
                              self.seBracketPreference,
                              self.seMethodPreference,
                              self.seStringPreference,
                              self.seDunderPreference,
                              self.seSelfPreference,
                              self.seBuiltInPreference,
                              self.seNumberPreference]

        self._preferencePath = None

    def initialize(self):

        if self.initialized:
            return

        # Add the script editor preferences to the script editor preference in the default
        # Nuke preference panel
        for preference in self.sePreferences:
            defaultKey = preference.key.split('.')[-1] + 'Default'
            preference.default = getattr(syntaxPython.PythonHighlighter, defaultKey)
            preference.callable = self.preferenceUpdated
            preference.initialize()
            if self.panel:
                self.scriptEditorLayout.addWidget(preference.colorChip)

        self.initialized = True

    def preferenceUpdated(self, preference):

        Globals.savePreference(preference)
        self.hackerParent.preferenceUpdated.emit(preference)

    @property
    def panelType(self):
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
        for preference in instance.sePreferences:
            parentInstance.updatePreferences(preference)
