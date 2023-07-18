
PERSIST_PATH_FILENAME = 'atroupeofmagicfrogstotk.path'

SAVE_SLOT_PREFIX = 'slot_'

SAVE_FILE_NAME = 'progress.sav'

# restore/refill max quantities
ARROW_MAX_QTY = 999
RUPEE_MAX_QTY = 999999
MATERIALS_MAX_QTY = 999
Z_DEVICE_MAX_QTY = 999

# restore/refill types
SWORD_DURABILITY = 'sword durability'
BOW_DURABILITY = 'bow durability'
SHIELD_DURABILITY = 'shield durability'
HEALTH_REFILL = 'health refill'
ARROW_REFILL = 'arrow refill'
RUPEE_REFILL = 'rupee refill'
MATERIALS_REFILL = 'materials refill'
Z_DEVICE_REFILL = 'z-device refill'

# totk title id: 0100F2C0115B6000

SLOT_LOCATION_EXAMPLE_Y = r'C:\Users\YOUR_NAME\AppData\Roaming\EMULATOR_NAME\nand\user\save\MANY_ZEROS\MANY_NUMERS_AND_LETTERS\0100F2C0115B6000'

SLOT_LOCATION_EXAMPLE_R = r'C:\Users\YOUR_NAME\AppData\Roaming\EMULATOR_NAME\bis\user\save\MANY_ZEROS_THEN_SMALL_NUMBER\1'

SHORT_PATH_WORKED = r'...\user\save\MANY_ZEROS_THEN_SMALL_NUMBER\1'
SHORT_PATH_DIDNT_WORK = r'...\user\save\MANY_ZEROS_THEN_SMALL_NUMBER\0'

DIR_SELECT_MESSAGE_TITLE = 'Info about selecting the parent directory of the TOTK save slots'

DIR_SELECT_MESSAGE = 'The parent directory of the TOTK save slots will have subdirectories named: slot_00, slot_01, ' \
                     'slot_02, etc' \
                     '\n\nYou will probably need the ability to "view hidden items" in your Windows settings.' \
                     '\n\nThe path to the directory might look like: ' + SLOT_LOCATION_EXAMPLE_Y + \
                     '\n\nOr it might look like: ' + SLOT_LOCATION_EXAMPLE_R + \
                     '\n\nYour emulator might duplicate the parent directory of the TOTK save slots with the first ' \
                     'named "0" and the other named "1".' \
                     '\n\nIn our tests, using this directory worked:\n' + SHORT_PATH_WORKED + \
                     '\nbut using this directory did not work:\n' + SHORT_PATH_DIDNT_WORK

DIR_SELECT_POP_UP = 'The next dialog will ask you to select the parent directory that contains the TOTK ' \
                    'save slots. ' + DIR_SELECT_MESSAGE

DIR_SELECT_TITLE = 'Select directory that contains the save slots. Example path: ' + SLOT_LOCATION_EXAMPLE_Y

WRITE_TO_FILE_WARNING_TITLE = 'WARNING'

WRITE_TO_FILE_WARNING = 'There is always a risk of data loss when using tools like this. By using this app you ' \
                        'are accepting responsibility for any data loss.' \
                        '\n\nThis app will attempt to:' \
                        '\n- Create a backup of the current save file' \
                        '\n- Write a new save file' \
                        '\n- Delete older backup files in some cases'
