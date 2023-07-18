import datetime
import os

import game_specific_constants as const
from gui_specific.gui_main import GUIMain
from model.file_system_utilities import FileSystemUtilities
from model.save_data import SaveData


class Main:

    # methods to be a GUIMain listener

    def on_confirm_and_continue_request(self):
        if self.save_slot_parent_dir_abs_path is not None:
            self._refresh_save_slot_table()
            self.gui.enter_slot_table_mode()

    def on_open_file_at_slot_index_request(self, slot_table_index):
        self._read_save_data_at_slot_index(slot_table_index)

    def on_open_individual_file_request(self, save_file_abs_path):
        self._read_save_data_from_individual_file(save_file_abs_path)

    def on_refresh_save_slot_table_request(self):
        self._refresh_save_slot_table()

    def on_set_directory_of_save_slots_request(self, path):
        self._set_directory_of_save_slots(path)

    def on_item_restore_request(self, request_type_id, int_value):
        if request_type_id is const.SWORD_DURABILITY:
            self._restore_durability_to_swords()
        elif request_type_id is const.BOW_DURABILITY:
            self._restore_durability_to_bows()
        elif request_type_id is const.SHIELD_DURABILITY:
            self._restore_durability_to_shields()
        elif request_type_id is const.HEALTH_REFILL:
            self._refill_health()
        elif request_type_id is const.ARROW_REFILL:
            self._refill_arrows(int_value)
        elif request_type_id is const.RUPEE_REFILL:
            self._refill_rupees(int_value)
        elif request_type_id is const.MATERIALS_REFILL:
            self._refill_materials(int_value)
        elif request_type_id is const.Z_DEVICE_REFILL:
            self._refill_z_devices(int_value)
        else:
            raise ValueError('the request_type_id is not valid')

    def on_write_save_data_to_file_request(self):
        self._write_changes()

    def on_discard_save_data_request(self):
        self._discard_save_data()

    def on_discard_save_data_and_reload_request(self):
        self._discard_save_data_and_reload()

    # methods to be a ByteData listener

    def on_byte_data_pattern_location_found(self, pattern_int, location_int):
        if self.verbose:
            self.gui.display_message_from_process('  byte pattern: ' + hex(pattern_int))
            self.gui.display_message_from_process('  location: ' + hex(location_int))

    def on_byte_data_pattern_value_found(self, pattern_int, value_int):
        if self.verbose:
            self.gui.display_message_from_process('  byte pattern: ' + hex(pattern_int))
            self.gui.display_message_from_process('  value: ' + hex(value_int))

    # methods to be a SaveData listener

    def on_save_data_message(self, message):
        if self.verbose:
            self.gui.display_message_from_process('\n' + message)

    def __init__(self, verbose=False):

        self.verbose = verbose

        # flag values about save data that is being worked with
        self.current_data_from_slot = False
        self.current_data_from_individual_file = False

        # file path values
        self.save_slot_parent_dir_abs_path = None
        self.save_file_abs_path = None

        # table of data about the save slots
        self.slot_name_date_status_tuple_list = None

        # reference to our SaveData object
        self.save_data = None

        # create our gui object and pass in self as a gui_listener
        self.gui = GUIMain(self)

        # try to read the directory of the save slots from a persistent file
        self._set_directory_of_save_slots_from_file()

        # start the gui
        self.gui.start_main_loop()

    def _set_directory_of_save_slots_from_file(self):

        # check for "file does not exist" early return condition
        if not os.path.isfile(const.PERSIST_PATH_FILENAME):
            self.gui.display_directory_of_save_slots('---')
            self.gui.display_message_from_process('\nDirectory of the save slots could not be loaded')
            return

        try:
            with open(const.PERSIST_PATH_FILENAME, 'r') as file:
                text = file.read()
            # incase the text was a relative path, convert it
            temp_save_slots_abs_path = os.path.abspath(text)
            # check if the temp_save_slots_abs_path
            if self._is_valid_directory_of_save_slots(temp_save_slots_abs_path):
                self.save_slot_parent_dir_abs_path = temp_save_slots_abs_path
                self.gui.display_directory_of_save_slots(self.save_slot_parent_dir_abs_path)
                self.gui.display_message_from_process('\nDirectory of the save slots loaded')
                self.gui.enable_directory_confirm_button()
            else:
                self.gui.display_directory_of_save_slots('---')
                self.gui.display_message_from_process('\nDirectory of the save slots could not be loaded')
        except:
            self.gui.display_directory_of_save_slots('---')
            self.gui.display_message_from_process(
                '\nAn error occurred while trying to load the directory of the save slots')

    def _set_directory_of_save_slots(self, directory):

        # in case we received a relative path, convert it to an absolute path (tkinter docs do not specify path type)
        save_slots_abs_path = os.path.abspath(directory)

        # if the path is valid, call our helper function to finish, and exit the function here
        if self._is_valid_directory_of_save_slots(save_slots_abs_path):
            self._finish_set_directory_of_save_slots(save_slots_abs_path)
            return

        # otherwise, adjust our temp path for the condition where the user selected a slot directory (a level too deep)
        save_slots_abs_path = os.path.dirname(save_slots_abs_path)

        # if the new path is valid, call our helper function to finish, and exit the function here
        if self._is_valid_directory_of_save_slots(save_slots_abs_path):
            self._finish_set_directory_of_save_slots(save_slots_abs_path)
            return

        # otherwise, update the gui that the path selection is not valid
        self.gui.display_message_from_process('\nThe selected directory did not contain save slots')
        self.gui.display_message_from_process('\nThe directory of the save slots has NOT been changed')

    def _finish_set_directory_of_save_slots(self, save_slots_abs_path):
        # set our attribute, write to our file, and update the gui
        self.save_slot_parent_dir_abs_path = save_slots_abs_path
        with open(const.PERSIST_PATH_FILENAME, 'w') as file:
            file.write(self.save_slot_parent_dir_abs_path)
        self.gui.display_directory_of_save_slots(self.save_slot_parent_dir_abs_path)
        self.gui.display_message_from_process('\nThe directory of the save slots has been set')
        self.gui.enable_directory_confirm_button()
        # refresh the save slot table
        self._refresh_save_slot_table()
        self.gui.enter_slot_table_mode()

    @staticmethod
    def _is_valid_directory_of_save_slots(abs_path):

        # check for "not a path" early return condition
        if not os.path.isdir(abs_path):
            return False

        # get a list of filesystem elements in the directory given by abs_path
        fs_elements = os.listdir(abs_path)

        # loop through our filesystem elements
        for fs_element in fs_elements:

            # create a full path for the current filesystem element
            fs_element_full_path = os.path.join(abs_path, fs_element)

            # return True if we find a directory that starts with the GAME_SAVE_SLOT_PREFIX
            if os.path.isdir(fs_element_full_path) and fs_element.startswith(const.SAVE_SLOT_PREFIX):
                return True

        # return false, if we got this far, no file system items matched our condition
        return False

    def _refresh_save_slot_table(self):

        # check for early return condition
        if self.save_slot_parent_dir_abs_path is None:
            self.gui.display_message_from_process('\nSave slot table could not be refreshed')
            self.gui.display_message_from_process('Directory of the save slots is not set')
            return

        # loop through the contents of the save slots directory
        fs_elements = os.listdir(self.save_slot_parent_dir_abs_path)
        self.slot_name_date_status_tuple_list = []
        for fs_element in fs_elements:

            # look for save slot directories
            filename_full_path = os.path.join(self.save_slot_parent_dir_abs_path, fs_element)
            if os.path.isdir(filename_full_path) and fs_element.startswith(const.SAVE_SLOT_PREFIX):

                date_and_status = self._calculate_save_slot_date_and_status(fs_element)

                self.slot_name_date_status_tuple_list.append((fs_element, date_and_status[0], date_and_status[1]))

        self.slot_name_date_status_tuple_list.sort(key=lambda a: a[1], reverse=True)

        self.gui.set_save_slot_table_data(self.slot_name_date_status_tuple_list)
        self.gui.display_message_from_process('\nSave slot table refreshed')

    def _delete_old_backup_files_from_save_slot(self):
        num_orig_to_keep = 4
        num_mod_to_keep = 4
        orig_pattern = r'progress\.\d{8}\.\d{6}\.orig'
        mod_pattern = r'progress\.\d{8}\.\d{6}\.mod'

        dir_abs_path = os.path.dirname(self.save_file_abs_path)

        deleted_files = FileSystemUtilities.delete_files_by_pattern_low_to_high(orig_pattern, dir_abs_path,
                                                                                num_orig_to_keep)
        for filename in deleted_files:
            self.gui.display_message_from_process('\nauto-deleted: ' + filename)

        deleted_files = FileSystemUtilities.delete_files_by_pattern_low_to_high(mod_pattern, dir_abs_path,
                                                                                num_mod_to_keep)
        for filename in deleted_files:
            self.gui.display_message_from_process('\nauto-deleted: ' + filename)

    def _calculate_save_slot_date_and_status(self, dir_name):

        # construct the full path for a save file that should be in this slot
        save_file_abs_path = os.path.join(self.save_slot_parent_dir_abs_path, dir_name, const.SAVE_FILE_NAME)

        # if the save file does not exist, return the pair: None, 'save file not found'
        if not os.path.isfile(save_file_abs_path):
            return 0, 'not_found'

        # otherwise, get the timestamp of the save file in this slot
        timestamp_float = os.path.getmtime(save_file_abs_path)

        # if the current save file matches a mod file, return the timestamp and 'mod'
        if FileSystemUtilities.does_save_file_match_a_mod_file(save_file_abs_path):
            return timestamp_float, 'mod'

        # otherwise, return the timestamp and 'orig'
        return timestamp_float, 'orig'

    def _discard_save_data(self):
        if self.current_data_from_slot:
            self._refresh_save_slot_table()
            self.gui.enter_slot_table_mode()
        else:
            self.gui.enter_directory_select_mode()

        self.save_data = None
        self.current_data_from_slot = False
        self.current_data_from_individual_file = False

    def _read_save_data_at_slot_index(self, save_slot_index):

        # get the save slot associated with the button index
        slot_name_date_status = self.slot_name_date_status_tuple_list[save_slot_index]
        save_slot_dir = slot_name_date_status[0]

        # read the save file to our save_data_bytearray
        self.save_file_abs_path = os.path.join(self.save_slot_parent_dir_abs_path, save_slot_dir, const.SAVE_FILE_NAME)

        self.current_data_from_slot = True
        self._read_save_data()

    def _read_save_data_from_individual_file(self, save_file_abs_path):

        # in case we somehow got a relative path, convert it to an absolute path (tkinter docs do not specify path type)
        self.save_file_abs_path = os.path.abspath(save_file_abs_path)
        self.current_data_from_individual_file = True
        self._read_save_data()

    def _discard_save_data_and_reload(self):

        if self.is_save_data_null():
            return

        if not self.save_data.is_data_modified():
            self.gui.display_message_from_process('\nThere are no changes to discard')
            return

        self.save_data = None
        self._read_save_data()

    def _read_save_data(self):

        try:
            with open(self.save_file_abs_path, 'rb') as file:
                save_data_bytearray = bytearray(file.read())
        except FileNotFoundError:
            self._discard_save_data()
            self.gui.display_message_from_process('\nCould not open: ' + self.save_file_abs_path +
                                                  ', the file is missing')
            return

        # create a SaveData object and pass self as a save_data_listener
        self.save_data = SaveData(save_data_bytearray, self)

        if self.save_data.are_all_addresses_set():
            filename = os.path.split(self.save_file_abs_path)[1]
            parent_dir = os.path.split(self.save_file_abs_path)[0]
            self.gui.display_message_from_process('\nOpened save data from: ' + filename +
                                                  ' in directory: ' + parent_dir)
            self._display_simple_save_data_stats()
            self.gui.enter_item_restore_mode()

        # if there was a problem reading the save file, notify the user and dereference the save data
        else:
            self.gui.display_message_from_process('\nThe save file could not be opened')
            self.gui.display_message_from_process('It does not appear to be a valid save file for this game')
            # self._send_message_with_timestamp_to_gui('Modify data routine cancelled')
            message = 'The save file could not be opened\n' \
                      'It does not appear to be a valid save file for this game'
            self.gui.display_popup_info(message)

            self.save_data = None
            self.current_data_from_slot = False
            self.current_data_from_individual_file = False

    def is_save_data_null(self):
        # this error condition should never happen, but might be reached if the gui's state is not consistent with main
        if self.save_data is None:
            self.gui.display_popup_info('Error: no save data is loaded')
            self.gui.display_message_from_process('\nError: no save data is loaded')
            return True
        else:
            return False

    def _restore_durability_to_swords(self):
        if self.is_save_data_null():
            return
        num_changed, num_total = self.save_data.restore_durability_to_swords()
        self._send_list_refill_message('Restored durability of', num_changed, num_total, 'swords', 255)

    def _restore_durability_to_bows(self):
        if self.is_save_data_null():
            return
        num_changed, num_total = self.save_data.restore_durability_to_bows()
        self._send_list_refill_message('Restored durability of', num_changed, num_total, 'bows', 255)

    def _restore_durability_to_shields(self):
        if self.is_save_data_null():
            return
        num_changed, num_total = self.save_data.restore_durability_to_shields()
        self._send_list_refill_message('Restored durability of', num_changed, num_total, 'shields', 255)

    def _refill_health(self):
        if self.is_save_data_null():
            return
        start_value, end_value = self.save_data.refill_health()
        start_value = start_value / 4
        end_value = end_value / 4
        self._send_simple_refill_message('hearts', start_value, end_value)

    def _refill_arrows(self, quantity):
        if self.is_save_data_null():
            return
        try:
            start_value, end_value = self.save_data.set_arrows_if_greater_than_current(quantity)
            self._send_simple_refill_message('arrows', start_value, end_value)
        except ValueError as e:
            self._generate_value_error_message(str(e))

    def _refill_rupees(self, quantity):
        if self.is_save_data_null():
            return
        try:
            start_value, end_value = self.save_data.set_rupees_if_greater_than_current(quantity)
            self._send_simple_refill_message('rupees', start_value, end_value)
        except ValueError as e:
            self._generate_value_error_message(str(e))

    def _refill_materials(self, quantity):
        if self.is_save_data_null():
            return
        try:
            num_changed, num_total = self.save_data.set_materials_quantity_if_greater_than_current(quantity)
            self._send_list_refill_message('Refilled', num_changed, num_total, 'materials', quantity)
        except ValueError as e:
            self._generate_value_error_message(str(e))

    def _refill_z_devices(self, quantity):
        if self.is_save_data_null():
            return
        try:
            num_changed, num_total = self.save_data.set_z_device_quantity_if_greater_than_current(quantity)
            self._send_list_refill_message('Refilled', num_changed, num_total, 'z-devices', quantity)
        except ValueError as e:
            self._generate_value_error_message(str(e))

    def _send_list_refill_message(self, action, num_changed, num_total, value_name, target_value):
        # self.gui.display_message_from_process(action + ' ' + str(num_changed) + ' of ' + str(num_total) +
        #                                       ' ' + value_name + ' to: ' + str(target_value))
        self.gui.display_message_from_process('\n' + action + ' all ' + value_name +
                                              ' to at least: ' + str(target_value))
        self.gui.display_message_from_process(str(num_changed) + ' of ' + str(num_total) + ' items affected')

    def _send_simple_refill_message(self, value_name, start_value, end_value):
        if end_value > start_value:
            self.gui.display_message_from_process('\nRefilled ' + value_name + ' from: ' + str(start_value) +
                                                  ' to: ' + str(end_value))
        elif end_value == start_value:
            self.gui.display_message_from_process('\nNo change in ' + value_name + ' value: ' + str(end_value))
        else:
            self.gui.display_message_from_process('\nLowered ' + value_name + ' from: ' + str(start_value) +
                                                  ' to: ' + str(end_value))

    def _write_changes(self):
        if self.is_save_data_null():
            return

        if not self.save_data.is_data_modified():
            self.gui.display_message_from_process('\nThere are no changes to write')
            return

        user_accepts = self.gui.display_write_to_file_warning()

        if not user_accepts:
            self.gui.display_message_from_process('\nWrite changes cancelled')
            return

        if self.verbose:
            self._display_simple_save_data_stats()

        # write our save data to the save file and create our backup files

        # if the current save file was written by the game, then back it up
        # we check this when a modification is requested in case the save file was updated by the game recently
        if not FileSystemUtilities.does_save_file_match_a_mod_file(self.save_file_abs_path):
            backup_name = FileSystemUtilities.rename_original_save_file(self.save_file_abs_path)
            self.gui.display_message_from_process('\noriginal save file renamed to:\n  ' + backup_name)

        backup_name = FileSystemUtilities.write_bytearray_to_save_file(self.save_data.get_bytearray(),
                                                                       self.save_file_abs_path)
        self.gui.display_message_from_process('\nmodified save data backed up as:\n  ' + backup_name)
        save_file_name = os.path.basename(self.save_file_abs_path)
        self.gui.display_message_from_process('\nmodified save data written as:\n  ' + save_file_name)

        if self.current_data_from_slot:
            self._delete_old_backup_files_from_save_slot()
            self._refresh_save_slot_table()
            self.gui.enter_slot_table_mode()
        else:
            self.gui.enter_directory_select_mode()

        self.save_data = None
        self.current_data_from_slot = False
        self.current_data_from_individual_file = False

    def _display_simple_save_data_stats(self):
        heart = self.save_data.get_heart_value()
        heart = heart / 4.0
        self.gui.display_message_from_process('hearts: ' + str(heart))

        max_heart = self.save_data.get_max_heart_value()
        max_heart = max_heart / 4.0
        self.gui.display_message_from_process('max_hearts: ' + str(max_heart))

        arrow = self.save_data.get_arrow_value()
        self.gui.display_message_from_process('arrows: ' + str(arrow))

        rupee = self.save_data.get_rupee_value()
        self.gui.display_message_from_process('rupees: ' + str(rupee))

    def _generate_value_error_message(self, message):
        self.gui.display_popup_info('value error: + message')
        self.gui.display_message_from_process('\nvalue error:')
        self.gui.display_message_from_process(message)

    def _send_message_with_timestamp_to_gui(self, message):
        now_datetime = datetime.datetime.now()
        now_time_str = now_datetime.strftime("%Y/%m/%d %H:%M:%S")
        self.gui.display_message_from_process('\n' + now_time_str + ' ' + message)


if __name__ == "__main__":
    main = Main(verbose=False)
