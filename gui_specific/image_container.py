import os
import sys
from PIL import Image, ImageTk

import game_specific_constants as const


class ImageContainer:
    """
    Holds references to images for our app
    Note that one of OUR main objects should maintain a reference to an instance of this class. If a tkinter
    widget is the only object to reference an image, the image will be garbage collected and tkinter widget
    will be blank.
    """

    def __init__(self):

        self.photo_image_dict = {}

        self._load_image(const.SWORD_DURABILITY, 'sword_60.png')
        self._load_image(const.BOW_DURABILITY, 'bow_60.png')
        self._load_image(const.SHIELD_DURABILITY, 'shield_60.png')
        self._load_image(const.HEALTH_REFILL, 'heart_60.png')
        self._load_image(const.ARROW_REFILL, 'arrow_60.png')
        self._load_image(const.RUPEE_REFILL, 'money_60.png')
        self._load_image(const.MATERIALS_REFILL, 'material_60.png')
        self._load_image(const.Z_DEVICE_REFILL, 'z_device_60.png')

    def get_image(self, image_name):
        return self.photo_image_dict[image_name]

    def _load_image(self, key_name, filename):
        image_path = ImageContainer._resolve_path(filename)
        image = Image.open(image_path)
        photo_image = ImageTk.PhotoImage(image)
        self.photo_image_dict[key_name] = photo_image
    
    @staticmethod
    def _resolve_path(image_name):
        """
        Creates a path to the image for the current execution environment
        Returns a path that includes sys._MEIPASS if this code is running as an exe created by pyinstaller
        Otherwise, returns the image_name with the 'image' directory prepended

        Based on a function by Richard Hayman-Joyce on stackoverflow
        stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file

        for future reference, when we ran this code as an exe, 'sys._MEIPASS\\images' became
        C:\\Users\\<username>\\AppData\\Local\\Temp\\_MEI<6-digit-number>\\images'
        :param image_name: the image file to create a path for
        :return: a path to the image file for the current execution environment
        """

        # if this code is currently running as an exe created by pyinstaller, return a path that includes sys._MEIPASS
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, 'images', image_name)
        # otherwise, simply prepend 'images' to image_name
        else:
            return os.path.join('images', image_name)
