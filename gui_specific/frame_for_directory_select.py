import tkinter as tk
from tkinter import ttk

from gui_general.frame_hidable import FrameHidable


class FrameForDirectorySelect(FrameHidable):

    def __init__(self, parent, frame_for_directory_select_listener, *args, **kwargs):
        super().__init__(parent, row=0, col=0, sticky=tk.NW, padx=10, pady=20, *args, **kwargs)

        self.listener = frame_for_directory_select_listener

        label = ttk.Label(self, text='Directory selection',
                          style='frame_mid.TLabel')
        label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        # set up the inner frame and its size control labels
        inner_frame = ttk.Frame(self, style='frame_inner.TFrame')
        inner_frame.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)

        vertical_size_control = ttk.Label(inner_frame, text='', style='frame_inner.TLabel')
        vertical_size_control.grid(row=0, column=100, rowspan=101, ipady=300)

        horizontal_size_control = ttk.Label(inner_frame, text='', style='frame_inner.TLabel')
        horizontal_size_control.grid(row=100, column=0, columnspan=101, ipadx=250)

        inner_inner_frame = ttk.Frame(inner_frame, style='frame_inner.TFrame')
        inner_inner_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=0, pady=0)

        label = ttk.Label(inner_inner_frame,
                          text='Select or confirm the parent directory that contains your TOTK save slots.'
                               '\nThis directory is inside your emulator\'s directories. Click "Info about '
                               '\nselecting the directory" for more information.')
        label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        label = ttk.Label(inner_inner_frame, text='Selected directory')
        label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self.textbox_save_slots_directory = tk.Text(inner_frame, background='#303030', foreground='#D0D0D0',
                                                    width=60, height=4)
        self.textbox_save_slots_directory.insert(1.0, 'None')
        self.textbox_save_slots_directory.configure(state=tk.DISABLED)
        self.textbox_save_slots_directory.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        inner_inner_frame = ttk.Frame(inner_frame, style='frame_inner.TFrame')
        inner_inner_frame.grid(row=2, column=0, sticky=tk.NSEW, padx=0, pady=0)

        self.confirm_button = ttk.Button(inner_inner_frame, text='Confirm directory\nand continue',
                                         command=self.listener.on_confirm_and_continue_request)
        self.confirm_button.configure(state=tk.DISABLED)
        self.confirm_button.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)

        button = ttk.Button(inner_inner_frame, text='Info about selecting\nthe directory',
                            command=self.listener.on_request_info_about_dir_select)
        button.grid(row=0, column=1, sticky=tk.NSEW, padx=5, pady=5, ipady=8)

        button = ttk.Button(inner_inner_frame, text='Select new\ndirectory',
                            command=self.listener.on_select_directory_request)
        button.grid(row=0, column=2, sticky=tk.NSEW, padx=5, pady=5, ipady=8)

        button = ttk.Button(inner_inner_frame, text='Select an individual\nsave file instead',
                            command=self.listener.on_select_individual_file_request)
        button.grid(row=0, column=3, sticky=tk.NSEW, padx=5, pady=5)

    def enable_directory_confirm_button(self):
        self.confirm_button.configure(state=tk.NORMAL)

    def disable_directory_confirm_button(self):
        self.confirm_button.configure(state=tk.DISABLED)

    def display_directory_of_save_slots(self, message):
        self.textbox_save_slots_directory.configure(state=tk.NORMAL)
        self.textbox_save_slots_directory.delete(1.0, tk.END)
        self.textbox_save_slots_directory.insert(1.0, message)
        self.textbox_save_slots_directory.configure(state=tk.DISABLED)
