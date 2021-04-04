from discord.ext import commands
from settings import PREFIX, TOKEN
from hero import *
from enemy import Enemy
import random
import asyncio

bot = commands.Bot(command_prefix=PREFIX, case_insensitive=True)


async def adventure(hero):
    dice = random.randint(0, 100)
    if dice <= 90:
        enemy = Enemy.create_enemy(hero)
        await battle(hero, enemy)

    elif 90 < dice <= 100:
        message = hero.get_item()
        await hero.ctx.send(message, delete_after=5)
        await hero_info(hero)


async def battle(hero, enemy):
    hero.battle = True
    msg = f"```[ BATTLE ]\n" \
          f"{hero.name}\tvs\t{enemy.name}\n" \
          f"Lvl {hero.lvl}\t\t\tLvl {enemy.lvl}\n" \
          f"HP {hero.hp}/{hero.max_hp}\t\t HP {enemy.hp}/{enemy.max_hp}\n\n" \
          f"Choose your action.```"

    msg_reactions = {'🗡️': 'attack', '🏃': 'flee', '🎲': 'dice'}
    reaction, user = await show_msg(hero, msg, msg_reactions)

    if str(reaction) == '🗡️':
        hero_attack = Hero.attack(hero, enemy)
        if Enemy.enemy_died(enemy, hero):
            xp, gold = Enemy.enemy_died(enemy, hero)
            await hero.ctx.send(f"```{hero_attack}\n"
                                f"{enemy.name} has been slain.\n\n"
                                f"You received {xp} experience and {gold} gold.```", delete_after=5)

            if hero.get_level():
                await hero.ctx.send(f"```You gained a level.```", delete_after=5)

            await hero_info(hero)
        else:
            enemy_attack = Enemy.enemy_attack(enemy, hero)

            if hero.hp <= 0:
                await hero.ctx.send(f'```[ DEATH ]\nYou have been slain by {enemy.name}.```', delete_after=5)
                await asyncio.sleep(3)
                await game(hero.ctx)

            await hero.ctx.send(f"```{hero_attack}\n{enemy_attack}```", delete_after=5)

        await battle(hero, enemy)

    elif str(reaction) == '🏃':
        message = Hero.flee(hero)
        await hero.ctx.send(message, delete_after=5)
        if hero.flee:
            await battle(hero, enemy)
        else:
            hero.flee = False
            await hero_info(hero)

    elif str(reaction) == '🎲':
        if random.randint(0, 1) == 0:
            hero.heal(hero.max_hp)
            await hero.ctx.send(f"```You have been restored by the gods.```", delete_after=6)
            await battle(hero, enemy)
        else:
            await hero.ctx.send(f"```[ DEATH ]\nYou have been slain by the gods.```", delete_after=6)
            await asyncio.sleep(3)
            await game(hero.ctx)


async def hero_info(hero):
    weapon, shield, armor = hero.get_equipped_items()
    hero.equip_gear()
    if hero.battle:
        hero.battle = False
        amount = hero.heal(hero.lvl * 5)
        await hero.ctx.send(f"```You have been healed for {amount} health.```", delete_after=5)

    msg = f"```[ {hero.name.upper()} ]\nLvl {hero.lvl} {hero.type}\n\n"                                     \
          f"Health: {hero.hp: >4}{'Mana:': >10} {hero.mana: >7}\n"                                          \
          f"Defense: {hero.defense:>3} {'Dodge:': >10} {hero.dodge: >6}\n"                                  \
          f"Attack: {hero.attack: >4} {'Critical:': >13} {hero.critical: >3}\n\n"                           \
          f"Gold: {hero.gold: >6}{'Exp:': >9} {hero.xp: >5}/{hero.next_lvl}\n\n"                            \
          f"[ GEAR ]\n"                                                                                     \
          f"{weapon}\n"                                                                                     \
          f"{shield}\n"                                                                                     \
          f"{armor}\n\n"                                                                                    \
          f"[ INVENTORY ]\n"                                                                                \
          f"{hero.get_inventory()}\n\n"                                                                     \
          f"Please choose your action.```"

    msg_reactions = {'🗺️': 'adventure', '🔨': 'repair', '💰': 'sell'}
    reaction, user = await show_msg(hero, msg, msg_reactions)

    if str(reaction) == '🗺️':
        await adventure(hero)


    elif str(reaction) == '🔨':
        await hero.ctx.send('```Feature not ready yet.```', delete_after=5)
        await hero_info(hero)

    elif str(reaction) == '💰':
        await hero.ctx.send('```Feature not ready yet.```', delete_after=5)
        await vendor(hero)


async def vendor(hero):
    msg = f"[ VENDOR ]\nHere you can sell your items."
    msg_reactions = {'🗺️': 'adventure', '🔨': 'repair', '💰': 'sell'}
    reaction, user = await show_msg(hero, msg, msg_reactions)
    return reaction, user


async def show_msg(hero, msg, msg_reactions):
    msg = await hero.ctx.send(msg)
    for reaction in msg_reactions:
        await msg.add_reaction(reaction)

    def get_reaction(_reaction, _user):
        return _user == hero.ctx.author and str(_reaction.emoji) in msg_reactions

    reaction, user = await bot.wait_for('reaction_add', check=get_reaction)
    await reaction.message.delete()

    return reaction, user


@bot.command(aliases=['g'])
async def game(ctx):
    msg = await ctx.send("```[ PyQuest ]\nWelcome to PyQuest\n\nPlease choose your hero.```")
    msg_reactions = {'🛡️': 'Warrior', '🪄': 'Wizard', '🏹': 'Ranger'}
    for reaction in msg_reactions:
        await msg.add_reaction(reaction)

    reaction, user = await bot.wait_for('reaction_add', check=lambda x, y: str(x) in msg_reactions and y == ctx.author)
    await msg.delete()

    if str(reaction) == '🛡️':
        hero = Warrior(ctx, user.name, msg_reactions[str(reaction)])
    elif str(reaction) == '🪄':
        hero = Wizard(ctx, user.name, msg_reactions[str(reaction)])
    else:
        hero = Ranger(ctx, user.name, msg_reactions[str(reaction)])

    await hero_info(hero)


@bot.event
async def on_ready():
    print("Logged in as", bot.user)


bot.run(TOKEN)
