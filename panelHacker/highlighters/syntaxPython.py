import builtins
import keyword
from PySide2 import QtGui, QtCore


class PythonHighlighter(QtGui.QSyntaxHighlighter):
    """
    Syntax highlighter for the Python language.
    """

    styleBold = 'bold'
    styleItalic = 'italic'

    operators = ['=', '==', '!=', '<', '<=', '>', '>=', '\+', '-', '\*', '/', '//', '\%', '\*\*',
                 '\+=', '-=', '\*=', '/=', '\%=', '\^', '\|', '\&', '\~', '>>', '<<']

    braces = ['\{', '\}', '\(', '\)', '\[', '\]']

    singleQuoteSearch = r'"[^"\\]*(\\.[^"\\]*)*"'
    doubleQuoteSearch = r"'[^'\\]*(\\.[^'\\]*)*'"

    keywordHighlighterDefault = [255, 140, 0]
    classNameHighlighterDefault = [201, 201, 201]
    operatorHighlighterDefault = [201, 201, 201]
    commentHighlighterDefault = [115, 115, 115]
    bracketHighlighterDefault = [255, 208, 0]
    methodHighlighterDefault = [255, 224, 138]
    stringHighlighterDefault = [74, 138, 63]
    dunderHighlighterDefault = [187, 0, 255]
    selfHighlighterDefault = [164, 73, 191]
    builtInHighlighterDefault = [137, 102, 196]
    numberHighlighterDefault = [75, 164, 191]

    def __init__(self, textEdit):
        """
        Args:
            textEdit (QtGui.QPlainTextEdit):
        """
        super(PythonHighlighter, self).__init__(textEdit.document())

        self._highlighters = None
        self._pythonBuiltIns = None
        self._keywords = None

        # Set Color defaults
        self._keywordHighlighter = self.keywordHighlighterDefault
        self._classNameHighlighter = self.classNameHighlighterDefault
        self._operatorHighlighter = self.operatorHighlighterDefault
        self._commentHighlighter = self.commentHighlighterDefault
        self._bracketHighlighter = self.bracketHighlighterDefault
        self._methodHighlighter = self.methodHighlighterDefault
        self._stringHighlighter = self.stringHighlighterDefault
        self._dunderHighlighter = self.dunderHighlighterDefault
        self._selfHighlighter = self.selfHighlighterDefault
        self._builtInHighlighter = self.builtInHighlighterDefault
        self._numberHighlighter = self.numberHighlighterDefault

        self._textEdit = textEdit

        self.tripleQuote = (QtCore.QRegExp('\'\'\''), 1,
                            self.getTextFormatter(self.stringHighlighter))
        self.tripleDoubleQuote = (QtCore.QRegExp('"""'), 2,
                                  self.getTextFormatter(self.stringHighlighter))

    @property
    def pythonBuiltIns(self):
        """
        Returns:
            list: List of all the python builtin methods
        """
        if self._pythonBuiltIns is None:
            self._pythonBuiltIns = dir(builtins)
        return self._pythonBuiltIns

    @property
    def keywords(self):
        """
        Returns:
            list: List of all the python keywords,  ie if, as, and, etc
        """
        if self._keywords is None:
            self._keywords = keyword.kwlist
        return self._keywords

    @property
    def keywordHighlighter(self):
        """
        Returns:
            list[int, int ,int]: rgb color value for keywords
        """
        return self._keywordHighlighter

    @keywordHighlighter.setter
    def keywordHighlighter(self, value):
        """
        Updates the color value and forces a refresh of the highlighting
        """
        self._keywordHighlighter = value
        self.refresh()

    @property
    def classNameHighlighter(self):
        """
        Returns:
            list[int, int ,int]: rgb color value for class names
        """
        return self._classNameHighlighter

    @classNameHighlighter.setter
    def classNameHighlighter(self, value):
        """
        Updates the color value and forces a refresh of the highlighting
        """
        self._classNameHighlighter = value
        self.refresh()

    @property
    def operatorHighlighter(self):
        """
        Returns:
            list[int, int ,int]: rgb color value for operators
        """
        return self._operatorHighlighter

    @operatorHighlighter.setter
    def operatorHighlighter(self, value):
        """
        Updates the color value and forces a refresh of the highlighting
        """
        self._operatorHighlighter = value
        self.refresh()

    @property
    def commentHighlighter(self):
        """
        Returns:
            list[int, int ,int]: rgb color value for comments
        """
        return self._commentHighlighter

    @commentHighlighter.setter
    def commentHighlighter(self, value):
        """
        Updates the color value and forces a refresh of the highlighting
        """
        self._commentHighlighter = value
        self.refresh()

    @property
    def bracketHighlighter(self):
        """
        Returns:
            list[int, int ,int]: rgb color value for brackets
        """
        return self._bracketHighlighter

    @bracketHighlighter.setter
    def bracketHighlighter(self, value):
        """
        Updates the color value and forces a refresh of the highlighting
        """
        self._bracketHighlighter = value
        self.refresh()

    @property
    def methodHighlighter(self):
        """
        Returns:
            list[int, int ,int]: rgb color value for method names
        """
        return self._methodHighlighter

    @methodHighlighter.setter
    def methodHighlighter(self, value):
        """
        Updates the color value and forces a refresh of the highlighting
        """
        self._methodHighlighter = value
        self.refresh()

    @property
    def stringHighlighter(self):
        """
        Returns:
            list[int, int ,int]: rgb color value for strings
        """
        return self._stringHighlighter

    @stringHighlighter.setter
    def stringHighlighter(self, value):
        """
        Updates the color value and forces a refresh of the highlighting
        """
        self._stringHighlighter = value
        self.refresh()

    @property
    def dunderHighlighter(self):
        """
        Returns:
            list[int, int ,int]: rgb color value for dunder methods ie: __init__
        """
        return self._dunderHighlighter

    @dunderHighlighter.setter
    def dunderHighlighter(self, value):
        """
        Updates the color value and forces a refresh of the highlighting
        """
        self._dunderHighlighter = value
        self.refresh()

    @property
    def selfHighlighter(self):
        """
        Returns:
            list[int, int ,int]: rgb color value for self
        """
        return self._selfHighlighter

    @selfHighlighter.setter
    def selfHighlighter(self, value):
        """
        Updates the color value and forces a refresh of the highlighting
        """
        self._selfHighlighter = value
        self.refresh()

    @property
    def builtInHighlighter(self):
        """
        Returns:
            list[int, int ,int]: rgb color value for python builtins ie: int, object, etc
        """
        return self._builtInHighlighter

    @builtInHighlighter.setter
    def builtInHighlighter(self, value):
        """
        Updates the color value and forces a refresh of the highlighting
        """
        self._builtInHighlighter = value
        self.refresh()

    @property
    def numberHighlighter(self):
        """
        Returns:
            list[int, int ,int]: rgb color value for numbers
        """
        return self._numberHighlighter

    @numberHighlighter.setter
    def numberHighlighter(self, value):
        """
        Updates the color value and forces a refresh of the highlighting
        """
        self._numberHighlighter = value
        self.refresh()

    @property
    def highlighters(self):
        """
        Returns:
            list[QtCore.QRegExp, int, QtGui.QTextCharFormat]: list of the regex, index and text
                formatter.  The index is the index of the regex to apply the formatter to
        """
        if self._highlighters is None:
            highlighters = list()

            highlighters.append((r'\bself\b', 0,
                                 self.getTextFormatter(self.selfHighlighter)))  # self
            highlighters.append((r'\bdef\b\s*(\w+)', 1,
                                 self.getTextFormatter(self.methodHighlighter)))  # def *
            highlighters.append((r'\bclass\b\s*(\w+)', 1,
                                 self.getTextFormatter(self.classNameHighlighter)))  # class *
            highlighters.append((r'\b[+-]?[0-9]+[lL]?\b', 0,
                                 self.getTextFormatter(self.numberHighlighter)))  # 0-9
            highlighters.append((r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0,
                                 self.getTextFormatter(self.numberHighlighter)))  # 0-9
            highlighters.append((r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0,
                                 self.getTextFormatter(self.numberHighlighter)))
            highlighters.append((r'\b__\w+__\b', 0,
                                 self.getTextFormatter(self.dunderHighlighter)))

            highlighters.extend([(r'\b{0}\b'.format(item), 0,
                                  self.getTextFormatter(self.builtInHighlighter)) for item in
                                 self.pythonBuiltIns])
            highlighters.extend([(r'\b{0}\b'.format(item), 0,
                                  self.getTextFormatter(self.keywordHighlighter)) for item in
                                 self.keywords])
            highlighters.extend([(r'{0}'.format(item), 0,
                                  self.getTextFormatter(self.operatorHighlighter)) for item in
                                 self.operators])
            highlighters.extend([(r'{0}'.format(item), 0,
                                  self.getTextFormatter(self.bracketHighlighter)) for item in
                                 self.braces])

            highlighters.append((r'#[^\n]*', 0,
                                 self.getTextFormatter(self.commentHighlighter)))
            highlighters.append((self.doubleQuoteSearch, 0,
                                 self.getTextFormatter(self.stringHighlighter)))
            highlighters.append((self.singleQuoteSearch, 0,
                                 self.getTextFormatter(self.stringHighlighter)))

            self._highlighters = [(QtCore.QRegExp(pat), index, fmt) for (pat, index, fmt) in
                                  highlighters]

        return self._highlighters

    def refresh(self):
        """
        Refresh the highlighting to ensure all colors are up to date
        """
        self._highlighters = None
        self.rehighlight()

    def reset(self):
        """
        Resets the highlighting back to the initial defaults
        """
        self.keywordHighlighter = self.keywordHighlighterDefault
        self.classNameHighlighter = self.classNameHighlighterDefault
        self.operatorNameHighlighter = self.operatorHighlighterDefault
        self.commentHighlighter = self.commentHighlighterDefault
        self.bracketHighlighter = self.bracketHighlighterDefault
        self.methodHighlighter = self.methodHighlighterDefault
        self.stringHighlighter = self.stringHighlighterDefault
        self.dunderHighlighter = self.dunderHighlighterDefault
        self.selfHighlighter = self.selfHighlighterDefault
        self.builtInHighlighter = self.builtInHighlighterDefault
        self.numberHighlighter = self.numberHighlighterDefault

    def getTextFormatter(self, color, style=None):
        """
        Creates a QtGui.QTextCharFormat for the given color
        Args:
            color (list[int, int ,int]): list with 3 rgb values for the color to use
            style (str|optional): The text style to set for the formatter ie: bold, italic

        Returns:

        """
        qtColor = QtGui.QColor()
        qtColor.setRgb(*color)
        textFormat = QtGui.QTextCharFormat()
        textFormat.setForeground(qtColor)

        if style == self.styleBold:
            textFormat.setFontWeight(QtGui.QFont.Bold)
        if style == self.styleItalic:
            textFormat.setFontItalic(True)

        return textFormat

    def highlightBlock(self, text):
        """
        Apply syntax highlighting to the given block of text.
        """
        docStringIndexes = []
        for search, searchIndex, textFormat in self.highlighters:
            index = search.indexIn(text, 0)
            if index >= 0:
                # if we are looking for quotes/string formatting then we need to check and see if
                # there are triple quotes to ensure that we format triple quotes/docs properly
                if search.pattern() in [self.singleQuoteSearch, self.doubleQuoteSearch]:
                    # Check for triple quotes
                    innerIndex = self.tripleQuote[0].indexIn(text, index + 1)
                    if innerIndex == -1:
                        # Check for triple double quotes
                        innerIndex = self.tripleDoubleQuote[0].indexIn(text, index + 1)

                    # If we have an index then we found triple quotes and update the doc string
                    # indexes for later formatting
                    if innerIndex != -1:
                        tripleQuoteIndexes = range(innerIndex, innerIndex + 3)
                        docStringIndexes.extend(tripleQuoteIndexes)

            while index >= 0:
                # if the current index is within the docstring indexes then we will skip those so
                # they get formatted correctly further along
                if index in docStringIndexes:
                    index += 1
                    search.indexIn(text, index)
                    continue

                # We actually want the index of the searchIndex match
                index = search.pos(searchIndex)
                length = len(search.cap(searchIndex))
                self.setFormat(index, length, textFormat)
                index = search.indexIn(text, index + length)

        self.setCurrentBlockState(0)
        self.matchMultiline(text, docStringIndexes)

    def matchMultiline(self, text, docStringIndexes):
        """
        Do highlighting of multi-line strings.
        Args:
            text (str): the text to check for a multiline triple quote/docstring
            docStringIndexes (list): List of indexes where quotes where found
        """
        for search, searchIndex, textFormat in [self.tripleQuote, self.tripleDoubleQuote]:
            # If inside triple-single quotes, start at 0
            if self.previousBlockState() == searchIndex:
                start = 0
                add = 0
            # Otherwise, look for the delimiter on this line
            else:
                start = search.indexIn(text)
                # skipping triple quotes within strings
                if start in docStringIndexes:
                    continue
                # Move past this match
                add = search.matchedLength()

            # As long as there's a delimiter match on this line...
            while start >= 0:
                # Look for the ending delimiter
                end = search.indexIn(text, start + add)
                # Ending delimiter on this line?
                if end >= add:
                    length = end - start + add + search.matchedLength()
                    self.setCurrentBlockState(0)
                # No; multi-line string
                else:
                    self.setCurrentBlockState(searchIndex)
                    length = len(text) - start + add
                # Apply formatting
                self.setFormat(start, length, textFormat)
                # Look for the next match
                start = search.indexIn(text, start + length)

            # Return True if still inside a multi-line string, False otherwise
            if self.currentBlockState() == searchIndex:
                return True
