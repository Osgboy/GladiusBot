#!~/bot-env/Scripts/python.exe
import discord
import os
from typing import Type, Callable
from item import *
from unit import *
from weapon import *
from trait import *
from action import *
from dotenv import load_dotenv
from discord.ext import commands
# import cProfile, pstats, io
# from pstats import SortKey
# pr = cProfile.Profile(timeunit=0.001)
# pr.enable()
# pr.disable()
# s = io.StringIO()
# sortby = SortKey.CUMULATIVE
# ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
# ps.print_stats()
# with open('cprofile.txt', 'w') as fout:
#     fout.write(s.getvalue())

load_dotenv()
TOKEN = os.getenv("TEST_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='$', intents=intents)


RARITY_COLORS = {'Common': discord.colour.Color.from_rgb(255, 255, 255),
                 'Uncommon': discord.colour.Color.from_rgb(0, 191, 191),
                 'Artefact': discord.colour.Color.from_rgb(191, 0, 191),
                 'Rare': discord.colour.Color.from_rgb(191, 0, 191)}
GLADIUS_FACTION_COLORS = {'AdeptusMechanicus': discord.colour.Color.from_rgb(159, 38, 40),
                          'AstraMilitarum': discord.colour.Color.from_rgb(50, 73, 53),
                          'ChaosSpaceMarines': discord.colour.Color.from_rgb(57, 75, 87),
                          'Drukhari': discord.colour.Color.from_rgb(15, 69, 78),
                          'Eldar': discord.colour.Color.from_rgb(52, 115, 121),
                          'Necrons': discord.colour.Color.from_rgb(4, 83, 42),
                          'Neutral': discord.colour.Color.from_rgb(255, 255, 255),
                          'Orks': discord.colour.Color.from_rgb(70, 91, 24),
                          'SistersOfBattle': discord.colour.Color.from_rgb(87, 12, 12),
                          'SpaceMarines': discord.colour.Color.from_rgb(75, 98, 98),
                          'Tau': discord.colour.Color.from_rgb(46, 90, 106),
                          'Tyranids': discord.colour.Color.from_rgb(99, 37, 103)}
ZEPHON_BRANCH_COLORS = {'Cyber': discord.colour.Color.from_rgb(16, 121, 130),
                        'Human': discord.colour.Color.from_rgb(154, 129, 35),
                        'Voice': discord.colour.Color.from_rgb(123, 65, 150),
                        'Zephon': discord.colour.Color.from_rgb(205, 59, 66),
                        'Reaver': discord.colour.Color.from_rgb(138, 97, 70),
                        'Acrin': discord.colour.Color.from_rgb(62, 192, 158),
                        'Neutral': discord.colour.Color.from_rgb(255, 255, 255)}
GLADIUS_ICONS = {'biomass': '<:Biomass:1240218802831233118>', 'requisitions': '<:Requisitions:1240222555588268032>',
                 'food': '<:Food:1240218818660532317>', 'ore': '<:Ore:1240218839644377181>',
                 'energy': '<:Energy:1240221846343782501>', 'influence': '<:Influence:1240218825836728341>',
                 'production': '<:Production:1240330971514011668>',

                 'armor': '<:Armor:1240218799832174703>', 'hitpoints': '<:Hitpoints:1240330759781482528>',
                 'morale': '<:Morale:1240218836171493386>', 'movement': '<:Movement:1240222322770579487>',
                 'cargoSlots': '<:CargoSlots:1240218804982775848>', 'itemSlots': '<:ItemSlots:1240218829280378912>',

                 'damage': '<:Damage:1240218813123919893>', 'attacks': '<:Attacks:1240218801799434241>',
                 'armorPenetration': '<:ArmorPenetration:1240218800855715840>', 'accuracy': '<:Accuracy:1240218797458063361>',
                 'range': '<:Range:1240218850763477013>',

                 'actions': '<:Actions:1240218798532071515>', 'cooldown': '<:Cooldown:1240218808224972800>',
                 'transport': '<:Transport:1256002013037203587>'}
ZEPHON_ICONS = {'food': '<:Food:1250986007537647687>', 'minerals': '<:Minerals:1250986099023806464>',
                'energy': '<:Energy:1250985795242954764>', 'influence': '<:Influence:1250986095739404339>',
                'algae': '<:Algae:1250981089540046929>', 'chips': '<:Chips:1250985791455494174>',
                'antimatter': '<:Antimatter:1250981090278117416>', 'dimensionalEchoes': '<:DimensionalEchoes:1250985794450227240>',
                'singularityCores': '<:SingularityCores:1250986245085986909>', 'transuranium': '<:Transuranium:1250986247086669937>',
                'production': '<:Production:1250986164626657383>',

                'groupSize': '<:GroupSize:1250986008606933012>',
                'armor': '<:Armor:1250981091125362788>', 'hitpoints': '<:Hitpoints:1250986009429282866>',
                'morale': '<:Morale:1250986099816530033>', 'movement': '<:Movement:1250986100621836400>',
                'cargoSlots': '<:CargoSlots:1250981096070582273>', 'itemSlots': '<:ItemSlots:1250986096616017961>',

                'damage': '<:Damage:1250985792197628004>', 'attacks': '<:Attacks:1250981093314662411>',
                'armorPenetration': '<:ArmorPenetration:1250981091917955193>', 'accuracy': '<:Accuracy:1250981087954468914>',
                'range': '<:Range:1250986241604849664>',

                'actions': '<:Actions:1250981088701186128>', 'turns': '<:Turns:1250986247896305776>',
                'transport': '<:Transport:1256002285536804936>'}
GLADIUS_RESOURCES = ('biomass', 'requisitions', 'food',
                     'ore', 'energy', 'influence')
ZEPHON_RESOURCES = ('food', 'minerals', 'energy', 'transuranium', 'antimatter',
                    'dimensionalEchoes', 'singularityCores', 'algae', 'chips', 'influence')


def camel_case_split(s: str) -> str:
    # use map to add an underscore before each uppercase letter
    modified_string = list(map(lambda x: '_' + x if x.isupper() else x, s))
    # join the modified string and split it at the underscores
    split_string = ''.join(modified_string).split('_')
    # remove any empty strings from the list
    # split_string = list(filter(lambda x: x != '', split_string))
    split_string = ' '.join(split_string)
    return split_string


class NotFoundError(Exception):
    def __init__(self, bestMatch: str):
        self.bestMatch = bestMatch


class UnitNotFoundError(Exception):
    def __init__(self, bestMatch: str):
        self.bestMatch = bestMatch


class ConfirmFuzzyMatch(discord.ui.View):
    def __init__(self, name, verbose, objCls, embedFunc, unitName):
        super().__init__(timeout=60)
        self.name = name
        self.verbose = verbose
        self.objCls = objCls
        self.embedFunc = embedFunc
        self.unitName = unitName

    @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed, fullIconPath = match_and_create_embed(
                self.name, self.verbose, self.objCls, self.embedFunc, self.unitName)
        except UnitNotFoundError as unf:
            await interaction.response.edit_message(content=f'**{self.unitName}** not found. Did you mean **{unf.bestMatch}**?')
            self.unitName = unf.bestMatch
            print(repr(unf))
        except ActionNotInUnitError as na:
            await interaction.response.edit_message(content=f'No **{na.actionName}** action found in list of actions for **{na.unitName}**.', view=None)
            print(repr(na))
        else:
            try:
                image = discord.File(fullIconPath, filename='icon.png')
                embed.set_thumbnail(url="attachment://icon.png")
                await interaction.response.edit_message(content=None, embed=embed, attachments=[image], view=None)
                print('Successfully returned request after editing.')
            except FileNotFoundError:
                await interaction.response.edit_message(content=None, embed=embed, view=None)
                print('Successfully returned request without icon after editing.')


def match_and_create_embed(name: str, verbose: bool, objCls: Type[Obj],
                           embedFunc: Callable[[Obj, bool, str], discord.Embed], unitName: str) -> tuple[discord.Embed, str]:
    obj = objCls(name)
    obj.fuzzy_match_name(obj.get_obj_info)
    if not obj.found:
        raise NotFoundError(obj.bestMatch)

    # Get embed
    embed = embedFunc(obj, verbose, unitName)

    # Get full icon path
    obj.get_icon_path()
    try:
        if not (internalPath := obj.iconPath):
            raise AttributeError
    except AttributeError:
        try:
            internalPath = os.path.join(obj.OBJ_CLASS, obj.factionAndID)
        except AttributeError:
            internalPath = os.path.join(obj.OBJ_CLASS, obj.internalID)
    fullIconPath = os.path.join(
        os.getcwd(), obj.GAME, 'Icons', internalPath + '.png')

    return embed, fullIconPath


async def return_info(interaction: discord.Interaction, name: str, verbose: bool, invisible: bool, objCls: Type[Obj],
                      embedFunc: Callable[[Obj, bool, str], discord.Embed], unitName: str = None):
    print(f'\nReceived request for:\n'
          f'- Obj Class: {objCls.__name__}\n'
          f'- Name: {name}\n'
          f'- Unit Name: {unitName}\n')
    try:
        embed, fullIconPath = match_and_create_embed(
            name, verbose, objCls, embedFunc, unitName)
    except NotFoundError as nf:
        await interaction.response.send_message(f'**{name}** not found. Did you mean **{nf.bestMatch}**?', ephemeral=invisible,
                                                view=ConfirmFuzzyMatch(nf.bestMatch, verbose, objCls, embedFunc, unitName))
        print(repr(nf))
    except UnitNotFoundError as unf:
        await interaction.response.send_message(f'**{unitName}** not found. Did you mean **{unf.bestMatch}**?', ephemeral=invisible,
                                                view=ConfirmFuzzyMatch(name, verbose, objCls, embedFunc, unf.bestMatch))
        print(repr(unf))
    except ActionNotInUnitError as na:
        await interaction.response.send_message(f'No **{na.actionName}** action found in list of actions for **{na.unitName}**.', ephemeral=invisible)
        print(repr(na))
    else:
        try:
            image = discord.File(fullIconPath, filename='icon.png')
            embed.set_thumbnail(url="attachment://icon.png")
            await interaction.response.send_message(embed=embed, file=image, ephemeral=invisible)
            print('Successfully returned request.')
        except FileNotFoundError:
            await interaction.response.send_message(embed=embed, ephemeral=invisible)
            print('Successfully returned request without icon.')


def create_gitem_embed(item: GItem, verbose: bool, _) -> discord.Embed:
    item.get_ability()
    item.get_rarity()
    item.get_influence_cost()

    # Name and Description
    embed = discord.Embed(title=item.name, description=item.description)

    # Color
    embed.colour = RARITY_COLORS[item.rarity]

    # Rarity
    embed.add_field(name='Rarity', value=item.rarity)

    # Influence cost
    embed.add_field(
        name='Cost', value=GLADIUS_ICONS['influence'] + ' ' + item.influenceCost)

    # Ability
    try:
        embed.add_field(
            name='Ability', value=item.ability[:1024], inline=False)
    except AttributeError:
        pass

    # Flavor
    if verbose:
        try:
            embed.add_field(
                name='Flavor', value=f'*{item.flavor}*', inline=False)
        except AttributeError:
            pass

    return embed


def create_zitem_embed(item: ZItem, verbose: bool, _) -> discord.Embed:
    item.get_branch()
    item.get_ability()
    item.get_rarity()
    item.get_influence_cost()
    item.get_buy_condition()

    # Name and Description
    try:
        embed = discord.Embed(title=item.name, description=item.description)
    except AttributeError:
        embed = discord.Embed(title=item.name)

    # Color
    embed.colour = RARITY_COLORS[item.rarity]

    # Rarity
    embed.add_field(name='Rarity', value=item.rarity)

    # Branch
    embed.add_field(name='Branch', value=item.branch)

    # Influence cost
    embed.add_field(
        name='Cost', value=ZEPHON_ICONS['influence'] + ' ' + item.influenceCost)

    # Buy condition
    try:
        embed.add_field(name='Prerequisite', value=item.buyCondition)
    except AttributeError:
        pass

    # Ability
    try:
        embed.add_field(
            name='Ability', value=item.ability[:1024], inline=False)
    except AttributeError:
        pass

    # Flavor
    if verbose:
        try:
            embed.add_field(
                name='Flavor', value=f'*{item.flavor}*', inline=False)
        except AttributeError:
            pass

    return embed


def create_gunit_embed(unit: GUnit, verbose: bool, _) -> discord.Embed:
    unit.get_stats()
    unit.get_group_size()
    unit.get_weapons()
    unit.get_traits()
    unit.get_actions()

    # Name and Description
    try:
        embed = discord.Embed(title=unit.name, description=unit.description)
    except AttributeError:
        embed = discord.Embed(title=unit.name)

    # Color
    embed.colour = GLADIUS_FACTION_COLORS[unit.faction]

    # Faction
    embed.add_field(name='Faction', value=camel_case_split(
        unit.faction), inline=False)

    # Cost
    costText = [GLADIUS_ICONS['production'],
                ' ', unit.resourceStats.productionCost]
    for resource in GLADIUS_RESOURCES:
        cost = resource + 'Cost'
        costValue = getattr(unit.resourceStats, cost)
        if costValue != '0':
            costText.extend((' | ', GLADIUS_ICONS[resource], ' ', costValue))
    embed.add_field(name="Cost", value=''.join(costText))

    # Upkeep
    upkeepText = []
    for resource in GLADIUS_RESOURCES:
        upkeep = resource + 'Upkeep'
        upkeepValue = getattr(unit.resourceStats, upkeep)
        if upkeepValue != '0':
            upkeepText.extend(
                (' | ', GLADIUS_ICONS[resource], ' ', upkeepValue))
    try:
        # delete initial ' | '
        del upkeepText[0]
    except IndexError:
        pass
    if upkeepText == []:
        upkeepText = ['None']
    embed.add_field(name='Upkeep', value=''.join(upkeepText))

    # Stats
    statText = (f"**{unit.combatStats.groupSizeMax} model(s)**\n"
                f"{GLADIUS_ICONS['armor']} {unit.combatStats.armor} | {GLADIUS_ICONS['hitpoints']} {round(unit.combatStats.hitpointsMax)} | "
                f"{GLADIUS_ICONS['morale']} {unit.combatStats.moraleMax}\n {GLADIUS_ICONS['movement']} {unit.combatStats.movementMax} | "
                f"{GLADIUS_ICONS['cargoSlots']} {unit.combatStats.cargoSlots} | {GLADIUS_ICONS['itemSlots']} {unit.combatStats.itemSlots}")
    embed.add_field(name='Stats', value=statText)

    # Weapons
    weaponsText = []
    for weapon in unit.weapons:
        # if upgrade required
        if unit.weapons[weapon]['requiredUpgrade']:
            upgrade = ' (U)'
        else:
            upgrade = ''
        # if weapon is secondary
        if unit.weapons[weapon]['secondary']:
            secondary = ' (S)'
        else:
            secondary = ''
        weaponsText.extend(
            f'{unit.weapons[weapon]["count"]}x {weapon}{upgrade}{secondary}\n')
    if weaponsText == []:
        weaponsText = ['None']
    embed.add_field(name='Weapons', value=''.join(weaponsText))

    # Traits
    traitsText = []
    for trait in unit.traits:
        # if upgrade required
        if unit.traits[trait]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        traitsText.extend((trait, upgrade, '\n'))
    if traitsText == []:
        traitsText = ['None']
    embed.add_field(name='Traits', value=''.join(traitsText))

    # Actions
    actionsText = []
    for action in unit.actions:
        # if upgrade required
        if unit.actions[action]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        actionsText.extend((action, upgrade, '\n'))
    if actionsText == []:
        actionsText = ['None']
    embed.add_field(name='Actions', value=''.join(actionsText))

    if verbose:
        # Flavor
        try:
            embed.add_field(
                name='Flavor', value=f'*{unit.flavor}*', inline=False)
        except AttributeError:
            pass
        embed.set_footer(text=('Traits/weapons marked with (U) require a researchable upgrade.\n'
                               'Weapons marked with (S) are secondary weapons.\n'
                               'Stat-changing traits like Fleet not taken into account.'))

    return embed


def create_zunit_embed(unit: ZUnit, verbose: bool, _) -> discord.Embed:
    unit.get_branch()
    unit.get_stats()
    unit.get_weapons()
    unit.get_traits()
    unit.get_actions()

    # Name and Description
    try:
        embed = discord.Embed(title=unit.name, description=unit.description)
    except AttributeError:
        embed = discord.Embed(title=unit.name)

    # Color
    embed.colour = ZEPHON_BRANCH_COLORS[unit.branch]

    # Branch
    embed.add_field(name='Branch', value=unit.branch, inline=False)

    # Cost
    costText = [ZEPHON_ICONS['production'],
                ' ', unit.resourceStats.productionCost]
    for resource in ZEPHON_RESOURCES:
        cost = resource + 'Cost'
        costValue = getattr(unit.resourceStats, cost)
        if costValue != '0':
            costText.extend((' | ', ZEPHON_ICONS[resource], ' ', costValue))
    embed.add_field(name="Cost", value=''.join(costText))

    # Upkeep
    upkeepText = []
    for resource in ZEPHON_RESOURCES:
        upkeep = resource + 'Upkeep'
        upkeepValue = getattr(unit.resourceStats, upkeep)
        if upkeepValue != '0':
            upkeepText.extend(
                (' | ', ZEPHON_ICONS[resource], ' ', upkeepValue))
    try:
        # delete initial ' | '
        del upkeepText[0]
    except IndexError:
        pass
    if upkeepText == []:
        upkeepText = ['None']
    embed.add_field(name='Upkeep', value=''.join(upkeepText))

    # Stats
    statText = (f"{ZEPHON_ICONS['groupSize']} {unit.combatStats.groupSizeMax} | {ZEPHON_ICONS['accuracy']} {unit.combatStats.accuracy}\n"
                f"{ZEPHON_ICONS['armor']} {unit.combatStats.armor} | {ZEPHON_ICONS['hitpoints']} {unit.combatStats.hitpointsMax} | "
                f"{ZEPHON_ICONS['morale']} {unit.combatStats.moraleMax}\n {ZEPHON_ICONS['movement']} {unit.combatStats.movementMax} | "
                f"{ZEPHON_ICONS['cargoSlots']} {unit.combatStats.cargoSlots} | {ZEPHON_ICONS['itemSlots']} {unit.combatStats.itemSlots}")
    embed.add_field(name='Stats', value=statText)

    # Weapons
    weaponsText = []
    for weapon in unit.weapons:
        # if upgrade required
        if unit.weapons[weapon]['requiredUpgrade']:
            upgrade = ' (U)'
        else:
            upgrade = ''
        # if weapon is secondary
        if unit.weapons[weapon]['secondary']:
            secondary = ' (S)'
        else:
            secondary = ''
        weaponsText.extend(
            f'{unit.weapons[weapon]["count"]}x {weapon}{upgrade}{secondary}\n')
    if weaponsText == []:
        weaponsText = ['None']
    embed.add_field(name='Weapons', value=''.join(weaponsText))

    # Traits
    traitsText = []
    for trait in unit.traits:
        # if upgrade required
        if unit.traits[trait]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        traitsText.extend((trait, upgrade, '\n'))
    if traitsText == []:
        traitsText = ['None']
    embed.add_field(name='Traits', value=''.join(traitsText))

    # Actions
    actionsText = []
    for action in unit.actions:
        # if upgrade required
        if unit.actions[action]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        actionsText.extend((action, upgrade, '\n'))
    if actionsText == []:
        actionsText = ['None']
    embed.add_field(name='Actions', value=''.join(actionsText))

    if verbose:
        # Flavor
        try:
            embed.add_field(
                name='Flavor', value=f'*{unit.flavor}*', inline=False)
        except AttributeError:
            pass
        embed.set_footer(text=('Traits/weapons marked with (U) require a researchable upgrade.\n'
                               'Weapons marked with (S) are secondary weapons.\n'
                               'Stat-changing traits like Fleet not taken into account.'))

    return embed


def create_gweapon_embed(weapon: GWeapon, verbose: bool, unitName: str = None) -> discord.Embed:
    if unitName:
        unit = GUnit(unitName)
        unit.fuzzy_match_name(unit.get_obj_min_info)
        if not unit.found:
            raise UnitNotFoundError(unit.bestMatch)
        unit.get_weapon_stats()
        weapon.unitStats = unit.weaponStats

    weapon.get_traits()
    weapon.get_range()
    weapon.get_innate_stats()
    weapon.calculate_final_stats()

    # Name and Description
    try:
        embed = discord.Embed(
            title=weapon.name, description=weapon.description)
    except AttributeError:
        embed = discord.Embed(title=weapon.name)

    # Wielder
    if unitName:
        embed.add_field(name='Wielder', value=unit.name, inline=False)

    # Stats
    statText = (f"{GLADIUS_ICONS['damage']} {weapon.finalStats.damage} | {GLADIUS_ICONS['attacks']} {weapon.finalStats.attacks} | "
                f"{GLADIUS_ICONS['armorPenetration']} {weapon.finalStats.armorPen} | {GLADIUS_ICONS['accuracy']} {weapon.finalStats.accuracy} | "
                f"{GLADIUS_ICONS['range']} {weapon.finalStats.range}")
    embed.add_field(name='Stats', value=statText)

    # Traits
    traitsText = []
    for trait in weapon.traits:
        # if upgrade required
        if weapon.traits[trait]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        traitsText.extend((trait, upgrade, '\n'))
    if traitsText == []:
        traitsText = ['None']
    embed.add_field(name='Traits', value=''.join(traitsText), inline=False)

    if verbose:
        # Flavor
        try:
            embed.add_field(
                name='Flavor', value=f'*{weapon.flavor}*', inline=False)
        except AttributeError:
            pass
        embed.set_footer(text=('Traits marked with (U) require a researchable upgrade.\n'
                               'Weapon stats depend on the unit wielding the weapon. Stat-changing traits like Twin-Linked not taken into account. '
                               'Values shown may not be accurate.'))

    return embed


def create_zweapon_embed(weapon: ZWeapon, verbose: bool, unitName: str = None) -> discord.Embed:
    if unitName:
        unit = ZUnit(unitName)
        unit.fuzzy_match_name(unit.get_obj_min_info)
        if not unit.found:
            raise UnitNotFoundError(unit.bestMatch)
        unit.get_accuracy()
        weapon.unitAccuracy = unit.combatStats.accuracy

    weapon.get_traits()
    weapon.get_range()
    weapon.get_innate_stats()
    weapon.calculate_final_stats()

    # Name and Description
    try:
        embed = discord.Embed(
            title=weapon.name, description=weapon.description)
    except AttributeError:
        embed = discord.Embed(title=weapon.name)

    # Wielder
    if unitName:
        embed.add_field(name='Wielder', value=unit.name, inline=False)

    # Stats
    statText = (f"{ZEPHON_ICONS['damage']} {weapon.finalStats.damage} | {ZEPHON_ICONS['attacks']} {weapon.finalStats.attacks} | "
                f"{ZEPHON_ICONS['armorPenetration']} {weapon.finalStats.armorPen} | {ZEPHON_ICONS['accuracy']} {weapon.finalStats.accuracy} | "
                f"{ZEPHON_ICONS['range']} {weapon.finalStats.range}")
    embed.add_field(name='Stats', value=statText)

    # Traits
    traitsText = []
    for trait in weapon.traits:
        # if upgrade required
        if weapon.traits[trait]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        traitsText.extend((trait, upgrade, '\n'))
    if traitsText == []:
        traitsText = ['None']
    embed.add_field(name='Traits', value=''.join(traitsText), inline=False)

    if verbose:
        # Flavor
        try:
            embed.add_field(
                name='Flavor', value=f'*{weapon.flavor}*', inline=False)
        except AttributeError:
            pass
        embed.set_footer(text=('Traits marked with (U) require a researchable upgrade.\n'
                               'Weapon stats depend on the unit wielding the weapon. Stat-changing traits like Twin-Linked not taken into account. '
                               'Values shown may not be accurate.'))

    return embed


def create_gtrait_embed(trait: GTrait, verbose: bool, _) -> discord.Embed:
    trait.get_modifiers()

    # Name and Description
    try:
        embed = discord.Embed(title=trait.name, description=trait.description)
    except AttributeError:
        embed = discord.Embed(title=trait.name)

    # Color
    try:
        embed.colour = GLADIUS_FACTION_COLORS[trait.faction]
    except (AttributeError, KeyError):
        embed.colour = GLADIUS_FACTION_COLORS['Neutral']

    # Faction
    embed.add_field(name='Faction', value=camel_case_split(trait.faction))

    # Modifiers
    try:
        embed.add_field(name='Modifiers',
                        value=trait.modifiers[:1024], inline=False)
    except AttributeError:
        pass

    if verbose:
        # Flavor
        try:
            embed.add_field(
                name='Flavor', value=f'*{trait.flavor}*', inline=False)
        except AttributeError:
            pass

    return embed


def create_ztrait_embed(trait: ZTrait, verbose: bool, _) -> discord.Embed:
    trait.get_modifiers()

    # Name and Description
    try:
        embed = discord.Embed(title=trait.name, description=trait.description)
    except AttributeError:
        embed = discord.Embed(title=trait.name)

    # Modifiers
    try:
        embed.add_field(name='Modifiers',
                        value=trait.modifiers[:1024], inline=False)
    except AttributeError:
        pass

    if verbose:
        # Flavor
        try:
            embed.add_field(
                name='Flavor', value=f'*{trait.flavor}*', inline=False)
        except AttributeError:
            pass

    return embed


def create_gaction_embed(action: GAction, verbose: bool, unitName: str) -> discord.Embed:
    unit = GUnit(unitName)
    unit.fuzzy_match_name(unit.get_obj_info)
    if not unit.found:
        raise UnitNotFoundError(unit.bestMatch)

    action.get_tree(unit)
    action.get_cooldown()
    action.get_conditions()
    action.get_modifiers()

    # Name and Description
    try:
        embed = discord.Embed(
            title=action.name, description=action.description)
    except AttributeError:
        embed = discord.Embed(title=action.name)

    # Color
    embed.colour = GLADIUS_FACTION_COLORS[unit.faction]

    # Cooldown
    if action.passive:
        embed.add_field(name='Cooldown', value='Passive', inline=False)
    else:
        embed.add_field(
            name='Cooldown', value=f"{GLADIUS_ICONS['cooldown']} {action.cooldown}", inline=False)

    # Conditions
    embed.add_field(name=f"Required upgrade", value=str(
        action.conditions.requiredUpgrade))
    embed.add_field(name=f"Requires {GLADIUS_ICONS['actions']} AP?", value=str(
        action.conditions.requiredActionPoints))
    embed.add_field(name=f"Requires {GLADIUS_ICONS['movement']} movement?", value=str(
        action.conditions.requiredMovement))
    embed.add_field(name=f"Usable in {GLADIUS_ICONS['transport']} transport?", value=str(
        action.conditions.usableInTransport))
    embed.add_field(name=f"Consumes {GLADIUS_ICONS['actions']} AP?", value=str(
        action.conditions.consumedActionPoints))
    embed.add_field(name=f"Consumes {GLADIUS_ICONS['movement']} movement?", value=str(
        action.conditions.consumedMovement))

    # Modifiers
    try:
        embed.add_field(name='Modifiers',
                        value=action.modifiers[:1024], inline=False)
    except AttributeError:
        pass

    if verbose:
        # Flavor
        try:
            embed.add_field(
                name='Flavor', value=f'*{action.flavor}*', inline=False)
        except AttributeError:
            pass

    return embed


def create_zaction_embed(action: ZAction, verbose: bool, unitName: str) -> discord.Embed:
    unit = ZUnit(unitName)
    unit.fuzzy_match_name(unit.get_obj_min_info)
    if not unit.found:
        raise UnitNotFoundError(unit.bestMatch)

    unit.get_branch()
    action.get_tree(unit)
    action.get_cooldown()
    action.get_conditions()
    action.get_modifiers()

    # Name and Description
    try:
        embed = discord.Embed(
            title=action.name, description=action.description)
    except AttributeError:
        embed = discord.Embed(title=action.name)

    # Color
    embed.colour = ZEPHON_BRANCH_COLORS[unit.branch]

    # Cooldown
    if action.passive:
        embed.add_field(name='Cooldown', value='Passive', inline=False)
    else:
        embed.add_field(
            name='Cooldown', value=f"{ZEPHON_ICONS['turns']} {action.cooldown}", inline=False)

    # Conditions
    embed.add_field(name=f"Required upgrade", value=str(
        action.conditions.requiredUpgrade))
    embed.add_field(name=f"Requires {ZEPHON_ICONS['actions']} AP?", value=str(
        action.conditions.requiredActionPoints))
    embed.add_field(name=f"Requires {ZEPHON_ICONS['movement']} movement?", value=str(
        action.conditions.requiredMovement))
    embed.add_field(name=f"Usable in {ZEPHON_ICONS['transport']} transport?", value=str(
        action.conditions.usableInTransport))
    embed.add_field(name=f"Consumes {ZEPHON_ICONS['actions']} AP?", value=str(
        action.conditions.consumedActionPoints))
    embed.add_field(name=f"Consumes {ZEPHON_ICONS['movement']} movement?", value=str(
        action.conditions.consumedMovement))

    # Modifiers
    try:
        embed.add_field(name='Modifiers',
                        value=action.modifiers[:1024], inline=False)
    except AttributeError:
        pass

    if verbose:
        # Flavor
        try:
            embed.add_field(
                name='Flavor', value=f'*{action.flavor}*', inline=False)
        except AttributeError:
            pass

    return embed


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    synced = await client.tree.sync()
    print("# CMDs synced: " + str(len(synced)))


def docstring_defaults(func):
    doc = func.__doc__ or ''
    doc += "\tverbose (bool): A flag to include flavor and footer text (default is False)" + \
        "\n\tinvisible (bool): A flag to make the bot's reply invisible to everyone except you (default is False)"
    func.__doc__ = doc
    return func


@client.tree.command(name='gitem')
@docstring_defaults
async def gitem(interaction: discord.Interaction, itemname: str, verbose: bool = False, invisible: bool = False):
    """Return info on a Gladius item.

    Args:
        itemname (str): Name of item to look up
    """
    await return_info(interaction, itemname, verbose, invisible, GItem, create_gitem_embed)


@client.tree.command(name='zitem')
@docstring_defaults
async def gitem(interaction: discord.Interaction, itemname: str, verbose: bool = False, invisible: bool = False):
    """Return info on a Zephon item.

    Args:
        itemname (str): Name of item to look up
    """
    await return_info(interaction, itemname, verbose, invisible, ZItem, create_zitem_embed)


@client.tree.command(name='gunit')
@docstring_defaults
async def gunit(interaction: discord.Interaction, unitname: str, verbose: bool = False, invisible: bool = False):
    """Return info on a Gladius unit.

    Args:
        unitname (str): Name of unit to look up
    """
    await return_info(interaction, unitname, verbose, invisible, GUnit, create_gunit_embed)


@client.tree.command(name='zunit')
@docstring_defaults
async def gunit(interaction: discord.Interaction, unitname: str, verbose: bool = False, invisible: bool = False):
    """Return info on a Zephon unit.

    Args:
        unitname (str): Name of unit to look up
    """
    await return_info(interaction, unitname, verbose, invisible, ZUnit, create_zunit_embed)


@client.tree.command(name='gweapon')
@docstring_defaults
async def gweapon(interaction: discord.Interaction, weaponname: str, unitname: str = '', verbose: bool = False, invisible: bool = False):
    """Return info on a Gladius weapon. Optionally include a unit name for more accurate info.

    Args:
        weaponname (str): Name of weapon to look up
        unitname (str): Name of unit wielding the weapon
    """
    await return_info(interaction, weaponname, verbose, invisible, GWeapon, create_gweapon_embed, unitname)


@client.tree.command(name='zweapon')
@docstring_defaults
async def zweapon(interaction: discord.Interaction, weaponname: str, unitname: str = '', verbose: bool = False, invisible: bool = False):
    """Return info on a Zephon weapon. Optionally include a unit name for more accurate info.

    Args:
        weaponname (str): Name of weapon to look up
        unitname (str): Name of unit wielding the weapon
    """
    await return_info(interaction, weaponname, verbose, invisible, ZWeapon, create_zweapon_embed, unitname)


@client.tree.command(name='gtrait')
@docstring_defaults
async def gtrait(interaction: discord.Interaction, traitname: str, verbose: bool = False, invisible: bool = False):
    """Return info on a Gladius trait.

    Args:
        traitname (str): Name of trait to look up
    """
    await return_info(interaction, traitname, verbose, invisible, GTrait, create_gtrait_embed)


@client.tree.command(name='ztrait')
@docstring_defaults
async def ztrait(interaction: discord.Interaction, traitname: str, verbose: bool = False, invisible: bool = False):
    """Return info on a Zephon trait.

    Args:
        traitname (str): Name of trait to look up
    """
    await return_info(interaction, traitname, verbose, invisible, ZTrait, create_ztrait_embed)


@client.tree.command(name='gaction')
@docstring_defaults
async def gaction(interaction: discord.Interaction, actionname: str, unitname: str, verbose: bool = False, invisible: bool = False):
    """Return info on a Gladius action. Requires the name of a unit with the action.

    Args:
        actionname (str): Name of action to look up
        unitname (str): Name of unit with the action
    """
    await return_info(interaction, actionname, verbose, invisible, GAction, create_gaction_embed, unitname)


@client.tree.command(name='zaction')
@docstring_defaults
async def zaction(interaction: discord.Interaction, actionname: str, unitname: str, verbose: bool = False, invisible: bool = False):
    """Return info on a Zephon action. Requires the name of a unit with the action.

    Args:
        actionname (str): Name of action to look up
        unitname (str): Name of unit with the action
    """
    await return_info(interaction, actionname, verbose, invisible, ZAction, create_zaction_embed, unitname)

client.run(TOKEN)
