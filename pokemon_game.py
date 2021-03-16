"""
Simple Pokemon Game

Player gets to pick a Pokemon and use it in battle

"""

import numpy as np
from typing import List

# Create the Class


class Pokemon:
    def __init__(self, name, types, moves, evs, health='====================',):
        # save variables as attributes
        self.name = name
        self.types = types
        self.moves = moves
        self.attack = evs['ATTACK']
        self.defense = evs['DEFENSE']
        self.health = health
        self.bars = 20 # number of health bars

'''
        print("+++++")
        print(f"\n{self.name}")
        print("TYPE/", self.types)
        print("ATTACK/", self.attack)
        print("LVL/", 3*(1+np.mean([self.attack, self.defense])))
        print("\nVS.")
        print(f"\n{Pokemon2.name}")
        print("TYPE/", Pokemon2.types)
        print("ATTACK/", Pokemon2.attack)
        print("LVL/", 3*(1+np.mean([Pokemon2.attack,Pokemon2.defense])))
'''




Charizard = Pokemon('Charizard', 'Fire', ['Flamethrower', 'Fly', 'Blast Burn', 'Fire Punch'],
                    {'ATTACK': 12, 'DEFENSE': 8})
Blastoise = Pokemon('Blastoise', 'Water', ['Water Gun', 'Bubblebeam', 'Hydro Pump', 'Surf'],
                    {'ATTACK': 10, 'DEFENSE': 10})
Venusaur = Pokemon('Venusaur', 'Grass', ['Vine Wip', 'Razor Leaf', 'Earthquake', 'Frenzy Plant'],
                   {'ATTACK': 8, 'DEFENSE': 12})

Charmander = Pokemon('Charmander', 'Fire', ['Ember', 'Scratch', 'Tackle', 'Fire Punch'], {'ATTACK': 4, 'DEFENSE': 2})
Squirtle = Pokemon('Squirtle', 'Water', ['Bubblebeam', 'Tackle', 'Headbutt', 'Surf'], {'ATTACK': 3, 'DEFENSE': 3})
Bulbasaur = Pokemon('Bulbasaur', 'Grass', ['Vine Wip', 'Razor Leaf', 'Tackle', 'Leech Seed'],
                    {'ATTACK': 2, 'DEFENSE': 4})

Charmeleon = Pokemon('Charmeleon', 'Fire', ['Ember', 'Scratch', 'Flamethrower', 'Fire Punch'],
                     {'ATTACK': 6, 'DEFENSE': 5})
Wartortle = Pokemon('Wartortle', 'Water', ['Bubblebeam', 'Water Gun', 'Headbutt', 'Surf'], {'ATTACK': 5, 'DEFENSE': 5})
Ivysaur = Pokemon('Ivysaur\t', 'Grass', ['Vine Wip', 'Razor Leaf', 'Bullet Seed', 'Leech Seed'],
                  {'ATTACK': 4, 'DEFENSE': 6})

selection = [Charmander, Charmeleon, Charizard,
             Squirtle, Wartortle, Blastoise,
             Bulbasaur, Ivysaur, Venusaur]


class Battle(object):

    def __init__(self):
        """
        Constructor for the Pokemon Battle
        """

    def player_pokemon_select(self, entry: int) -> Pokemon:
        """
        Player selects pokemon to use, return the input published to the broker

        :param entry: number of pokemon to select
        :return: selected_pokemon
        """
        if 0 <= entry < len(selection):
            selected_pokemon = selection[entry]
        else:
            selected_pokemon = selection[0]  # default pokemon will be charmander if selection is invalid

        return selected_pokemon

    def player_move_select(self, number: int, pokemon: Pokemon) -> str:
        """
        Player selects a move to make by entering a number, selection options can be seen in the topic
        For simplicity all moves do same damage, damage difference will be determined by
        type advantage. Also assuming unlimited move uses.

        :param number: enter number for selection
        :param pokemon: enter number for selection
        :return: msg_move_select
        """
        msg_move_select = f"{pokemon.name} used {pokemon.moves[number]}!"

        return msg_move_select

    def attack_status(self, attacker: Pokemon, defender: Pokemon):
        """
        Returns a string depending whether if the attack is effect or not

        :param attacker:
        :param defender:
        :return: msg_attack_status = "Its very effective!" or "Its not very effective..."
        """
        # currently using 3 attribute types for simplicity
        attribute = ['Fire', 'Water', 'Grass']

        for i, k in enumerate(attribute):
            if attacker.types == k:

                # Both are the same type
                if defender.types == k:
                    msg_attack_status = 'Its not very effective ...'

                # defender has advantage, (note in attribute tuple that pokemon to the right beats the left)
                if defender.types == attribute[(i + 1) % 3]:
                    msg_attack_status = 'Its not very effective ...'

                # defender has disadvantage
                if defender.types == attribute[(i + 2) % 3]:
                    msg_attack_status = 'Its very effective!'

        return msg_attack_status

    def type_advantage_calculation(self, player1_pokemon: Pokemon, player2_pokemon: Pokemon) -> List[Pokemon]:
        """
        Updates both players pokemon attack and defense values based on type advantage

        :param player1_pokemon:
        :param player2_pokemon:
        :return: updated_pokemon[player1_pokemon_updated, player2_pokemon_updated]
        """

        # currently using 3 attribute types for simplicity
        attribute = ['Fire', 'Water', 'Grass']

        for i, k in enumerate(attribute):
            if player1_pokemon.types == k:

                # Both are the same type, halve attack and defense
                if player2_pokemon.types == k:
                    player1_pokemon.attack /= 2
                    player1_pokemon.defense /= 2
                    player2_pokemon.attack /= 2
                    player2_pokemon.defense /= 2

                # player2_pokemon has advantage, (note in attribute tuple that pokemon to the right beats the left)
                if player2_pokemon.types == attribute[(i + 1) % 3]:
                    player1_pokemon.attack /= 2
                    player1_pokemon.defense /= 2
                    player2_pokemon.attack *= 2
                    player2_pokemon.defense *= 2

                # player2_pokemon has disadvantage
                if player2_pokemon.types == attribute[(i + 2) % 3]:
                    player1_pokemon.attack *= 2
                    player1_pokemon.defense *= 2
                    player2_pokemon.attack -= 2
                    player2_pokemon.defense -= 2

            updated_pokemon = [player1_pokemon, player2_pokemon]

        return updated_pokemon


    def damage_calculation(self, attacker: Pokemon, defender: Pokemon):
        """
        Calculates damage based on Pokemon's stats after type advantage is applied.
        This value is taken from the pokemons health.

        Damage = attackers attack - .1 defenders defense
        :param attacker:
        :param defender:
        :return: updated_defender
        """
        updated_defender = defender

        # Determine damage
        updated_defender.bars -= attacker.attack
        updated_defender.health = ""

        # Add back bars plus defense boost
        for j in range(int(defender.bars + .1 * defender.defense)):
            updated_defender.health += "="

        return updated_defender

    def check_lose_condition(self, defender: Pokemon) -> bool:
        """
        Return True if defender health is <= 0

        :param defender:
        :return: bool
        """
        if defender.bars <= 0:
            return True
        else:
            return False





