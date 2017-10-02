from unittest import TestCase
from unittest.mock import Mock
import src.controller as cont


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
        button = cont.Button("test button", self.controller_1)
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

    def test_dpad(self):
        dpad = cont.Dpad("test dpad", self.controller_1)
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
