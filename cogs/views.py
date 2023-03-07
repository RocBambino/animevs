import textwrap
import discord
from discord.ext import commands
import bot as main
import crown_utilities
import db
import messages as m
import numpy as np
import help_commands as h
import unique_traits as ut
import destiny as d
# Converters
from discord import User
from discord import Member
# from PIL import Image, ImageFont, ImageDraw
import random
from .classes.card_class import Card
from .classes.title_class import Title
from .classes.arm_class import Arm
from .classes.summon_class import Summon
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash import cog_ext, SlashContext
from discord_slash import SlashCommand
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle
from dinteractions_Paginator import Paginator
import re




class Views(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Views Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @cog_ext.cog_slash(description="Equip a Card", guild_ids=main.guild_ids)
    async def equipcard(self, ctx, card: str):
        a_registered_player = await crown_utilities.player_check(ctx)
        if not a_registered_player:
            return

        card_name = card
        user_query = {'DID': str(ctx.author.id)}
        user = db.queryUser(user_query)

        vault_query = {'DID': str(ctx.author.id)}
        vault = db.altQueryVault(vault_query)

        resp = db.queryCard({'NAME': {"$regex": f"^{str(card)}$", "$options": "i"}})

        card_name = resp["NAME"]
        # Do not Check Tourney wins
        if card_name in vault['CARDS']:
            response = db.updateUserNoFilter(user_query, {'$set': {'CARD': str(card_name)}})
            await ctx.send(f"**{card_name}** has been equipped.")
        else:
            await ctx.send(m.USER_DOESNT_HAVE_THE_CARD, hidden=True)


    @cog_ext.cog_slash(description="Type a card name, title, arm, universe, house, hall, or boss to view it!", guild_ids=main.guild_ids)
    async def view(self, ctx, name):
        await ctx.defer()
        if not await crown_utilities.player_check(ctx):
            return

        response = db.viewQuery(f"^{str(name)}$")

        if response:
            if len(response) == 1:
                if response[0]['TYPE'] == "CARDS":
                    await viewcard(self, ctx, response[0]['DATA'])
                if response[0]['TYPE'] == "TITLES":
                    await viewtitle(self, ctx, response[0]['DATA'])
                if response[0]['TYPE'] == "ARM":
                    await viewarm(self, ctx, response[0]['DATA'])
                if response[0]['TYPE'] == "PET":
                    await viewsummon(self, ctx, response[0]['DATA'])
                if response[0]['TYPE'] == "UNIVERSE":
                    await viewuniverse(self, ctx, response[0]['DATA'])
                if response[0]['TYPE'] == "BOSS":
                    await viewboss(self, ctx, response[0]['DATA'])
                if response[0]['TYPE'] == "HALL":
                    await viewhall(self, ctx, response[0]['DATA'])
                if response[0]['TYPE'] == "HOUSE":
                    await viewhouse(self, ctx, response[0]['DATA'])
                return
            else:
                list_of_results = []
                counter = 0
                if response:
                    for result in response:
                        if result['TYPE'] == "CARDS":
                            list_of_results.append({'TYPE': 'CARD', 'NUMBER': result['INDEX'], 'TEXT': f"Did you mean the card 🎴 {result['DATA']['NAME']}?", 'DATA': result['DATA']})
                        
                        if result['TYPE'] == "TITLES":
                            list_of_results.append({'TYPE': 'TITLE', 'NUMBER': result['INDEX'], 'TEXT': f"Did you mean the title 🎗️ {result['DATA']['TITLE']}?", 'DATA': result['DATA']})
                        
                        if result['TYPE'] == "ARM":
                            list_of_results.append({'TYPE': 'ARM', 'NUMBER': result['INDEX'], 'TEXT': f"Did you mean the arm 🦾 {result['DATA']['ARM']}", 'DATA': result['DATA']})
                        
                        if result['TYPE'] == "PET":
                            list_of_results.append({'TYPE': 'PET', 'NUMBER': result['INDEX'], 'TEXT': f"Did you mean the summon 🐦 {result['DATA']['PET']}", 'DATA': result['DATA']})
                        
                        if result['TYPE'] == "UNIVERSE":
                            list_of_results.append({'TYPE': 'UNIVERSE', 'NUMBER': result['INDEX'], 'TEXT': f"Did you mean the universe 🌍 {result['DATA']['TITLE']}", 'DATA': result['DATA']})
                        
                        if result['TYPE'] == "BOSS":
                            list_of_results.append({'TYPE': 'BOSS', 'NUMBER': result['INDEX'], 'TEXT': f"Did you mean the boss 👹 {result['DATA']['NAME']}", 'DATA': result['DATA']})
                        
                        if result['TYPE'] == "HALL":
                            list_of_results.append({'TYPE': 'HALL', 'NUMBER': result['INDEX'], 'TEXT': f"Did you mean the hall ⛩️ {result['DATA']['HALL']}", 'DATA': result['DATA']})
                        
                        if result['TYPE'] == "HOUSE":
                            list_of_results.append({'TYPE': 'HOUSE', 'NUMBER': result['INDEX'], 'TEXT': f"Did you mean the house 🏠 {result['DATA']['HOUSE']}", 'DATA': result['DATA']})
                    
                if list_of_results:
                    message = [f"{result['TEXT']}\n\n" for result in list_of_results]
                    me = ''.join(message)
                    embedVar = discord.Embed(title="Did you mean?...", description=textwrap.dedent(f"""\
                    {me}
                    """), colour=0xf1c40f)

                    buttons = []
                    
                    for result in list_of_results:
                        if result['TYPE'] == "CARD":
                            buttons.append(
                                manage_components.create_button(
                                    style=ButtonStyle.blue,
                                    label=f"🎴 {result['DATA']['NAME']}",
                                    custom_id=f"{str(result['NUMBER'])}"
                                )
                            )
                        
                        if result['TYPE'] == "TITLE":
                            buttons.append(
                                manage_components.create_button(
                                    style=ButtonStyle.blue,
                                    label=f"🎗️ {result['DATA']['TITLE']}",
                                    custom_id=f"{str(result['NUMBER'])}"
                                )
                            )
                        
                        if result['TYPE'] == "ARM":
                            buttons.append(
                                manage_components.create_button(
                                    style=ButtonStyle.blue,
                                    label=f"🦾 {result['DATA']['ARM']}",
                                    custom_id=f"{str(result['NUMBER'])}"
                                )
                            )
                        
                        if result['TYPE'] == "PET":
                            buttons.append(
                                manage_components.create_button(
                                    style=ButtonStyle.blue,
                                    label=f"🐦 {result['DATA']['PET']}",
                                    custom_id=f"{str(result['NUMBER'])}"
                                )
                            )
                        
                        if result['TYPE'] == "UNIVERSE":
                            buttons.append(
                                manage_components.create_button(
                                    style=ButtonStyle.blue,
                                    label=f"🌍 {result['DATA']['TITLE']}",
                                    custom_id=f"{str(result['NUMBER'])}"
                                )
                            )
                        
                        if result['TYPE'] == "BOSS":
                            buttons.append(
                                manage_components.create_button(
                                    style=ButtonStyle.blue,
                                    label=f"👹 {result['DATA']['NAME']}",
                                    custom_id=f"{str(result['NUMBER'])}"
                                )
                            )
                        
                        if result['TYPE'] == "HALL":
                            buttons.append(
                                manage_components.create_button(
                                    style=ButtonStyle.blue,
                                    label=f"⛩️ {result['DATA']['HALL']}",
                                    custom_id=f"{str(result['NUMBER'])}"
                                )
                            )
                        
                        if result['TYPE'] == "HOUSE":
                            buttons.append(
                                manage_components.create_button(
                                    style=ButtonStyle.blue,
                                    label=f"🏠 {result['DATA']['HOUSE']}",
                                    custom_id=f"{str(result['NUMBER'])}"
                                )
                            )

                    buttons.append(manage_components.create_button(
                        style=ButtonStyle.red,
                        label="❌ Cancel",
                        custom_id="cancel"
                    ))
                    buttons_action_row = manage_components.create_actionrow(*buttons)

                    msg = await ctx.send(embed=embedVar, components=[buttons_action_row])
                    
                    def check(button_ctx):
                        return button_ctx.author == ctx.author

                    try:
                        button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[buttons_action_row, buttons], timeout=300, check=check)
                        
                        for result in list_of_results:
                            if button_ctx.custom_id == str(result['NUMBER']):
                                await msg.edit(components=[])
                                await button_ctx.defer(ignore=True)
                                await view_selection(self, ctx, result)
                                return                 
                        if button_ctx.custom_id == "cancel":
                            await msg.edit(components=[])
                            await button_ctx.defer(ignore=True)
                            return
                    except Exception as ex:
                        trace = []
                        tb = ex.__traceback__
                        while tb is not None:
                            trace.append({
                                "filename": tb.tb_frame.f_code.co_filename,
                                "name": tb.tb_frame.f_code.co_name,
                                "lineno": tb.tb_lineno
                            })
                            tb = tb.tb_next
                        print(str({
                            'type': type(ex).__name__,
                            'message': str(ex),
                            'trace': trace
                        }))
                        await ctx.send("You took too long to respond.", hidden=True)
                        return
                else:
                    pass

        if not response:
            results = db.viewQuerySearch(f".*{str(name)}.*")
            list_of_results = []
            counter = 0
            if results:
                for result in results:
                    if result['TYPE'] == "CARDS":
                        list_of_results.append({'TYPE': 'CARD', 'NUMBER': result['INDEX'], 'TEXT': f"Did you mean the card 🎴 {result['DATA']['NAME']}?", 'DATA': result['DATA']})
                    
                    if result['TYPE'] == "TITLES":
                        list_of_results.append({'TYPE': 'TITLE', 'NUMBER': result['INDEX'], 'TEXT': f"Did you mean the title 🎗️ {result['DATA']['TITLE']}?", 'DATA': result['DATA']})
                    
                    if result['TYPE'] == "ARM":
                        list_of_results.append({'TYPE': 'ARM', 'NUMBER': result['INDEX'], 'TEXT': f"Did you mean the arm 🦾 {result['DATA']['ARM']}", 'DATA': result['DATA']})
                    
                    if result['TYPE'] == "PET":
                        list_of_results.append({'TYPE': 'PET', 'NUMBER': result['INDEX'], 'TEXT': f"Did you mean the summon 🐦 {result['DATA']['PET']}", 'DATA': result['DATA']})
                    
                    if result['TYPE'] == "UNIVERSE":
                        list_of_results.append({'TYPE': 'UNIVERSE', 'NUMBER': result['INDEX'], 'TEXT': f"Did you mean the universe 🌍 {result['DATA']['TITLE']}", 'DATA': result['DATA']})
                    
                    if result['TYPE'] == "BOSS":
                        list_of_results.append({'TYPE': 'BOSS', 'NUMBER': result['INDEX'], 'TEXT': f"Did you mean the boss 👹 {result['DATA']['NAME']}", 'DATA': result['DATA']})
                    
                    if result['TYPE'] == "HALL":
                        list_of_results.append({'TYPE': 'HALL', 'NUMBER': result['INDEX'], 'TEXT': f"Did you mean the hall ⛩️ {result['DATA']['HALL']}", 'DATA': result['DATA']})
                    
                    if result['TYPE'] == "HOUSE":
                        list_of_results.append({'TYPE': 'HOUSE', 'NUMBER': result['INDEX'], 'TEXT': f"Did you mean the house 🏠 {result['DATA']['HOUSE']}", 'DATA': result['DATA']})
                
            if list_of_results:
                message = [f"{result['TEXT']}\n\n" for result in list_of_results]
                me = ''.join(message)
                embedVar = discord.Embed(title="Did you mean?...", description=textwrap.dedent(f"""\
                {me}
                """), colour=0xf1c40f)

                buttons = []
                
                for result in list_of_results:
                    if result['TYPE'] == "CARD":
                        buttons.append(
                            manage_components.create_button(
                                style=ButtonStyle.blue,
                                label=f"🎴 {result['DATA']['NAME']}",
                                custom_id=f"{str(result['NUMBER'])}"
                            )
                        )
                    
                    if result['TYPE'] == "TITLE":
                        buttons.append(
                            manage_components.create_button(
                                style=ButtonStyle.blue,
                                label=f"🎗️ {result['DATA']['TITLE']}",
                                custom_id=f"{str(result['NUMBER'])}"
                            )
                        )
                    
                    if result['TYPE'] == "ARM":
                        buttons.append(
                            manage_components.create_button(
                                style=ButtonStyle.blue,
                                label=f"🦾 {result['DATA']['ARM']}",
                                custom_id=f"{str(result['NUMBER'])}"
                            )
                        )
                    
                    if result['TYPE'] == "PET":
                        buttons.append(
                            manage_components.create_button(
                                style=ButtonStyle.blue,
                                label=f"🐦 {result['DATA']['PET']}",
                                custom_id=f"{str(result['NUMBER'])}"
                            )
                        )
                    
                    if result['TYPE'] == "UNIVERSE":
                        buttons.append(
                            manage_components.create_button(
                                style=ButtonStyle.blue,
                                label=f"🌍 {result['DATA']['TITLE']}",
                                custom_id=f"{str(result['NUMBER'])}"
                            )
                        )
                    
                    if result['TYPE'] == "BOSS":
                        buttons.append(
                            manage_components.create_button(
                                style=ButtonStyle.blue,
                                label=f"👹 {result['DATA']['NAME']}",
                                custom_id=f"{str(result['NUMBER'])}"
                            )
                        )
                    
                    if result['TYPE'] == "HALL":
                        buttons.append(
                            manage_components.create_button(
                                style=ButtonStyle.blue,
                                label=f"⛩️ {result['DATA']['HALL']}",
                                custom_id=f"{str(result['NUMBER'])}"
                            )
                        )
                    
                    if result['TYPE'] == "HOUSE":
                        buttons.append(
                            manage_components.create_button(
                                style=ButtonStyle.blue,
                                label=f"🏠 {result['DATA']['HOUSE']}",
                                custom_id=f"{str(result['NUMBER'])}"
                            )
                        )

                buttons.append(manage_components.create_button(
                    style=ButtonStyle.red,
                    label="❌ Cancel",
                    custom_id="cancel"
                ))
                buttons_action_row = manage_components.create_actionrow(*buttons)

                msg = await ctx.send(embed=embedVar, components=[buttons_action_row])
                
                def check(button_ctx):
                    return button_ctx.author == ctx.author

                try:
                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[buttons_action_row, buttons], timeout=300, check=check)
                    
                    for result in list_of_results:
                        if button_ctx.custom_id == str(result['NUMBER']):
                            await msg.edit(components=[])
                            await button_ctx.defer(ignore=True)
                            await view_selection(self, ctx, result)
                            return                 
                    if button_ctx.custom_id == "cancel":
                        await msg.edit(components=[])
                        await button_ctx.defer(ignore=True)
                        return
                except Exception as ex:
                    trace = []
                    tb = ex.__traceback__
                    while tb is not None:
                        trace.append({
                            "filename": tb.tb_frame.f_code.co_filename,
                            "name": tb.tb_frame.f_code.co_name,
                            "lineno": tb.tb_lineno
                        })
                        tb = tb.tb_next
                    print(str({
                        'type': type(ex).__name__,
                        'message': str(ex),
                        'trace': trace
                    }))
                    await ctx.send("You took too long to respond.", hidden=True)
                    return
            else:
                pass

        regex_pattern = r'.*\belements\b.*'
        
        if re.match(regex_pattern, name):
            embedVar = discord.Embed(title= f"What does each element do?", description=h.ELEMENTS, colour=0x7289da)
            embedVar.set_footer(text=f"/animevs - Anime VS+ Manual")
            await ctx.send(embed=embedVar)
            return

        if re.search(r"(manual|help|guide)", name):
            await main.animevs(ctx)
            return

        if re.search(r"(enhancers|passives|talents)", name):
            await main.enhancers(ctx)
            return

        
        await ctx.send("No results found.", hidden=True)
        return

    async def direct_selection(self, ctx, results):
        print("Hello Direct Selection")
        message = [f"{result['TEXT']}\n\n" for result in results]
        me = ''.join(message)
        embedVar = discord.Embed(title="Did you mean?...", description=textwrap.dedent(f"""\
        {me}
        """), colour=0xf1c40f)

        buttons = []
        
        for result in results:
            if result['TYPE'] == "CARDS":
                buttons.append(
                    manage_components.create_button(
                        style=ButtonStyle.blue,
                        label=f"🎴 {result['DATA']['NAME']}",
                        custom_id=f"{str(result['NUMBER'])}"
                    )
                )
            
            if result['TYPE'] == "TITLES":
                buttons.append(
                    manage_components.create_button(
                        style=ButtonStyle.blue,
                        label=f"🎗️ {result['DATA']['TITLE']}",
                        custom_id=f"{str(result['NUMBER'])}"
                    )
                )
            
            if result['TYPE'] == "ARM":
                buttons.append(
                    manage_components.create_button(
                        style=ButtonStyle.blue,
                        label=f"🦾 {result['DATA']['ARM']}",
                        custom_id=f"{str(result['NUMBER'])}"
                    )
                )
            
            if result['TYPE'] == "PET":
                buttons.append(
                    manage_components.create_button(
                        style=ButtonStyle.blue,
                        label=f"🐦 {result['DATA']['PET']}",
                        custom_id=f"{str(result['NUMBER'])}"
                    )
                )
            
            if result['TYPE'] == "UNIVERSE":
                buttons.append(
                    manage_components.create_button(
                        style=ButtonStyle.blue,
                        label=f"🌍 {result['DATA']['TITLE']}",
                        custom_id=f"{str(result['NUMBER'])}"
                    )
                )
            
            if result['TYPE'] == "BOSS":
                buttons.append(
                    manage_components.create_button(
                        style=ButtonStyle.blue,
                        label=f"👹 {result['DATA']['NAME']}",
                        custom_id=f"{str(result['NUMBER'])}"
                    )
                )
            
            if result['TYPE'] == "HALL":
                buttons.append(
                    manage_components.create_button(
                        style=ButtonStyle.blue,
                        label=f"⛩️ {result['DATA']['HALL']}",
                        custom_id=f"{str(result['NUMBER'])}"
                    )
                )
            
            if result['TYPE'] == "HOUSE":
                buttons.append(
                    manage_components.create_button(
                        style=ButtonStyle.blue,
                        label=f"🏠 {result['DATA']['HOUSE']}",
                        custom_id=f"{str(result['NUMBER'])}"
                    )
                )

        buttons.append(manage_components.create_button(
            style=ButtonStyle.red,
            label="❌ Cancel",
            custom_id="cancel"
        ))
        buttons_action_row = manage_components.create_actionrow(*buttons)

        msg = await ctx.send(embed=embedVar, components=[buttons_action_row])
        
        def check(button_ctx):
            return button_ctx.author == ctx.author

        try:
            button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[buttons_action_row, buttons], timeout=300, check=check)

            if button_ctx.custom_id == "0":
                if results["NUMBER"] == 0:
                    await button_ctx.defer(ignore=True)
                    await view_selection(ctx, results["DATA"])
                    return
            if button_ctx.custom_id == "1":
                if results["NUMBER"] == 1:
                    await button_ctx.defer(ignore=True)
                    await view_selection(ctx, results["DATA"])
                    return
            if button_ctx.custom_id == "2":
                if results["NUMBER"] == 2:
                    await button_ctx.defer(ignore=True)
                    await view_selection(ctx, results["DATA"])
                    return
            if button_ctx.custom_id == "3":
                if results["NUMBER"] == 3:
                    await button_ctx.defer(ignore=True)
                    await view_selection(ctx, results["DATA"])
                    return
            if button_ctx.custom_id == "4":
                if results["NUMBER"] == 4:
                    await button_ctx.defer(ignore=True)
                    await view_selection(ctx, results["DATA"])
                    return
            if button_ctx.custom_id == "cancel":
                await button_ctx.defer(ignore=True)
                return
        except Exception as ex:
            trace = []
            tb = ex.__traceback__
            while tb is not None:
                trace.append({
                    "filename": tb.tb_frame.f_code.co_filename,
                    "name": tb.tb_frame.f_code.co_name,
                    "lineno": tb.tb_lineno
                })
                tb = tb.tb_next
            print(str({
                'type': type(ex).__name__,
                'message': str(ex),
                'trace': trace
            }))
            await ctx.send("You took too long to respond.", hidden=True)
            return


        

