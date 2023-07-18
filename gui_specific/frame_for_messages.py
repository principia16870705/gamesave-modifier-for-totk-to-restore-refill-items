import tkinter as tk
from tkinter import ttk

from gui_general.frame_hidable import FrameHidable


class FrameForMessages(FrameHidable):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, row=0, col=3, sticky=tk.N, padx=10, pady=20, *args, **kwargs)

        label = ttk.Label(self, text='Messages', style='frame_mid.TLabel')
        label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        frame_messages = ttk.Frame(self, style='frame_inner.TFrame')
        frame_messages.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)

        self.textbox_messages_from_processes = tk.Text(frame_messages, background='#303030', foreground='#D0D0D0',
                                                       width=60, height=30)
        self.textbox_messages_from_processes.configure(state=tk.DISABLED)
        self.textbox_messages_from_processes.grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)

    def clear_message_area(self):
        self.textbox_messages_from_processes.configure(state=tk.NORMAL)
        self.textbox_messages_from_processes.delete(1.0, tk.END)
        self.textbox_messages_from_processes.configure(state=tk.DISABLED)

    def display_message_from_process(self, text):
        self.textbox_messages_from_processes.configure(state=tk.NORMAL)
        self.textbox_messages_from_processes.insert(tk.END, text + '\n')
        self.textbox_messages_from_processes.configure(state=tk.DISABLED)
        # scroll to end
        self.textbox_messages_from_processes.see('end')

