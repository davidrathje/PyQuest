from hero import Hero
import random

class Enemy(Hero):
    def __init__(self, ctx, hero_type):
        super().__init__(ctx, hero_type)
        self.name = random.choice(['a giant rat', 'a small coyote', 'a basilisk'])
        self.type = hero_type
        self.lvl = random.randint(round(self.lvl * 0.75), int(self.lvl * 1.25))
        self.xp = random.randint(2 * self.lvl, 5 * self.lvl)
        self.gold = random.randint(1, 3 * self.lvl)
        self.max_hp = random.randint(10 * self.lvl, 12 * self.lvl)
        self.cur_hp = self.max_hp

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