def setup(bot):
    bot.add_cog(Views(bot))


async def view_selection(self, ctx, result):
    if result['TYPE'] == "CARD":
        await viewcard(self, ctx, result['DATA'])
        return
    
    if result['TYPE'] == "TITLE":
        await viewtitle(self, ctx, result['DATA'])
        return
    
    if result['TYPE'] == "ARM":
        await viewarm(self, ctx, result['DATA'])
        return
    
    if result['TYPE'] == "PET":
        await viewpet(self, ctx, result['DATA'])
        return
    
    if result['TYPE'] == "UNIVERSE":
        await viewuniverse(self, ctx, result['DATA'])
        return
    
    if result['TYPE'] == "BOSS":
        await viewboss(self, ctx, result['DATA'])
        return
    
    if result['TYPE'] == "HALL":
        await viewhall(self, ctx, result['DATA'])
        return
    
    if result['TYPE'] == "HOUSE":
        await viewhouse(self, ctx, result['DATA'])
        return

async def viewcard(self, ctx, data):
    query = {'DID': str(ctx.author.id)}
    d = db.queryUser(query)
    card = data
    try:
        if card:
            if "FPATH" not in card:
                card['FPATH'] = card['PATH']

            c = Card(card['NAME'], card['PATH'], card['PRICE'], card['EXCLUSIVE'], card['AVAILABLE'], card['IS_SKIN'], card['SKIN_FOR'], card['HLT'], card['HLT'], card['STAM'], card['STAM'], card['MOVESET'], card['ATK'], card['DEF'], card['TYPE'], card['PASS'][0], card['SPD'], card['UNIVERSE'], card['HAS_COLLECTION'], card['TIER'], card['COLLECTION'], card['WEAKNESS'], card['RESISTANT'], card['REPEL'], card['ABSORB'], card['IMMUNE'], card['GIF'], card['FPATH'], card['RNAME'], card['RPATH'], False)
            title = {'TITLE': 'CARD PREVIEW'}
            arm = {'ARM': 'CARD PREVIEW'}

            if c.is_universe_unbound():
                await ctx.send("You cannot view this card at this time. ", hidden=True)
                return
            c.set_price_message_and_card_icon()
            c.set_tip_and_view_card_message()
            att = 0
            defe = 0
            turn = 0

            active_pet = {}
            pet_ability_power = 0
            card_exp = 150

            
            if d['PERFORMANCE']:
                embedVar = discord.Embed(title=f"{c.card_icon} {c.price_message} {c.name}", description=textwrap.dedent(f"""\
                :mahjong: {c.tier}
                ❤️ {c.max_health}
                🗡️ {c.attack}
                🛡️ {c.defense}
                🏃 {c.speed}

                🩸 {c.passive_name}: {c.passive_type} {c.passive_num}{crown_utilities.passive_enhancer_suffix_mapping[c.passive_type]}                

                {c.move1_emoji} {c.move1}: {c.move1ap}
                {c.move2_emoji} {c.move2}: {c.move2ap}
                {c.move3_emoji} {c.move3}: {c.move3ap}
                🦠 {c.move4}: {c.move4enh} {c.move4ap} {crown_utilities.passive_enhancer_suffix_mapping[c.move4enh]}   

                ♾️ {c.set_trait_message()}
                """), colour=000000)
                embedVar.add_field(name="__Affinities__", value=f"{c.set_affinity_message()}")
                embedVar.set_footer(text=f"{c.tip}")
                await ctx.send(embed=embedVar)

            else:
                embedVar = discord.Embed(title=f"", colour=000000)
                embedVar.add_field(name="__Affinities__", value=f"{c.set_affinity_message()}")
                embedVar.set_image(url="attachment://image.png")
                embedVar.set_thumbnail(url=c.set_universe_image())
                embedVar.set_author(name=textwrap.dedent(f"""\
                {c.card_icon} {c.price_message}
                Passive & Universe Trait
                🩸 {c.passive_name}: {c.passive_type} {c.passive_num}{crown_utilities.passive_enhancer_suffix_mapping[c.passive_type]}
                ♾️ {c.set_trait_message()}
                🏃 {c.speed}
                """))
                embedVar.set_footer(text=f"{c.tip}")

                await ctx.send(file=c.showcard("non-battle", "none", title, 0, 0), embed=embedVar)
        else:
            await ctx.send(m.CARD_DOESNT_EXIST, hidden=True)
    except Exception as ex:
        trace = []
        tb = ex.__traceback__
        while tb is not None:
            trace.append({
                "filename": tb.tb_frame.f_code.co_filename,
                "name": tb.tb_frame.f_code.co_name,
                "lineno": tb.tb_lineno
            })
            tb = tb.tb_next
        print(str({
            'type': type(ex).__name__,
            'message': str(ex),
            'trace': trace
        }))
        return
        await ctx.send("There was an issue with loading the card.", hidden=True)


