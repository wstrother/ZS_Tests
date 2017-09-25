from unittest import TestCase
from unittest.mock import Mock
import src.entities as ent


class TestEntities(TestCase):
    def test_entity(self):
        self.entity = ent.Entity("Test Entity")

        self.entity.set_size(800, 600)
        self.assertEqual(
            self.entity.size, (800, 600)
        )

        self.entity.set_position(100, 100)
        self.assertEqual(
            self.entity.position, (100, 100)
        )
        self.entity.move(100, 100)
        self.assertEqual(
            self.entity.position, (200, 200)
        )

        update_method = Mock(name="update_method")
        self.entity.add_to_list("update_methods", update_method)
        self.entity.update()
        update_method.assert_called_once()

        cfg = self.entity.get_cfg()["Test Entity"]
        self.assertEqual(
            cfg["size"], "800, 600"
        )
        self.assertEqual(
            cfg["position"], "200, 200"
        )

    def test_layer(self):
        layer_1 = ent.Layer("Test Layer")
        test_sprite = Mock(name="Test Sprite")

        parent_layer = Mock(name="Parent Layer")
        parent_layer.name = "Parent Layer"
        parent_layer.sub_layers = []

        layer_1.set_parent_layer(parent_layer)
        self.assertTrue(
            layer_1 in parent_layer.sub_layers
        )

        mock_group = Mock(name="Mock Group")
        mock_group.name = "Mock Group"
        mock_group.sprites = [test_sprite]
        layer_1.set_groups(mock_group)
        self.assertTrue(
            mock_group in layer_1.groups
        )

        cfg = layer_1.get_cfg()["Test Layer"]
        self.assertEqual(
            cfg["groups"], "Mock Group"
        )

        layer_1.update_sprites()
        test_sprite.update.assert_called_once()

        sub_layer = Mock(name="Sub Layer")
        layer_1.sub_layers = [sub_layer]
        layer_1.update_sub_layers()
        sub_layer.update.assert_called_once()

    def test_sprite(self):
        sprite_1 = ent.Sprite("Test Sprite")
        group = Mock(name="Group")
        group.name = "Test Group"
        sprite_1.set_group(group)
        self.assertEqual(
            sprite_1.group, "Test Group"
        )
        group.add_member.asset_called_once_with(
            sprite_1
        )

    def test_environment(self):
        env_1 = ent.Environment("Test Environment")
        test_group = ent.Group("Test Group")
        test_layer = ent.Layer("Test Layer")
        env_1.model = {
            "Test Layer": test_layer,
            "Test Group": test_group
        }

        self.assertTrue(
            test_group in env_1.get_groups()
        )
        self.assertTrue(
            test_layer in env_1.get_layers()
        )

        test_sprite = ent.Sprite("Test Sprite")
        test_sprite.set_group(test_group)
        test_sprite.move(100, 100)
        test_sprite.size = 50, 50

        cfg = env_1.get_state_as_cfg()
        self.assertEqual(
            cfg["groups"], {"Test Group": {}}
        )
        self.assertEqual(
            cfg["layers"], {"Test Layer": {
                "class": "Layer"
            }}
        )
        self.assertEqual(
            cfg["populate"], {"Test Sprite": {
                "class": "Sprite",
                "group": "Test Group",
                "size": "50, 50",
                "position": "100, 100"
            }}
        )
