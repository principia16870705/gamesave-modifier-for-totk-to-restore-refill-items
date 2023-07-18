import tkinter as tk
from tkinter import ttk


class EntryWithIntRange(ttk.Entry):

    def __init__(self, min_int, max_int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_int = min_int
        self.max_int = max_int
        self.entry_string_var = tk.StringVar(value='')
        self.configure(textvariable=self.entry_string_var,
                       validate="focusout",
                       validatecommand=self._validate)

    def is_set_and_in_range(self):
        # if the current text can be converted to an int, return the result of the range check
        if self._can_convert_to_int(self.entry_string_var.get()):
            return self.min_int <= int(self.entry_string_var.get()) <= self.max_int
        # otherwise, return false
        return False

    def get_int_value(self):
        try:
            return int(self.entry_string_var.get())
        except ValueError:
            raise ValueError('the text could not be converted to an int, is the entry box blank?')

    @staticmethod
    def _can_convert_to_int(value):
        # checks if a value can be converted to an int
        try:
            int(value)
            return True
        except ValueError:
            return False

    def _validate(self):
        # always returns True to stay subscribed to future validate requests
        if not self._can_convert_to_int(self.entry_string_var.get()):
            self.entry_string_var.set('')
            return True

        if int(self.entry_string_var.get()) < self.min_int:
            self.entry_string_var.set(str(self.min_int))

        elif int(self.entry_string_var.get()) > self.max_int:
            self.entry_string_var.set(str(self.max_int))

        return True
