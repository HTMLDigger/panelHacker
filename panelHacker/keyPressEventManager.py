import nuke
import traceback

from PySide2 import QtGui, QtCore


class KeyPressEventManager(QtCore.QObject):

    def __init__(self):
        super(KeyPressEventManager, self).__init__()
        self.sequences = dict()

    def registerSequence(self, sequence, action, **kwargs):
        """
        Registers a key sequence to be used with the event filter
        Args:
            sequence (str): Key sequence to be registered ie: 'Ctrl+Shift+P'
            action (callable): Function to be called when the key sequence is pressed

        Kwargs:
            kwargs will be passed along to the action function
        """
        data = {'kwargs': kwargs,
                'action': action}
        self.sequences[sequence.lower()] = data

    def eventFilter(self, obj, event):
        """
        Event filter that will be used to capture key press events and trigger the registered
        actions if the key sequence is found.  If the key sequence is not found then the event
        will be passed along to the default event filter
        Args:
            obj (object): Object that the event is being filtered for
            event (QtCore.QEvent): Event that is being filtered
        """
        if event.type() == QtCore.QEvent.KeyPress:
            keySequence = QtGui.QKeySequence(event.modifiers() | event.key())
            data = self.sequences.get(keySequence.toString().lower())
            if data:
                action = data.get('action', None)
                if callable(action):
                    try:
                        kwargs = data.get('kwargs', dict())
                        if kwargs:
                            kwargs['event'] = event
                            kwargs['obj'] = obj
                            action(**kwargs)
                        else:
                            action()

                    # Open-ended exception handling as we don't know what errors we might get here
                    # But we ensure to print out the error
                    except Exception:
                        error = traceback.format_exc()
                        for line in error.split('\n'):
                            nuke.tprint(f'[Keypress Manager Error] {line}')
                        return False

                    return True

        return super(KeyPressEventManager, self).eventFilter(obj, event)