async def viewtitle(self, ctx, data):
    try:
        title = data
        if title:
            t = Title(title['TITLE'], title['UNIVERSE'], title['PRICE'], title['EXCLUSIVE'], title['AVAILABLE'], title['ABILITIES'])            
            t.set_type_message_and_price_message()

            embedVar = discord.Embed(title=f"🎗️ | {t.name}\n{crown_utilities.crest_dict[t.universe]} | {t.universe}\n{t.price_message}".format(self), colour=000000)
            if t.universe != "Unbound":
                embedVar.set_thumbnail(url=t.title_img)
            embedVar.add_field(name=f"**Unique Passive**", value=f"{t.set_title_embed_message()}", inline=False)
            embedVar.set_footer(text=f"{t.passive_type}: {crown_utilities.title_enhancer_mapping[t.passive_type]}")
            await ctx.send(embed=embedVar)

        else:
            await ctx.send("That title doesn't exist.", hidden=True)
    except Exception as ex:
        trace = []
        tb = ex.__traceback__
        while tb is not None:
            trace.append({
                "filename": tb.tb_frame.f_code.co_filename,
                "name": tb.tb_frame.f_code.co_name,
                "lineno": tb.tb_lineno
            })
            tb = tb.tb_next
        print(str({
            'type': type(ex).__name__,
            'message': str(ex),
            'trace': trace
        }))


