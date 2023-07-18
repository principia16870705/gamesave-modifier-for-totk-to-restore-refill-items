

class ByteData:
    """
    Holds binary data and methods to operate on the data.
    Is (somewhat) generalized from any specific project and hopefully useful in other projects.
    """

    def __init__(self, m_bytearray, listener):
        """
        A pretty standard constructor

        The listener object must have these functions:
            on_byte_data_pattern_location_found(pattern_int, location_int):
            on_byte_data_pattern_value_found(pattern_int, value_int):

        :param m_bytearray: our main binary data
        :param listener: an object that will receive notifications from this object
        """
        self.m_bytearray = m_bytearray
        self.listener = listener
        self.is_modified = False

    def is_data_modified(self):
        return self.is_modified

    def get_bytearray(self):
        return self.m_bytearray

    def get_value_at_address(self, address_int):
        value_bytes = self.m_bytearray[address_int:address_int + 4]
        return int.from_bytes(value_bytes, byteorder="little")

    def loop_write(self, value_int, start_address, iteration_limit, terminate_pattern_bytes):
        """
        Writes a value to our byte data in four byte steps until it finds the termination pattern or reaches its
        iteration limit.
        :param value_int: value to write
        :param start_address: address to begin writing at
        :param iteration_limit: number that limits the write loop
        :param terminate_pattern_bytes: byte pattern that stops the write loop
        """
        # create the bytes to be written
        value_bytes = value_int.to_bytes(length=4, byteorder="little")
        # loop up to the limit given by our parameter
        for i in range(iteration_limit):
            address = start_address + (i * 4)
            # if we run into the terminate_pattern, break out of the loop
            if terminate_pattern_bytes == self.m_bytearray[address:address + 4]:
                break
            # otherwise, write our bytes
            self.m_bytearray[address:address + 4] = value_bytes

    def loop_write_if_gt_current(self, value_int, start_address, iteration_limit, terminate_pattern_bytes):
        """
        Writes a value to our byte data, in four byte steps, if the value is greater than the bytes it will overwrite.
        The write loop continues until it finds the termination pattern or until it reaches its iteration limit.
        :param value_int: value to write
        :param start_address: address to begin writing at
        :param iteration_limit: number that limits the write loop
        :param terminate_pattern_bytes: byte pattern that stops the write loop
        :return: the number of locations that were written to, the total number of locations that were encountered
        """
        # create the bytes to be written
        value_bytes = value_int.to_bytes(length=4, byteorder="little")
        num_locations_total = 0
        num_locations_changed = 0
        # loop up to the limit given by our parameter
        for i in range(iteration_limit):
            address = start_address + (i * 4)
            current_bytes = self.m_bytearray[address:address + 4]
            if current_bytes == terminate_pattern_bytes:
                break
            current_int = int.from_bytes(current_bytes, byteorder="little")
            num_locations_total += 1
            if value_int > current_int:
                self.m_bytearray[address:address + 4] = value_bytes
                num_locations_changed += 1

        return num_locations_changed, num_locations_total

    def write_if_gt_current(self, value_int, address_int):
        """
        Writes a value to the byte data if the value is greater than the bytes it will overwrite.
        :param value_int: value to write
        :param address_int: address to write to
        :return: True if location was written to, False otherwise
        """
        # if the current_int is less than new_int, write new_int to the bytearray, and return True
        current_int = self.get_value_at_address(address_int)
        if value_int > current_int:
            value_bytes = value_int.to_bytes(length=4, byteorder="little")
            self.m_bytearray[address_int:address_int + 4] = value_bytes
            return True
        # otherwise, return False
        return False

    def get_value_after_pattern(self, pattern_int):
        """
        :raises: ValueError
        """
        # MAY RAISE ValueError here
        location_after_pattern = self.get_location_after_pattern(pattern_int)

        # get the value as bytes and convert to int
        value_after_pattern_bytes = self.m_bytearray[location_after_pattern:location_after_pattern + 4]
        value_after_pattern_int = int.from_bytes(value_after_pattern_bytes, byteorder="little")

        # call our listener and return
        self.listener.on_byte_data_pattern_value_found(pattern_int, value_after_pattern_int)
        return value_after_pattern_int

    def get_location_after_pattern(self, pattern_as_int):
        """
        :raises: ValueError
        """
        # call our helper function to get a list of locations where the pattern occurs
        pattern_location_list = self._build_pattern_location_list(pattern_as_int)

        # if the pattern occurred more than once, inform our listener, and return early
        if len(pattern_location_list) > 1:
            raise ValueError('the requested byte pattern was found more than once')

        # if the pattern did not occur at all, inform our listener, and return early
        if len(pattern_location_list) < 1:
            raise ValueError('the requested byte pattern was not found')

        self.listener.on_byte_data_pattern_location_found(pattern_as_int, pattern_location_list[0])
        return pattern_location_list[0] + 4

    def _build_pattern_location_list(self, pattern_int):
        # finds the locations of a four-byte pattern in four-byte steps

        # create the bytes to look for
        pattern_bytes = pattern_int.to_bytes(length=4, byteorder="big")
        location_list = []

        # loop through the byte array in 4 byte steps
        i = 0
        step = 4
        while i < len(self.m_bytearray):
            # if our byte pattern matches the current bytes, add the location to our list
            if pattern_bytes == self.m_bytearray[i:i + 4]:
                location_list.append(i)
            i += step

        return location_list
