import tkinter as tk
from tkinter import ttk

import game_specific_constants as const
from gui_general.button_show_hide import ButtonShowHide
from gui_general.button_with_callback_id import ButtonWithCallbackID
from gui_general.frame_hidable import FrameHidable
from gui_specific.widget_group_for_refill_app_specific import WidgetGroupForRefill


class FrameForItemRestore(FrameHidable):

    def __init__(self, parent, frame_for_item_restore_listener, image_container, *args, **kwargs):
        super().__init__(parent, row=0, col=2, sticky=tk.N, padx=10, pady=20, *args, **kwargs)

        self.listener = frame_for_item_restore_listener

        label = ttk.Label(self, text='Click frogs to restore and refill game items', style='frame_mid.TLabel')
        label.grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

        # set up the inner frame and its size control labels
        inner_frame = ttk.Frame(self, style='frame_mid.TFrame')
        inner_frame.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)

        vertical_size_control = ttk.Label(inner_frame, text='', style='frame_mid.TLabel')
        vertical_size_control.grid(row=0, column=100, rowspan=101, ipady=300)

        horizontal_size_control = ttk.Label(inner_frame, text='', style='frame_mid.TLabel')
        horizontal_size_control.grid(row=100, column=0, columnspan=101, ipadx=250)

        frame2_1 = ttk.Frame(inner_frame, style='frame_inner.TFrame')
        frame2_1.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)
        current_row = 0

        horizontal_size_control = ttk.Label(frame2_1, text='', style='frame_inner.TLabel')
        horizontal_size_control.grid(row=100, column=0, columnspan=101, ipadx=115)

        label = ttk.Label(frame2_1,
                          text='Click these frogs to restore weapon\n'
                               'durability and health',
                          style='frame_inner.TLabel')
        label.grid(row=current_row, column=0, columnspan=3, sticky=tk.NSEW, padx=5, pady=5)
        current_row += 1

        button = ButtonWithCallbackID(frame2_1, callback_id=const.SWORD_DURABILITY,
                                      callback=self.listener.on_item_restore_request,
                                      image=image_container.get_image(const.SWORD_DURABILITY))
        button.grid(row=current_row, column=1, sticky=tk.W, padx=5, pady=5)
        label = ttk.Label(frame2_1, text='Restore sword\ndurability', style='frame_inner.TLabel')
        label.grid(row=current_row, column=0, sticky=tk.W, padx=5, pady=5)
        current_row += 1

        button = ButtonWithCallbackID(frame2_1, callback_id=const.BOW_DURABILITY,
                                      callback=self.listener.on_item_restore_request,
                                      image=image_container.get_image(const.BOW_DURABILITY))
        button.grid(row=current_row, column=1, sticky=tk.W, padx=5, pady=5)
        label = ttk.Label(frame2_1, text='Restore bow\ndurability', style='frame_inner.TLabel')
        label.grid(row=current_row, column=0, sticky=tk.W, padx=5, pady=5)
        current_row += 1

        button = ButtonWithCallbackID(frame2_1, callback_id=const.SHIELD_DURABILITY,
                                      callback=self.listener.on_item_restore_request,
                                      image=image_container.get_image(const.SHIELD_DURABILITY))
        button.grid(row=current_row, column=1, sticky=tk.W, padx=5, pady=5)
        label = ttk.Label(frame2_1, text='Restore shield\ndurability', style='frame_inner.TLabel')
        label.grid(row=current_row, column=0, sticky=tk.W, padx=5, pady=5)
        current_row += 1

        button = ButtonWithCallbackID(frame2_1, callback_id=const.HEALTH_REFILL,
                                      callback=self.listener.on_item_restore_request,
                                      image=image_container.get_image(const.HEALTH_REFILL))
        button.grid(row=current_row, column=1, sticky=tk.W, padx=5, pady=5)
        label = ttk.Label(frame2_1, text='Refill Health', style='frame_inner.TLabel')
        label.grid(row=current_row, column=0, sticky=tk.W, padx=5, pady=5)
        current_row += 1

        frame2_2 = ttk.Frame(inner_frame, style='frame_inner.TFrame')
        frame2_2.grid(row=1, column=1, sticky=tk.NSEW, padx=5, pady=5)

        horizontal_size_control = ttk.Label(frame2_2, text='', style='frame_inner.TLabel')
        horizontal_size_control.grid(row=100, column=0, columnspan=101, ipadx=120)

        current_row = 0

        label = ttk.Label(frame2_2,
                          text='Click these frogs to refill arrows, rupees,\n'
                               'and materials. Or skip these to keep your\n'
                               'playthrough more authentic.',
                          style='frame_inner.TLabel')
        label.grid(row=current_row, column=0, columnspan=3, sticky=tk.W, padx=5, pady=5)
        current_row += 1

        self.widget_group_list = []

        widget_group = WidgetGroupForRefill(frame2_2, current_row, 0, 'Refill arrows',
                                            value_id=const.ARROW_REFILL,
                                            photo_image=image_container.get_image(const.ARROW_REFILL),
                                            simple_options=['50', '50', '100', '200'],
                                            max_int=const.ARROW_MAX_QTY,
                                            callback_to_notify_value=self.listener.on_item_restore_request,
                                            callback_to_notify_not_set=self.listener.on_value_not_set)
        self.widget_group_list.append(widget_group)
        current_row += 2

        widget_group = WidgetGroupForRefill(frame2_2, current_row, 0, 'Refill rupees',
                                            value_id=const.RUPEE_REFILL,
                                            photo_image=image_container.get_image(const.RUPEE_REFILL),
                                            simple_options=['250', '250', '500', '1000'],
                                            max_int=const.RUPEE_MAX_QTY,
                                            callback_to_notify_value=self.listener.on_item_restore_request,
                                            callback_to_notify_not_set=self.listener.on_value_not_set)
        self.widget_group_list.append(widget_group)
        current_row += 2

        widget_group = WidgetGroupForRefill(frame2_2, current_row, 0, 'Refill materials',
                                            value_id=const.MATERIALS_REFILL,
                                            photo_image=image_container.get_image(const.MATERIALS_REFILL),
                                            simple_options=['10', '10', '20', '40'],
                                            max_int=const.MATERIALS_MAX_QTY,
                                            callback_to_notify_value=self.listener.on_item_restore_request,
                                            callback_to_notify_not_set=self.listener.on_value_not_set)
        self.widget_group_list.append(widget_group)
        current_row += 2

        widget_group = WidgetGroupForRefill(frame2_2, current_row, 0, 'Refill z-devices',
                                            value_id=const.Z_DEVICE_REFILL,
                                            photo_image=image_container.get_image(const.Z_DEVICE_REFILL),
                                            simple_options=['10', '10', '20', '40'],
                                            max_int=const.Z_DEVICE_MAX_QTY,
                                            callback_to_notify_value=self.listener.on_item_restore_request,
                                            callback_to_notify_not_set=self.listener.on_value_not_set)
        self.widget_group_list.append(widget_group)
        current_row += 2

        label = ttk.Label(frame2_2, text='Enable/disable the\n'
                                         'fun-ruining option to\n'
                                         'enter large numbers', style='frame_inner.TLabel')
        label.grid(row=current_row, column=0, sticky=tk.W, padx=5, pady=5)

        button_show_hide = ButtonShowHide(frame2_2,
                                          self._button_listener_show_overpowered_options,
                                          self._button_listener_hide_overpowered_options,
                                          show_text='Enable\nfun-ruining',
                                          hide_text='Disable\nfun-ruining')
        button_show_hide.grid(row=current_row, column=1, sticky=tk.NW, padx=5, pady=5)

        frame2_3 = ttk.Frame(inner_frame, style='frame_inner.TFrame')
        frame2_3.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)

        vertical_size_control = ttk.Label(frame2_3, text='', style='frame_inner.TLabel')
        vertical_size_control.grid(row=0, column=100, rowspan=101, ipady=40)

        label = ttk.Label(frame2_3, text='Save and discard options for the save data', style='frame_inner.TLabel')
        label.grid(row=0, column=0, columnspan=3, sticky=tk.W, padx=5, pady=5)

        button = ttk.Button(frame2_3, text='Write changes\nto save file',
                            command=self.listener.on_write_changes_request)
        button.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        button = ttk.Button(frame2_3, text='Discard changes\nand go back',
                            command=self.listener.on_discard_changes_request)
        button.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        button = ttk.Button(frame2_3, text='Discard changes and\nre-open save file',
                            command=self.listener.on_discard_changes_and_reload_request)
        button.grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)

    def _button_listener_show_overpowered_options(self, callback_id):
        for widget_group in self.widget_group_list:
            widget_group.enter_advanced_mode()

    def _button_listener_hide_overpowered_options(self, callback_id):
        for widget_group in self.widget_group_list:
            widget_group.enter_simple_mode()
