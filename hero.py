import random
from item import random_item_list


class Hero:
    def __init__(self, ctx):
        self.ctx = ctx
        self.lvl = 1
        self.xp = 0
        self.next_lvl = 15
        self.gold = 0
        self.battle = False
        self.flee = False

        self.base_hp = 0
        self.base_mana = 0
        self.base_atk = 0
        self.base_def = 0
        self.base_dodge = 0
        self.base_crit = 0

        self.max_hp = self.base_hp
        self.cur_hp = self.max_hp
        self.max_mana = self.base_mana
        self.cur_mana = self.max_mana
        self.attack = self.base_atk
        self.defense = self.base_def
        self.dodge = self.base_dodge
        self.critical = self.base_crit

        self.inventory = []

        self.equipped_weapon = {}
        self.equipped_shield = {}
        self.equipped_armor = {}

    def hero_attack(self, enemy):
        hero_damage = random.randint(0, 4 * self.lvl)
        hero_attack = {'miss': f"You miss {enemy.name}.",
                       'point': f"You attack {enemy.name} for {hero_damage} point of damage.",
                       'points': f"You attack {enemy.name} for {hero_damage} points of damage."}

        if hero_damage == 0:
            hero_attack = hero_attack['miss']
        elif hero_damage == 1:
            hero_attack = hero_attack['point']
        elif hero_damage > 1:
            hero_attack = hero_attack['points']
            if random.randint(int(self.critical * 0.2), 3) == 3:
                hero_damage *= 2
                hero_attack = f"You crunch {enemy.name} for {hero_damage} points of damage. (CRITICAL)"

        enemy.cur_hp -= hero_damage

        return hero_attack

    def flee(self):
        if self.flee:
            message = "```You may only flee once.```"
        elif random.randint(0, 3) == 1:
            self.battle = False
            message = "```You managed to escape.```"
        else:
            self.flee = True
            message = "```You failed to escape.```"

        return message

    def heal(self, amount):
        self.cur_hp += amount
        if self.cur_hp > self.max_hp:
            self.cur_hp = self.max_hp
        return amount

    def get_level(self):
        if self.xp > self.next_lvl:
            self.lvl += 1
            self.xp -= self.next_lvl
            self.next_lvl *= self.lvl

            self.base_hp = int(self.max_hp + self.lvl * 1.5)
            self.base_mana = int(self.max_mana + self.lvl * 15)

            self.base_atk += int(self.base_atk * 0.2)
            self.base_def += int(self.base_atk * 0.2)
            self.base_dodge += int(self.base_dodge * 0.2)
            self.base_crit += int(self.base_crit * 0.2)

            return True

    def get_item(self):
        if len(self.inventory) >= 3:
            message = "```Your inventory is full.```"
        else:
            message = f"```You found something.```"
        return message

    def sell_item(self, item):
        if self.gold > item.value:
            # TODO
            return item

    def repair(self):
        # TODO
        pass

    def get_inventory_items(self):
        stats = {'attack': ' 🗡️', 'defense': ' 🦾', 'critical': ' 🤺', 'dodge': ' 🤸‍♂', 'health': ' ❤'}
        inventory = ""
        for item in self.inventory:
            inventory += f"{item['name']: <16}"
            for k, v in item['stats'].items():
                inventory += stats[k] + str(v)
            inventory += "\n"

        return inventory

    def get_equipped_items(self):
        stats = {'attack': ' 🗡️', 'defense': ' 🦾', 'critical': ' 🤺', 'dodge': ' 🤸‍♂'}
        weapon = f"{self.equipped_weapon['name']: <16}"
        for k, v in self.equipped_weapon['stats'].items():
            weapon += stats[k] + str(v)

        shield = f"{self.equipped_shield['name']: <16}"
        for k, v in self.equipped_shield['stats'].items():
            shield += stats[k] + str(v)

        armor = f"{self.equipped_armor['name']: <16}"
        for k, v in self.equipped_armor['stats'].items():
            armor += stats[k] + str(v)

        return weapon, shield, armor

    def set_base_stats(self):
        self.max_hp = self.base_hp
        self.max_mana = self.base_mana
        self.attack = self.base_atk
        self.defense = self.base_def
        self.dodge = self.base_dodge
        self.critical = self.base_crit

    def set_equipped_stats(self):
        self.set_base_stats()
        for d in self.equipped_weapon['stats'], self.equipped_armor['stats'], self.equipped_shield['stats']:
            for k, v in d.items():
                setattr(self, k, getattr(self, k) + v)

class Warrior(Hero):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.name = ctx.author.name
        self.type = 'Warrior'
        self.base_hp = 15
        self.base_mana = 0
        self.base_atk = 5
        self.base_def = 10
        self.base_dodge = 5
        self.base_crit = 10

        self.cur_hp = self.base_hp

        self.inventory = [random.choice(random_item_list),
                          random.choice(random_item_list)]

        self.equipped_weapon = random_item_list[9]
        self.equipped_shield = random_item_list[8]
        self.equipped_armor = random_item_list[7]

class Wizard(Hero):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.name = ctx.author.name
        self.type = 'Ranger'
        self.base_hp = 10
        self.base_mana = 10
        self.base_atk = 6
        self.base_def = 3
        self.base_dodge = 5
        self.base_crit = 7

        self.inventory = [random.choice(random_item_list),
                          random.choice(random_item_list)]

        self.equipped_weapon = random_item_list[3]
        self.equipped_shield = random_item_list[1]
        self.equipped_armor = random_item_list[4]

class Ranger(Hero):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.name = ctx.author.name
        self.type = 'Wizard'
        self.base_hp = 12
        self.base_mana = 5
        self.base_atk = 8
        self.base_def = 7
        self.base_dodge = 5
        self.base_crit = 10

        self.inventory = [random.choice(random_item_list),
                          random.choice(random_item_list)]

        self.equipped_weapon = random_item_list[2]
        self.equipped_shield = random_item_list[5]
        self.equipped_armor = random_item_list[6]