async def viewarm(self, ctx, data):
    arm = data
    try:
        if arm:
            a = Arm(arm['ARM'], arm['UNIVERSE'], arm['PRICE'], arm['ABILITIES'], arm['EXCLUSIVE'], arm['AVAILABLE'], arm['ELEMENT'])
            embedVar = discord.Embed(title=f"🦾 | {a.name}\n{crown_utilities.crest_dict[a.universe]} | {a.universe}\n{a.price_message}".format(self), colour=000000)
            if a.universe != "Unbound":
                embedVar.set_thumbnail(url=a.show_img)

            if a.is_move():
                # embedVar.add_field(name=f"Arm Move Element", value=f"{element}", inline=False)
                embedVar.add_field(name=f"{a.type_message} {a.element.title()} Attack", value=f"{a.element_emoji} | **{a.name}**: **{a.passive_value}**\n *{a.element_ability}*", inline=False)
                # embedVar.add_field(name=f":sunny: | Elemental Effect", value=f"*{a.element_ability}*", inline=False)
                embedVar.set_footer(text=f"The new {a.type_message} attack will reflect on your card when equipped")

            else:
                embedVar.add_field(name=f"Unique Passive", value=f"Increases {a.type_message} by **{a.passive_value}**", inline=False)
                embedVar.set_footer(text=f"{a.passive_type}: {crown_utilities.enhancer_mapping[a.passive_type]}")

            await ctx.send(embed=embedVar)

        else:
            await ctx.send(m.ARM_DOESNT_EXIST, hidden=True)
    except Exception as ex:
        trace = []
        tb = ex.__traceback__
        while tb is not None:
            trace.append({
                "filename": tb.tb_frame.f_code.co_filename,
                "name": tb.tb_frame.f_code.co_name,
                "lineno": tb.tb_lineno
            })
            tb = tb.tb_next
        print(str({
            'type': type(ex).__name__,
            'message': str(ex),
            'trace': trace
        }))
        return


