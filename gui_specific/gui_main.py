import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import game_specific_constants as const
from gui_specific.image_container import ImageContainer
from gui_specific.frame_for_directory_select import FrameForDirectorySelect
from gui_specific.frame_for_item_restore import FrameForItemRestore
from gui_specific.frame_for_messages import FrameForMessages
from gui_specific.frame_for_slot_table import FrameForSlotTable


class GUIMain:

    WINDOW_TITLE = 'A Troupe of Magic Frogs Heal Your Items While You Rest (and reload your game) - TOTK'
    NUM_SAVE_SLOT_TABLE_ROWS = 10

    # colors we considered
    # light blue   '#C0C0D0'
    # light green  '#C0D0C0''
    # med green    '#90B090'
    # dark green   '#609060'
    # gray         '#E0E0E0'
    COLOR_OUTER = '#C0C0D0'
    COLOR_MID = '#90B090'
    COLOR_INNER = '#C0D0C0'

    # - - methods to be a frame_for_directory_select_listener - -
    def on_confirm_and_continue_request(self):
        self.listener.on_confirm_and_continue_request()

    def on_select_directory_request(self):
        messagebox.showinfo(title='Tip', message=const.DIR_SELECT_POP_UP)
        # open a dialog to select the parent directory of the save slots
        dir_name = filedialog.askdirectory(title=const.DIR_SELECT_TITLE)
        # if the dialog is cancelled we, do not need to notify the listener
        if dir_name is None:
            return
        if len(dir_name) < 1:
            return
        self.listener.on_set_directory_of_save_slots_request(dir_name)

    def on_request_info_about_dir_select(self):
        self.display_message_from_process('')
        self.display_message_from_process(const.DIR_SELECT_MESSAGE_TITLE)
        self.display_message_from_process('')
        self.display_message_from_process(const.DIR_SELECT_MESSAGE)

    def on_select_individual_file_request(self):
        filename = filedialog.askopenfilename(filetypes=(("save data files", "progress.sav"), ("all files", "*.*")))
        # if the dialog is cancelled we, do not need to notify the listener
        if filename is None:
            return
        if len(filename) < 1:
            return
        self.listener.on_open_individual_file_request(filename)

    # - - methods to be a frame_for_slot_table_listener - -
    def on_save_slot_refresh_request(self):
        self.listener.on_refresh_save_slot_table_request()

    def on_open_save_slot_request(self, index):
        self.listener.on_open_file_at_slot_index_request(index)

    def on_go_back_to_directory_select_request(self):
        self.enter_directory_select_mode()

    # - - methods to be a frame_for_item_restore_listener - -
    def on_item_restore_request(self, request_type_id, int_value=0):
        self.listener.on_item_restore_request(request_type_id, int_value)

    def on_value_not_set(self, value_id):
        self.display_message_from_process(value_id + ' value is not set')

    def on_write_changes_request(self):
        self.listener.on_write_save_data_to_file_request()

    def on_discard_changes_request(self):
        self.listener.on_discard_save_data_request()

    def on_discard_changes_and_reload_request(self):
        self.listener.on_discard_save_data_and_reload_request()

    def __init__(self, gui_listener):

        # reference our listener
        self.listener = gui_listener

        # setup references for some widgets
        self.textbox_save_slots_directory = None
        self.textbox_individual_save_file = None
        self.textbox_messages_from_processes = None
        self.checkbutton_sword_durability = None
        self.checkbutton_bow_durability = None
        self.checkbutton_shield_durability = None
        self.checkbutton_refill_health = None

        # create our main window object
        self.main_window = tk.Tk()
        self.main_window.title(GUIMain.WINDOW_TITLE)
        self.main_window.configure(background=GUIMain.COLOR_OUTER)

        # setup our image container
        self.image_container = ImageContainer()

        # create our styles
        self._create_styles()

        # create our main gui_specific frames
        self.frame_for_directory_select = FrameForDirectorySelect(self.main_window,
                                                                  frame_for_directory_select_listener=self)
        self.frame_for_directory_select.show()

        self.frame_for_slot_table = FrameForSlotTable(self.main_window, frame_for_slot_table_listener=self)
        # self.frame_for_slot_table.show()

        self.frame_for_item_restore = FrameForItemRestore(self.main_window,
                                                          frame_for_item_restore_listener=self,
                                                          image_container=self.image_container)

        self.frame_for_messages = FrameForMessages(self.main_window)
        self.frame_for_messages.show()

    def enable_directory_confirm_button(self):
        self.frame_for_directory_select.enable_directory_confirm_button()

    def disable_directory_confirm_button(self):
        self.frame_for_directory_select.disable_directory_confirm_button()

    def start_main_loop(self):
        self.main_window.mainloop()

    def set_save_slot_table_data(self, name_date_status_tuple_list):
        self.frame_for_slot_table.display_save_slot_table(name_date_status_tuple_list)

    def clear_message_area(self):
        self.frame_for_messages.clear_message_area()

    def display_message_from_process(self, text):
        self.frame_for_messages.display_message_from_process(text)

    def display_directory_of_save_slots(self, message):
        self.frame_for_directory_select.display_directory_of_save_slots(message)

    @staticmethod
    def display_popup_info(message):
        messagebox.showinfo(message=message)

    @staticmethod
    def display_write_to_file_warning():
        return messagebox.askokcancel(title=const.WRITE_TO_FILE_WARNING_TITLE,
                                      icon='warning',
                                      message=const.WRITE_TO_FILE_WARNING)

    def enter_directory_select_mode(self):
        self.frame_for_directory_select.show()
        self.frame_for_slot_table.hide()
        self.frame_for_item_restore.hide()

    def enter_slot_table_mode(self):
        self.frame_for_directory_select.hide()
        self.frame_for_slot_table.show()
        self.frame_for_item_restore.hide()

    def enter_item_restore_mode(self):
        self.frame_for_directory_select.hide()
        self.frame_for_slot_table.hide()
        self.frame_for_item_restore.show()

    def _create_styles(self):

        # create and configure a ttk.Style
        # note that some ttk widgets require a ttk.Style to set background
        ttk_style = ttk.Style(self.main_window)

        # note that 'clam' allowed us to set our notebook tab color while other themes did not
        ttk_style.theme_use('clam')

        # default styles for our mid-level widgets
        ttk_style.configure('TFrame', background=self.COLOR_MID)

        # default styles for our innermost widgets
        ttk_style.configure('TLabel', background=self.COLOR_INNER)
        ttk_style.configure('TButton', background=self.COLOR_INNER)
        ttk_style.configure('TCheckbutton', background=self.COLOR_INNER)
        ttk_style.configure('TMenubutton', background=self.COLOR_INNER)

        # override styles for test widgets
        ttk_style.configure('frame_outer.TLabel', background=self.COLOR_OUTER)

        # override styles for our mid-level widgets
        ttk_style.configure('frame_mid.TLabel', background=self.COLOR_MID)

        # override styles for our innermost widgets
        ttk_style.configure('frame_inner.TFrame', background=self.COLOR_INNER)
