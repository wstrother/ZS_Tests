from unittest import TestCase
from unittest.mock import Mock, patch
import src.context as context

CFG_JSON = {
    "populate": {
        "Test Sprite": {
            "add_to_model": True,
            "class": "Sprite",
            "size": [50, 50],
            "position": [100, 100],
            "group": "Sprite Group"
        }
    },
    "groups": {
        "Sprite Group": {}
    },
    "layers": {
        "Sprite Layer": {
            "class": "Layer",
            "groups": "Sprite Group"
        }
    },
    "data": {
        "Test Item": {
            "field_1": 1,
            "field_2": 2,
            "field_3": 3
        }
    }
}


class TestContext(TestCase):
    def setUp(self):
        env_1 = Mock()
        env_1.model = {}
        self.env_1 = env_1
        self.cfg = CFG_JSON

        self.class_dict = {
            "Layer": Mock(name="Layer"),
            "Environment": Mock(name="Environment"),
            "Sprite": Mock(name="Sprite")
        }

    def test_model(self):
        with patch('src.context.Group') as mock_group:
            context.update_model(
                self.class_dict,
                self.cfg,
                self.env_1,
            )

            self.class_dict["Layer"].assert_called_with(
                "Sprite Layer"
            )
            self.class_dict["Sprite"].assert_not_called()
            self.class_dict["Environment"].assert_not_called()
            mock_group.assert_called_with(
                "Sprite Group"
            )

            model = self.env_1.model
            self.assertEqual(
                model["Test Item"],
                self.cfg["data"]["Test Item"]
            )

    def test_layers(self):
        model = self.env_1.model
        sprite_layer = Mock(name="Sprite Layer")
        sprite_layer.init_order = []
        model["Sprite Layer"] = sprite_layer

        context.add_layers(
            self.class_dict,
            self.cfg,
            self.env_1,
        )

        sprite_layer.set_parent_layer.assert_called_with(
            self.env_1, False
        )
        sprite_layer.set_groups.assert_called_with(
            "Sprite Group"
        )

    def test_populate(self):
        sprite_group = Mock(name="Sprite Group")
        self.env_1.model["Sprite Group"] = sprite_group

        new_test_sprite = self.class_dict["Sprite"].return_value
        new_test_sprite.init_order = []
        new_test_sprite.cfg_dict = {}
        new_test_sprite.name = "Test Sprite"

        context.populate(
            self.class_dict,
            self.cfg,
            self.env_1,
        )

        self.class_dict["Sprite"].assert_called_once_with(
            "Test Sprite"
        )
        self.assertTrue(
            "Test Sprite" in self.env_1.model
        )
        test_sprite = self.env_1.model["Test Sprite"]
        test_sprite.set_group.assert_called_with(
            sprite_group
        )

        test_sprite.set_size.assert_called_with(
            50, 50
        )
        test_sprite.set_position.assert_called_with(
            100, 100
        )