async def viewsummon(self, ctx, data):
    pet = data
    try:
        if pet:
            s = Summon(pet['PET'], pet['UNIVERSE'], pet['PATH'], pet['ABILITIES'], pet['AVAILABLE'], pet['EXCLUSIVE'])
            s.set_messages()

            summon_file = crown_utilities.showsummon(s.path, s.name, s.value, 0, 0)
            embedVar = discord.Embed(title=f"Summon".format(self), colour=000000)
            if s.is_not_universe_unbound:
                embedVar.set_thumbnail(url=s.show_img)
                        
            embedVar.set_image(url="attachment://pet.png")

            await ctx.send(file=summon_file)

        else:
            await ctx.send(m.PET_DOESNT_EXIST, hidden=True)
    except Exception as ex:
        trace = []
        tb = ex.__traceback__
        while tb is not None:
            trace.append({
                "filename": tb.tb_frame.f_code.co_filename,
                "name": tb.tb_frame.f_code.co_name,
                "lineno": tb.tb_lineno
            })
            tb = tb.tb_next
        print(str({
            'type': type(ex).__name__,
            'message': str(ex),
            'trace': trace
        }))
        return


async def viewuniverse(self, ctx, data):
    try:
        universe = data
        universe_name = universe['TITLE']
        ttitle = "Starter"
        tarm = "Stock"
        dtitle = "Reborn"
        darm = "Reborn Stock"
        dpet = "Chick"
        boss = "Bossless"
        crest = crown_utilities.crest_dict['Unbound']
        prerec = ""
        owner = "PCG"
        traits = ut.traits
        if universe:
            universe_title= universe['TITLE']
            fights = len(universe['CROWN_TALES'])
            dungeon_fights = len(universe['DUNGEONS'])
            crest = crown_utilities.crest_dict[universe_title]
            universe_image = universe['PATH']
            ttitle = universe['UTITLE']
            tarm = universe['UARM']
            dtitle = universe['DTITLE']
            darm = universe['DARM']
            upet = universe['UPET']
            dpet = universe['DPET']
            boss = universe['UNIVERSE_BOSS']
            tier = universe['TIER']
            bossmessage = f"*/view {boss} 👹 It's A Boss*"
            if boss == "":
                bossmessage = f"No {universe_title} Boss available yet!"
            prerec = universe['PREREQUISITE']
            
            prerecmessage = f"Compelete the {prerec} Tale to unlock this Universe!"
            if prerec == "":
                if tier == 9:
                    prerec = "Crown Rift"
                    prerecmessage = "Complete Battles To Open Crown Rifts!"
                else:
                    prerec = "Starter Universe"
                    prerecmessage = "Complete this Tale to unlock rewards!"
            owner = universe['GUILD']
            ownermessage = f"{universe_title} is owned by the {owner} Guild!"
            if owner == "PCG":
                owner = "Crest Unclaimed"
                ownermessage = "*Complete the **Dungeon** and Claim this Universe for your Guild!*"
                
            
            mytrait = {}
            traitmessage = ''
            for trait in traits:
                if trait['NAME'] == universe_title:
                    mytrait = trait
                if universe_title == 'Kanto Region' or universe_title == 'Johto Region' or universe_title == 'Kalos Region' or universe_title == 'Unova Region' or universe_title == 'Sinnoh Region' or universe_title == 'Hoenn Region' or universe_title == 'Galar Region' or universe_title == 'Alola Region':
                    if trait['NAME'] == 'Pokemon':
                        mytrait = trait
            if mytrait:
                traitmessage = f"**{mytrait['EFFECT']}**| {mytrait['TRAIT']}"
                

            embedVar = discord.Embed(title=f":earth_africa: | {universe_title} :crossed_swords: {fights} :fire: {dungeon_fights} ", description=textwrap.dedent(f"""
            {crest} | **{ownermessage}**
            
            🗒️ | **Details**
            :crown: | **Tales Build** 
            :reminder_ribbon: | **Title** - {ttitle}
            :mechanical_arm: | **Arm** - {tarm}
            🧬 | **Universe Summon ** - {upet}
            
            :fire: | **Dungeon Build**
            :reminder_ribbon: | **Title** - {dtitle}
            :mechanical_arm: | **Arm** - {darm}
            🧬 | **Dungeon Summon ** - {dpet}
            
            :japanese_ogre: | **Universe Boss**
            :flower_playing_cards: | **Card** - {boss}
            {bossmessage}
            :infinity: | **Universe Trait** - {traitmessage}
            """), colour=000000)
            embedVar.set_image(url=universe_image)
            embedVar.set_footer(text=f"{universe_title} Details")

            await ctx.send(embed=embedVar)

        else:
            await ctx.send(m.UNIVERSE_DOES_NOT_EXIST)
    except Exception as ex:
        trace = []
        tb = ex.__traceback__
        while tb is not None:
            trace.append({
                "filename": tb.tb_frame.f_code.co_filename,
                "name": tb.tb_frame.f_code.co_name,
                "lineno": tb.tb_lineno
            })
            tb = tb.tb_next
        print(str({
            'type': type(ex).__name__,
            'message': str(ex),
            'trace': trace
        }))
        await ctx.send(f"Error when viewing universe. Alert support. Thank you!")
        return


