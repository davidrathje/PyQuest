from hero import Hero
from item import random_item_list
import random

class Enemy(Hero):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.name = random.choice(['giant rat', 'small coyote', 'basilisk'])
        self.xp = random.randint(2 * self.lvl, 5 * self.lvl)
        self.gold = random.randint(1, 3 * self.lvl)

        self.base_hp = 12 * self.lvl
        self.base_mana = 5
        self.base_atk = 8
        self.base_def = 7
        self.base_dodge = 5
        self.base_crit = 10

        self.max_hp = self.base_hp
        self.cur_hp = self.max_hp
        self.max_mana = self.base_mana
        self.cur_mana = self.max_mana

        self.attack = self.base_atk
        self.defense = self.base_def
        self.dodge = self.base_dodge
        self.critical = self.base_crit

        self.inventory = [random.choice(random_item_list)]

        self.equipped_weapon = {}
        self.equipped_shield = {}
        self.equipped_armor = {}

    def set_enemy_lvl(self, hero):
        self.lvl = random.randint(round(hero.lvl * 0.75), int(hero.lvl * 1.25))


    def enemy_attack(self, hero):
        enemy_damage = random.randint(0, 4 * self.lvl)
        hero.cur_hp -= enemy_damage

        if enemy_damage == 0:
            enemy_attack = f"{self.name.capitalize()} miss."
        elif enemy_damage == 1:
            enemy_attack = f"{self.name.capitalize()} hits you for {enemy_damage} point of damage."
        else:
            enemy_attack = f"{self.name.capitalize()} hits you for {enemy_damage} points of damage."

        return enemy_attack


    def enemy_died(self, hero):
        if self.cur_hp <= 0:
            hero.gold += self.gold
            hero.xp += self.xp
            return self.xp, self.gold
