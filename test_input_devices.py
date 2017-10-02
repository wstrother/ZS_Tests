from unittest import TestCase
from unittest.mock import Mock
import src.controller as cont


class TestInputDevices(TestCase):
    def test_button(self):
        controller = Mock(name="Controller")
        button = cont.Button("test button", controller)
        mapping = Mock(name="ButtonMapping")



    def test_dpad(self):
        pass

    def test_stick(self):
        pass

    def test_trigger(self):
        pass
