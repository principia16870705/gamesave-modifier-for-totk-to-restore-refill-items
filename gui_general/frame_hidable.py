from tkinter import ttk


class FrameHidable(ttk.Frame):

    def __init__(self, parent, row, col, sticky, padx, pady, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.row = row
        self.col = col
        self.sticky = sticky
        self.padx = padx
        self.pady = pady

    def show(self):
        self.grid(column=self.col, row=self.row, sticky=self.sticky, padx=self.padx, pady=self.pady)

    def hide(self):
        self.grid_remove()
