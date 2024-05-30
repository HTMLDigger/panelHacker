from PySide2 import QtGui, QtCore


class KeyPressEventManager(QtCore.QObject):

    def __init__(self):
        super(KeyPressEventManager, self).__init__()

        self.sequences = dict()

    def registerSequence(self, sequence, action, **kwargs):

        data = {'kwargs': kwargs,
                'action': action}
        self.sequences[sequence.lower()] = data

    def eventFilter(self, obj, event):

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
                    except Exception:
                        return False

                    return True

        return super(KeyPressEventManager, self).eventFilter(obj, event)