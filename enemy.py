from hero import Hero
import random

class Enemy(Hero):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.name = random.choice(['a giant rat', 'a small coyote', 'a basilisk'])
        self.type = random.choice(['Warrior', 'Wizard', 'Ranger'])
        self.lvl = random.randint(round(self.lvl * 0.75), int(self.lvl * 1.25))
        self.xp = random.randint(2 * self.lvl, 5 * self.lvl)
        self.max_hp = random.randint(int(self.max_hp * 0.75), self.max_hp)
        self.hp = self.max_hp
        self.gold = random.randint(1, 3 * self.lvl)

    def enemy_attack(self, hero):
        enemy_damage = random.randint(0, 4 * self.lvl)
        hero.hp = hero.hp - enemy_damage

        if enemy_damage == 0:
            enemy_attack = f"{self.name.capitalize()} miss."
        elif enemy_damage == 1:
            enemy_attack = f"{self.name.capitalize()} hits you for {enemy_damage} point of damage."
        else:
            enemy_attack = f"{self.name.capitalize()} hits you for {enemy_damage} points of damage."

        return enemy_attack

    def enemy_died(self, hero):
        if self.hp <= 0:
            hero.gold += self.gold
            hero.xp += self.xp
            return self.xp, self.gold