async def viewhouse(self, ctx, data):
    house = data
    if house:
        house_house = house['HOUSE']
        house_price = house['PRICE']
        house_img = house['PATH']
        house_multiplier = house['MULT']

        message=""
        
        price_message ="" 
        price_message = f":coin: {'{:,}'.format(house_price)}"


        embedVar = discord.Embed(title=f"{house_house}\n{price_message}".format(self), colour=000000)
        embedVar.set_image(url=house_img)
        embedVar.add_field(name="Income Multiplier", value=f"Family earns **{house_multiplier}x** :coin: per match!", inline=False)
        embedVar.set_footer(text=f"/houses - House Menu")

        await ctx.send(embed=embedVar)

    else:
        await ctx.send(m.HOUSE_DOESNT_EXIST, delete_after=3)


async def viewhall(self, ctx, data):
    hall = data
    if hall:
        hall_hall = hall['HALL']
        hall_price = hall['PRICE']
        hall_img = hall['PATH']
        hall_multiplier = hall['MULT']
        hall_fee = hall['FEE']
        hall_split = hall['SPLIT']
        hall_def = hall['DEFENSE']

        message=""
        
        price_message ="" 
        price_message = f":coin: {'{:,}'.format(hall_price)}"


        embedVar = discord.Embed(title=f"{hall_hall}\n{price_message}", colour=000000)
        embedVar.set_image(url=hall_img)
        embedVar.add_field(name="Bounty Fee", value=f"**{'{:,}'.format(hall_fee)}** :yen: per **Raid**!", inline=False)
        embedVar.add_field(name="Multiplier", value=f"Association earns **{hall_multiplier}x** :coin: per match!", inline=False)
        embedVar.add_field(name="Split", value=f"**Guilds** earn **{hall_split}x** :coin: per match!", inline=False)
        embedVar.add_field(name="Defenses", value=f"**Shield** Defense Boost: **{hall_def}x**", inline=False)
        embedVar.set_footer(text=f"/halls - Hall Menu")

        await ctx.send(embed=embedVar)

    else:
        await ctx.send(m.HALL_DOESNT_EXIST, delete_after=3)


