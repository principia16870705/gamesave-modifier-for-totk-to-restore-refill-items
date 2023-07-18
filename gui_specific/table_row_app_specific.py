import tkinter as tk
from tkinter import ttk


class TableRow(ttk.Frame):

    def __init__(self, parent, row_num, text_list, column_width_list, width_addition, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.row_num = row_num
        self.current_column = 0

        self.grid(column=0, row=self.row_num, sticky=tk.W, padx=0, pady=0)

        self.button = None

        for text in text_list:
            width = column_width_list[self.current_column] + width_addition
            label = ttk.Label(self, width=width, text=text)
            label.grid(row=0, column=self.current_column, sticky=tk.W, padx=2, pady=2, ipady=6)
            self.current_column += 1

    def set_button(self, button):
        self.button = button

    def show_button(self):
        if self.button is not None:
            self.button.grid(row=0, column=self.current_column, sticky=tk.W, padx=2, pady=2)

    def hide_button(self):
        if self.button is not None:
            self.button.grid_remove()
