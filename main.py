from discord.ext import commands
from settings import PREFIX, TOKEN
from hero import Warrior, Wizard, Ranger
from enemy import Enemy
from item import random_item_list
import random
import asyncio

bot = commands.Bot(command_prefix=PREFIX, case_insensitive=True)


async def adventure(hero):
    """
    Main adventure loop. Random to see what kind of adventure. Battle, riddle, item?
    """
    dice = random.randint(0, 100)
    if dice <= 90:
        enemy = Enemy(hero)
        enemy.set_enemy_lvl(hero)
        await battle(hero, enemy)

    elif 90 < dice <= 100:
        message = hero.get_item()
        await hero.ctx.send(message, delete_after=5)
        await hero_info(hero)


async def hero_info(hero):
    """
    Character info screen. Displays data about our character.
    """
    hero.cur_hp = hero.base_hp
    weapon, offhand, armor = hero.get_equipped_items()
    hero.set_equipped_stats()
    inventory = hero.get_inventory_items()

    msg = f"```css\n[ {hero.name} ]\nLvl {hero.lvl} {hero.type}\n\n" \
          f"Health: {hero.cur_hp: >4}{'Mana:': >10} {hero.cur_mana: >7}\n" \
          f"Defense: {hero.defense:>3} {'Dodge:': >10} {hero.dodge: >6}\n" \
          f"Attack: {hero.attack: >4} {'Critical:': >13} {hero.critical: >3}\n\n" \
          f"Gold: {hero.gold: >6}{'Exp:': >9} {hero.xp: >5}/{hero.next_lvl}\n\n" \
          f"[ GEAR ]\n{weapon}\n{offhand}\n{armor}\n\n" \
          f"[ INVENTORY ]\n{inventory}\n\n" \
          f"Please choose your action.```"

    msg_reactions = {'🗺️': 'adventure', '💰': 'sell'}
    msg_reactions, item_reactions = hero.set_item_reactions(msg_reactions)

    reaction, user = await get_reaction(hero, msg, msg_reactions)


    if str(reaction) == '🗺️':
        await adventure(hero)

    elif str(reaction) == '💰':
        await vendor(hero)

    for i, v in enumerate(item_reactions.values()):
        if str(reaction) == v:
            message = hero.equip_item(hero.inventory[i], i)
            await hero.ctx.send(message, delete_after=5)

    await hero_info(hero)


async def battle(hero, enemy):
    """
    Battle loop. 1 round per iteration, check input and calculate outcome.
    """
    hero.battle = True
    msg = f"```css\n[ BATTLE ]\n" \
          f"{hero.name: <12}{'vs': <7}{enemy.name}\n" \
          f"Lvl {hero.lvl: <15}Lvl {enemy.lvl}\n" \
          f"HP{hero.cur_hp: >3}/{hero.max_hp: <13}{'HP'}{enemy.cur_hp: >3}/{enemy.max_hp}\n" \
          f"MP{hero.cur_mana: >3}/{hero.max_mana: <13}{'MP'}{enemy.cur_mana: >3}/{enemy.max_mana}\n\n" \
          f"Choose your action.```"

    msg_reactions = {'🗡️': 'attack'}
    for value in hero.inventory:
        if value['name'] == 'Health Potion':
            msg_reactions['❤️'] = 'Health Potion'

        elif value['name'] == 'Mana Potion':
            msg_reactions['⚗️'] = 'Mana Potion'

    msg_reactions['🏃'] = 'flee'
    msg_reactions['🎲'] = 'dice'

    reaction, user = await get_reaction(hero, msg, msg_reactions)

    if str(reaction) == '🗡️':
        hero_attack = hero.hero_attack(enemy)
        if Enemy.enemy_died(enemy, hero):
            xp, gold = Enemy.enemy_died(enemy, hero)
            await hero.ctx.send(f"```{hero_attack}\n"
                                f"{enemy.name} has been slain.\n\n"
                                f"You received {xp} experience and {gold} gold.```", delete_after=5)

            if hero.get_level():
                await hero.ctx.send(f"```You gained a level.```", delete_after=5)

            if random.randint(0, 100) > 90:
                message = hero.get_item()
                await hero.ctx.send(message, delete_after=5)

            await hero_info(hero)
        else:
            enemy_attack = Enemy.enemy_attack(enemy, hero)

            await hero.ctx.send(f"```{hero_attack}\n{enemy_attack}```", delete_after=5)

            if hero.cur_hp <= 0:
                await hero.ctx.send(f'```css\n[ DEATH ]\nYou have been slain by {enemy.name}.```', delete_after=5)
                await asyncio.sleep(3)
                await game(hero.ctx)

        await battle(hero, enemy)


    elif str(reaction) == '🏃':
        message = hero.hero_flee()
        await hero.ctx.send(message, delete_after=5)
        if hero.flee:
            await battle(hero, enemy)
        else:
            hero.flee = False
            await hero_info(hero)

    elif str(reaction) == '🎲':
        if random.random() < 1 / 3:
            hero.cur_hp = hero.max_hp
            await hero.ctx.send(f"```You have been restored by the gods.```", delete_after=6)
            await battle(hero, enemy)
        else:
            await hero.ctx.send(f"```css\n[ DEATH ]\nYou have been slain by the gods.```", delete_after=6)
            await asyncio.sleep(3)
            await game(hero.ctx)

    for i, v in enumerate(msg_reactions):
        if str(reaction) == v:
            message = hero.use_item(hero.inventory[i - 2], i - 2)
            await hero.ctx.send(message, delete_after=5)
            await battle(hero, enemy)


