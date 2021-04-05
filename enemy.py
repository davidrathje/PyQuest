from hero import Hero
import random

class Enemy(Hero):
    def __init__(self, ctx, hero_type):
        super().__init__(ctx, hero_type)

    def enemy_attack(self, hero):
        enemy_damage = random.randint(0, 4 * self.lvl)
        hero.cur_hp = hero.cur_hp - enemy_damage

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
