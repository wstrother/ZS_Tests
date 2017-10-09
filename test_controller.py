from unittest import TestCase
from unittest.mock import Mock, patch
import src.controller as cont
import src.controller_io as cont_io


class TestController(TestCase):
    def setUp(self):
        self.controller_1 = cont.Controller("Test Controller")

    def test_get_device(self):
        new_device = Mock(name="InputDevice")
        new_device.name = "test device"
        mapping = Mock(name="Mapping")

        self.controller_1.add_device(new_device, mapping)

        self.assertEqual(
            new_device, self.controller_1.get_device("test device")
        )

    def test_get_device_frames(self):
        new_device = Mock(name="InputDevice")
        new_device.name = "test device"
        new_device.get_input.return_value = 1
        mapping = Mock(name="Mapping")

        self.controller_1.add_device(new_device, mapping)

        self.controller_1.update()
        device_frames = self.controller_1.get_device_frames("test device")
        self.assertEqual(
            device_frames[-1], 1
        )

    def test_add_device(self):
        new_device = Mock(name="InputDevice")
        new_device.name = "test device"
        mapping = Mock(name="Mapping")

        self.controller_1.add_device(new_device, mapping)
        self.assertTrue(
            new_device in self.controller_1.devices
        )

    def test_update(self):
        new_device = Mock(name="InputDevice")
        new_device.name = "test device"
        new_device.get_input.return_value = 1
        mapping = Mock(name="Mapping")

        self.controller_1.add_device(new_device, mapping)

        self.controller_1.update()
        self.assertEqual(
            self.controller_1.frames[-1], [1]
        )

    def test_button(self):
        button = cont.Button("test button")
        button.init_delay = 5
        button.held_delay = 2
        mapping = Mock(name="ButtonMapping")

        self.controller_1.add_device(
            button, mapping
        )

        self.assertEqual(
            button.get_value(), 0
        )
        inputs = [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
        held = 0
        frame_num = 0
        for i in inputs:
            held += i

            mapping.is_pressed.return_value = i
            self.controller_1.update()
            self.assertEqual(
                button.get_value(), i
            )
            if i:
                self.assertEqual(
                    button.held, held
                )

            frame_num += 1

            if frame_num in (2, 3, 4, 6, 8):
                self.assertTrue(
                    button.ignore
                )

            if frame_num in (1, 5, 7, 9):
                self.assertTrue(
                    not button.ignore
                )

            if frame_num == 10:
                self.assertTrue(
                    button.negative_edge()
                )

    def test_trigger(self):
        trigger = cont.Trigger("test trigger")
        trigger.dead_zone = .95
        mapping = Mock(name="TriggerMapping")

        self.controller_1.add_device(
            trigger, mapping
        )

        self.assertEqual(
            trigger.get_value(), 0.0
        )

        inputs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        frame_num = 0
        for i in inputs:
            frame_num += 1
            mapping.get_value.return_value = i
            self.controller_1.update()

            self.assertEqual(
                trigger.get_displacement(), i
            )

            if frame_num < 10:
                self.assertTrue(
                    not trigger.check()
                )

            if frame_num == 10:
                self.assertTrue(
                    trigger.check
                )

    def test_dpad(self):
        dpad = cont.Dpad("test dpad")
        mappings = [
            Mock(name="ButtonMapping"),
            Mock(name="ButtonMapping"),
            Mock(name="ButtonMapping"),
            Mock(name="ButtonMapping"),
        ]

        self.controller_1.add_device(
            dpad, mappings
        )

        inputs = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
        frame_num = 0
        for i in inputs:
            mappings[0].is_pressed.return_value = i
            for m in mappings[1:]:
                m.is_pressed.return_value = 0

            self.controller_1.update()
            dpad.update()
            frame_num += 1

            if i:
                self.assertTrue(
                    dpad.held
                )

            if frame_num <= 4:
                self.assertEqual(
                    dpad.get_direction(), (0, -1)
                )
            else:
                self.assertEqual(
                    dpad.get_direction(), (0, 0)
                )

    def test_thumb_stick(self):
        stick = cont.ThumbStick("test stick")
        stick.dead_zone = 0.25
        mappings = [
            Mock(name="AxisMapping"),
            Mock(name="AxisMapping"),
        ]

        self.controller_1.add_device(
            stick, mappings
        )

        self.assertEqual(
            stick.get_value(), (0.0, 0.0)
        )

        inputs = [0.0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        frame_num = 0
        for i in inputs:
            frame_num += 1

            mappings[0].get_value.return_value = i
            mappings[1].get_value.return_value = 0.0
            self.controller_1.update()

            self.assertEqual(
                stick.get_direction(), (i, 0.0)
            )

            self.assertEqual(
                stick.x_axis, i
            )

            self.assertEqual(
                stick.y_axis, 0.0
            )

            self.assertEqual(
                round(stick.get_magnitude(), 1), i
            )

            if frame_num in (1, 2):
                self.assertTrue(
                    not stick.check()
                )

            if frame_num > 2:
                self.assertTrue(
                    stick.check()
                )

    def test_controller_io(self):
        dpad = {
            "class": "dpad",
            "up": ("button_map_key", "up"),
            "down": ("button_map_key", "down"),
            "left": ("button_map_key", "left"),
            "right": ("button_map_key", "right")
        }
        button = {
            "class": "button",
            "mapping": ("button_map_key", "a")
        }
        trigger = {
            "class": "trigger",
            "mapping": ("axis_map", 0, "Test Device", 0, 1)
        }
        stick = {
            "class": "thumb_stick",
            "x_axis": ("axis_map", 1, "Test Device", 0, 1),
            "y_axis": ("axis_map", 2, "Test Device", 0, -1)
        }
        devices = {
            "Dpad": dpad,
            "Button": button,
            "Trigger": trigger,
            "ThumbStick": stick
        }
        with patch('src.input_manager.pygame') as mock:
            mock.K_UP, mock.K_DOWN, mock.K_RIGHT, mock.K_LEFT, mock.K_a = (
                1, 2, 3, 4, 5
            )

            with patch('src.input_manager.InputManager') as mock_im:
                mock_im.INPUT_DEVICES = [Mock(name="Input Device")]
                mock_joy = mock_im.INPUT_DEVICES[0]
                mock_joy.get_name.return_value = "Test Device"

                c = cont_io.ControllerIO.make_controller(
                    "Test Controller", devices
                )

                self.assertEqual(
                    type(c.get_device("Dpad")), cont.Dpad
                )
                self.assertEqual(
                    type(c.mappings["Dpad"][0]),
                    cont_io.ButtonMappingKey
                )

                self.assertEqual(
                    type(c.get_device("Button")), cont.Button
                )
                self.assertEqual(
                    type(c.mappings["Button"]),
                    cont_io.ButtonMappingKey
                )

                self.assertEqual(
                    type(c.get_device("Trigger")), cont.Trigger
                )
                self.assertEqual(
                    type(c.mappings["Trigger"]), cont_io.AxisMapping
                )

                self.assertEqual(
                    type(c.get_device("ThumbStick")), cont.ThumbStick
                )
                self.assertEqual(
                    type(c.mappings["ThumbStick"][0]), cont_io.AxisMapping
                )
