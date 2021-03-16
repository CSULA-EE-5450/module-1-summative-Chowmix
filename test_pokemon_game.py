from unittest import TestCase
from pokemon_game import Pokemon, Battle, selection


class TestPokemonGame(TestCase):
    def setUp(self):
        self.battle = Battle

    def test_player_selection(self):
        self.assertEqual(self.battle.player_pokemon_select(self, 1), selection[1])
        self.assertEqual(self.battle.player_pokemon_select(self, 8), selection[8])
        self.assertEqual(self.battle.player_pokemon_select(self, 23), selection[0])
        self.assertEqual(self.battle.player_pokemon_select(self, -1), selection[0])

    def test_move_select(self):
        self.assertEqual(self.battle.player_move_select(self, 0, selection[2]), "Charizard used Flamethrower!")
        self.assertEqual(self.battle.player_move_select(self, 1, selection[2]), "Charizard used Fly!")
        self.assertEqual(self.battle.player_move_select(self, 2, selection[2]), "Charizard used Blast Burn!")
        self.assertEqual(self.battle.player_move_select(self, 3, selection[2]), "Charizard used Fire Punch!")

    def test_move_effectiveness(self):
        self.assertEqual(self.battle.attack_status(self, selection[1], selection[2]), "Its not very effective ...")
        self.assertEqual(self.battle.attack_status(self, selection[8], selection[1]), "Its not very effective ...")
        self.assertEqual(self.battle.attack_status(self, selection[4], selection[1]), "Its very effective!")

    def check_attribute_type_situation(self):
        self.fire_vs_water = self.battle.type_advantage_calculation(self, selection[0], selection[3])
        self.fire_vs_grass = self.battle.type_advantage_calculation(self, selection[0], selection[6])
        self.water_vs_grass = self.battle.type_advantage_calculation(self, selection[3], selection[6])


    def test_damage_calculation(self):
        self.assertNotEqual(self.battle.damage_calculation(self, selection[1], selection[5]), selection[5])