import random
from item import random_item_list


class Hero:
    def __init__(self, ctx):
        self.ctx = ctx
        self.xp = 0
        self.lvl = 1
        self.next_lvl = 12
        self.gold = 10
        self.battle = False
        self.flee = False

        self.max_hp = 0
        self.max_mana = 0
        self.cur_hp = 0
        self.cur_mana = 0
        self.base_hp = 0
        self.base_mana = 0
        self.base_atk = 0
        self.base_def = 0
        self.base_dodge = 0
        self.base_crit = 0

        self.attack = 0
        self.defense = 0
        self.dodge = 0
        self.critical = 0

        self.inventory = [random_item_list[2], random_item_list[4], random_item_list[5]]

        self.equipped_weapon = {}
        self.equipped_offhand = {}
        self.equipped_armor = {}

    def hero_attack(self, enemy):
        # Calculate damage
        hero_damage = random.randint(0, int(4 + ((self.lvl + self.attack) - (enemy.lvl + enemy.defense))))

        hero_attack = {0: f"You miss {enemy.name}.",
                       1: f"You attack {enemy.name} for {hero_damage} point of damage.",
                       2: f"You attack {enemy.name} for {hero_damage} points of damage."}

        # Check for dodge
        if random.randint(0, self.attack - enemy.defense) == 0:
            hero_attack = {0: f"{enemy.name} dodged your attack."}
            hero_damage = 0

        for k, v in hero_attack.items():
            if hero_damage >= k:
                hero_attack = v

                if random.randint(0, 50 - self.attack) == 0:
                    hero_damage *= int(1.5)
                    hero_attack = f"You crunch {enemy.name} for {hero_damage} points of damage. (CRITICAL)"

        enemy.cur_hp -= hero_damage

        return hero_attack

    def hero_flee(self):
        if self.flee:
            message = "```You may only flee once.```"
        elif random.random() < 1 / 3:
            message = "```You managed to escape.```"
            self.battle = False
            self.flee = False
        else:
            message = "```You failed to escape.```"
            self.flee = True
        return message

    def get_level(self):
        if self.xp > self.next_lvl:
            self.lvl += 1
            self.xp -= self.next_lvl
            self.next_lvl *= self.lvl

            self.base_hp = int(self.max_hp + self.lvl * 1.5)
            self.base_mana = int(self.max_mana + (1.5 * self.base_mana))

            self.base_atk += int(self.base_atk * 0.2)
            self.base_def += int(self.base_atk * 0.2)
            self.base_dodge += int(self.base_dodge * 0.2)
            self.base_crit += int(self.base_crit * 0.2)

            self.cur_hp = self.max_hp
            self.cur_mana = self.max_mana
            return True

    def get_item(self):
        if len(self.inventory) < 3:
            item = random.choice(random_item_list)
            self.inventory.append(item)
            return f"```You found a {item['name']}.```"
        return "```Your inventory is full.```"

    def sell_item(self, item):
        for i, d in enumerate(self.inventory):
            if i == item:
                del self.inventory[item]
                self.gold += d['value']
                return f"```You sold {d['name']} for {d['value']} gold.```"

    def buy_item(self, item):
        if self.gold >= item['value']:
            if len(self.inventory) < 3:
                self.inventory.append(item)
                self.gold -= item['value']
            else:
                return f"```Your inventory is full.```"
            return f"```You bought {item['name']} for {item['value']} gold.```"
        return f"```You can't afford {item['name']}.```"

    def equip_item(self, item, i):
        message = f"```You equipped {item['name']}```"

        if item['type'] == 'Consumable':
            return "```You can't equip a potion. Try using it in a fight.```"

        elif item['type'] == 'Weapon':
            del self.inventory[i]
            self.inventory.append(self.equipped_weapon)
            self.equipped_weapon = item

        elif item['type'] == 'Offhand':
            del self.inventory[i]
            self.inventory.append(self.equipped_offhand)
            self.equipped_offhand = item

        elif item['type'] == 'Armor':
            del self.inventory[i]
            self.inventory.append(self.equipped_armor)
            self.equipped_armor = item

        return message

    def use_item(self, item, i):
        if item['name'] == 'Health Potion':
            self.cur_hp += item['stats']['health']
            if self.cur_hp > self.max_hp:
                self.cur_hp = self.max_hp
            del self.inventory[i]

            return f"```You regained {item['stats']['health']} points of health.```"

        if item['name'] == 'Mana Potion':
            self.cur_mana += item['stats']['mana']
            if self.cur_mana > self.max_mana:
                self.cur_mana = self.max_mana
            del self.inventory[i]

            return f"```You regained {item['stats']['mana']} points of mana.```"

    def set_item_reactions(self, msg_reactions):
        item_reactions = {0: '????', 1: '????', 2: '????', 3: '????'}
        for i, item in enumerate(self.inventory):
            msg_reactions[item_reactions[i]] = item['name']

        return msg_reactions, item_reactions

    def set_vendor_reactions(self):
        msg_reactions = {'???????': 'Continue adventure', '??????': 'Buy Health Potion', '??????': 'Buy Mana Potion'}
        vendor_reactions = {0: '????', 1: '????', 2: '????', 3: '????'}
        for i, item in enumerate(self.inventory):
            msg_reactions[vendor_reactions[i]] = f"Sell {item['name']}"

        return msg_reactions, vendor_reactions

    def get_inventory_items(self):
        stats = {'attack': ' ???????', 'defense': ' ????', 'critical': ' ????', 'dodge': ' ??????????', 'health': ' ??????',
                 'mana': ' ??????'}
        inventory = ""
        for i, item in enumerate(self.inventory):
            inventory += f"{i + 1}. {item['name']: <13}"
            for k, v in item['stats'].items():
                inventory += stats[k] + str(v)
            inventory += "\n"

        return inventory

    def get_equipped_items(self):
        stats = {'attack': ' ???????', 'defense': ' ????', 'critical': ' ????', 'dodge': ' ??????????'}
        weapon = f"{self.equipped_weapon['name']: <16}"
        for k, v in self.equipped_weapon['stats'].items():
            weapon += stats[k] + str(v)

        offhand = f"{self.equipped_offhand['name']: <16}"
        for k, v in self.equipped_offhand['stats'].items():
            offhand += stats[k] + str(v)

        armor = f"{self.equipped_armor['name']: <16}"
        for k, v in self.equipped_armor['stats'].items():
            armor += stats[k] + str(v)

        return weapon, offhand, armor

    def set_base_stats(self):
        self.max_hp = self.base_hp
        self.max_mana = self.base_mana
        self.attack = self.base_atk
        self.defense = self.base_def
        self.dodge = self.base_dodge
        self.critical = self.base_crit

    def set_equipped_stats(self):
        self.set_base_stats()
        for d in self.equipped_weapon['stats'], self.equipped_armor['stats'], self.equipped_offhand['stats']:
            for k, v in d.items():
                setattr(self, k, getattr(self, k) + v)


