import tkinter as tk
from tkinter import ttk

from gui_general.entry_with_int_range import EntryWithIntRange


class WidgetGroupForRefill:

    def __init__(self, frame, row, col, text, value_id, photo_image, simple_options, max_int,
                 callback_to_notify_value, callback_to_notify_not_set):

        self.row = row
        self.col = col
        self.text = text
        self.value_id = value_id
        self.callback_to_notify_value = callback_to_notify_value
        self.callback_to_notify_not_set = callback_to_notify_not_set
        self.simple_mode = True

        label = ttk.Label(frame, text=text)
        label.grid(row=row, column=col, sticky=tk.W, padx=5, pady=5)

        button = ttk.Button(frame, image=photo_image, command=self._internal_callback)
        button.grid(row=row, column=col+1, rowspan=2, sticky=tk.W, padx=5, pady=5)

        self.string_var = tk.StringVar()
        self.string_var.set(simple_options[0])
        self.option_menu = ttk.OptionMenu(frame, self.string_var, *simple_options)
        self.option_menu.grid(row=row+1, column=col, sticky=tk.W, padx=5, pady=5)

        self.entry_int_range = EntryWithIntRange(min_int=0, max_int=max_int, master=frame, width=10)

    def _internal_callback(self):
        if self._is_set_and_in_range():
            self.callback_to_notify_value(self.value_id, self._get_int_value())
        else:
            self.callback_to_notify_not_set(self.value_id)

    def _get_int_value(self):
        if self.simple_mode:
            return int(self.string_var.get())
        else:
            return self.entry_int_range.get_int_value()

    def _is_set_and_in_range(self):
        if self.simple_mode:
            return True
        else:
            return self.entry_int_range.is_set_and_in_range()

    def enter_advanced_mode(self):
        self.simple_mode = False
        self.option_menu.grid_remove()
        self.entry_int_range.grid(row=self.row+1, column=self.col, sticky=tk.W, padx=5, pady=5)

    def enter_simple_mode(self):
        self.simple_mode = True
        self.entry_int_range.grid_remove()
        self.option_menu.grid(row=self.row+1, column=self.col, sticky=tk.W, padx=5, pady=5)
