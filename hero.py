import random
from item import Item


class Hero:
    def __init__(self, ctx, name, hero_type):
        self.ctx = ctx
        self.name = name
        self.type = hero_type
        self.lvl = 1
        self.xp = 0
        self.next_lvl = 15
        self.max_hp = 10
        self.hp = self.max_hp
        self.mana = 0
        self.base_atk = 5
        self.base_def = 5
        self.base_dodge = 5
        self.base_crit = 5
        self.attack = self.base_atk
        self.defense = self.base_def
        self.dodge = 5
        self.critical = 5
        self.gold = 0
        self.inventory = {}
        self.battle = False
        self.flee = False
        self.equipped_weapon = None
        self.equipped_shield = None
        self.equipped_armor = None

    def attack(self, enemy):
        hero_damage = random.randint(0, 4 * self.lvl)
        enemy.hp = enemy.hp - hero_damage

        if hero_damage == 0:
            hero_attack = "You miss " + enemy.name + "."
        elif hero_damage == 1:
            hero_attack = "You attack " + enemy.name + " for " + str(hero_damage) + " point of damage."
        else:
            hero_attack = "You attack " + enemy.name + " for " + str(hero_damage) + " points of damage."

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
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        return amount

    def get_level(self):
        if self.xp > self.next_lvl:
            self.lvl = self.lvl + 1
            self.xp = self.xp - self.next_lvl
            self.next_lvl = 15 * self.lvl

            self.max_hp = round(self.max_hp + (1.5 * self.lvl))
            self.hp = self.max_hp

            self.base_atk += int(self.base_atk * 0.2)
            self.base_def += int(self.base_atk * 0.2)
            self.base_dodge += int(self.base_dodge * 0.2)
            self.critical += int(self.base_crit * 0.2)

            return True

    def get_item(self):
        if len(self.inventory) >= 3:
            message = "```Your inventory is full.```"
        else:
            item = Item('Rusty Sword', 'Weapon', 1, {'attack': 1, 'critical': 2, 'dodge': 1})
            self.inventory.pop(item)
            message = f"```You found {item.name}.```"
        return message

    def get_inventory(self):
        stats = {'attack': ' 🗡️', 'defense': ' 🦾', 'critical': ' 🤺', 'dodge': '🤸‍♂'}
        inventory = ""
        for item in self.inventory:
            inventory += f"{item['name']: <16}"
            for k, v in item['stats'].items():
                inventory += stats[k] + str(v)
            inventory += "\n"

        return inventory

    def get_equipped_items(self):
        stats = {'attack': ' 🗡️', 'defense': ' 🦾', 'critical': ' 🤺', 'dodge': '🤸‍♂'}
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

    def equip_gear(self):
        self.attack = self.base_atk
        self.attack = self.base_atk
        self.defense = self.base_def
        self.dodge = self.base_dodge
        self.critical = self.base_crit

        for d in self.equipped_weapon['stats'], self.equipped_armor['stats'], self.equipped_shield['stats']:
            for key, value in d.items():
                if key == 'attack':
                    self.attack += value
                elif key == 'defense':
                    self.defense += value
                elif key == 'critical':
                    self.critical += value
                elif key == 'dodge':
                    self.dodge += value


class Warrior(Hero):
    def __init__(self, ctx, name, hero_type):
        super().__init__(ctx, name, hero_type)
        self.max_hp = 15
        self.hp = self.max_hp
        self.mana = 0
        self.base_atk = 5
        self.base_def = 10
        self.dodge = 5
        self.critical = 10

        self.inventory = [{'name': 'Short Bow',
                           'type': 'Weapon',
                           'value': 2,
                           'stats': {'attack': 1, 'critical': 2, 'dodge': 1}
                           },
                          {'name': 'Lantern',
                           'type': 'Offhand',
                           'value': 0,
                           'stats': {'defense': 1, 'dodge': 1}
                           }]

        self.equipped_weapon = {'name': 'Rusty Longsword',
                                'type': 'Weapon',
                                'value': 0,
                                'stats': {'attack': 5, 'critical': 5, 'dodge': 5}
                                }

        self.equipped_shield = {'name': 'Kite Shield',
                                'type': 'Offhand',
                                'value': 0,
                                'stats': {'defense': 5, 'dodge': 5}
                                }

        self.equipped_armor = {'name': 'Plate Armor',
                               'type': 'Armor',
                               'value': 0,
                               'stats': {'defense': 5, 'dodge': 5}
                               }


class Wizard(Hero):
    def __init__(self, ctx, name, hero_type):
        super().__init__(ctx, name, hero_type)
        self.max_hp = 10
        self.hp = self.max_hp
        self.mana = 10
        self.attack = 10
        self.defense = 5
        self.dodge = 5
        self.critical = 5

        self.inventory = [{'name': 'Short Bow',
                           'type': 'Weapon',
                           'value': 2,
                           'stats': {'attack': 1, 'critical': 2, 'dodge': 1}
                           },
                          {'name': 'Lantern',
                           'type': 'Offhand',
                           'value': 0,
                           'stats': {'defense': 1, 'dodge': 1}
                           }]

        self.equipped_weapon = {'name': 'Wand',
                                'type': 'Weapon',
                                'value': 0,
                                'stats': {'attack': 5, 'critical': 5, 'dodge': 5}
                                }

        self.equipped_shield = {'name': 'Lantern',
                                'type': 'Offhand',
                                'value': 0,
                                'stats': {'defense': 1, 'dodge': 1}
                                }

        self.equipped_armor = {'name': 'Cloth Robe',
                               'type': 'Armor',
                               'value': 0,
                               'stats': {'attack': 4, 'defense': 3, 'dodge': 2}
                               }


class Ranger(Hero):
    def __init__(self, ctx, name, hero_type):
        super().__init__(ctx, name, hero_type)
        self.max_hp = 12
        self.hp = self.max_hp
        self.mana = 5
        self.attack = 8
        self.defense = 7
        self.dodge = 5
        self.critical = 5

        self.inventory = [{'name': 'Short Bow',
                           'type': 'Weapon',
                           'value': 2,
                           'stats': {'attack': 1, 'critical': 2, 'dodge': 1}
                           },
                          {'name': 'Lantern',
                           'type': 'Offhand',
                           'value': 0,
                           'stats': {'defense': 1, 'dodge': 1}
                           }]

        self.equipped_weapon = {'name': 'Short Bow',
                                'type': 'Weapon',
                                'value': 0,
                                'stats': {'attack': 1, 'critical': 2, 'dodge': 1}
                                }

        self.equipped_shield = {'name': 'Quiver',
                                'type': 'Offhand',
                                'value': 0,
                                'stats': {'critical': 3, 'dodge': 1}
                                }

        self.equipped_armor = {'name': 'Leather Armor',
                               'type': 'Armor',
                               'value': 0,
                               'stats': {'defense': 5, 'dodge': 5}
                               }
