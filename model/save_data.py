import game_specific_constants as const
from model.byte_data import ByteData


class SaveData(ByteData):
    """
    Holds binary data, addresses within the data, and methods to operate on the data.
    Is specific to the current project.

    Note that "location" "index" and "address" are all pretty much synonymous when dealing with our binary data
    """

    # for this project, we must add an address offset to any address that is given by a byte pattern
    # this is because the data values start 4 bytes beyond the address given by the byte pattern
    ADDRESS_OFFSET = 4

    # max number of items
    SWORD_LIMIT = 20
    BOW_LIMIT = 14
    SHIELD_LIMIT = 20
    # this value might actually be 258
    MATERIALS_LIMIT = 280
    # this value might actually be 27
    ZONAI_DEVICE_LIMIT = 30

    # value we use to restore sword, bow, shield durability
    DEFAULT_DURABILITY_INT = 0xFF
    TERMINATE_PATTERN_BYTES = int.to_bytes(0xFFFFFFFF, length=4, byteorder="little")

    # the sword durability byte pattern precedes an integer
    # that integer is the address where the sword durability values are stored
    # the same is true for other game items that require a list of values
    SWORD_DURABILITY_PATTERN = 0x62D0128B
    BOW_DURABILITY_PATTERN = 0x00925860
    SHIELD_DURABILITY_PATTERN = 0x196D41C3

    HEART_PATTERN = 0x8055AB31
    MAX_HEART_PATTERN = 0xA11DE0FB
    ARROW_PATTERN = 0x947DB253
    RUPEE_PATTERN = 0xD72179A7
    SWORD_PATTERN = 0xBED0EF65
    MATERIALS_PATTERN = 0x00852DDE
    Z_DEVICE_PATTERN = 0xB06AD160

    def __init__(self, m_bytearray, listener):
        """
        A pretty standard constructor

        The listener object must have these functions:
            on_save_data_message(message):

        :param m_bytearray: our main binary data
        :param listener: an object that will receive notifications from this object
        """

        super().__init__(m_bytearray, listener)

        self.listener.on_save_data_message('sword_durability')
        self.sword_durability_address_int = self._read_value_after_pattern_as_a_location(
            SaveData.SWORD_DURABILITY_PATTERN)

        self.listener.on_save_data_message('bow_durability')
        self.bow_durability_address_int = self._read_value_after_pattern_as_a_location(
            SaveData.BOW_DURABILITY_PATTERN)

        self.listener.on_save_data_message('shield_durability')
        self.shield_durability_address_int = self._read_value_after_pattern_as_a_location(
            SaveData.SHIELD_DURABILITY_PATTERN)

        self.listener.on_save_data_message('heart')
        try:
            self.heart_address_int = self.get_location_after_pattern(SaveData.HEART_PATTERN)
        except ValueError:
            self.heart_address_int = None

        self.listener.on_save_data_message('heart_max')
        try:
            self.max_heart_address_int = self.get_location_after_pattern(SaveData.MAX_HEART_PATTERN)
        except ValueError:
            self.max_heart_address_int = None

        self.listener.on_save_data_message('arrow')
        self.arrow_address_int = self._read_value_after_pattern_as_a_location(SaveData.ARROW_PATTERN)

        self.listener.on_save_data_message('rupee')
        try:
            self.rupee_address_int = self.get_location_after_pattern(SaveData.RUPEE_PATTERN)
        except ValueError:
            self.rupee_address_int = None

        self.listener.on_save_data_message('materials')
        self.materials_address_int = self._read_value_after_pattern_as_a_location(SaveData.MATERIALS_PATTERN)

        self.listener.on_save_data_message('zonai device')
        self.z_device_address_int = self._read_value_after_pattern_as_a_location(SaveData.Z_DEVICE_PATTERN)

    def are_all_addresses_set(self):
        # if all our addresses are an instance of int, then all our addresses are set
        return isinstance(self.sword_durability_address_int, int) \
            and isinstance(self.bow_durability_address_int, int) \
            and isinstance(self.shield_durability_address_int, int) \
            and isinstance(self.heart_address_int, int) \
            and isinstance(self.max_heart_address_int, int) \
            and isinstance(self.arrow_address_int, int) \
            and isinstance(self.rupee_address_int, int) \
            and isinstance(self.materials_address_int, int) \
            and isinstance(self.z_device_address_int, int)

    def get_heart_value(self):
        return self.get_value_at_address(self.heart_address_int)

    def get_max_heart_value(self):
        return self.get_value_at_address(self.max_heart_address_int)

    def get_arrow_value(self):
        return self.get_value_at_address(self.arrow_address_int)

    def get_rupee_value(self):
        return self.get_value_at_address(self.rupee_address_int)

    def restore_durability_to_swords(self):
        num_changed, num_total = self.loop_write_if_gt_current(
            value_int=SaveData.DEFAULT_DURABILITY_INT,
            start_address=self.sword_durability_address_int,
            iteration_limit=SaveData.SWORD_LIMIT,
            terminate_pattern_bytes=SaveData.TERMINATE_PATTERN_BYTES)
        self._update_modified_flag(num_changed > 0)
        return num_changed, num_total

    def restore_durability_to_bows(self):
        num_changed, num_total = self.loop_write_if_gt_current(
            value_int=SaveData.DEFAULT_DURABILITY_INT,
            start_address=self.bow_durability_address_int,
            iteration_limit=SaveData.BOW_LIMIT,
            terminate_pattern_bytes=SaveData.TERMINATE_PATTERN_BYTES)
        self._update_modified_flag(num_changed > 0)
        return num_changed, num_total

    def restore_durability_to_shields(self):
        num_changed, num_total = self.loop_write_if_gt_current(
            value_int=SaveData.DEFAULT_DURABILITY_INT,
            start_address=self.shield_durability_address_int,
            iteration_limit=SaveData.SHIELD_LIMIT,
            terminate_pattern_bytes=SaveData.TERMINATE_PATTERN_BYTES)
        self._update_modified_flag(num_changed > 0)
        return num_changed, num_total

    def refill_health(self):
        start_value = self.get_heart_value()
        max_heart_int = self.get_max_heart_value()
        max_heart_bytes = max_heart_int.to_bytes(length=4, byteorder="little")
        self.m_bytearray[self.heart_address_int:self.heart_address_int + 4] = max_heart_bytes
        end_value = self.get_heart_value()
        self._update_modified_flag(end_value > start_value)
        return start_value, end_value

    def set_arrows_if_greater_than_current(self, arrows_int):
        """
        :raises: ValueError
        """
        start_value = self.get_arrow_value()
        if not (0 <= arrows_int <= const.ARROW_MAX_QTY):
            raise ValueError('number of arrows is out of range: ' + str(arrows_int))

        did_write = self.write_if_gt_current(arrows_int, self.arrow_address_int)
        self._update_modified_flag(did_write)
        end_value = self.get_arrow_value()
        return start_value, end_value

    def set_rupees_if_greater_than_current(self, rupees_int):
        """
        :raises: ValueError
        """
        start_value = self.get_rupee_value()
        if not (0 <= rupees_int <= const.RUPEE_MAX_QTY):
            raise ValueError('number of rupees is out of range: ' + str(rupees_int))

        did_write = self.write_if_gt_current(rupees_int, self.rupee_address_int)
        self._update_modified_flag(did_write)
        end_value = self.get_rupee_value()
        return start_value, end_value

    def set_materials_quantity_if_greater_than_current(self, materials_qty_int):
        """
        :raises: ValueError
        """
        if not (0 <= materials_qty_int <= const.MATERIALS_MAX_QTY):
            raise ValueError('material quantity is out of range: ' + str(materials_qty_int))

        num_changed, num_total = self.loop_write_if_gt_current(
            value_int=materials_qty_int,
            start_address=self.materials_address_int,
            iteration_limit=SaveData.MATERIALS_LIMIT,
            terminate_pattern_bytes=SaveData.TERMINATE_PATTERN_BYTES)
        self._update_modified_flag(num_changed > 0)
        return num_changed, num_total

    def set_z_device_quantity_if_greater_than_current(self, z_device_qty_int):
        """
        :raises: ValueError
        """
        if not (0 <= z_device_qty_int <= const.Z_DEVICE_MAX_QTY):
            raise ValueError('zonai device quantity is out of range: ' + str(z_device_qty_int))

        num_changed, num_total = self.loop_write_if_gt_current(
            value_int=z_device_qty_int,
            start_address=self.z_device_address_int,
            iteration_limit=SaveData.ZONAI_DEVICE_LIMIT,
            terminate_pattern_bytes=SaveData.TERMINATE_PATTERN_BYTES)
        self._update_modified_flag(num_changed > 0)
        return num_changed, num_total

    def _update_modified_flag(self, bool_value):
        self.is_modified = self.is_modified or bool_value

    def _read_value_after_pattern_as_a_location(self, pattern_int):
        try:
            value_after_pattern = self.get_value_after_pattern(pattern_int)
        # if there is an error, simply return None
        except ValueError:
            return None
        # for this project, we must add an address offset to any address that is given by a byte pattern
        # this is because the data values start 4 bytes beyond the address given by the byte pattern
        return value_after_pattern + SaveData.ADDRESS_OFFSET