async def viewboss(self, ctx, data):
    try:
        uboss = data
        if uboss:
            uboss_name = uboss['NAME']
            uboss_show = uboss['UNIVERSE']
            uboss_title = uboss['TITLE']
            uboss_arm = uboss['ARM']
            uboss_desc = uboss['DESCRIPTION'][3]
            uboss_pic = uboss['PATH']
            uboss_pet = uboss['PET']
            uboss_card = uboss['CARD']

            arm = db.queryArm({'ARM': uboss_arm})
            arm_passive = arm['ABILITIES'][0]
            arm_passive_type = list(arm_passive.keys())[0]
            arm_passive_value = list(arm_passive.values())[0]

            title = db.queryTitle({'TITLE': uboss_title})
            title_passive = title['ABILITIES'][0]
            title_passive_type = list(title_passive.keys())[0]
            title_passive_value = list(title_passive.values())[0]
            
            pet = db.queryPet({'PET': uboss_pet})
            pet_ability = pet['ABILITIES'][0]
            pet_ability_name = list(pet_ability.keys())[0]
            pet_ability_type = list(pet_ability.values())[1]
            pet_ability_value = list(pet_ability.values())[0]

            traits = ut.traits

            if uboss_show != 'Unbound':
                uboss_show_img = db.queryUniverse({'TITLE': uboss_show})['PATH']
            message= uboss_desc
            
            mytrait = {}
            traitmessage = ''
            for trait in traits:
                if trait['NAME'] == uboss_show:
                    mytrait = trait
                if uboss_show == 'Kanto Region' or uboss_show == 'Johto Region' or uboss_show == 'Kalos Region' or uboss_show == 'Unova Region' or uboss_show == 'Sinnoh Region' or uboss_show == 'Hoenn Region' or uboss_show == 'Galar Region' or uboss_show == 'Alola Region':
                    if trait['NAME'] == 'Pokemon':
                        mytrait = trait
            if mytrait:
                traitmessage = f"**{mytrait['EFFECT']}**| {mytrait['TRAIT']}"
            
            embedVar = discord.Embed(title=f":japanese_ogre: | {uboss_name}\n:earth_africa: | {uboss_show} Boss", description=textwrap.dedent(f"""
            *{message}*
            
            :flower_playing_cards: | **Card** - {uboss_card}
            :reminder_ribbon: | **Title** - {uboss_title}: **{title_passive_type}** - {title_passive_value}
            :mechanical_arm: | **Arm** - {uboss_arm}: **{arm_passive_type}** - {arm_passive_value}
            :dna: | **Summon** - {uboss_pet}: **{pet_ability_type}**: {pet_ability_value}
            
            :infinity: | **Universe Trait** - {traitmessage}
            """), colour=000000)
            if uboss_show != "Unbound":
                embedVar.set_thumbnail(url=uboss_show_img)
            embedVar.set_image(url=uboss_pic)

            await ctx.send(embed=embedVar)


        else:
            await ctx.send(m.BOSS_DOESNT_EXIST, delete_after=3)
        
    except Exception as ex:
        trace = []
        tb = ex.__traceback__
        while tb is not None:
            trace.append({
                "filename": tb.tb_frame.f_code.co_filename,
                "name": tb.tb_frame.f_code.co_name,
                "lineno": tb.tb_lineno
            })
            tb = tb.tb_next
        print(str({
            'type': type(ex).__name__,
            'message': str(ex),
            'trace': trace
        }))
        await ctx.send(f"Error when viewing boss. Alert support. Thank you!")
        return


