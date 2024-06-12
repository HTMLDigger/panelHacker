from panels import basePanel
from globals import Globals
from panels.preferences.scriptEditor import ColorPreference
from highlighters import syntaxPython


class Preferences(basePanel.BasePanel):
    # This should be updated with all the required attributes for the preferences panel that you
    # are wanting to hack
    requiredAttributes = ['scriptEditorLayout']

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
        """
        Initialize the preferences panel.  This will ensure that all the preferences are added to
        the panel and that the preferences are initialized

        Currently, this is only handling the script editor preferences
        """
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
        """
        This is triggered when any preference is updated.  It will save the preference to disk and
        emit the preferenceUpdated signal to ensure that whatever the preferences is connected to
        is updated with the new preference

        Args:
            preference (Preference): The preference that was updated
        """
        Globals.savePreference(preference)
        self.hackerParent.preferenceUpdated.emit(preference)

    @property
    def panelType(self):
        """
        Returns:
            str: The type of the panel as defined in the globals
        """
        return Globals.preferencesType

    @property
    def scriptEditorLayout(self):
        """
        Iterates over the panels layout to find the script editor layout.  This is hardcoded to
        the script editor layout so if the layout changes then this will need to be updated.

        # TODO: This should be changed to be more dynamic and not hardcoded
        Returns:
            QtWidgets.QLayout: The layout for the script editor section in the preferences panel
        """
        if self._scriptEditorLayout is None:
            stackedLayout = self.panel.layout().itemAt(0).widget().layout()
            stackedWidget = stackedLayout.itemAt(1).widget()
            self._scriptEditorLayout = stackedWidget.layout().itemAt(21).widget().layout()

        return self._scriptEditorLayout

    @classmethod
    def regex(cls):
        """
        Returns:
            str: The regex that will be used to find the preferences panel
        """
        return str('.*preferencesdialog')