class Warrior(Hero):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.name = ctx.author.name
        self.lvl = 1
        self.type = 'Warrior'
        self.base_hp = 15
        self.base_mana = 0
        self.cur_hp = self.base_hp
        self.cur_mana = self.base_mana
        self.base_atk = 5
        self.base_def = 10
        self.base_dodge = 5
        self.base_crit = 10

        self.equipped_weapon = random_item_list[9]
        self.equipped_offhand = random_item_list[8]
        self.equipped_armor = random_item_list[7]


class Ranger(Hero):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.name = ctx.author.name
        self.type = 'Ranger'
        self.base_hp = 12
        self.base_mana = 5
        self.cur_hp = self.base_hp
        self.cur_mana = self.base_mana
        self.base_atk = 8
        self.base_def = 7
        self.base_dodge = 5
        self.base_crit = 10

        self.equipped_weapon = random_item_list[2]
        self.equipped_offhand = random_item_list[5]
        self.equipped_armor = random_item_list[6]


class Wizard(Hero):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.name = ctx.author.name
        self.type = 'Wizard'
        self.base_hp = 10
        self.base_mana = 10
        self.cur_hp = self.base_hp
        self.cur_mana = self.base_mana
        self.base_atk = 6
        self.base_def = 3
        self.base_dodge = 5
        self.base_crit = 7

        self.equipped_weapon = random_item_list[3]
        self.equipped_offhand = random_item_list[10]
        self.equipped_armor = random_item_list[4]