enhancer_mapping = {'ATK': 'Increase Attack %',
'DEF': 'Increase Defense %',
'STAM': 'Increase Stamina',
'HLT': 'Heal yourself or companion',
'LIFE': 'Steal Health from Opponent',
'DRAIN': 'Drain Stamina from Opponent',
'FLOG': 'Steal Attack from Opponent',
'WITHER': 'Steal Defense from Opponent',
'RAGE': 'Lose Defense, Increase Attack',
'BRACE': 'Lose Attack, Increase Defense',
'BZRK': 'Lose Health, Increase Attack',
'CRYSTAL': 'Lose Health, Increase Defense',
'GROWTH': 'Lose Health, Increase Attack & Defense',
'STANCE': 'Swap your Attack & Defense, Increase Attack',
'CONFUSE': 'Swap Opponent Attack & Defense, Decrease Opponent Defense',
'BLINK': 'Decrease your  Stamina, Increase Target Stamina',
'SLOW': 'Decrease Opponent Stamina, Swap Stamina with Opponent',
'HASTE': ' Increase your Stamina, Swap Stamina with Opponent',
'FEAR': 'Decrease your Health, Decrease Opponent Attack and Defense',
'SOULCHAIN': 'You and Your Opponent Stamina Link',
'GAMBLE': 'You and Your Opponent Health Link',
'WAVE': 'Deal Damage, Decreases over time',
'CREATION': 'Heals you, Decreases over time',
'BLAST': 'Deals Damage, Increases over time',
'DESTRUCTION': 'Decreases Opponent Max Health, Increases over time',
'BASIC': 'Increase Basic Attack AP',
'SPECIAL': 'Increase Special Attack AP',
'ULTIMATE': 'Increase Ultimate Attack AP',
'ULTIMAX': 'Increase All AP Values',
'MANA': 'Increase Enchancer AP',
'SHIELD': 'Blocks Incoming DMG, until broken',
'BARRIER': 'Nullifies Incoming Attacks, until broken',
'PARRY': 'Returns 25% Damage, until broken',
'SIPHON': 'Heal for 10% DMG inflicted + AP'
}


enhancer_suffix_mapping = {'ATK': '%',
'DEF': '%',
'STAM': ' Flat',
'HLT': '%',
'LIFE': '%',
'DRAIN': ' Flat',
'FLOG': '%',
'WITHER': '%',
'RAGE': '%',
'BRACE': '%',
'BZRK': '%',
'CRYSTAL': '%',
'GROWTH': '%',
'STANCE': ' Flat',
'CONFUSE': ' Flat',
'BLINK': ' Flat',
'SLOW': ' Flat',
'HASTE': ' Flat',
'FEAR': '%',
'SOULCHAIN': ' Flat',
'GAMBLE': ' Flat',
'WAVE': ' Flat',
'CREATION': ' Flat',
'BLAST': ' Flat',
'DESTRUCTION': ' Flat',
'BASIC': ' Flat',
'SPECIAL': ' Flat',
'ULTIMATE': ' Flat',
'ULTIMAX': ' Flat',
'MANA': ' %',
'SHIELD': ' DMG 🌐',
'BARRIER': ' Blocks 💠',
'PARRY': ' Counters 🔄',
'SIPHON': ' Healing 💉'
}

