import datetime
import tkinter as tk
from tkinter import ttk

from gui_general.button_with_callback_id import ButtonWithCallbackID
from gui_general.button_show_hide import ButtonShowHide
from gui_general.frame_hidable import FrameHidable
from gui_specific.table_row_app_specific import TableRow


class FrameForSlotTable(FrameHidable):

    def __init__(self, parent, frame_for_slot_table_listener, *args, **kwargs):
        super().__init__(parent, row=0, col=1, sticky=tk.N, padx=10, pady=20, *args, **kwargs)

        label = ttk.Label(self, text='Save slot table', style='frame_mid.TLabel')
        label.grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

        # set up the inner frame and its size control labels
        inner_frame = ttk.Frame(self, style='frame_inner.TFrame')
        inner_frame.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)

        vertical_size_control = ttk.Label(inner_frame, text='', style='frame_inner.TLabel')
        vertical_size_control.grid(row=0, column=100, rowspan=101, ipady=300)

        horizontal_size_control = ttk.Label(inner_frame, text='', style='frame_inner.TLabel')
        horizontal_size_control.grid(row=100, column=0, columnspan=101, ipadx=250)

        self.listener = frame_for_slot_table_listener
        self.table_row_list = None

        frame_pre_table = ttk.Frame(inner_frame, style='frame_inner.TFrame')
        frame_pre_table.grid(row=0, column=0, sticky=tk.NSEW, padx=0, pady=0)

        label = ttk.Label(frame_pre_table,
                          text='Click "Open save file from newest slot" or "Enable opening from older slots"\n'
                               'The game uses slot_00 to slot_05 in an order that is random to us.\n'
                               'Typically, you can ignore the slot name and just "Open save file from newest slot"',
                          style='frame_inner.TLabel')
        label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        # - - set up sub frame - -

        self.frame_slot_table = ttk.Frame(inner_frame, style='frame_inner.TFrame')
        self.frame_slot_table.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)

        frame_post_table = ttk.Frame(inner_frame, style='frame_inner.TFrame')
        frame_post_table.grid(row=2, column=0, sticky=tk.NSEW, padx=0, pady=0)

        button = ttk.Button(frame_post_table, text='Refresh',
                            command=self.listener.on_save_slot_refresh_request)
        button.grid(row=0, column=0, sticky=tk.NW, padx=5, pady=5, ipady=7)

        button = ButtonWithCallbackID(frame_post_table, callback_id=0,
                                      callback=self.listener.on_open_save_slot_request,
                                      text='Open save file\n'
                                           'from newest slot', width=16)
        button.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        # button = ttk.Button(frame_post_table, text='Enable selecting\nolder slots')
        # button.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        button = ttk.Button(frame_post_table, text='Go back to directory\nselection',
                            command=self.listener.on_go_back_to_directory_select_request)

        button.grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)

        self.button_show_hide = ButtonShowHide(frame_post_table,
                                               self._button_listener_show_older_slots,
                                               self._button_listener_hide_older_slots,
                                               show_initially=False,
                                               show_text='Enable opening\nfrom older slots',
                                               hide_text='Disable opening\nfrom older slots')
        self.button_show_hide.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)

    def display_save_slot_table(self, name_date_status_tuple_list):

        show_all_rows = self.button_show_hide.is_showing()

        if self.table_row_list is not None:
            for table_row in self.table_row_list:
                table_row.destroy()

        # recreate our table row list, this also de-references the old list
        self.table_row_list = []

        header_cells = ['Newness rank', 'Name', 'Modified date', 'Modified by']
        header_cell_widths = [11, 4, 11, 10]
        list_of_row_cells = [header_cells]
        row_cell_widths = header_cell_widths

        for i in range(len(name_date_status_tuple_list)):

            prefix = str(i + 1)

            # get our current name, timestamp, and status code
            name, timestamp_float, status_code = name_date_status_tuple_list[i]

            # format the time stamp
            if timestamp_float == 0:
                timestamp_str = 'none'
            else:
                timestamp_datetime = datetime.datetime.fromtimestamp(timestamp_float)
                timestamp_str = timestamp_datetime.strftime("%Y/%m/%d %H:%M:%S")

            # create a message from the status code
            if status_code == 'orig':
                status_text = 'the game'
            elif status_code == 'mod':
                status_text = 'this app'
            elif status_code == 'not_found':
                status_text = 'file not found'
            else:
                status_text = 'error interpreting status code'

            # line = prefix + ' - ' + name + ' - timestamp ' + timestamp_str + ' - ' + status_text
            row_cells = [prefix, name, timestamp_str, status_text]
            # row_cell_widths = [len(prefix), len(name), len(timestamp_str), len(status_text)]
            list_of_row_cells.append(row_cells)
            # list_of_row_cell_widths.append(row_cell_widths)

            for j in range(len(row_cells)):
                # take the max() of our stored int and the length of current text
                row_cell_widths[j] = max(row_cell_widths[j], len(row_cells[j]))

        row_offset = 2
        callback_id_offset = -1
        for i in range(len(list_of_row_cells)):

            # create the table row and add it to our list
            table_row = TableRow(self.frame_slot_table, i + row_offset,
                                 list_of_row_cells[i], row_cell_widths, width_addition=2)
            self.table_row_list.append(table_row)

            # if we are past the header and first row, and this row has a timestamp, append a button to the row
            if i > 1 and list_of_row_cells[i][2] != 'none':
                text = 'Open save file'
                button = ButtonWithCallbackID(table_row, callback_id=i + callback_id_offset,
                                              callback=self.listener.on_open_save_slot_request,
                                              text=text, width=16)
                table_row.set_button(button)

            # if we are on the first two rows or if show all is set, show the row
            if show_all_rows:
                table_row.show_button()

    def _button_listener_show_older_slots(self, callback_id):
        for i in range(len(self.table_row_list)):
            self.table_row_list[i].show_button()

    def _button_listener_hide_older_slots(self, callback_id):
        for i in range(len(self.table_row_list)):
            self.table_row_list[i].hide_button()
