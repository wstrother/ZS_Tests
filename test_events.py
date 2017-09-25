from unittest import TestCase
from unittest.mock import Mock
from src.entities import Sprite


class TestEvents(TestCase):
    def setUp(self):
        self.sprite_1 = Sprite("Slavoj")

    def test_handle_event(self):
        s = self.sprite_1
        s.on_spawn = Mock(name="on_spawn")
        s.handle_event("spawn")
        s.on_spawn.assert_called_once()

    def test_listener(self):
        s = self.sprite_1
        s.on_hear_spawn = Mock(name="on_hear_spawn")
        s.add_listener("spawn hear_spawn")
        s.handle_event("spawn")
        s.on_hear_spawn.assert_called_once()
        self.assertTrue(s.listening_for("spawn"))

        s.on_hear_spawn.reset_mock()
        s.remove_listener("spawn", "hear_spawn")
        s.handle_event("spawn")
        s.on_hear_spawn.assert_not_called()
        self.assertFalse(s.listening_for("spawn"))

    def test_chain(self):
        s = self.sprite_1
        s.on_live = Mock(name="on_live")
        s.on_die = Mock(name="on_die")

        s.queue_event(
            "spawn",
            {"name": "live", "duration": 10},
            "die"
        )
        s.update()

        for i in range(10):
            s.update()
            s.on_live.assert_called_with()

        s.update()
        s.on_die.assert_called_once()
