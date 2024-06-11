import re
import traceback
import keyPressEventManager

from panels import basePanel
from panels.preferences.scriptEditor import ColorPreference
from globals import Globals
from highlighters import syntaxPython
from PySide2 import QtGui, QtWidgets, QtCore


class ScriptEditor(basePanel.BasePanel):

    requiredAttributes = ['textEditor']

    def __init__(self, panel, hackerParent=None):
        super(ScriptEditor, self).__init__(panel, hackerParent=hackerParent)

        self.panel = panel

        self.initialized = False
        self.highlighter = None
        self._textEditor = None
        self._outputWindow = None
        self._splitter = None
        self._buttons = None

        self.eventFilter = keyPressEventManager.KeyPressEventManager()

    def initialize(self):

        if self.initialized:
            return

        self.highlighter = syntaxPython.PythonHighlighter(self.textEditor)
        self.textEditor.installEventFilter(self.eventFilter)
        self.eventFilter.registerSequence('Ctrl+V', self.paste)
        # Currently this is not working due to how nuke handles keyboard shortcuts at a global level
        # self.eventFilter.registerSequence('Ctrl+S',
        #                                   lambda: self.saveScriptButton.click())
        self.eventFilter.registerSequence('Ctrl+Shift+V',
                                          self.paste,
                                          **{'normalizeSpace': True})
        # Currently this is not working due to how nuke handles keyboard shortcuts at a global level
        # self.eventFilter.registerSequence('Ctrl+W', self.expandSelection)
        self.eventFilter.registerSequence('Ctrl+/', self.toggleComment)

        for preference in Globals.preferences.values():
            self.updatePreferences(preference)

        self.initialized = True

    def updatePreferences(self, preference):
        if isinstance(preference, dict):
            preference = ColorPreference(**preference)
        super(ScriptEditor, self).updatePreferences(preference)

    @property
    def panelType(self):
        return Globals.scriptEditorType

    @property
    def splitter(self):

        if self._splitter is None:
            for child in self.panel.children():
                if isinstance(child, QtWidgets.QSplitter):
                    self._splitter = child

        return self._splitter
        
    @property
    def textEditor(self):

        if self._textEditor is None:
            for child in self.splitter.children():
                if isinstance(child, QtWidgets.QPlainTextEdit):
                    self._textEditor = child

        return self._textEditor

    @property
    def previousScriptButton(self):

        return self.buttons.get('previousScript')

    @property
    def nextScriptButton(self):

        return self.buttons.get('nextScript')

    @property
    def clearHistoryButton(self):

        return self.buttons.get('clearHistory')

    @property
    def sourceScriptButton(self):

        return self.buttons.get('sourceScript')

    @property
    def loadScriptButton(self):

        return self.buttons.get('loadScript')

    @property
    def saveScriptButton(self):

        return self.buttons.get('saveScript')

    @property
    def runScriptButton(self):

        return self.buttons.get('runScript')

    @property
    def showInputButton(self):

        return self.buttons.get('showInput')

    @property
    def showOutputButton(self):

        return self.buttons.get('showOutput')

    @property
    def showAllButton(self):

        return self.buttons.get('showAll')

    @property
    def clearButton(self):

        return self.buttons.get('clear')

    @property
    def buttons(self):

        if self._buttons is None:
            self._buttons = dict()
            for widget in self.panel.children():
                if isinstance(widget, QtWidgets.QPushButton):
                    toolTip = widget.toolTip()
                    if not toolTip:
                        continue

                    if 'Previous script' in toolTip:
                        self._buttons['previousScript'] = widget
                        continue
                    elif 'Next script' in toolTip:
                        self._buttons['nextScript'] = widget
                        continue
                    elif 'Clear history' in toolTip:
                        self._buttons['clearHistory'] = widget
                        continue
                    elif 'Source a script' in toolTip:
                        self._buttons['sourceScript'] = widget
                        continue
                    elif 'Load a script' in toolTip:
                        self._buttons['loadScript'] = widget
                        continue
                    elif 'Save a script' in toolTip:
                        self._buttons['saveScript'] = widget
                        continue
                    elif 'Run the current script' in toolTip:
                        self._buttons['runScript'] = widget
                        continue
                    elif 'Show input only' in toolTip:
                        self._buttons['showInput'] = widget
                        continue
                    elif 'Show output only' in toolTip:
                        self._buttons['showOutput'] = widget
                        continue
                    elif 'Show both input and output' in toolTip:
                        self._buttons['showAll'] = widget
                        continue
                    elif 'Clear output window' in toolTip:
                        self._buttons['clear'] = widget
                        continue

        return self._buttons

    @staticmethod
    def normalizeSpaces(text):

        lines = text.split('\n')
        smallSpace = None

        for line in lines:
            spaceSearch = re.search('(\s+).*', line)
            if spaceSearch:
                space = len(spaceSearch.groups()[0])
                if not smallSpace:
                    smallSpace = space
                else:
                    if space:
                        smallSpace = min([smallSpace, space])

        if smallSpace:
            lines = [line[smallSpace:] for line in lines]

        return '\n'.join(lines)

    def paste(self, **kwargs):

        normalizeSpace = kwargs.get('normalizeSpace', False)
        clipboard = QtGui.QClipboard()
        currentText = ''
        try:
            currentText = str(clipboard.mimeData().text())
        except Exception:
            traceback.print_exception()

        if not currentText:
            return False

        if normalizeSpace:
            currentText = self.normalizeSpaces(currentText)

        self.textEditor.insertPlainText(currentText)
        self.textEditor.ensureCursorVisible()

        return True

    def expandSelection(self):

        # Currently shortcuts are not working completely with the current context due to how nuke
        # is handling keyboard shortcuts.  This will need to be revisited in the future
        return

    def toggleComment(self):

        cursor = self.textEditor.textCursor()

        # Get selection stats
        selectionStart = cursor.selectionStart()
        selectionEnd = cursor.selectionEnd()

        # Get selection split to lines
        if singleLine := selectionStart == selectionEnd:
            selectedText = cursor.block().text()
        else:
            cursor.movePosition(cursor.StartOfLine, cursor.KeepAnchor)
            selectedText = cursor.selectedText()

        selectedLines = selectedText.splitlines(keepends=True)
        comment = any([re.sub('\s+', '', line).startswith('#') for line in selectedText.splitlines()])

        if comment:
            newLines = [line.replace('# ', '', 1) for line in selectedLines]
            modifier = -1
        else:
            newLines = [f'# {line}' if line else line for line in selectedLines]
            modifier = 1

        newText = ''.join(newLines)
        addition = (selectedText.count('# ') if comment else newText.count('# ')) * 2

        # Replace text
        if singleLine:
            cursor.select(QtGui.QTextCursor.BlockUnderCursor)
            cursor.insertText(f'\n{newText}')
            cursor.setPosition(selectionStart + (2*modifier))
        else:
            cursor.insertText(newText)
            cursor.setPosition(selectionStart)
            cursor.setPosition(selectionEnd + addition*modifier,
                               QtGui.QTextCursor.KeepAnchor)

        self.textEditor.setTextCursor(cursor)

        return

    @classmethod
    def regex(cls):
        return str('.*scripteditor\.\d+')