async def vendor(hero):
    """
    A vendor for buying potions and selling gear.
    """
    msg_reactions, item_reactions = hero.set_vendor_reactions()

    msg = f"```css\n[ VENDOR ]\nBuy or sell items.\n\n"
    for key, val in msg_reactions.items():
        msg += f"{key} {val} \n"

    msg += f"\nGold: {hero.gold}\n\n[ INVENTORY ]\n{hero.get_inventory_items()}\n" \
           f"What would you like to do?\n\n```"

    reaction, user = await get_reaction(hero, msg, msg_reactions)

    if str(reaction) == '🗺️':
        await hero_info(hero)

    # TODO
    elif str(reaction) == '❤️':
        message = hero.buy_item(random_item_list[0])
        await hero.ctx.send(message, delete_after=5)
        await vendor(hero)


    elif str(reaction) == '⚗️':
        message = hero.buy_item(random_item_list[1])
        await hero.ctx.send(message, delete_after=5)
        await vendor(hero)

    for i, k in enumerate(item_reactions.values()):
        if str(reaction) == k:
            message = hero.sell_item(i)

            await hero.ctx.send(message, delete_after=5)

            await vendor(hero)

    return reaction, user


async def get_reaction(hero, msg, msg_reactions):
    """
    A function for adding reactions to a game message, and handle input from player.
    """
    msg = await hero.ctx.send(msg)
    for reaction in msg_reactions:
        await msg.add_reaction(reaction)

    def check_reaction(_reaction, _user):
        return _user == hero.ctx.author and str(_reaction.emoji) in msg_reactions

    reaction, user = await bot.wait_for('reaction_add', check=check_reaction)
    await reaction.message.delete()

    return reaction, user


@bot.command(aliases=['g'])
async def game(ctx):
    """
    Create a new game.
    Store data from context as a Hero class. (Warrior, Ranger, Wizard)
    """
    msg = await ctx.send("```css\n[ PyQuest ]\nWelcome to PyQuest\n\nPlease choose your hero.```")
    msg_reactions = {'🛡️': 'Warrior', '🏹': 'Ranger', '🧙‍♂️': 'Wizard'}
    for reaction in msg_reactions:
        await msg.add_reaction(reaction)

    reaction, user = await bot.wait_for('reaction_add', check=lambda x, y: str(x) in msg_reactions and y == ctx.author)
    await msg.delete()

    if str(reaction) == '🛡️':
        hero = Warrior(ctx)
    elif str(reaction) == '🏹':
        hero = Ranger(ctx)
    else:
        hero = Wizard(ctx)

    await hero_info(hero)


@bot.event
async def on_ready():
    print("Logged in as", bot.user)


bot.run(TOKEN)
