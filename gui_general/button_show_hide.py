from tkinter import ttk


class ButtonShowHide(ttk.Button):

    def __init__(self, parent, show_callback, hide_callback, show_initially=False,
                 show_text='Show', hide_text='Hide', show_callback_id=None, hide_callback_id=None):
        super().__init__(parent)
        self._show_callback = show_callback
        self._hide_callback = hide_callback
        self._showing = show_initially
        self._show_text = show_text
        self._hide_text = hide_text
        self._show_callback_id = show_callback_id
        self._hide_callback_id = hide_callback_id
        self.configure(command=self._toggle)
        self._refresh_text()

    def is_showing(self):
        return self._showing

    def set_showing(self):
        self._showing = True
        self._show_callback(self._show_callback_id)
        self._refresh_text()

    def set_hiding(self):
        self._showing = False
        self._hide_callback(self._hide_callback_id)
        self._refresh_text()

    def _refresh_text(self):
        if self._showing:
            self.configure(text=self._hide_text)
        else:
            self.configure(text=self._show_text)

    def _toggle(self):
        self._showing = not self._showing
        if self._showing:
            self._show_callback(self._show_callback_id)
        else:
            self._hide_callback(self._hide_callback_id)
        self._refresh_text()
