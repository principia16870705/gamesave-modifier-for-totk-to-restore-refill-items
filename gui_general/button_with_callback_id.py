from tkinter import ttk


class ButtonWithCallbackID(ttk.Button):

    def __init__(self, parent, callback_id, callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callback_id = callback_id
        self.callback = callback
        self.configure(command=self._command)

    def _command(self):
        self.callback(self.callback_id)
