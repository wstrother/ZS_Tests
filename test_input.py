from unittest import TestCase
from unittest.mock import Mock, patch
import src.input_manager as im


class TestInput(TestCase):
    def setUp(self):
        self.KEYDOWN = 0
        self.JOYBUTTONDOWN = 1
        self.JOYHATMOTION = 2
        self.JOYAXISMOTION = 3
        self.QUIT = 4
        self.K_SPACE = 1

        with patch('src.input_manager.pygame') as mock:
            mock.joystick.get_count.return_value = 1
            mock_device = Mock()
            mock.joystick.Joystick.return_value = mock_device
            mock_device.get_numaxes.return_value = 2
            mock_device.get_axis.return_value = 0
            mock_device.get_hat.return_value = 1, 0
            mock_device.get_name.return_value = "Test Controller"
            mock_device.get_id.return_value = 0

            self.mock_device = mock_device
            self.input_manager_1 = im.InputManager()
            self.input_manager_1.INPUT_DEVICES = [
                self.mock_device
            ]

    @staticmethod
    def get_mock_event(event_type, **kwargs):
        m = Mock(spec=["type"])
        m.type = event_type
        for key in kwargs:
            m.__dict__[key] = kwargs[key]

        return m

    def get_mapping_response(self, event_type, device="button", **kwargs):
        with patch('src.input_manager.pygame') as mock:
            mock.JOYAXISMOTION, mock.JOYBUTTONDOWN, mock.JOYHATMOTION, mock.KEYDOWN, mock.QUIT = [
                self.JOYAXISMOTION, self.JOYBUTTONDOWN, self.JOYHATMOTION, self.KEYDOWN, self.QUIT
                ]

            mock.event.get.return_value = [
                self.get_mock_event(event_type, **kwargs)
            ]

            mock.__dict__['K_SPACE'] = self.K_SPACE

            with patch('src.input_manager.InputManager') as mock_im:
                mock_im.INPUT_DEVICES = self.input_manager_1.INPUT_DEVICES
                mock_im.AXIS_NEUTRAL = False
                mock_im.AXIS_MIN = .9
                mock_im.STICK_DEAD_ZONE = .1

                if device == "button":
                    mapping = self.input_manager_1.get_mapping()
                else:
                    mapping = self.input_manager_1.get_axis()

                return mapping

    def get_axis_response(self, event_type, **kwargs):
        with patch('src.input_manager.pygame') as mock:
            mock.JOYAXISMOTION, mock.JOYBUTTONDOWN, mock.JOYHATMOTION, mock.KEYDOWN, mock.QUIT = [
                self.JOYAXISMOTION, self.JOYBUTTONDOWN, self.JOYHATMOTION, self.KEYDOWN, self.QUIT
                ]

            mock.event.get.return_value = [
                self.get_mock_event(event_type, **kwargs)
            ]

            with patch('src.input_manager.InputManager') as mock_im:
                mock_im.INPUT_DEVICES = self.input_manager_1.INPUT_DEVICES
                mock_im.AXIS_NEUTRAL = False
                mock_im.AXIS_MIN = .9
                mock_im.STICK_DEAD_ZONE = .1
                mapping = self.input_manager_1.get_axis()

                return mapping

    def test_button_mapping_button(self):
        mapping = self.get_mapping_response(
            self.JOYBUTTONDOWN, joy=0, button=1
        )
        self.assertTrue(
            isinstance(mapping, im.ButtonMappingButton)
        )
        self.assertEqual(
            mapping.id_num, 1
        )
        self.assertEqual(
            mapping.joy_device, self.mock_device
        )

    def test_button_mapping_key(self):
        mapping = self.get_mapping_response(
            self.KEYDOWN, key="space"
        )
        self.assertTrue(
            isinstance(mapping, im.ButtonMappingKey)
        )
        self.assertEqual(
            mapping.id_num, self.K_SPACE
        )

    def test_button_mapping_axis(self):
        mapping = self.get_mapping_response(
            self.JOYAXISMOTION, joy=0, axis=1, value=1.0
        )
        self.assertTrue(
            isinstance(mapping, im.ButtonMappingAxis)
        )
        self.assertEqual(
            mapping.id_num, 1
        )
        self.assertEqual(
            mapping.joy_device, self.mock_device
        )
        self.assertEqual(
            mapping.sign, 1
        )

    def test_button_mapping_hat(self):
        mapping = self.get_mapping_response(
            self.JOYHATMOTION, joy=0, hat=1, value=(1, 0)
        )
        self.assertTrue(
            isinstance(mapping, im.ButtonMappingHat)
        )
        self.assertEqual(
            mapping.id_num, 1
        )
        self.assertEqual(
            mapping.position, 1
        )
        self.assertEqual(
            mapping.axis, 0
        )

    def test_axis_mapping(self):
        mapping = self.get_mapping_response(
            self.JOYAXISMOTION, joy=0, axis=1, value=1.0, device="axis"
        )
        self.assertTrue(
            isinstance(mapping, im.AxisMapping)
        )
        self.assertEqual(
            mapping.joy_device, self.mock_device
        )
        self.assertEqual(
            mapping.id_num, 1
        )
        self.assertEqual(
            mapping.sign, 1
        )
