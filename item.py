class Item:
    def __init__(self, name, item_type, value, stats):
        self.name = name
        self.type = item_type
        self.value = value
        self.stats = stats


item_list = {
    0: {'name': 'Health Potion',
        'type': 'Consumable',
        'value': 2,
        'stats': {'health': 10}
        },

    1: {'name': 'Lantern',
        'type': 'Offhand',
        'value': 0,
        'stats': {'defense': 1, 'dodge': 1}
        },

    2: {'name': 'Short Bow',
        'type': 'Weapon',
        'value': 2,
        'stats': {'attack': 1, 'critical': 2, 'dodge': 1}
        },
    3: {'name': 'Wand',
        'type': 'Weapon',
        'value': 0,
        'stats': {'attack': 5, 'critical': 5, 'dodge': 5}
        },
    4: {'name': 'Cloth Robe',
        'type': 'Armor',
        'value': 0,
        'stats': {'attack': 4, 'defense': 3, 'dodge': 2}
        },
    5: {'name': 'Quiver',
        'type': 'Offhand',
        'value': 0,
        'stats': {'critical': 3, 'dodge': 1}
        },
    6: {'name': 'Leather Armor',
        'type': 'Armor',
        'value': 0,
        'stats': {'defense': 5, 'dodge': 5}
        },
    7:
        {'name': 'Plate Armor',
         'type': 'Armor',
         'value': 0,
         'stats': {'defense': 5, 'dodge': 5}
         },
    8: {'name': 'Kite Shield',
        'type': 'Offhand',
        'value': 0,
        'stats': {'defense': 5, 'dodge': 5}
        },
    9: {'name': 'Kite Shield',
        'type': 'Offhand',
        'value': 0,
        'stats': {'defense': 5, 'dodge': 5}
        }
}
