import datetime
import os
import re


class FileSystemUtilities:

    @staticmethod
    def delete_files_by_pattern_low_to_high(regex_pattern, dir_abs_path, num_to_preserve):
        """
        Deletes files that match the regex pattern, in ascending order but leaves the final n number of files
        where n is given by the parameter num_to_preserve.

        For this project, the low-numbered files that match our regex pattern are our oldest backup files
        :param regex_pattern: pattern to compare the filenames to
        :param dir_abs_path: directory to look in
        :param num_to_preserve: number of files not-delete at the end of our ordered listing of the files
        :return: list of files that were deleted
        """
        file_list = []

        # loop through the contents of the save slots directory
        fs_elements = os.listdir(dir_abs_path)
        for fs_element in fs_elements:
            # if the fs_element is a full match for our pattern, add it to the list
            if re.fullmatch(regex_pattern, fs_element) is not None:
                file_list.append(fs_element)

        # if the number of matching files is less than or equal to the number we want to keep...
        # exit early and return an empty list
        if len(file_list) <= num_to_preserve:
            return []

        # otherwise, sort from lowest to highest, and trim the number to keep from the end
        file_list.sort()
        file_list = file_list[0:-num_to_preserve]

        # loop through the list and delete each file
        for file in file_list:
            file_abs_path = os.path.join(dir_abs_path, file)
            os.remove(file_abs_path)

        # return the list of deleted files
        return file_list

    @staticmethod
    def does_save_file_match_a_mod_file(save_file_abs_path):
        """
        Returns if there is a .mod file whose name indicates it is a copy of the save file.

        This app writes save data to two files simultaneously.
        The usual filenames are "progress.sav" and "progress.<current-timestamp>.mod".
        So, we can check if a current "progress.sav" matches one of our mod files by checking if its
        timestamp matches the timestamp in the middle of the name of a .mod file.

        :param save_file_abs_path: absolute path of the save file to examine
        :return: True if there is a .mod file that is a copy of the save file, False otherwise
        """

        # get the time stamp of the current save file
        timestamp_float = os.path.getmtime(save_file_abs_path)

        # get the fs_elements in this directory
        parent_dir = os.path.dirname(save_file_abs_path)
        fs_elements = os.listdir(parent_dir)

        file_name = os.path.basename(save_file_abs_path)
        short_name = os.path.splitext(file_name)[0]
        return FileSystemUtilities._shortname_and_timestamp_match_a_mod_file(short_name, timestamp_float, fs_elements)

    @staticmethod
    def rename_original_save_file(save_file_abs_path):
        """
        Changes the name of the save file to the format this app uses for backups of original save files.
        For example: from <original-name>.sav to <original-name>.<file-modified-timestamp>.orig

        :param save_file_abs_path: absolute path of the save file to rename
        :return:
        """

        parent_dir = os.path.dirname(save_file_abs_path)
        filename = os.path.basename(save_file_abs_path)
        short_name = os.path.splitext(filename)[0]

        # create a backup of the original save file
        timestamp_float = os.path.getmtime(save_file_abs_path)
        backup_name = FileSystemUtilities._backup_name_for_original_file(short_name, timestamp_float)
        backup_name_abs_path = os.path.join(parent_dir, backup_name)

        # rename via os.replace so FileExistsError is not raised if the destination file already exists
        os.replace(save_file_abs_path, backup_name_abs_path)

        return backup_name

    @staticmethod
    def write_bytearray_to_save_file(save_file_bytearray, save_file_abs_path):
        """
        Writes the byte array data to a standard save file and to a backup file.
        For example: <save-file-name>.sav and <save-file-name>.<current-timestamp>.mod

        :param save_file_bytearray: bytearray containing the data to be written
        :param save_file_abs_path: absolute path of the save file to write to
        :return:
        """

        parent_dir = os.path.dirname(save_file_abs_path)
        filename = os.path.basename(save_file_abs_path)
        short_name = os.path.splitext(filename)[0]

        # get the current time to stamp our modified data backup file
        now_datetime = datetime.datetime.now()

        # write our modified data to a backup file
        backup_name = FileSystemUtilities._sandwich_timestamp(short_name, now_datetime, '.mod')
        backup_name_abs_path = os.path.join(parent_dir, backup_name)
        with open(backup_name_abs_path, 'wb') as file:
            file.write(save_file_bytearray)

        # write our modified data to the regular save file that will be read by the game
        with open(save_file_abs_path, 'wb') as file:
            file.write(save_file_bytearray)

        return backup_name

    @staticmethod
    def _shortname_and_timestamp_match_a_mod_file(shortname, timestamp_float, filename_list):

        # generate mod file names we would expect to see from the time stamp given by time_float
        mod_file_option_1 = FileSystemUtilities._backup_name_for_modified_file(shortname, timestamp_float - 1)
        mod_file_option_2 = FileSystemUtilities._backup_name_for_modified_file(shortname, timestamp_float)
        mod_file_option_3 = FileSystemUtilities._backup_name_for_modified_file(shortname, timestamp_float + 1)

        # if any of our candidate mod file names are found in filename_list, return True
        if mod_file_option_1 in filename_list:
            return True
        if mod_file_option_2 in filename_list:
            return True
        if mod_file_option_3 in filename_list:
            return True

        # otherwise, return False
        return False

    @staticmethod
    def _backup_name_for_original_file(shortname, timestamp_float):
        timestamp_datetime = datetime.datetime.fromtimestamp(timestamp_float)
        return FileSystemUtilities._sandwich_timestamp(shortname, timestamp_datetime, '.orig')

    @staticmethod
    def _backup_name_for_modified_file(shortname, timestamp_float):
        timestamp_datetime = datetime.datetime.fromtimestamp(timestamp_float)
        return FileSystemUtilities._sandwich_timestamp(shortname, timestamp_datetime, '.mod')

    @staticmethod
    def _sandwich_timestamp(prefix, timestamp_datetime, suffix):
        timestamp_str = timestamp_datetime.strftime("%Y%m%d.%H%M%S")
        return prefix + '.' + timestamp_str + suffix
