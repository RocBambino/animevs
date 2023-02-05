import time
from operator import floordiv
from discord import guild, message
from re import T
import discord
from discord.ext import commands
import db
import dcf_file as data
import destiny as d
import messages as m
import numpy as np
import help_commands as h
# Converters
from discord import User
from discord import Member
import DiscordUtils
from PIL import Image, ImageFont, ImageDraw
import requests
import random
from collections import ChainMap
now = time.asctime()
import base64
from io import BytesIO
import io
import asyncio
import textwrap
import bot as main
import crown_utilities
from .classes.player_class import Player
from .classes.card_class import Card
from .classes.title_class import Title
from .classes.arm_class import Arm
from .classes.summon_class import Summon
from .classes.battle_class  import Battle
from discord import Embed
from discord_slash import cog_ext, SlashContext
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_commands import create_option, create_choice
from dinteractions_Paginator import Paginator
import typing
from pilmoji import Pilmoji
import destiny as d


class CrownUnlimited(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(1, 5, commands.BucketType.member)  # Change accordingly. Currently every 8 minutes (3600 seconds == 60 minutes)
        self._lvl_cd = commands.CooldownMapping.from_cooldown(1, 3000, commands.BucketType.member)
    co_op_modes = ['CTales', 'DTales', 'CDungeon', 'DDungeon']
    ai_co_op_modes = ['DTales', 'DDungeon']
    U_modes = ['ATales', 'Tales', 'CTales', 'DTales']
    D_modes = ['CDungeon', 'DDungeon', 'Dungeon', 'ADungeon']
    solo_modes = ['ATales', 'Tales', 'Dungeon', 'Boss']
    opponent_pet_modes = ['Dungeon', 'DDungeon', 'CDungeon']
    max_items = 150

    @commands.Cog.listener()
    async def on_ready(self):
        print('Anime 🆚+ Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    async def companion(user):
        user_data = db.queryUser({'DID': str(user.id)})
        companion = user_data['DISNAME']
        return companion

    def get_ratelimit(self, message: discord.Message) -> typing.Optional[int]:
        """Returns the ratelimit left"""
        bucket = self._cd.get_bucket(message)
        return bucket.update_rate_limit()

    def get_lvl_ratelimit(self, message: discord.Message) -> typing.Optional[int]:
        """Returns the level ratelimit left"""
        bucket = self._lvl_cd.get_bucket(message)
        return bucket.update_rate_limit()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == main.bot.user:
            return
        level_ratelimit = self.get_lvl_ratelimit(message)
        ratelimit = self.get_ratelimit(message)

        if level_ratelimit is None:
            try:
                player_that_leveled = db.queryUser({'DID': str(message.author.id)})
                if player_that_leveled:
                    card_that_leveled = db.queryCard({'NAME': player_that_leveled['CARD']})
                    uni = card_that_leveled['UNIVERSE']
                    nam = card_that_leveled['NAME']
                    mode = "Tales"
                    u = await main.bot.fetch_user(str(message.author.id))
                    await crown_utilities.cardlevel(u, nam, str(message.author.id), mode, uni)
                else:
                    return
            except Exception as e:
                print(f"{str(message.author)} Error in on_message: {e}")

        if ratelimit is None:
            if isinstance(message.channel, discord.channel.DMChannel):
                return

            g = message.author.guild
            channel_list = message.author.guild.text_channels
            channel_names = []
            for channel in channel_list:
                channel_names.append(channel.name)

            server_channel_response = db.queryServer({'GNAME': str(g)})
            server_channel = ""
            if server_channel_response:
                server_channel = str(server_channel_response['EXP_CHANNEL'])
            
            if "explore-encounters" in channel_names:
                server_channel = "explore-encounters"
            
            if not server_channel:
                return

            mode = "EXPLORE"

            # Pull Character Information
            player = db.queryUser({'DID': str(message.author.id)})
            if not player:
                return
            p = Player(player['DISNAME'], player['DID'], player['AVATAR'], player['GUILD'], player['TEAM'], player['FAMILY'], player['TITLE'], player['CARD'], player['ARM'], player['PET'], player['TALISMAN'], player['CROWN_TALES'], player['DUNGEONS'], player['BOSS_WINS'], player['RIFT'], player['REBIRTH'], player['LEVEL'], player['EXPLORE'], player['SAVE_SPOT'], player['PERFORMANCE'], player['TRADING'], player['BOSS_FOUGHT'], player['DIFFICULTY'], player['STORAGE_TYPE'], player['USED_CODES'], player['BATTLE_HISTORY'], player['PVP_WINS'], player['PVP_LOSS'], player['RETRIES'], player['PRESTIGE'], player['PATRON'], player['FAMILY_PET'], player['EXPLORE_LOCATION'])    
            battle = Battle(mode, p)
            if p.get_locked_feature(mode):
                return

            if p.explore is False:
                return


            if p.explore_location == "NULL":
                all_universes = db.queryExploreUniverses()
                available_universes = [x for x in all_universes]

                u = len(available_universes) - 1
                rand_universe = random.randint(1, u)
                universetitle = available_universes[rand_universe]['TITLE']
                universe = available_universes[rand_universe]
            else:
                universe = db.queryUniverse({"TITLE": p.explore_location})
                universetitle = universe['TITLE']


            # Select Card at Random
            all_available_drop_cards = db.querySpecificDropCards(universetitle)
            cards = [x for x in all_available_drop_cards]

            c = len(cards) - 1
            rand_card = random.randint(1, c)
            selected_card = Card(cards[rand_card]['NAME'], cards[rand_card]['PATH'], cards[rand_card]['PRICE'], cards[rand_card]['EXCLUSIVE'], cards[rand_card]['AVAILABLE'], cards[rand_card]['IS_SKIN'], cards[rand_card]['SKIN_FOR'], cards[rand_card]['HLT'], cards[rand_card]['HLT'], cards[rand_card]['STAM'], cards[rand_card]['STAM'], cards[rand_card]['MOVESET'], cards[rand_card]['ATK'], cards[rand_card]['DEF'], cards[rand_card]['TYPE'], cards[rand_card]['PASS'][0], cards[rand_card]['SPD'], cards[rand_card]['UNIVERSE'], cards[rand_card]['HAS_COLLECTION'], cards[rand_card]['TIER'], cards[rand_card]['COLLECTION'], cards[rand_card]['WEAKNESS'], cards[rand_card]['RESISTANT'], cards[rand_card]['REPEL'], cards[rand_card]['ABSORB'], cards[rand_card]['IMMUNE'], cards[rand_card]['GIF'], cards[rand_card]['FPATH'], cards[rand_card]['RNAME'], cards[rand_card]['RPATH'])
            selected_card.set_affinity_message()
            selected_card.set_explore_bounty_and_difficulty(battle)

            battle.set_explore_config(universe, selected_card)
            battle.bounty = selected_card.bounty

            random_battle_buttons = [
                manage_components.create_button(
                    style=ButtonStyle.blue,
                    label="Gold",
                    custom_id="gold"
                ),
                manage_components.create_button(
                    style=ButtonStyle.red,
                    label="Ignore",
                    custom_id="ignore"
                ),
            ]
            if selected_card.tier > 4 and selected_card.card_lvl > 350:
                random_battle_buttons.append(manage_components.create_button(
                    style=ButtonStyle.blue,
                    label="Glory",
                    custom_id="glory"
                ),)
            random_battle_buttons_action_row = manage_components.create_actionrow(*random_battle_buttons)


            # Send Message
            embedVar = discord.Embed(title=f"**{selected_card.approach_message}{selected_card.name}** has a bounty!",
                                     description=textwrap.dedent(f"""\
            **Bounty** **{selected_card.bounty_message}**
            {selected_card.battle_message}
            """), colour=0xf1c40f)
         
            embedVar.set_image(url="attachment://image.png")
            embedVar.set_thumbnail(url=message.author.avatar_url)

            setchannel = discord.utils.get(channel_list, name=server_channel)
            await setchannel.send(f"{message.author.mention}") 
            msg = await setchannel.send(embed=embedVar, file=selected_card.showcard("non-battle", "none", {'TITLE': 'EXPLORE TITLE'}, 0, 0), components=[random_battle_buttons_action_row])     

            def check(button_ctx):
                return button_ctx.author == message.author

            try:
                button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[
                    random_battle_buttons_action_row], timeout=120, check=check)

                if button_ctx.custom_id == "glory":
                    await button_ctx.defer(ignore=True)
                    battle.explore_type = "glory"
                    await battle_commands(self, button_ctx, battle, p, selected_card, _player2=None)
                    await msg.edit(components=[])

                if button_ctx.custom_id == "gold":
                    await button_ctx.defer(ignore=True)
                    battle.explore_type = "gold"
                    await battle_commands(self, button_ctx, battle, p, selected_card, _player2=None)
                    await msg.edit(components=[])
                if button_ctx.custom_id == "ignore":
                    await button_ctx.defer(ignore=True)
                    await msg.edit(components=[])

            except Exception as ex:
                await msg.edit(components=[])
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



    @cog_ext.cog_slash(description="Toggle Explore Mode On/Off",
                        options=[
                           create_option(
                               name="toggle",
                               description="Turn explore off or keep on",
                               option_type=3,
                               required=True,
                               choices=[
                                   create_choice(
                                       name="Turn Explore Mode Off",
                                       value="1"
                                   ),
                                   create_choice(
                                       name="Turn Explore Mode On",
                                       value="2"
                                   ),
                               ]
                           )], guild_ids=main.guild_ids)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def toggleexplore(self, ctx: SlashContext, toggle):
        try:
            player = db.queryUser({"DID": str(ctx.author.id)})
            p = Player(player['DISNAME'], player['DID'], player['AVATAR'], player['GUILD'], player['TEAM'], player['FAMILY'], player['TITLE'], player['CARD'], player['ARM'], player['PET'], player['TALISMAN'], player['CROWN_TALES'], player['DUNGEONS'], player['BOSS_WINS'], player['RIFT'], player['REBIRTH'], player['LEVEL'], player['EXPLORE'], player['SAVE_SPOT'], player['PERFORMANCE'], player['TRADING'], player['BOSS_FOUGHT'], player['DIFFICULTY'], player['STORAGE_TYPE'], player['USED_CODES'], player['BATTLE_HISTORY'], player['PVP_WINS'], player['PVP_LOSS'], player['RETRIES'], player['PRESTIGE'], player['PATRON'], player['FAMILY_PET'], player['EXPLORE_LOCATION'])
            
            if not self.explore:
                db.updateUserNoFilter({'DID': str(self.did)}, {'$set': {'EXPLORE': True}})
                message = f"You are now entering Explore Mode :milky_way: "
            
            if self.explore:
                db.updateUserNoFilter({'DID': str(self.did)}, {'$set': {'EXPLORE': False, 'EXPLORE_LOCATION': "NULL"}})
                message = "Exiting Exploration Mode :rotating_light:"
            
            await ctx.send(f"{message}")
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

    @cog_ext.cog_slash(description="Type universe you want to explore, or type all to explore all universes", guild_ids=main.guild_ids)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def exploreuniverse(self, ctx: SlashContext, universe: str):
        try:
            player = db.queryUser({"DID": str(ctx.author.id)})
            p = Player(player['DISNAME'], player['DID'], player['AVATAR'], player['GUILD'], player['TEAM'], player['FAMILY'], player['TITLE'], player['CARD'], player['ARM'], player['PET'], player['TALISMAN'], player['CROWN_TALES'], player['DUNGEONS'], player['BOSS_WINS'], player['RIFT'], player['REBIRTH'], player['LEVEL'], player['EXPLORE'], player['SAVE_SPOT'], player['PERFORMANCE'], player['TRADING'], player['BOSS_FOUGHT'], player['DIFFICULTY'], player['STORAGE_TYPE'], player['USED_CODES'], player['BATTLE_HISTORY'], player['PVP_WINS'], player['PVP_LOSS'], player['RETRIES'], player['PRESTIGE'], player['PATRON'], player['FAMILY_PET'], player['EXPLORE_LOCATION'])
            await ctx.send(f"{p.set_explore(universe)}")
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


    @cog_ext.cog_slash(description="Set Explore Channel", guild_ids=main.guild_ids)
    async def setexplorechannel(self, ctx: SlashContext):
        if ctx.author.guild_permissions.administrator:
            guild = ctx.guild
            server_channel = ctx.channel
            server_query = {'GNAME': str(guild), 'EXP_CHANNEL': str(server_channel)}
            try:
                response = db.queryServer({'GNAME': str(guild)})
                if response:
                    update_channel = db.updateServer({'GNAME': str(guild)}, {'$set': {'EXP_CHANNEL': str(server_channel)}})
                    await ctx.send(f"Explore Channel updated to **{server_channel}**")
                    return
                else:
                    update_channel = db.createServer(data.newServer(server_query))
                    await ctx.send("Explore Channel set.")
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
        else:
            await ctx.send("Admin command only.")
            return


    @cog_ext.cog_slash(description="Create Default Server Explore Channel", guild_ids=main.guild_ids)
    async def createexplorechannel(self, ctx: SlashContext):
        guild = ctx.guild
        categoryname = "Explore"
        channelname = "explore-encounters"
        try:
            if ctx.author.guild_permissions.administrator == True:
                category = discord.utils.get(guild.categories, name=categoryname)
                if category is None: #If there's no category matching with the `name`
                    category = await guild.create_category_channel(categoryname)
                    setchannel = await guild.create_text_channel(channelname, category=category)
                    await ctx.send(f"New **Explore** Category and **{channelname}** Channel Created!")
                    await setchannel.send("**Explore Channel Set**")
                    return setchannel

                else: #Else if it found the categoty
                    setchannel = discord.utils.get(guild.text_channels, name=channelname)
                    if channel is None:
                        setchannel = await guild.create_text_channel(channelname, category=category)
                        await ctx.send(f"New Explore Channel is **{channelname}**")
                        await setchannel.send("**Explore Channel Set**")
                    else:
                        await ctx.send(f"Explore Channel Already Exist **{channelname}**")
                        await setchannel.send(f"{ctx.author.mention} Explore Here")            
                
            # else:
            #     print("Not Admin")
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
    

    @cog_ext.cog_slash(description="Duo pve to earn cards, accessories, gold, gems, and more with your AI companion",
                       options=[
                           create_option(
                               name="deck",
                               description="AI Preset (this is from your preset list)",
                               option_type=3,
                               required=True,
                               choices=[
                                   create_choice(
                                       name="Preset 1",
                                       value="1"
                                   ),
                                   create_choice(
                                       name="Preset 2",
                                       value="2"
                                   ),
                                   create_choice(
                                       name="Preset 3",
                                       value="3"
                                   )
                               ]
                           ),
                           create_option(
                               name="mode",
                               description="Difficulty Level",
                               option_type=3,
                               required=True,
                               choices=[
                                   create_choice(
                                       name="⚔️ Duo Tales (Normal)",
                                       value="DTales"
                                   ),
                                   create_choice(
                                       name="🔥 Duo Dungeon (Hard)",
                                       value="DDungeon"
                                   )
                               ]
                           )
                       ]
        , guild_ids=main.guild_ids)
    async def duo(self, ctx: SlashContext, deck: int, mode: str):
        a_registered_player = await crown_utilities.player_check(ctx)
        if not a_registered_player:
            return

        U_modes = ['ATales', 'Tales', 'CTales', 'DTales']
        D_modes = ['CDungeon', 'DDungeon', 'Dungeon', 'ADungeon']
        B_MODES = ['Boss', 'CBoss']
        try:
            # await ctx.defer()
            deck = int(deck)
            if deck != 1 and deck != 2 and deck != 3:
                await ctx.send("Not a valid Deck Option")
                return
            deckNumber = deck - 1
            sowner = db.queryUser({'DID': str(ctx.author.id)})
            oteam = sowner['TEAM']
            ofam = sowner['FAMILY']
            cowner = sowner
            cteam = oteam
            cfam = ofam
            # if sowner['DIFFICULTY'] != "EASY":
            #     if sowner['LEVEL'] < 8:
            #         await ctx.send(f"🔓 Unlock **Duo** by completing **Floor 7** of the 🌑 **Abyss**! Use **Abyss** in /solo to enter the abyss.")
            #         return
            
            if sowner['DIFFICULTY'] == "EASY" and mode in D_modes or mode in B_MODES:
                await ctx.send("Dungeons and Boss fights unavailable on Easy Mode! Use /difficulty to change your difficulty setting.")
                return


            if mode in D_modes and sowner['LEVEL'] < 41 and int(sowner['PRESTIGE']) == 0:
                await ctx.send("🔓 Unlock **Duo Dungeons** by completing **Floor 40** of the 🌑 **Abyss**! Use **Abyss** in /solo to enter the abyss.")
                return



            universe_selection = await select_universe(self, ctx, sowner, oteam, ofam, mode, None)
            if not universe_selection:
                return
            selected_universe = universe_selection['SELECTED_UNIVERSE']
            universe = universe_selection['UNIVERSE_DATA']
            crestlist = universe_selection['CREST_LIST']
            crestsearch = universe_selection['CREST_SEARCH']
            currentopponent =  universe_selection['CURRENTOPPONENT']

            if mode in D_modes:
                completed_universes = universe_selection['COMPLETED_DUNGEONS']
            else:
                completed_universes = universe_selection['COMPLETED_TALES']
            if crestsearch:
                oguild = universe_selection['OGUILD']
            else:
                oguild = "PCG"

            await battle_commands(self, ctx, mode, universe, selected_universe, completed_universes, oguild, crestlist,
                                  crestsearch, sowner, oteam, ofam, currentopponent, cowner, cteam, cfam, deckNumber,
                                  None, None, None, None, None)
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


    @cog_ext.cog_slash(description="Co-op pve to earn cards, accessories, gold, gems, and more with friends",
                       options=[
                           create_option(
                               name="user",
                               description="player you want to co-op with",
                               option_type=6,
                               required=True
                           ),
                           create_option(
                               name="mode",
                               description="Difficulty Level",
                               option_type=3,
                               required=True,
                               choices=[
                                   create_choice(
                                       name="⚔️ Co-Op Tales (Normal)",
                                       value="CTales"
                                   ),
                                   create_choice(
                                       name="🔥 Co-Op Dungeon (Hard)",
                                       value="CDungeon"
                                   ),
                                   create_choice(
                                       name="👹 Co-Op Boss Enounter (Extreme)",
                                       value="CBoss"
                                   ),
                               ]
                           )
                       ]
        , guild_ids=main.guild_ids)
    async def coop(self, ctx: SlashContext, user: User, mode: str):
        a_registered_player = await crown_utilities.player_check(ctx)
        if not a_registered_player:
            return

        try:
            player = db.queryUser({'DID': str(ctx.author.id)})
            player2 = db.queryUser({'DID': str(user.id)})
            p1 = Player(player['DISNAME'], player['DID'], player['AVATAR'], player['GUILD'], player['TEAM'], player['FAMILY'], player['TITLE'], player['CARD'], player['ARM'], player['PET'], player['TALISMAN'], player['CROWN_TALES'], player['DUNGEONS'], player['BOSS_WINS'], player['RIFT'], player['REBIRTH'], player['LEVEL'], player['EXPLORE'], player['SAVE_SPOT'], player['PERFORMANCE'], player['TRADING'], player['BOSS_FOUGHT'], player['DIFFICULTY'], player['STORAGE_TYPE'], player['USED_CODES'], player['BATTLE_HISTORY'], player['PVP_WINS'], player['PVP_LOSS'], player['RETRIES'], player['PRESTIGE'], player['PATRON'], player['FAMILY_PET'], player['EXPLORE_LOCATION'])    
            p2 = Player(player2['DISNAME'], player2['DID'], player2['AVATAR'], player2['GUILD'], player2['TEAM'], player2['FAMILY'], player2['TITLE'], player2['CARD'], player2['ARM'], player2['PET'], player2['TALISMAN'], player2['CROWN_TALES'], player2['DUNGEONS'], player2['BOSS_WINS'], player2['RIFT'], player2['REBIRTH'], player2['LEVEL'], player2['EXPLORE'], player2['SAVE_SPOT'], player2['PERFORMANCE'], player2['TRADING'], player2['BOSS_FOUGHT'], player2['DIFFICULTY'], player2['STORAGE_TYPE'], player2['USED_CODES'], player2['BATTLE_HISTORY'], player2['PVP_WINS'], player2['PVP_LOSS'], player2['RETRIES'], player2['PRESTIGE'], player2['PATRON'], player2['FAMILY_PET'], player2['EXPLORE_LOCATION'])    
            battle = Battle(mode, p1)


            universe_selection = await select_universe(self, ctx, p1, mode, p2)
            if not universe_selection:
                return

            await battle_commands(self, ctx, battle, p1, None, p2)
        
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


    @cog_ext.cog_slash(description="pve to earn cards, accessories, gold, gems, and more as a solo player",
                    options=[
                        create_option(
                            name="mode",
                            description="abyss: climb ladder, tales: normal pve mode, dungeon: hard pve run, and boss: extreme encounters",
                            option_type=3,
                            required=True,
                            choices=[
                                create_choice(
                                    name="🆘 The Tutorial",
                                    value="Tutorial"
                                ),
                                create_choice(
                                    name="🌑 The Abyss!",
                                    value="Abyss"
                                ),
                                create_choice(
                                    name="⚔️ Tales & Scenario Battles!",
                                    value="Tales"
                                ),
                                create_choice(
                                    name="🔥 Dungeon Run!",
                                    value="Dungeon"
                                ),
                                create_choice(
                                    name="👹 Boss Encounter!",
                                    value="Boss"
                                ),
                            ]
                        )
                    ]
        , guild_ids=main.guild_ids)
    async def solo(self, ctx: SlashContext, mode: str):
        a_registered_player = await crown_utilities.player_check(ctx)
        if not a_registered_player:
            return
        
        try:
            # await ctx.defer()

            player = db.queryUser({'DID': str(ctx.author.id)})
            p = Player(player['DISNAME'], player['DID'], player['AVATAR'], player['GUILD'], player['TEAM'], player['FAMILY'], player['TITLE'], player['CARD'], player['ARM'], player['PET'], player['TALISMAN'], player['CROWN_TALES'], player['DUNGEONS'], player['BOSS_WINS'], player['RIFT'], player['REBIRTH'], player['LEVEL'], player['EXPLORE'], player['SAVE_SPOT'], player['PERFORMANCE'], player['TRADING'], player['BOSS_FOUGHT'], player['DIFFICULTY'], player['STORAGE_TYPE'], player['USED_CODES'], player['BATTLE_HISTORY'], player['PVP_WINS'], player['PVP_LOSS'], player['RETRIES'], player['PRESTIGE'], player['PATRON'], player['FAMILY_PET'], player['EXPLORE_LOCATION'])    

                         
            if p.get_locked_feature(mode):
                await ctx.send(p._locked_feature_message)
                return

            universe_selection = await select_universe(self, ctx, p, mode, None)
            
            if universe_selection == None:
                return

            battle = Battle(mode, p)


            if battle.mode == "Abyss":
                await abyss(self, ctx)
                return

            if battle.mode == "Tutorial":
                await tutorial(self, ctx)
                return

            battle.set_universe_selection_config(universe_selection)
                
            await battle_commands(self, ctx, battle, p, None, _player2=None)
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
            guild = self.bot.get_guild(main.guild_id)
            channel = guild.get_channel(main.guild_channel)
            await channel.send(f"'PLAYER': **{str(ctx.author)}**, 'GUILD': **{str(ctx.author.guild)}**,  TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")
            return


    @cog_ext.cog_slash(description="pvp battle against a friend or rival", guild_ids=main.guild_ids)
    async def pvp(self, ctx: SlashContext, opponent: User):
        try:
            await ctx.defer()

            a_registered_player = await crown_utilities.player_check(ctx)
            if not a_registered_player:
                return
            mode = "PVP"
            player = db.queryUser({'DID': str(ctx.author.id)})
            player2 = db.queryUser({'DID': str(opponent.id)})
            p1 = Player(player['DISNAME'], player['DID'], player['AVATAR'], player['GUILD'], player['TEAM'], player['FAMILY'], player['TITLE'], player['CARD'], player['ARM'], player['PET'], player['TALISMAN'], player['CROWN_TALES'], player['DUNGEONS'], player['BOSS_WINS'], player['RIFT'], player['REBIRTH'], player['LEVEL'], player['EXPLORE'], player['SAVE_SPOT'], player['PERFORMANCE'], player['TRADING'], player['BOSS_FOUGHT'], player['DIFFICULTY'], player['STORAGE_TYPE'], player['USED_CODES'], player['BATTLE_HISTORY'], player['PVP_WINS'], player['PVP_LOSS'], player['RETRIES'], player['PRESTIGE'], player['PATRON'], player['FAMILY_PET'], player['EXPLORE_LOCATION'])    
            p2 = Player(player2['DISNAME'], player2['DID'], player2['AVATAR'], player2['GUILD'], player2['TEAM'], player2['FAMILY'], player2['TITLE'], player2['CARD'], player2['ARM'], player2['PET'], player2['TALISMAN'], player2['CROWN_TALES'], player2['DUNGEONS'], player2['BOSS_WINS'], player2['RIFT'], player2['REBIRTH'], player2['LEVEL'], player2['EXPLORE'], player2['SAVE_SPOT'], player2['PERFORMANCE'], player2['TRADING'], player2['BOSS_FOUGHT'], player2['DIFFICULTY'], player2['STORAGE_TYPE'], player2['USED_CODES'], player2['BATTLE_HISTORY'], player2['PVP_WINS'], player2['PVP_LOSS'], player2['RETRIES'], player2['PRESTIGE'], player2['PATRON'], player2['FAMILY_PET'], player2['EXPLORE_LOCATION'])    
            battle = Battle(mode, p1)
            battle.set_tutorial(p2.did)
            
            if p1.did == p2.did:
                await ctx.send("You cannot PVP against yourself.", hidden=True)
                return
            await ctx.send("🆚 Building PVP Match...", delete_after=10)

            starttime = time.asctime()
            h_gametime = starttime[11:13]
            m_gametime = starttime[14:16]
            s_gametime = starttime[17:19]

            if p1.get_locked_feature(mode):
                await ctx.send(p1._locked_feature_message)
                return
            if p2.get_locked_feature(mode):
                await ctx.send(p2._locked_feature_message)
                return

            await battle_commands(self, ctx, mode, battle, p1, None, p2)

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
                'PLAYER': str(ctx.author),
                'type': type(ex).__name__,
                'message': str(ex),
                'trace': trace
            }))
            guild = self.bot.get_guild(main.guild_id)
            channel = guild.get_channel(main.guild_channel)
            await channel.send(f"'PLAYER': **{str(ctx.author)}**, 'GUILD': **{str(ctx.author.guild)}**,  TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")
            return


    @cog_ext.cog_slash(description="Start an Association Raid", guild_ids=main.guild_ids)
    async def raid(self, ctx: SlashContext, guild: str):
        a_registered_player = await crown_utilities.player_check(ctx)
        if not a_registered_player:
            return

        try:
            guildname = guild
            private_channel = ctx
            if isinstance(private_channel.channel, discord.channel.DMChannel):
                await private_channel.send(m.SERVER_FUNCTION_ONLY)
                return
            starttime = time.asctime()
            h_gametime = starttime[11:13]
            m_gametime = starttime[14:16]
            s_gametime = starttime[17:19]

            # Get Session Owner Disname for scoring
            sowner = db.queryUser({'DID': str(ctx.author.id)})
            if sowner['DIFFICULTY'] == "EASY":
                await ctx.send("Raiding is unavailable on Easy Mode! Use /difficulty to change your difficulty setting.")
                return

            oteam = sowner['TEAM']
            oteam_info = db.queryTeam({'TEAM_NAME': oteam.lower()})
            oguild_name = "PCG"
            shield_test_active = False
            shield_training_active = False
            if oteam_info:
                oguild_name = oteam_info['GUILD']
                oguild = db.queryGuildAlt({'GNAME': oguild_name})
            player_guild = sowner['GUILD']

            if oguild_name == "PCG":
                await ctx.send(m.NO_GUILD, delete_after=5)
                return
            if oguild['SHIELD'] == sowner['DISNAME']:
                shield_training_active = True
            elif player_guild == guildname:
                shield_test_active = True
                

            guild_query = {'GNAME': guildname}
            guild_info = db.queryGuildAlt(guild_query)
            guild_shield = ""

            if not guild_info:
                await ctx.send(m.GUILD_DOESNT_EXIST, delete_after=5)
                return
            guild_shield = guild_info['SHIELD']
            shield_id = guild_info['SDID']
            guild_hall = guild_info['HALL']
            hall_info = db.queryHall({'HALL': str(guild_hall)})
            hall_def = hall_info['DEFENSE']
            t_user = db.queryUser({'DID': shield_id})
            tteam_name = t_user['TEAM']
            tteam_info = db.queryTeam({'TEAM_NAME': tteam_name.lower()})
            tteam = tteam_info['TEAM_NAME']
            tguild = tteam_info['GUILD']
            if tteam_info:
                tguild = tteam_info['GUILD']
            tarm = db.queryArm({'ARM': t_user['ARM']})
            ttitle = db.queryTitle({'TITLE': t_user['TITLE']})
            
            mode = "RAID"

            # Guild Fees
            title_match_active = False
            fee = hall_info['FEE']
            if oguild_name == tguild:
                title_match_active = True

            o = db.queryCard({'NAME': sowner['CARD']})
            otitle = db.queryTitle({'TITLE': sowner['TITLE']})

            t = db.queryCard({'NAME': t_user['CARD']})
            ttitle = db.queryTitle({'TITLE': t_user['TITLE']})
            
            if private_channel:
                await battle_commands(self, ctx, mode, hall_info, title_match_active, shield_test_active, oguild, shield_training_active, None, sowner, oteam, None, t_user,tteam, tguild, None, None, None, None, None, None, None)
            else:
                await ctx.send("Failed to start raid battle!")
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
                'PLAYER': str(ctx.author),
                'type': type(ex).__name__,
                'message': str(ex),
                'trace': trace
            }))
            guild = self.bot.get_guild(main.guild_id)
            channel = guild.get_channel(main.guild_channel)
            await channel.send(f"'PLAYER': **{str(ctx.author)}**, 'GUILD': **{str(ctx.author.guild)}**,  TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")
            return


    @cog_ext.cog_slash(description="View all available Universes and their cards, summons, destinies, and accessories", guild_ids=main.guild_ids)
    async def universes(self, ctx: SlashContext):
        a_registered_player = await crown_utilities.player_check(ctx)
        if not a_registered_player:
            return

        try:
            universe_data = db.queryAllUniverse()
            # user = db.queryUser({'DID': str(ctx.author.id)})
            universe_embed_list = []
            for uni in universe_data:
                available = ""
                # if len(uni['CROWN_TALES']) > 2:
                if uni['CROWN_TALES']:
                    available = f"{crown_utilities.crest_dict[uni['TITLE']]}"
                    
                    tales_list = ", ".join(uni['CROWN_TALES'])

                    embedVar = discord.Embed(title= f"{uni['TITLE']}", description=textwrap.dedent(f"""
                    {crown_utilities.crest_dict[uni['TITLE']]} **Number of Fights**: :crossed_swords: **{len(uni['CROWN_TALES'])}**
                    🎗️ **Universe Title**: {uni['UTITLE']}
                    🦾 **Universe Arm**: {uni['UARM']}
                    🧬 **Universe Summon**: {uni['UPET']}

                    :crossed_swords: **Tales Order**: {tales_list}
                    """))
                    embedVar.set_image(url=uni['PATH'])
                    universe_embed_list.append(embedVar)
                

            buttons = [
                manage_components.create_button(style=3, label="🎴 Cards", custom_id="cards"),
                manage_components.create_button(style=1, label="🎗️ Titles", custom_id="titles"),
                manage_components.create_button(style=1, label="🦾 Arms", custom_id="arms"),
                manage_components.create_button(style=1, label="🧬 Summons", custom_id="summons"),
                manage_components.create_button(style=2, label="✨ Destinies", custom_id="destinies")
            ]
            custom_action_row = manage_components.create_actionrow(*buttons)

            async def custom_function(self, button_ctx):
                universe_name = str(button_ctx.origin_message.embeds[0].title)
                await button_ctx.defer(ignore=True)
                if button_ctx.author == ctx.author:
                    if button_ctx.custom_id == "cards":
                        await cardlist(self, ctx, universe_name)
                        #self.stop = True
                    if button_ctx.custom_id == "titles":
                        await titlelist(self, ctx, universe_name)
                        #self.stop = True
                    if button_ctx.custom_id == "arms":
                        await armlist(self, ctx, universe_name)
                        #self.stop = True
                    if button_ctx.custom_id == "summons":
                        await summonlist(self, ctx, universe_name)
                        #self.stop = True
                    if button_ctx.custom_id == "destinies":
                        await destinylist(self, ctx, universe_name)
                        #self.stop = True
                else:
                    await ctx.send("This is not your command.")


            await Paginator(bot=self.bot, ctx=ctx, useQuitButton=True, deleteAfterTimeout=True, pages=universe_embed_list, customActionRow=[
                custom_action_row,
                custom_function,
            ]).run()


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


    @cog_ext.cog_slash(description="View all Homes for purchase", guild_ids=main.guild_ids)
    async def houses(self, ctx: SlashContext):
        a_registered_player = await crown_utilities.player_check(ctx)
        if not a_registered_player:
            return


        house_data = db.queryAllHouses()
        user = db.queryUser({'DID': str(ctx.author.id)})

        house_list = []
        for homes in house_data:
            house_list.append(
                f":house: | {homes['HOUSE']}\n:coin: | **COST: **{'{:,}'.format(homes['PRICE'])}\n:part_alternation_mark: | **MULT: **{homes['MULT']}x\n_______________")

        total_houses = len(house_list)
        while len(house_list) % 10 != 0:
            house_list.append("")

        # Check if divisible by 10, then start to split evenly
        if len(house_list) % 10 == 0:
            first_digit = int(str(len(house_list))[:1])
            houses_broken_up = np.array_split(house_list, first_digit)

        # If it's not an array greater than 10, show paginationless embed
        if len(house_list) < 10:
            embedVar = discord.Embed(title=f"House List", description="\n".join(house_list), colour=0x7289da)
            embedVar.set_footer(text=f"{total_houses} Total Houses\n/viewhouse - View House Details")
            await ctx.send(embed=embedVar)

        embed_list = []
        for i in range(0, len(houses_broken_up)):
            globals()['embedVar%s' % i] = discord.Embed(title=f":house: House List",
                                                        description="\n".join(houses_broken_up[i]), colour=0x7289da)
            globals()['embedVar%s' % i].set_footer(text=f"{total_houses} Total Houses\n/view *House Name* `:house: It's a House` - View House Details")
            embed_list.append(globals()['embedVar%s' % i])

        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⬅️', "back")
        paginator.add_reaction('🔐', "lock")
        paginator.add_reaction('➡️', "next")
        paginator.add_reaction('⏭️', "last")
        embeds = embed_list
        await paginator.run(embeds)


    @cog_ext.cog_slash(description="View all Halls for purchase", guild_ids=main.guild_ids)
    async def halls(self, ctx: SlashContext):
        a_registered_player = await crown_utilities.player_check(ctx)
        if not a_registered_player:
            return


        hall_data = db.queryAllHalls()
        user = db.queryUser({'DID': str(ctx.author.id)})

        hall_list = []
        for homes in hall_data:
            hall_list.append(
                f":flags: | {homes['HALL']}\n🛡️ | **DEF: **{homes['DEFENSE']}\n:coin: | **COST: **{'{:,}'.format(homes['PRICE'])}\n:part_alternation_mark: | **MULT: **{homes['MULT']}x\n:moneybag: | **SPLIT: **{'{:,}'.format(homes['SPLIT'])}x\n:yen: | **FEE: **{'{:,}'.format(homes['FEE'])}\n_______________")

        total_halls = len(hall_list)
        while len(hall_list) % 10 != 0:
            hall_list.append("")

        # Check if divisible by 10, then start to split evenly
        if len(hall_list) % 10 == 0:
            first_digit = int(str(len(hall_list))[:1])
            halls_broken_up = np.array_split(hall_list, first_digit)

        # If it's not an array greater than 10, show paginationless embed
        if len(hall_list) < 10:
            embedVar = discord.Embed(title=f"Hall List", description="\n".join(hall_list), colour=0x7289da)
            embedVar.set_footer(text=f"{total_halls} Total Halls\n/viewhall - View Hall Details")
            await ctx.send(embed=embedVar)

        embed_list = []
        for i in range(0, len(halls_broken_up)):
            globals()['embedVar%s' % i] = discord.Embed(title=f":flags: Hall List",
                                                        description="\n".join(halls_broken_up[i]), colour=0x7289da)
            globals()['embedVar%s' % i].set_footer(text=f"{total_halls} Total Halls\n/view *Hall Name* `:flags: It's A Hall` - View Hall Details")
            embed_list.append(globals()['embedVar%s' % i])

        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⬅️', "back")
        paginator.add_reaction('🔐', "lock")
        paginator.add_reaction('➡️', "next")
        paginator.add_reaction('⏭️', "last")
        embeds = embed_list
        await paginator.run(embeds)


async def tutorial(self, ctx: SlashContext):
    try:
        await ctx.defer()
        a_registered_player = await crown_utilities.player_check(ctx)
        if not a_registered_player:
            return

        await ctx.send("🆚 Building Tutorial Match...", delete_after=10)
        private_channel = ctx
        starttime = time.asctime()
        h_gametime = starttime[11:13]
        m_gametime = starttime[14:16]
        s_gametime = starttime[17:19]

        # Tutorial Code
        tutorialbot = '837538366509154407'
        legendbot = '845672426113466395'
        tutorial_user = await self.bot.fetch_user(tutorialbot)
        opponent = db.queryUser({'DISNAME': str(tutorial_user)})
        oppDID = opponent['DID']
        tutorial = False
        if oppDID == tutorialbot or oppDID == legendbot:
            tutorial = True
        mode = "PVP"

        # Get Session Owner Disname for scoring
        sowner = db.queryUser({'DID': str(ctx.author.id)})
        opponent = db.queryUser({'DISNAME': str(tutorial_user)})
        oteam = sowner['TEAM']
        tteam = opponent['TEAM']
        oteam_info = db.queryTeam({'TEAM_NAME':str(oteam)})
        tteam_info = db.queryTeam({'TEAM_NAME':str(tteam)})
        if oteam_info:
            oguild = oteam_info['GUILD']
        else:
            oguild ="PCG"
        if tteam_info:
            tguild = tteam_info['GUILD']
        else:
            tguild ="PCG"

        o = db.queryCard({'NAME': sowner['CARD']})
        otitle = db.queryTitle({'TITLE': sowner['TITLE']})

        t = db.queryCard({'NAME': opponent['CARD']})
        ttitle = db.queryTitle({'TITLE': opponent['TITLE']})

        # universe = "Naruto"
        # selected_universe = {"TITLE": "Naruto"}
        if private_channel:
            await battle_commands(self, ctx, mode, None, None, None, oguild, None, None, sowner, oteam, None, opponent, tteam, tguild, None, None, None, None, None, "Tutorial", None)
        else:
            await ctx.send("Failed to start battle!")
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
            'PLAYER': str(ctx.author),
            'type': type(ex).__name__,
            'message': str(ex),
            'trace': trace
        }))
        guild = self.bot.get_guild(main.guild_id)
        channel = guild.get_channel(main.guild_channel)
        await channel.send(f"'PLAYER': **{str(ctx.author)}**, 'GUILD': **{str(ctx.author.guild)}**,  TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")
        return


async def score(owner, user: User):
    session_query = {"OWNER": str(owner), "AVAILABLE": True, "KINGSGAMBIT": False}
    session_data = db.querySession(session_query)
    teams = [x for x in session_data['TEAMS']]
    winning_team = {}
    for x in teams:
        if str(user) in x['TEAM']:
            winning_team = x
    new_score = winning_team['SCORE'] + 1
    update_query = {'$set': {'TEAMS.$.SCORE': new_score}}
    query = {"_id": session_data["_id"], "TEAMS.TEAM": str(user)}
    response = db.updateSession(session_query, query, update_query)
    reciever = db.queryUser({'DISNAME': str(user)})
    name = reciever['DISNAME']
    message = ":one: You Scored, Don't Let Up :one:"

    if response:
        message = ":one:"
    else:
        message = "Score not added. Please, try again. "

    return message


async def quest(player, opponent, mode):
    user_data = db.queryVault({'DID': str(player.id)})
    quest_data = {}
    try:
        if user_data['QUESTS']:
            for quest in user_data['QUESTS']:
                if opponent == quest['OPPONENT']:
                    quest_data = quest

            if quest_data == {}:
                return
            completion = quest_data['GOAL'] - (quest_data['WINS'] + 1)
            reward = int(quest_data['REWARD'])

            if str(mode) == "Dungeon" and completion >= 0:
                message = "Quest progressed!"
                if completion == 0:
                    await crown_utilities.bless(reward, player.id)
                    message = f"Quest Completed! :coin:{reward} has been added to your balance."

                    # server_query = {'GNAME': str(player.guild)}
                    # update_server_query = {
                    #     '$inc': {'SERVER_BALANCE': 10000}
                    # }
                    # updated_server = db.updateServer(server_query, update_server_query)

                query = {'DID': str(player.id)}
                update_query = {'$inc': {'QUESTS.$[type].' + "WINS": 2}}
                filter_query = [{'type.' + "OPPONENT": opponent}]
                resp = db.updateVault(query, update_query, filter_query)
                return message

            elif str(mode) == "Tales" and completion >= 0:
                message = "Quest progressed!"
                if completion == 0:
                    await crown_utilities.bless(reward, player.id)
                    message = f"Quest Completed! :coin:{reward} has been added to your balance."
                    # server_query = {'GNAME': str(player.guild)}
                    # update_server_query = {
                    #     '$inc': {'SERVER_BALANCE': 5000}
                    # }
                    # updated_server = db.updateServer(server_query, update_server_query)

                query = {'DID': str(player.id)}
                update_query = {'$inc': {'QUESTS.$[type].' + "WINS": 1}}
                filter_query = [{'type.' + "OPPONENT": opponent}]
                resp = db.updateVault(query, update_query, filter_query)

                return message
            else:
                return False
        else:
            return False
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


async def destiny(player, opponent, mode):
    vault = db.queryVault({'DID': str(player.id)})
    user = db.queryUser({"DID": str(player.id)})
    vault_query = {'DID': str(player.id)}
    card_info = db.queryCard({"NAME": str(user['CARD'])})
    skin_for = card_info['SKIN_FOR']
    
    hand_limit = 25
    storage_allowed_amount = user['STORAGE_TYPE'] * 15
    storage_amount = len(vault['STORAGE'])
    hand_length = len(vault['CARDS'])
    list1 = vault['CARDS']
    list2 = vault['STORAGE']
    current_cards = list1.extend(list2)

    if hand_length >= hand_limit and storage_amount >= storage_allowed_amount:
        message = f"Your storage is full. You are unable to complete the destinies until you have available storage for rewarded destiny cards."
        return message



    owned_destinies = []
    for destiny in vault['DESTINY']:
        owned_destinies.append(destiny['NAME'])

    owned_card_levels_list = []
    for c in vault['CARD_LEVELS']:
        owned_card_levels_list.append(c['CARD'])
    message = ""
    completion = 1
    try:
        if vault['DESTINY']:
            # TALES
            for destiny in vault['DESTINY']:
                if (user['CARD'] in destiny['USE_CARDS'] or skin_for in destiny['USE_CARDS']) and opponent == destiny['DEFEAT'] and mode == "Tales":
                    if destiny['WINS'] < destiny['REQUIRED']:
                        message = f"Secured a win toward **{destiny['NAME']}**. Keep it up!"
                        completion = destiny['REQUIRED'] - (destiny['WINS'] + 1)

                    if completion == 0:
                        try:
                            if destiny['EARN'] not in owned_card_levels_list:
                                # Add the CARD_LEVELS for Destiny Card
                                update_query = {'$addToSet': {
                                    'CARD_LEVELS': {'CARD': str(destiny['EARN']), 'LVL': 0, 'TIER': 0, 'EXP': 0,
                                                    'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0}}}
                                db.updateVaultNoFilter(vault_query, update_query)
                                #
                        except Exception as ex:
                            print(f"Error in Completing Destiny: {ex}")

                        if len(list1) >= 25 and storage_amount < storage_allowed_amount:
                            response = db.updateVaultNoFilter(vault_query, {'$addToSet': {'STORAGE': str(destiny['EARN'])}})
                            message = f"**{destiny['NAME']}** completed! **{destiny['EARN']}** has been added to your storage!"
                        else:
                            response = db.updateVaultNoFilter(vault_query, {'$addToSet': {'CARDS': str(destiny['EARN'])}})
                            message = f"**{destiny['NAME']}** completed! **{destiny['EARN']}** has been added to your vault!"
                        query = {'DID': str(player.id)}
                        update_query = {'$pull': {'DESTINY': {'NAME': destiny['NAME']}}}
                        resp = db.updateVaultNoFilter(query, update_query)

                        for dest in d.destiny:
                            if destiny['EARN'] in dest["USE_CARDS"] and dest['NAME'] not in owned_destinies:
                                db.updateVaultNoFilter(vault_query, {'$addToSet': {'DESTINY': dest}})
                                message = f"**DESTINY AWAITS!**\n**New Destinies** have been added to your vault."
                        await player.send(message)
                        return message

                    query = {'DID': str(player.id)}
                    update_query = {'$inc': {'DESTINY.$[type].' + "WINS": 1}}
                    filter_query = [{'type.' + "DEFEAT": opponent, 'type.' + 'USE_CARDS':user['CARD']}]
                    if user['CARD'] not in destiny['USE_CARDS']:
                        filter_query = [{'type.' + "DEFEAT": opponent, 'type.' + 'USE_CARDS':skin_for}]
                    resp = db.updateVault(query, update_query, filter_query)
                    await player.send(message)
                    return message

            # Dungeon
            for destiny in vault['DESTINY']:
                if user['CARD'] in destiny['USE_CARDS'] and opponent == destiny['DEFEAT'] and mode == "Dungeon":
                    message = f"Secured a win toward **{destiny['NAME']}**. Keep it up!"
                    completion = destiny['REQUIRED'] - (destiny['WINS'] + 3)

                    if completion <= 0:
                        try:
                            if destiny['EARN'] not in owned_card_levels_list:
                                # Add the CARD_LEVELS for Destiny Card
                                update_query = {'$addToSet': {
                                    'CARD_LEVELS': {'CARD': str(destiny['EARN']), 'LVL': 0, 'TIER': 0, 'EXP': 0,
                                                    'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0}}}
                                db.updateVaultNoFilter(vault_query, update_query)
                                #
                        except Exception as ex:
                            print(f"Error in Completing Destiny: {ex}")

                        if len(list1) >= 25 and storage_amount < storage_allowed_amount:
                            response = db.updateVaultNoFilter(vault_query, {'$addToSet': {'STORAGE': str(destiny['EARN'])}})
                            message = f"**{destiny['NAME']}** completed! **{destiny['EARN']}** has been added to your storage!"
                        else:
                            response = db.updateVaultNoFilter(vault_query, {'$addToSet': {'CARDS': str(destiny['EARN'])}})
                            message = f"**{destiny['NAME']}** completed! **{destiny['EARN']}** has been added to your vault!"
                        query = {'DID': str(player.id)}
                        update_query = {'$pull': {'DESTINY': {'NAME': destiny['NAME']}}}
                        resp = db.updateVaultNoFilter(query, update_query)

                        for dest in d.destiny:
                            if destiny['EARN'] in dest["USE_CARDS"] and dest['NAME'] not in owned_destinies:
                                db.updateVaultNoFilter(vault_query, {'$addToSet': {'DESTINY': dest}})
                                message = f"**DESTINY AWAITS!**\n**New Destinies** have been added to your vault."
                        await player.send(message)
                        return message

                    query = {'DID': str(player.id)}
                    update_query = {'$inc': {'DESTINY.$[type].' + "WINS": 3}}
                    filter_query = [{'type.' + "DEFEAT": opponent}]
                    resp = db.updateVault(query, update_query, filter_query)
                    await player.send(message)
                    return message
        
        else:
            return False
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
        await player.send(
            "There's an issue with your Destiny. Alert support.")
        return


async def summonlevel(pet, player):
    vault = db.queryVault({'DID': str(player.id)})
    player_info = db.queryUser({'DID': str(player.id)})
    family_name = player_info['FAMILY']
    
    if family_name != 'PCG':
        family_info = db.queryFamily({'HEAD':str(family_name)})
        family_summon = family_info['SUMMON']
        if family_summon['NAME'] == str(pet):
            return False
    petinfo = {}
    try:
        for x in vault['PETS']:
            if x['NAME'] == str(pet):
                petinfo = x

        lvl = petinfo['LVL']  # To Level Up -(lvl * 10 = xp required)
        lvl_req = lvl * 10
        exp = petinfo['EXP']
        petmove_text = list(petinfo.keys())[3]  # Name of the ability
        petmove_ap = list(petinfo.values())[3]  # Ability Power
        petmove_type = petinfo['TYPE']
        bond = petinfo['BOND']
        bondexp = petinfo['BONDEXP']
        bond_req = ((petmove_ap * 5) * (bond + 1))

        if lvl < 10:
            # Non Level Up Code
            if exp < (lvl_req - 1):
                query = {'DID': str(player.id)}
                update_query = {'$inc': {'PETS.$[type].' + "EXP": 1}}
                filter_query = [{'type.' + "NAME": str(pet)}]
                response = db.updateVault(query, update_query, filter_query)

            # Level Up Code
            if exp >= (lvl_req - 1):
                query = {'DID': str(player.id)}
                update_query = {'$set': {'PETS.$[type].' + "EXP": 0}, '$inc': {'PETS.$[type].' + "LVL": 1}}
                filter_query = [{'type.' + "NAME": str(pet)}]
                response = db.updateVault(query, update_query, filter_query)

        if bond < 3:
            # Non Bond Level Up Code
            if bondexp < (bond_req - 1):
                query = {'DID': str(player.id)}
                update_query = {'$inc': {'PETS.$[type].' + "BONDEXP": 1}}
                filter_query = [{'type.' + "NAME": str(pet)}]
                response = db.updateVault(query, update_query, filter_query)

            # Bond Level Up Code
            if bondexp >= (bond_req - 1):
                query = {'DID': str(player.id)}
                update_query = {'$set': {'PETS.$[type].' + "BONDEXP": 0}, '$inc': {'PETS.$[type].' + "BOND": 1}}
                filter_query = [{'type.' + "NAME": str(pet)}]
                response = db.updateVault(query, update_query, filter_query)
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
        await ctx.send(
            "There's an issue with leveling your Summon. Alert support.")
        return


async def savematch(player, card, path, title, arm, universe, universe_type, exclusive):
    matchquery = {'PLAYER': player, 'CARD': card, 'PATH': path, 'TITLE': title, 'ARM': arm, 'UNIVERSE': universe,
                  'UNIVERSE_TYPE': universe_type, 'EXCLUSIVE': exclusive}
    save_match = db.createMatch(data.newMatch(matchquery))


def starting_position(o, t):
    if o > t:
        return True
    else:
        return False


async def abyss_level_up_message(did, floor, card, title, arm):
    try:
        message = ""
        drop_message = []
        maxed_out_messages = []
        new_unlock = False
        vault_query = {'DID': did}
        vault = db.altQueryVault(vault_query)
        owned_destinies = []
        for destiny in vault['DESTINY']:
            owned_destinies.append(destiny['NAME'])
        card_info = db.queryCard({'NAME': str(card)})
        title_info = db.queryTitle({'TITLE': str(title)})
        arm = db.queryArm({'ARM':str(arm)})
        arm_arm = arm['ARM']
        floor_val = int(floor)
        coin_drop = round(100000 + (floor_val * 10000))
        durability = random.randint(75, 125)
        card_drop = card
        title_drop = title
        arm_drop = arm
        # Determine first to beat floor 100
        if floor == 100:
            all_users = db.queryAllUsers()
            first = True
            for user in all_users:
                if user['LEVEL'] == 101:
                    first = False
            if first:
                winner = {
                    'PLAYER': vault['OWNER'],
                    'DID': vault['DID'],
                    'CARD': card,
                    'TITLE': title,
                    'ARM': arm
                }
                rr = db.createGods(data.newGods(winner))

        
        if floor in abyss_floor_reward_list:
            u = await main.bot.fetch_user(did)
            tresponse = await crown_utilities.store_drop_card(u, did, title_drop, title_info['UNIVERSE'], vault, owned_destinies, coin_drop, coin_drop, "Abyss", False, 0, "titles")
            # current_titles = vault['TITLES']
            # if len(current_titles) >=25:
            #     drop_message.append("You have max amount of Titles. You did not receive the **Floor Title**.")
            # elif title in current_titles:
            #     maxed_out_messages.append(f"You already own {title_drop} so you did not receive it.")
            # else:
            #     db.updateVaultNoFilter(vault_query,{'$addToSet':{'TITLES': str(title_drop)}}) 
            #     drop_message.append(f"🎗️ **{title_drop}**")

            aresponse = await crown_utilities.store_drop_card(u, did, arm_arm, arm['UNIVERSE'], vault, durability, coin_drop, coin_drop, "Abyss", False, 0, "arms")
            # current_arms = []
            # for arm in vault['ARMS']:
            #     current_arms.append(arm['ARM'])
            # if len(current_arms) >=25:
            #     maxed_out_messages.append("You have max amount of Arms. You did not receive the **Floor Arm**.")
            # elif arm_arm in current_arms:
            #     maxed_out_messages.append(f"You already own {arm_drop['ARM']} so you did not receive it.")
            # else:
            #     db.updateVaultNoFilter(vault_query,{'$addToSet':{'ARMS': {'ARM': str(arm_drop['ARM']), 'DUR': 25}}})
            #     drop_message.append(f"🦾 **{arm_drop['ARM']}**")
            
            cresponse = await crown_utilities.store_drop_card(u, did, card_drop, card_info['UNIVERSE'], vault, owned_destinies, coin_drop, coin_drop, "Abyss", False, 0, "cards")
            drop_message.append(tresponse)
            drop_message.append(aresponse)
            drop_message.append(cresponse)
            # current_cards = vault['CARDS']
            # if len(current_cards) >= 25:
            #     maxed_out_messages.append("You have max amount of Cards. You did not earn receive **Floor Card**.")
            # elif card in current_cards:
            #     maxed_out_messages.append(f"You already own {card_drop} so you did not receive it.")
            # else:
            #     db.updateVaultNoFilter(vault_query,{'$addToSet': {'CARDS': str(card_drop)}})
            #     drop_message.append(f"🎴 **{card_drop}**")

            
            # owned_card_levels_list = []
            # for c in vault['CARD_LEVELS']:
            #     owned_card_levels_list.append(c['CARD'])

            # owned_destinies = []
            # for destiny in vault['DESTINY']:
            #     owned_destinies.append(destiny['NAME'])
            
            # if card not in owned_card_levels_list:
            #     update_query = {'$addToSet': {'CARD_LEVELS': {'CARD': str(card), 'LVL': 0, 'TIER': 0, 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0}}}
            #     r = db.updateVaultNoFilter(vault_query, update_query)

            # counter = 2
            # for destiny in d.destiny:
            #     if card in destiny["USE_CARDS"] and destiny['NAME'] not in owned_destinies:
            #         counter = counter - 1
            #         db.updateVaultNoFilter(vault_query, {'$addToSet': {'DESTINY': destiny}})
            #         if counter >=1:
            #             drop_message.append(f"**DESTINY AWAITS!**")
        else:
            drop_message.append(f":coin: **{'{:,}'.format(coin_drop)}** has been added to your vault!")

        # if floor == 0:
        #     message = "🎊 Congratulations! 🎊 You unlocked **Shop!**. Use the **/shop** command to purchase Cards, Titles and Arms!"
        #     new_unlock = True
        
        # if floor == 2:
        #     message = "🎊 Congratulations! 🎊 You unlocked **Tales! and Scenarios!**. Use the **/solo** command to battle through Universes to earn Cards, Titles, Arms, Summons, and Money!"
        #     new_unlock = True

        # if floor == 8:
        #     message = "🎊 Congratulations! 🎊 You unlocked **Crafting!**. Use the **/craft** command to craft Universe Items such as Universe Souls, or even Destiny Line Wins toward Destiny Cards!"
        #     new_unlock = True

        if floor == 3:
            message = "🎊 Congratulations! 🎊 You unlocked **PVP and Guilds**. Use /pvp to battle another player or join together to form a Guild! Use /help to learn more.!"
            new_unlock = True

        if floor == 31:
            message = "🎊 Congratulations! 🎊 You unlocked **Marriage**. You're now able to join Families!Share summons and purchase houses.Use /help to learn more about  Family commands!"
            new_unlock = True
            
        if floor == 10:
            message = "🎊 Congratulations! 🎊 You unlocked **Trading**. Use the **/trade** command to Trade Cards, Titles and Arms with other players!"
            new_unlock = True

        # if floor == 3:
        #     message = "🎊 Congratulations! 🎊 You unlocked **PVP**. \nUse the /**pvp** command to PVP against other players!"
        #     new_unlock = True

        if floor == 20:
            message = "🎊 Congratulations! 🎊 You unlocked **Gifting**. Use the **/gift** command to gift players money!"
            new_unlock = True
        
        # if floor == 3:
        #     message = "🎊 Congratulations! 🎊 You unlocked **Co-Op**. Use the **/coop** to traverse Tales with other players!"
        #     new_unlock = True
            
        if floor == 15:
            message = "🎊 Congratulations! 🎊 You unlocked **Associations**. Use the **/oath** to create an association with another Guild Owner!"
            new_unlock = True

        if floor == 25:
            message = "🎊 Congratulations! 🎊 You unlocked **Explore Mode**. Explore Mode allows for Cards to spawn randomly with Bounties! If you defeat the Card you will earn that Card + it's Bounty! Happy Hunting!"
            new_unlock = True

        if floor == 40:
            message = "🎊 Congratulations! 🎊 You unlocked **Dungeons**. Use the **/solo** command and select Dungeons to battle through the Hard Mode of Universes to earn super rare Cards, Titles, and Arms!"
            new_unlock = True
            
        # if floor == 7:
        #     message = "🎊 Congratulations! 🎊 You unlocked **Duo**. Use the **/duo** command and select a Difficulty and a Preset to bring into Tales with you!"
        #     new_unlock = True

        if floor == 60:
            message = "🎊 Congratulations! 🎊 You unlocked **Bosses**. Use the **/solo** command and select Boss to battle Universe Bosses too earn ultra rare Cards, Titles, and Arms!"
            new_unlock = True
            
        if floor == 100:
            message = "🎊 Congratulations! 🎊 You unlocked **Soul Exchange**. Use the **/exchange** command and Exchange any boss souls for cards from their respective universe! This will Reset your Abyss Level!"
            new_unlock = True


        return {"MESSAGE": message, "NEW_UNLOCK": new_unlock, "DROP_MESSAGE": drop_message}
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

# DONT REMOVE THIS
cache = dict()

def get_card(url, cardname, cardtype):
    try:
        # save_path = f"image_cache/{str(cardtype)}/{str(cardname)}.png"
        # # print(save_path)
        
        # if url not in cache:
        #     # print("Not in Cache")
        #     cache[url] = save_path
        #     im = Image.open(requests.get(url, stream=True).raw)
        #     im.save(f"{save_path}", "PNG")
        #     # print(f"NO : {cardname}")
        #     return im

        # else:
        #     # print("In Cache")
        #     im = Image.open(cache[url])
        #     # print(f"YES : {cardname}")
        #     return im
        im = Image.open(requests.get(url, stream=True).raw)
        return im
           
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

     
def showsummon(url, summon, message, lvl, bond):
    # Card Name can be 16 Characters before going off Card
    # Lower Card Name Font once after 16 characters
    try:
        im = Image.open(requests.get(url, stream=True).raw)

        draw = ImageDraw.Draw(im)

        # Font Size Adjustments
        # Name not go over Card
        name_font_size = 80
        if len(list(summon)) >= 10:
            name_font_size = 45
        if len(list(summon)) >= 14:
            name_font_size = 36
        

        header = ImageFont.truetype("YesevaOne-Regular.ttf", name_font_size)
        s = ImageFont.truetype("Roboto-Bold.ttf", 22)
        h = ImageFont.truetype("YesevaOne-Regular.ttf", 37)
        m = ImageFont.truetype("Roboto-Bold.ttf", 25)
        r = ImageFont.truetype("Freedom-10eM.ttf", 40)
        lvl_font = ImageFont.truetype("Neuton-Bold.ttf", 68)
        health_and_stamina_font = ImageFont.truetype("Neuton-Light.ttf", 41)
        attack_and_shield_font = ImageFont.truetype("Neuton-Bold.ttf", 48)
        moveset_font = ImageFont.truetype("antonio.regular.ttf", 40)
        rhs = ImageFont.truetype("destructobeambb_bold.ttf", 35)
        stats = ImageFont.truetype("Freedom-10eM.ttf", 30)
        card_details_font_size = ImageFont.truetype("destructobeambb_bold.ttf", 25)
        card_levels = ImageFont.truetype("destructobeambb_bold.ttf", 40)

        # Pet Name
        draw.text((600, 160), summon, (255, 255, 255), font=header, stroke_width=1, stroke_fill=(0, 0, 0),
                    align="left")

        # Level
        lvl_sizing = (89, 70)
        if int(lvl) > 9:
            lvl_sizing = (75, 70)
 
        draw.text(lvl_sizing, f"{lvl}", (255, 255, 255), font=lvl_font, stroke_width=1, stroke_fill=(0, 0, 0),
                    align="center")
        draw.text((1096, 65), f"{bond}", (255, 255, 255), font=lvl_font, stroke_width=1, stroke_fill=(0, 0, 0),
                    align="center")

        lines = textwrap.wrap(message, width=28)
        y_text = 330
        for line in lines:
            font=moveset_font
            width, height = font.getsize(line)
            with Pilmoji(im) as pilmoji:
                pilmoji.text(((1730 - width) / 2, y_text), line, (255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
            y_text += height


        with BytesIO() as image_binary:
            im.save(image_binary, "PNG")
            image_binary.seek(0)
            # await ctx.send(file=discord.File(fp=image_binary,filename="image.png"))
            file = discord.File(fp=image_binary,filename="pet.png")
            return file

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


def setup(bot):
    bot.add_cog(CrownUnlimited(bot))



async def abyss(self, ctx: SlashContext, _player):
    await ctx.defer()
    a_registered_player = await crown_utilities.player_check(ctx)
    if not a_registered_player:
        return

    mode = "ABYSS"
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(m.SERVER_FUNCTION_ONLY)
        return

    try:
        # Use Battle Class Method "set_abyss_config" here which populates
        abyss = Battle(mode, _player)

        abyss_embed = abyss.set_abyss_config(_player)

        abyss_buttons = [
            manage_components.create_button(
                style=ButtonStyle.blue,
                label="Begin",
                custom_id="Yes"
            ),
            manage_components.create_button(
                style=ButtonStyle.red,
                label="Quit",
                custom_id="No"
            )
        ]

        abyss_buttons_action_row = manage_components.create_actionrow(*abyss_buttons)


        msg = await ctx.send(embed=abyss_embed, components=[abyss_buttons_action_row])

        def check(button_ctx):
            return button_ctx.author == ctx.author

        try:
            button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[
                abyss_buttons_action_row, abyss_buttons], timeout=120, check=check)

            if button_ctx.custom_id == "Yes":
                await button_ctx.defer(ignore=True)
                await msg.edit(components=[])

                if abyss.abyss_player_card_tier_is_banned:
                    await ctx.send(
                        f":x: We're sorry! The tier of your equipped card is banned on floor {floor}. Please, try again with another card.")
                    return
                
                await battle_commands(self, ctx, abyss, _player, None, _player2=None)

            elif button_ctx.custom_id == "No":
                await button_ctx.send("Leaving the Abyss...")
                await msg.edit(components=[])
                return
            else:
                await button_ctx.send("Leaving the Abyss...")
                await msg.edit(components=[])
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
            guild = self.bot.get_guild(main.guild_id)
            channel = guild.get_channel(main.guild_channel)
            await channel.send(f"'PLAYER': **{str(ctx.author)}**, 'GUILD': **{str(ctx.author.guild)}**,  TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")
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
        guild = self.bot.get_guild(main.guild_id)
        channel = guild.get_channel(main.guild_channel)
        await channel.send(f"'PLAYER': **{str(ctx.author)}**, TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")
        return


async def scenario(self, ctx: SlashContext, _player, universe: str):
    a_registered_player = await crown_utilities.player_check(ctx)
    if not a_registered_player:
        return

    mode = "SCENARIO"
    try:
        scenario = Battle(mode, _player)
        scenario._selected_universe = universe
        embed_list = scenario.set_scenario_selection()
        
        if not embed_list:
            await ctx.send(f"There are currently no Scenario battles available in **{universe}**.")

        buttons = [
            manage_components.create_button(style=3, label="Start This Scenario Battle!", custom_id="start"),
        ]
        custom_action_row = manage_components.create_actionrow(*buttons)


        async def custom_function(self, button_ctx):
            if button_ctx.author == ctx.author:
                selected_scenario = str(button_ctx.origin_message.embeds[0].title)
                if button_ctx.custom_id == "start":
                    await button_ctx.defer(ignore=True)
                    selected_scenario = db.queryScenario({'TITLE':selected_scenario})
                    scenario.set_scenario_config(selected_scenario)
                    await battle_commands(self, ctx, scenario, _player, None, _player2=None)
                    self.stop = True
            else:
                await ctx.send("This is not your prompt! Shoo! Go Away!")


        await Paginator(bot=self.bot, ctx=ctx, useQuitButton=True, pages=embed_list, timeout=60, customActionRow=[
            custom_action_row,
            custom_function,
        ]).run()

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


async def cardlist(self, ctx: SlashContext, universe: str):
    a_registered_player = await crown_utilities.player_check(ctx)
    if not a_registered_player:
        return

    universe_data = db.queryUniverse({'TITLE': {"$regex": str(universe), "$options": "i"}})
    user = db.queryUser({'DID': str(ctx.author.id)})
    list_of_cards = db.queryAllCardsBasedOnUniverse({'UNIVERSE': {"$regex": str(universe), "$options": "i"}})
    cards = [x for x in list_of_cards]
    dungeon_card_details = []
    tales_card_details = []
    destiny_card_details = []
    for card in cards:
        moveset = card['MOVESET']
        move3 = moveset[2]
        move2 = moveset[1]
        move1 = moveset[0]
        basic_attack_emoji = crown_utilities.set_emoji(list(move1.values())[2])
        super_attack_emoji = crown_utilities.set_emoji(list(move2.values())[2])
        ultimate_attack_emoji = crown_utilities.set_emoji(list(move3.values())[2])


        available = ""
        is_skin = ""
        if card['AVAILABLE'] and card['EXCLUSIVE']:
            available = ":purple_circle:"
        elif card['AVAILABLE'] and not card['HAS_COLLECTION']:
            available = ":green_circle:"
        elif card['HAS_COLLECTION']:
            available = ":blue_circle:"
        else:
            available = "🟠"
        if card['IS_SKIN']:
            is_skin = ":white_circle:"
        if card['EXCLUSIVE'] and not card['HAS_COLLECTION']:
            dungeon_card_details.append(
                f"{is_skin}{available}  :mahjong: {card['TIER']} **{card['NAME']}** {basic_attack_emoji} {super_attack_emoji} {ultimate_attack_emoji}\n:heart: {card['HLT']} :dagger: {card['ATK']}  🛡️ {card['DEF']}\n")
        elif not card['HAS_COLLECTION']:
            tales_card_details.append(
                f"{is_skin}{available} :mahjong: {card['TIER']} **{card['NAME']}** {basic_attack_emoji} {super_attack_emoji} {ultimate_attack_emoji}\n:heart: {card['HLT']} :dagger: {card['ATK']}  🛡️ {card['DEF']}\n")
        elif card['HAS_COLLECTION']:
            destiny_card_details.append(
                f"{is_skin}{available} :mahjong: {card['TIER']} **{card['NAME']}** {basic_attack_emoji} {super_attack_emoji} {ultimate_attack_emoji}\n:heart: {card['HLT']} :dagger: {card['ATK']}  🛡️ {card['DEF']}\n")

    all_cards = []
    if tales_card_details:
        for t in tales_card_details:
            all_cards.append(t)

    if dungeon_card_details:
        for d in dungeon_card_details:
            all_cards.append(d)

    if destiny_card_details:
        for de in destiny_card_details:
            all_cards.append(de)

    total_cards = len(all_cards)

    # Adding to array until divisible by 10
    while len(all_cards) % 10 != 0:
        all_cards.append("")
    # Check if divisible by 10, then start to split evenly

    if len(all_cards) % 10 == 0:
        first_digit = int(str(len(all_cards))[:1])
        if len(all_cards) >= 89:
            if first_digit == 1:
                first_digit = 10
        # first_digit = 10
        cards_broken_up = np.array_split(all_cards, first_digit)

    # If it's not an array greater than 10, show paginationless embed
    if len(all_cards) < 10:
        embedVar = discord.Embed(title=f"{universe} Card List", description="\n".join(all_cards), colour=0x7289da)
        embedVar.set_footer(
            text=f"{total_cards} Total Cards\n🟢 Tale Drop\n🟣 Dungeon Drop\n🔵 Destiny Line\n🟠 Scenario Drop\n⚪ Skin")
        await ctx.send(embed=embedVar)

    embed_list = []
    for i in range(0, len(cards_broken_up)):
        globals()['embedVar%s' % i] = discord.Embed(
            title=f":flower_playing_cards: {universe_data['TITLE']} Card List",
            description="\n".join(cards_broken_up[i]), colour=0x7289da)
        globals()['embedVar%s' % i].set_footer(
            text=f"{total_cards} Total Cards\n🟢 Tale Drop\n🟣 Dungeon Drop\n🔵 Destiny Line\n🟠 Scenario Drop\n⚪ Skin\n/view *Card Name* `🎴 It's A Card`")
        embed_list.append(globals()['embedVar%s' % i])

    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
    paginator.add_reaction('⏮️', "first")
    paginator.add_reaction('⬅️', "back")
    paginator.add_reaction('🔐', "lock")
    paginator.add_reaction('➡️', "next")
    paginator.add_reaction('⏭️', "last")
    embeds = embed_list
    await paginator.run(embeds)


async def titlelist(self, ctx: SlashContext, universe: str):
    a_registered_player = await crown_utilities.player_check(ctx)
    if not a_registered_player:
        return


    universe_data = db.queryUniverse({'TITLE': {"$regex": universe, "$options": "i"}})
    user = db.queryUser({'DID': str(ctx.author.id)})
    list_of_titles = db.queryAllTitlesBasedOnUniverses({'UNIVERSE': {"$regex": str(universe), "$options": "i"}})
    titles = [x for x in list_of_titles]
    dungeon_titles_details = []
    tales_titles_details = []
    for title in titles:
        title_passive = title['ABILITIES'][0]
        title_passive_type = list(title_passive.keys())[0].title()
        title_passive_value = list(title_passive.values())[0]

        available = ""
        if title['AVAILABLE'] and title['EXCLUSIVE']:
            available = ":purple_circle:"
        elif title['AVAILABLE']:
            available = ":green_circle:"
        else:
            available = ":red_circle:"
        if title['EXCLUSIVE']:
            dungeon_titles_details.append(
                f"{available} :reminder_ribbon: **{title['TITLE']}**\n**{title_passive_type}:** {title_passive_value}\n")
        else:
            tales_titles_details.append(
                f"{available} :reminder_ribbon: **{title['TITLE']}**\n**{title_passive_type}:** {title_passive_value}\n")

    all_titles = []
    if tales_titles_details:
        for t in tales_titles_details:
            all_titles.append(t)

    if dungeon_titles_details:
        for d in dungeon_titles_details:
            all_titles.append(d)

    total_titles = len(all_titles)

    # Adding to array until divisible by 10
    while len(all_titles) % 10 != 0:
        all_titles.append("")
    # Check if divisible by 10, then start to split evenly
    if len(all_titles) % 10 == 0:
        first_digit = int(str(len(all_titles))[:1])
        if len(all_titles) >= 89:
            if first_digit == 1:
                first_digit = 10
        titles_broken_up = np.array_split(all_titles, first_digit)

    # If it's not an array greater than 10, show paginationless embed
    if len(all_titles) < 10:
        embedVar = discord.Embed(title=f"{universe} Title List", description="\n".join(all_titles), colour=0x7289da)
        # embedVar.set_thumbnail(url={universe_data['PATH']})
        embedVar.set_footer(text=f"{total_titles} Total Titles\n🟢 Tale Drop\n🟣 Dungeon Drop\n🔴 Boss Drop")
        await ctx.send(embed=embedVar)

    embed_list = []
    for i in range(0, len(titles_broken_up)):
        globals()['embedVar%s' % i] = discord.Embed(title=f":reminder_ribbon: {universe_data['TITLE']} Title List",
                                                    description="\n".join(titles_broken_up[i]), colour=0x7289da)
        # globals()['embedVar%s' % i].set_thumbnail(url={universe_data['PATH']})
        globals()['embedVar%s' % i].set_footer(
            text=f"{total_titles} Total Titles\n🟢 Tale Drop\n🟣 Dungeon Drop\n🔴 Boss Drop\n/view *Title Name* `🎗️ It's A Title` - View Title Details")
        embed_list.append(globals()['embedVar%s' % i])

    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
    paginator.add_reaction('⏮️', "first")
    paginator.add_reaction('⬅️', "back")
    paginator.add_reaction('🔐', "lock")
    paginator.add_reaction('➡️', "next")
    paginator.add_reaction('⏭️', "last")
    embeds = embed_list
    await paginator.run(embeds)


async def armlist(self, ctx: SlashContext, universe: str):
    a_registered_player = await crown_utilities.player_check(ctx)
    if not a_registered_player:
        return


    universe_data = db.queryUniverse({'TITLE': {"$regex": universe, "$options": "i"}})
    user = db.queryUser({'DID': str(ctx.author.id)})
    list_of_arms = db.queryAllArmsBasedOnUniverses({'UNIVERSE': {"$regex": str(universe), "$options": "i"}})
    arms = [x for x in list_of_arms]
    dungeon_arms_details = []
    tales_arms_details = []
    for arm in arms:
        arm_passive = arm['ABILITIES'][0]
        arm_passive_type = list(arm_passive.keys())[0].title()
        arm_passive_value = list(arm_passive.values())[0]

        arm_message = f"🦾 **{arm['ARM']}**\n**{arm_passive_type}:** {arm_passive_value}\n"

        element = arm['ELEMENT']
        element_available = ['BASIC', 'SPECIAL', 'ULTIMATE']
        if element and arm_passive_type.upper() in element_available:
            element_name = element
            element = crown_utilities.set_emoji(element)
            arm_message = f"🦾 **{arm['ARM']}**\n{element} **{arm_passive_type} {element_name.title()} Attack:** {arm_passive_value}\n"

        available = ""
        if arm['AVAILABLE'] and arm['EXCLUSIVE']:
            available = ":purple_circle:"
        elif arm['AVAILABLE']:
            available = ":green_circle:"
        else:
            available = ":red_circle:"

        
        if arm['EXCLUSIVE']:
            dungeon_arms_details.append(
                f"{available} {arm_message}")
        else:
            tales_arms_details.append(
                f"{available} {arm_message}")

    all_arms = []
    if tales_arms_details:
        for t in tales_arms_details:
            all_arms.append(t)

    if dungeon_arms_details:
        for d in dungeon_arms_details:
            all_arms.append(d)

    total_arms = len(all_arms)
    # Adding to array until divisible by 10
    while len(all_arms) % 10 != 0:
        all_arms.append("")
    # Check if divisible by 10, then start to split evenly
    if len(all_arms) % 10 == 0:
        first_digit = int(str(len(all_arms))[:1])
        if len(all_arms) >= 89:
            if first_digit == 1:
                first_digit = 10
        arms_broken_up = np.array_split(all_arms, first_digit)

    # If it's not an array greater than 10, show paginationless embed
    if len(all_arms) < 10:
        embedVar = discord.Embed(title=f"{universe} Arms List", description="\n".join(all_arms), colour=0x7289da)
        embedVar.set_footer(text=f"{total_arms} Total Arms\n🟢 Tale Drop\n🟣 Dungeon Drop\n🔴 Boss Drop")
        await ctx.send(embed=embedVar)

    embed_list = []
    for i in range(0, len(arms_broken_up)):
        globals()['embedVar%s' % i] = discord.Embed(title=f"🦾 {universe_data['TITLE']} Arms List",
                                                    description="\n".join(arms_broken_up[i]), colour=0x7289da)
        globals()['embedVar%s' % i].set_footer(
            text=f"{total_arms} Total Arms\n🟢 Tale Drop\n🟣 Dungeon Drop\n🔴 Boss Drop\n /view *Arm Name* `🦾Its' An Arm`")
        embed_list.append(globals()['embedVar%s' % i])

    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
    paginator.add_reaction('⏮️', "first")
    paginator.add_reaction('⬅️', "back")
    paginator.add_reaction('🔐', "lock")
    paginator.add_reaction('➡️', "next")
    paginator.add_reaction('⏭️', "last")
    embeds = embed_list
    await paginator.run(embeds)


async def destinylist(self, ctx: SlashContext, universe: str):
    a_registered_player = await crown_utilities.player_check(ctx)
    if not a_registered_player:
        return


    universe_data = db.queryUniverse({'TITLE': {"$regex": universe, "$options": "i"}})
    user = db.queryUser({'DID': str(ctx.author.id)})
    destinies = []
    for destiny in d.destiny:
        if destiny["UNIVERSE"].upper() == universe.upper():
            destinies.append(destiny)

    destiny_details = []
    for de in destinies:
        destiny_details.append(
            f":sparkles: **{de['NAME']}**\nDefeat {de['DEFEAT']} with {' '.join(de['USE_CARDS'])} {str(de['REQUIRED'])} times: Unlock **{de['EARN']}**\n")

    total_destinies = len(destiny_details)
    if total_destinies <= 0:
        await ctx.send(f"There are no current Destinies in **{universe_data['TITLE']}**. Check again later")
        return

    # Adding to array until divisible by 10
    while len(destiny_details) % 10 != 0:
        destiny_details.append("")
    # Check if divisible by 10, then start to split evenly

    if len(destiny_details) % 10 == 0:
        first_digit = int(str(len(destiny_details))[:1])
        if len(destiny_details) >= 89:
            if first_digit == 1:
                first_digit = 10
        destinies_broken_up = np.array_split(destiny_details, first_digit)

    # If it's not an array greater than 10, show paginationless embed
    if len(destiny_details) < 10:
        embedVar = discord.Embed(title=f"{universe} Destiny List", description="\n".join(destiny_details),
                                colour=0x7289da)
        globals()['embedVar%s' % i].set_footer(text=f"{total_destinies} Total Destiny Lines")
        await ctx.send(embed=embedVar)

    embed_list = []
    for i in range(0, len(destinies_broken_up)):
        globals()['embedVar%s' % i] = discord.Embed(title=f":rosette: {universe_data['TITLE']} Destiny List",
                                                    description="\n".join(destinies_broken_up[i]), colour=0x7289da)
        globals()['embedVar%s' % i].set_footer(text=f"{total_destinies} Total Destiny Lines")
        embed_list.append(globals()['embedVar%s' % i])

    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
    paginator.add_reaction('⏮️', "first")
    paginator.add_reaction('⬅️', "back")
    paginator.add_reaction('🔐', "lock")
    paginator.add_reaction('➡️', "next")
    paginator.add_reaction('⏭️', "last")
    embeds = embed_list
    await paginator.run(embeds)


async def summonlist(self, ctx: SlashContext, universe: str):
    a_registered_player = await crown_utilities.player_check(ctx)
    if not a_registered_player:
        return


    universe_data = db.queryUniverse({'TITLE': {"$regex": universe, "$options": "i"}})
    user = db.queryUser({'DID': str(ctx.author.id)})
    list_of_pets = db.queryAllPetsBasedOnUniverses({'UNIVERSE': {"$regex": str(universe), "$options": "i"}})
    pets = [x for x in list_of_pets]
    dungeon_pets_details = []
    tales_pets_details = []
    for pet in pets:
        pet_ability = list(pet['ABILITIES'][0].keys())[0]
        pet_ability_power = list(pet['ABILITIES'][0].values())[0]
        pet_ability_type = list(pet['ABILITIES'][0].values())[1]
        available = ""
        if pet['AVAILABLE'] and pet['EXCLUSIVE']:
            available = ":purple_circle:"
        elif pet['AVAILABLE']:
            available = ":green_circle:"
        else:
            available = ":red_circle:"
        if pet['EXCLUSIVE']:
            dungeon_pets_details.append(
                f"{available} 🧬 **{pet['PET']}**\n**{pet_ability}:** {pet_ability_power}\n**Type:** {pet_ability_type}\n")
        else:
            tales_pets_details.append(
                f"{available} 🧬 **{pet['PET']}**\n**{pet_ability}:** {pet_ability_power}\n**Type:** {pet_ability_type}\n")

    all_pets = []
    if tales_pets_details:
        for t in tales_pets_details:
            all_pets.append(t)

    if dungeon_pets_details:
        for d in dungeon_pets_details:
            all_pets.append(d)

    total_pets = len(all_pets)

    # Adding to array until divisible by 10
    while len(all_pets) % 10 != 0:
        all_pets.append("")

    # Check if divisible by 10, then start to split evenly
    if len(all_pets) % 10 == 0:
        first_digit = int(str(len(all_pets))[:1])
        if len(all_pets) >= 89:
            if first_digit == 1:
                first_digit = 10
        pets_broken_up = np.array_split(all_pets, first_digit)

    # If it's not an array greater than 10, show paginationless embed
    if len(all_pets) < 10:
        embedVar = discord.Embed(title=f"{universe} Summon List", description="\n".join(all_pets), colour=0x7289da)
        embedVar.set_footer(text=f"{total_pets} Total Summons\n🟢 Tale Drop\n🟣 Dungeon Drop\n🔴 Boss Drop")
        await ctx.send(embed=embedVar)

    embed_list = []
    for i in range(0, len(pets_broken_up)):
        globals()['embedVar%s' % i] = discord.Embed(title=f"🧬 {universe_data['TITLE']} Summon List",
                                                    description="\n".join(pets_broken_up[i]), colour=0x7289da)
        globals()['embedVar%s' % i].set_footer(
            text=f"{total_pets} Total Summons\n🟢 Tale Drop\n🟣 Dungeon Drop\n🔴 Boss Drop\n/view *Summon Name* `:dna: It's A Summon`")
        embed_list.append(globals()['embedVar%s' % i])

    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
    paginator.add_reaction('⏮️', "first")
    paginator.add_reaction('⬅️', "back")
    paginator.add_reaction('🔐', "lock")
    paginator.add_reaction('➡️', "next")
    paginator.add_reaction('⏭️', "last")
    embeds = embed_list
    await paginator.run(embeds)


async def select_universe(self, ctx, p: object, mode: str, p2: None):
    p.set_rift_on()
    await p.set_guild_data()

    if mode in crown_utilities.CO_OP_M:
        await ctx.send(f"{p.name} needs your help! React in server to join their Coop Tale!!")
        coop_buttons = [
                    manage_components.create_button(
                        style=ButtonStyle.green,
                        label="Join Battle!",
                        custom_id="yes"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red,
                        label="Decline",
                        custom_id="no"
                    )
                ]
        coop_buttons_action_row = manage_components.create_actionrow(*coop_buttons)
        msg = await ctx.send(f"{p2.did.mention} Do you accept the **Coop Invite**?", components=[coop_buttons_action_row])
        def check(button_ctx):
            return button_ctx.author.id == p2.did
        try:
            button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[coop_buttons_action_row], timeout=120, check=check)

            if button_ctx.custom_id == "no":
                await button_ctx.send("Coop **Declined**")
                self.stop = True
                return
            
            if button_ctx.custom_id == "yes":
                await button_ctx.defer(ignore=True)
        
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
            guild = self.bot.get_guild(main.guild_id)
            channel = guild.get_channel(main.guild_channel)
            await channel.send(f"'PLAYER': **{str(ctx.author)}**, 'GUILD': **{str(ctx.author.guild)}**,  TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")
            return
    
    
    if p.set_auto_battle_on(mode):
        embedVar = discord.Embed(title=f"Auto-Battles Locked", description=f"To Unlock Auto-Battles Join Patreon!",
                                 colour=0xe91e63)
        embedVar.add_field(
            name=f"Check out the #patreon channel!\nThank you for supporting the development of future games!",
            value="-Party Chat Dev Team")
        await ctx.send(embed=embedVar)
        return

    if mode in crown_utilities.TALE_M or mode in crown_utilities.DUNGEON_M:
        available_universes = p.set_selectable_universes(ctx, mode)

        buttons = [
            manage_components.create_button(style=3, label="Start Battle!", custom_id="start"),
            manage_components.create_button(style=1, label="View Available Scenario Battles!", custom_id="scenario"),
        ]
        custom_action_row = manage_components.create_actionrow(*buttons)        


        async def custom_function(self, button_ctx):
            if button_ctx.author == ctx.author:
                if button_ctx.custom_id == "scenario":
                    await button_ctx.defer(ignore=True)
                    universe = str(button_ctx.origin_message.embeds[0].title)
                    await scenario(self, ctx, p, universe)
                    self.stop = True
                    return
                elif button_ctx.custom_id == "start":                
                    await button_ctx.defer(ignore=True)
                    selected_universe = custom_function
                    custom_function.selected_universe = str(button_ctx.origin_message.embeds[0].title)
                    self.stop = True
            else:
                await ctx.send("This is not your button.", hidden=True)

        await Paginator(bot=self.bot, ctx=ctx, useQuitButton=True, deleteAfterTimeout=True, pages=available_universes, timeout=60, customActionRow=[
            custom_action_row,
            custom_function,
        ]).run()
        

        try:
            # print(custom_function.selected_universez
            selected_universe = custom_function.selected_universe
            if selected_universe == "":
                return

            universe = db.queryUniverse({'TITLE': str(selected_universe)})
            universe_owner = universe['GUILD']

            #Universe Cost
            entrance_fee = 1000


            if mode in crown_utilities.DUNGEON_M:
                entrance_fee = 5000
                
            if selected_universe in p.crestlist:
                await ctx.send(f"{crown_utilities.crest_dict[selected_universe]} | :flags: {p.association} {selected_universe} Crest Activated! No entrance fee!")
            else:
                if int(p._balance) <= entrance_fee:
                    await ctx.send(f"Tales require an :coin: {'{:,}'.format(entrance_fee)} entrance fee!", delete_after=5)
                    db.updateUserNoFilter({'DID': str(ctx.author.id)}, {'$set': {'AVAILABLE': True}})
                    return
                else:
                    await crown_utilities.curse(entrance_fee, str(ctx.author.id))
                    if universe_owner != 'PCG':
                        crest_guild = db.queryGuildAlt({'GNAME' : universe_owner})
                        if crest_guild:
                            await crown_utilities.blessguild(entrance_fee, universe['GUILD'])
                            await ctx.send(f"{crown_utilities.crest_dict[selected_universe]} | {crest_guild['GNAME']} Universe Toll Paid! :coin:{'{:,}'.format(entrance_fee)}")
            
            currentopponent = 0
            if p.difficulty != "EASY":
                currentopponent = update_save_spot(self, ctx, p.save_spot, selected_universe, crown_utilities.TALE_M)
                if mode in crown_utilities.DUNGEON_M:
                    currentopponent = update_save_spot(self, ctx, p.save_spot, selected_universe, crown_utilities.DUNGEON_M)
            else:
                currentopponent = 0

            if p.rift_on:
                update_team_response = db.updateTeam(p.filter_query, p.guild_buff_update_query)

            response = {'SELECTED_UNIVERSE': selected_universe,
                    'UNIVERSE_DATA': universe, 'CREST_LIST': p.crestlist, 'CREST_SEARCH': p.crestsearch,
                    'COMPLETED_TALES': p.completed_tales, 'OGUILD': p.association_info, 'CURRENTOPPONENT': currentopponent}
            
            if mode in crown_utilities.DUNGEON_M:
                response.update({'COMPLETED_DUNGEONS': p.completed_dungeons})

            return response
            
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

    if mode in crown_utilities.BOSS_M:
        completed_crown_tales = p.completed_tales
        all_universes = db.queryAllUniverse()
        available_universes = []
        selected_universe = ""
        universe_menu = []
        universe_embed_list = []
        for uni in p.completed_dungeons:
            if uni != "":
                searchUni = db.queryUniverse({'TITLE': str(uni)})
                if searchUni['GUILD'] != "PCG":
                    owner_message = f"{crown_utilities.crest_dict[searchUni['TITLE']]} **Crest Owned**: {searchUni['GUILD']}"
                else: 
                    owner_message = f"{crown_utilities.crest_dict[searchUni['TITLE']]} *Crest Unclaimed*"
                if searchUni['UNIVERSE_BOSS'] != "":
                    boss_info = db.queryBoss({"NAME": searchUni['UNIVERSE_BOSS']})
                    if boss_info:
                        embedVar = discord.Embed(title= f"{uni}", description=textwrap.dedent(f"""
                        {crown_utilities.crest_dict[uni]} **Boss**: :japanese_ogre: **{boss_info['NAME']}**
                        🎗️ **Boss Title**: {boss_info['TITLE']}
                        🦾 **Boss Arm**: {boss_info['ARM']}
                        🧬 **Boss Summon**: {boss_info['PET']}
                        
                        {owner_message}
                        """))
                        embedVar.set_image(url=boss_info['PATH'])
                        embedVar.set_thumbnail(url=ctx.author.avatar_url)
                        embedVar.set_footer(text="📿| Boss Talismans ignore all Affinities. Be Prepared")
                        universe_embed_list.append(embedVar)
        if not universe_embed_list:
            await ctx.send("No available Bosses for you at this time!")
            return
        
        custom_button = manage_components.create_button(style=3, label="Select")

        async def custom_function(self, button_ctx):
            if button_ctx.author == ctx.author:
                await button_ctx.defer(ignore=True)
                selected_universe = custom_function
                custom_function.selected_universe = str(button_ctx.origin_message.embeds[0].title)
                self.stop = True
            else:
                await ctx.send("This is not your button.", hidden=True)

        await Paginator(bot=self.bot, ctx=ctx, useQuitButton=True, deleteAfterTimeout=True, pages=universe_embed_list, timeout=60,  customButton=[
            custom_button,
            custom_function,
        ]).run()

        try:
            # Universe Cost
            selected_universe = custom_function.selected_universe
            universe = db.queryUniverse({'TITLE': str(selected_universe)})
            universe_owner = universe['GUILD']
            #Universe Cost
            entrance_fee = 10000
            if selected_universe in crestlist:
                await ctx.send(f"{crown_utilities.crest_dict[selected_universe]} | :flags: {guildname} {selected_universe} Crest Activated! No entrance fee!")
            else:
                if p._balance <= entrance_fee:
                    await ctx.send(f"Tales require an :coin: {'{:,}'.format(entrance_fee)} entrance fee!", delete_after=5)
                    db.updateUserNoFilter({'DID': str(ctx.author.id)}, {'$set': {'AVAILABLE': True}})
                    return
                else:
                    await crown_utilities.curse(entrance_fee, str(ctx.author.id))
                    if universe['GUILD'] != 'PCG':
                        crest_guild = db.queryGuildAlt({'GNAME' : universe['GUILD']})
                        if crest_guild:
                            await crown_utilities.blessguild(entrance_fee, universe['GUILD'])
                            await ctx.send(f"{crown_utilities.crest_dict[selected_universe]} | {crest_guild['GNAME']} Universe Toll Paid! :coin:{'{:,}'.format(entrance_fee)}")
            categoryname = "Crown Unlimited"
            #category = discord.utils.get(guild.categories, name=categoryname)

            # if category is None: #If there's no category matching with the `name`
            #     category = await guild.create_category_channel(categoryname)
            # private_channel = await guild.create_text_channel(f'{str(ctx.author)}-{mode}-fight', overwrites=overwrites, category=category)
            # await private_channel.send(f"{ctx.author.mention} private channel has been opened for you.")

            currentopponent = 0
            return {'SELECTED_UNIVERSE': selected_universe,
                    'UNIVERSE_DATA': universe, 'CREST_LIST': p.crestlist, 'CREST_SEARCH': p.crestsearch,
                    'COMPLETED_DUNGEONS': p.completed_dungeons, 'OGUILD': p.association_info, 'BOSS_NAME': universe['UNIVERSE_BOSS'],
                    'CURRENTOPPONENT': currentopponent}
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
                'PLAYER': str(ctx.author),
                'type': type(ex).__name__,
                'message': str(ex),
                'trace': trace
            }))
            #embedVar = discord.Embed(title=f"Unable to start boss fight. Seek support in the Anime 🆚+ support server https://discord.gg/cqP4M92", delete_after=30, colour=0xe91e63)
            #await ctx.send(embed=embedVar)
            guild = self.bot.get_guild(main.guild_id)
            channel = guild.get_channel(main.guild_channel)
            await channel.send(f"'PLAYER': **{str(ctx.author)}**, 'GUILD': **{str(ctx.author.guild)}**, TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")
            return


async def battle_commands(self, ctx, _battle, _player, _custom_explore_card, _player2=None):
    
    private_channel = ctx.channel

    try:
        starttime = time.asctime()
        h_gametime = starttime[11:13]
        m_gametime = starttime[14:16]
        s_gametime = starttime[17:19]

        continued = True

        while continued == True:
            opponent_talisman_emoji = ""
            # While "continued" is True, Create Class for Players and Opponents anew
            # Opponent card will be based on list of enemies[current oppponent]
            # If player changes their equipment after a round the new class will pick it up
            player1 = _player
            player1.get_battle_ready()
            player1_card = Card(player1._equipped_card_data['NAME'], player1._equipped_card_data['PATH'], player1._equipped_card_data['PRICE'], player1._equipped_card_data['EXCLUSIVE'], player1._equipped_card_data['AVAILABLE'], player1._equipped_card_data['IS_SKIN'], player1._equipped_card_data['SKIN_FOR'], player1._equipped_card_data['HLT'], player1._equipped_card_data['HLT'], player1._equipped_card_data['STAM'], player1._equipped_card_data['STAM'], player1._equipped_card_data['MOVESET'], player1._equipped_card_data['ATK'], player1._equipped_card_data['DEF'], player1._equipped_card_data['TYPE'], player1._equipped_card_data['PASS'][0], player1._equipped_card_data['SPD'], player1._equipped_card_data['UNIVERSE'], player1._equipped_card_data['HAS_COLLECTION'], player1._equipped_card_data['TIER'], player1._equipped_card_data['COLLECTION'], player1._equipped_card_data['WEAKNESS'], player1._equipped_card_data['RESISTANT'], player1._equipped_card_data['REPEL'], player1._equipped_card_data['ABSORB'], player1._equipped_card_data['IMMUNE'], player1._equipped_card_data['GIF'], player1._equipped_card_data['FPATH'], player1._equipped_card_data['RNAME'], player1._equipped_card_data['RPATH'])
            player1_title = Title(player1._equipped_title_data['TITLE'], player1._equipped_title_data['UNIVERSE'], player1._equipped_title_data['PRICE'], player1._equipped_title_data['EXCLUSIVE'], player1._equipped_title_data['AVAILABLE'], player1._equipped_title_data['ABILITIES'])            
            player1_arm = Arm(player1._equipped_arm_data['ARM'], player1._equipped_arm_data['UNIVERSE'], player1._equipped_arm_data['PRICE'], player1._equipped_arm_data['ABILITIES'], player1._equipped_arm_data['EXCLUSIVE'], player1._equipped_arm_data['AVAILABLE'], player1._equipped_arm_data['ELEMENT'])

            player1_arm.set_durability(player1.equipped_arm, player1._arms)
            player1_card.set_card_level_buffs(player1._card_levels)
            player1_card.set_arm_config(player1_arm.passive_type, player1_arm.name, player1_arm.passive_value, player1_arm.element)
            player1_card.set_affinity_message()
            player1.get_summon_ready(player1_card)
            player1.get_talisman_ready(player1_card)

            if _battle.mode in crown_utilities.PVP_M:
                _player2.get_battle_ready()
                player2_card = Card(_player2._equipped_card_data['NAME'], _player2._equipped_card_data['PATH'], _player2._equipped_card_data['PRICE'], _player2._equipped_card_data['EXCLUSIVE'], _player2._equipped_card_data['AVAILABLE'], _player2._equipped_card_data['IS_SKIN'], _player2._equipped_card_data['SKIN_FOR'], _player2._equipped_card_data['HLT'], _player2._equipped_card_data['HLT'], _player2._equipped_card_data['STAM'], _player2._equipped_card_data['STAM'], _player2._equipped_card_data['MOVESET'], _player2._equipped_card_data['ATK'], _player2._equipped_card_data['DEF'], _player2._equipped_card_data['TYPE'], _player2._equipped_card_data['PASS'][0], _player2._equipped_card_data['SPD'], _player2._equipped_card_data['UNIVERSE'], _player2._equipped_card_data['HAS_COLLECTION'], _player2._equipped_card_data['TIER'], _player2._equipped_card_data['COLLECTION'], _player2._equipped_card_data['WEAKNESS'], _player2._equipped_card_data['RESISTANT'], _player2._equipped_card_data['REPEL'], _player2._equipped_card_data['ABSORB'], _player2._equipped_card_data['IMMUNE'], _player2._equipped_card_data['GIF'], _player2._equipped_card_data['FPATH'], _player2._equipped_card_data['RNAME'], _player2._equipped_card_data['RPATH'])
                player2_title = Title(_player2._equipped_title_data['TITLE'], _player2._equipped_title_data['UNIVERSE'], _player2._equipped_title_data['PRICE'], _player2._equipped_title_data['EXCLUSIVE'], _player2._equipped_title_data['AVAILABLE'], _player2._equipped_title_data['ABILITIES'])            
                player2_arm = Arm(_player2._equipped_arm_data['ARM'], _player2._equipped_arm_data['UNIVERSE'], _player2._equipped_arm_data['PRICE'], _player2._equipped_arm_data['ABILITIES'], _player2._equipped_arm_data['EXCLUSIVE'], _player2._equipped_arm_data['AVAILABLE'], _player2._equipped_arm_data['ELEMENT'])
                opponent_talisman_emoji = crown_utilities.set_emoji(_player2.equipped_talisman)
                player2_arm.set_durability(_player2.equipped_arm, _player2._arms)
                player2_card.set_card_level_buffs(player2._card_levels)
                player2_card.set_arm_config(player2_arm.passive_type, player2_arm.name, player2_arm.passive_value, player2_arm.element)
                player2_card.set_solo_leveling_config(player1_card._shield_active, player1_card._shield_value, player1_card._barrier_active, player1_card._barrier_value, player1_card._parry_active, player1_card._parry_value)
                player2_card.set_affinity_message()
                player2.get_summon_ready(player2_card)
                player2.get_talisman_ready(player2_card)

            if _battle.mode in crown_utilities.CO_OP_M:
                _player3.get_battle_ready()
                player3_card = Card(_player3._equipped_card_data['NAME'], _player3._equipped_card_data['PATH'], _player3._equipped_card_data['PRICE'], _player3._equipped_card_data['EXCLUSIVE'], _player3._equipped_card_data['AVAILABLE'], _player3._equipped_card_data['IS_SKIN'], _player3._equipped_card_data['SKIN_FOR'], _player3._equipped_card_data['HLT'], _player3._equipped_card_data['HLT'], _player3._equipped_card_data['STAM'], _player3._equipped_card_data['STAM'], _player3._equipped_card_data['MOVESET'], _player3._equipped_card_data['ATK'], _player3._equipped_card_data['DEF'], _player3._equipped_card_data['TYPE'], _player3._equipped_card_data['PASS'][0], _player3._equipped_card_data['SPD'], _player3._equipped_card_data['UNIVERSE'], _player3._equipped_card_data['HAS_COLLECTION'], _player3._equipped_card_data['TIER'], _player3._equipped_card_data['COLLECTION'], _player3._equipped_card_data['WEAKNESS'], _player3._equipped_card_data['RESISTANT'], _player3._equipped_card_data['REPEL'], _player3._equipped_card_data['ABSORB'], _player3._equipped_card_data['IMMUNE'], _player3._equipped_card_data['GIF'], _player3._equipped_card_data['FPATH'], _player3._equipped_card_data['RNAME'], _player3._equipped_card_data['RPATH'])
                player3_title = Title(_player3._equipped_title_data['TITLE'], _player3._equipped_title_data['UNIVERSE'], _player3._equipped_title_data['PRICE'], _player3._equipped_title_data['EXCLUSIVE'], _player3._equipped_title_data['AVAILABLE'], _player3._equipped_title_data['ABILITIES'])            
                player3_arm = Arm(_player3._equipped_arm_data['ARM'], _player3._equipped_arm_data['UNIVERSE'], _player3._equipped_arm_data['PRICE'], _player3._equipped_arm_data['ABILITIES'], _player3._equipped_arm_data['EXCLUSIVE'], _player3._equipped_arm_data['AVAILABLE'], _player3._equipped_arm_data['ELEMENT'])
                player3_talisman_emoji = crown_utilities.set_emoji(_player3.equipped_talisman)
                player3_arm.set_durability(_player3.equipped_arm, _player3._arms)
                player3_card.set_card_level_buffs()
                player3_card.set_arm_config(player3_arm.passive_type, player3_arm.name, player3_arm.passive_value, player3_arm.element)
                player3_card.set_solo_leveling_config(player1._shield_active, player1._shield_value, player1._barrier_active, player1._barrier_value, player1._parry_active, player1._parry_value)
                player3_card.set_affinity_message()
                player3.get_summon_ready(player3_card)
                player3.get_talisman_ready(player3_card)
            
            if _battle.is_ai_opponent:
                if _battle._is_explore:
                    player2_card = _custom_explore_card
                else:
                    _battle.get_ai_battle_ready()
                    player2_card = Card(_battle._ai_opponent_card_data['NAME'], _battle._ai_opponent_card_data['PATH'], _battle._ai_opponent_card_data['PRICE'], _battle._ai_opponent_card_data['EXCLUSIVE'], _battle._ai_opponent_card_data['AVAILABLE'], _battle._ai_opponent_card_data['IS_SKIN'], _battle._ai_opponent_card_data['SKIN_FOR'], _battle._ai_opponent_card_data['HLT'], _battle._ai_opponent_card_data['HLT'], _battle._ai_opponent_card_data['STAM'], _battle._ai_opponent_card_data['STAM'], _battle._ai_opponent_card_data['MOVESET'], _battle._ai_opponent_card_data['ATK'], _battle._ai_opponent_card_data['DEF'], _battle._ai_opponent_card_data['TYPE'], _battle._ai_opponent_card_data['PASS'][0], _battle._ai_opponent_card_data['SPD'], _battle._ai_opponent_card_data['UNIVERSE'], _battle._ai_opponent_card_data['HAS_COLLECTION'], _battle._ai_opponent_card_data['TIER'], _battle._ai_opponent_card_data['COLLECTION'], _battle._ai_opponent_card_data['WEAKNESS'], _battle._ai_opponent_card_data['RESISTANT'], _battle._ai_opponent_card_data['REPEL'], _battle._ai_opponent_card_data['ABSORB'], _battle._ai_opponent_card_data['IMMUNE'], _battle._ai_opponent_card_data['GIF'], _battle._ai_opponent_card_data['FPATH'], _battle._ai_opponent_card_data['RNAME'], _battle._ai_opponent_card_data['RPATH'])
                    player2_card.set_ai_card_buffs(_battle._ai_opponent_card_lvl, _battle.stat_buff, _battle.stat_debuff, _battle.health_buff, _battle.health_debuff, _battle.ap_buff, _battle.ap_debuff)
                player2_card.set_talisman(_battle)
                player2_title = Title(_battle._ai_opponent_title_data['TITLE'], _battle._ai_opponent_title_data['UNIVERSE'], _battle._ai_opponent_title_data['PRICE'], _battle._ai_opponent_title_data['EXCLUSIVE'], _battle._ai_opponent_title_data['AVAILABLE'], _battle._ai_opponent_title_data['ABILITIES'])            
                player2_arm = Arm(_battle._ai_opponent_arm_data['ARM'], _battle._ai_opponent_arm_data['UNIVERSE'], _battle._ai_opponent_arm_data['PRICE'], _battle._ai_opponent_arm_data['ABILITIES'], _battle._ai_opponent_arm_data['EXCLUSIVE'], _battle._ai_opponent_arm_data['AVAILABLE'], _battle._ai_opponent_arm_data['ELEMENT'])
                opponent_talisman_emoji = ""
                player2_card.set_arm_config(player2_arm.passive_type, player2_arm.name, player2_arm.passive_value, player2_arm.element)
                player2_card.set_affinity_message()
                # Set potential boss descriptions
                _battle.set_boss_descriptions(player2_card.name)
                player2_card.set_solo_leveling_config(player1_card._shield_active, player1_card._shield_value, player1_card._barrier_active, player1_card._barrier_value, player1_card._parry_active, player1_card._parry_value)
                player1_card.set_solo_leveling_config(player2_card._shield_active, player2_card._shield_value, player2_card._barrier_active, player2_card._barrier_value, player2_card._parry_active, player2_card._parry_value)
                _battle.get_ai_summon_ready(player1_card)

                if _battle.mode in crown_utilities.CO_OP_M:
                    player2_card.set_solo_leveling_config(player3_card._shield_active, player3_card._shield_value, player3_card._barrier_active, player3_card._barrier_value, player3_card._parry_active, player3_card._parry_value)
            
            if _battle.mode in crown_utilities.PVP_M:
                player1_card.set_solo_leveling_config(player2_card._shield_active, player2_card._shield_value, player2_card._barrier_active, player2_card._barrier_value, player2_card._parry_active, player2_card._parry_value)

            if _battle.mode == "RAID":
                raidActive = True
                botActive= False

            options = [1, 2, 3, 4, 5, 0]

            start_tales_buttons = [
                manage_components.create_button(
                    style=ButtonStyle.blue,
                    label="Start Match",
                    custom_id="start_tales_yes"
                ),
                manage_components.create_button(
                    style=ButtonStyle.red,
                    label="End",
                    custom_id="start_tales_no"
                ),
            ]

            if _battle._can_auto_battle and not _battle._is_co_op and not _battle._is_duo:
                start_tales_buttons.append(
                    manage_components.create_button(
                        style=ButtonStyle.grey,
                        label="Auto Battle",
                        custom_id="start_auto_tales"
                    )

                )
            
            if not _battle._is_tutorial and _battle.get_can_save_match():
                if _battle._currentopponent > 0:
                    start_tales_buttons.append(
                        manage_components.create_button(
                            style=ButtonStyle.green,
                            label="Save Game",
                            custom_id="save_tales_yes"
                        )
                    )

            start_tales_buttons_action_row = manage_components.create_actionrow(*start_tales_buttons)            
            
            _battle.set_who_starts_match(player1_card.speed, player2_card.speed)
            user1 = await main.bot.fetch_user(player1.did)

            if _battle._is_pvp_match and not _battle._is_tutorial:
                user2 = await main.bot.fetch_user(_player2.did)
                battle_ping_message = await private_channel.send(f"{player_1_fetched_user.mention} 🆚 {player_2_fetched_user.mention} ")
            
            if _battle._is_co_op:
                user2 = await main.bot.fetch_user(_player3.did)

            title_lvl_msg = f"{_battle.set_levels_message(player1_card, player2_card)}"
            if _battle._is_co_op:
                title_lvl_msg = f"{_battle.set_levels_message(player1_card, player2_card, player3_card)}"

            await private_channel.send(content=f"{ctx.author.mention} 🆚...", )
            embedVar = discord.Embed(title=f"{_battle.starting_match_title}\n{title_lvl_msg}")
            embedVar.add_field(name=f"__Your Affinities: {crown_utilities.set_emoji(player1.equipped_talisman)}__", value=f"{player1_card.affinity_message}")
            embedVar.add_field(name=f"__Opponent Affinities: {crown_utilities.set_emoji(player2_card._talisman)}__", value=f"{player2_card.affinity_message}")
            embedVar.set_image(url="attachment://image.png")
            embedVar.set_thumbnail(url=ctx.author.avatar_url)
            battle_msg = await private_channel.send(embed=embedVar, components=[start_tales_buttons_action_row], file=player2_card.showcard(_battle.mode, player2_arm, player2_title, _battle._turn_total, player1_card.defense))                

            def check(button_ctx):
                if _battle._is_pvp_match:
                    if _battle._is_tutorial:
                        return button_ctx.author == ctx.author
                    else:
                        return button_ctx.author == _player2.did
                elif _battle._is_co_op:
                    return button_ctx.author == ctx.author
                else:
                    return button_ctx.author == ctx.author

            try:
                button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[
                            start_tales_buttons_action_row], timeout=300, check=check)

                if button_ctx.custom_id == "start_tales_no":
                    await battle_msg.delete()
                    # await battle_ping_message.delete()
                    return

                if button_ctx.custom_id == "save_tales_yes":
                    await battle_msg.delete()
                    # await battle_ping_message.delete()
                    await save_spot(self, ctx, _battle._selected_universe, _battle.mode, _battle._currentopponent)
                    await button_ctx.send(f"Game has been saved.")
                    return
                
                if button_ctx.custom_id == "start_tales_yes" or button_ctx.custom_id == "start_auto_tales":
                    # await battle_ping_message.delete()
                    if button_ctx.custom_id == "start_auto_tales":
                        _battle._is_auto_battle = True
                        embedVar = discord.Embed(title=f"Auto Battle has started", color=0xe74c3c)
                        embedVar.set_thumbnail(url=ctx.author.avatar_url)
                        await battle_msg.delete(delay=2)
                        await asyncio.sleep(2)
                        battle_msg = await private_channel.send(embed=embedVar)
                    # await button_ctx.defer(ignore=True)
                    tmove_issue = False
                    omove_issue = False

                    
                    
                    while (_battle.game_over(player1_card, player2_card) is not True):
                        if _battle.previous_moves:
                            _battle.previous_moves_len = len(_battle.previous_moves)
                            if _battle.previous_moves_len >= player1.battle_history:
                                _battle.previous_moves = _battle.previous_moves[-player1.battle_history:]
                        
                        if _battle._is_turn == 0:
                            player1_card.reset_stats_to_limiter(player2_card)

                            player1_card.yuyu_hakusho_attack_increase()
                            
                            player1_card.activate_chainsawman_trait(_battle)

                            _battle.add_battle_history_messsage(player1_card.set_bleed_hit(_battle._turn_total, player2_card))

                            _battle.add_battle_history_messsage(player1_card.set_burn_hit(player2_card))
                            
                            if player2_card.freeze_enh:
                                new_turn = player1_card.frozen(_battle, player2_card)
                                _battle._is_turn = new_turn['MESSAGE']
                                _battle.add_battle_history_messsage(new_turn['TURN'])
                                continue
                            player1_card.freeze_enh = False
                            
                            if _battle._is_co_op:
                                player3_card.freeze_enh = False

                            _battle.add_battle_history_messsage(player1_card.set_poison_hit(player2_card))
                                
                            player1_card.set_gravity_hit()

                            player1_title.activate_title_passive(_battle, player1_card, player2_card)
                            
                            player1_card.activate_card_passive(player2_card)

                            player1_card.activate_demon_slayer_trait(_battle, player2_card)

                            player2_card.activate_demon_slayer_trait(_battle, player1_card)


                            if player1_card.used_block == True:
                                player1_card.defense = int(player1_card.defense / 2)
                                player1_card.used_block = False
                            if player1_card.used_defend == True:
                                player1_card.defense = int(player1_card.defense / 2)
                                player1_card.used_defend = False

                            player1_card.set_deathnote_message(_battle)
                            player2_card.set_deathnote_message(_battle)
                            if _battle._is_co_op:
                                player3_card.set_deathnote_message(_battle)                            

                            if _battle._turn_total == 0:
                                if _battle._is_tutorial:
                                    embedVar = discord.Embed(title=f"Welcome to **Anime VS+**!",
                                                            description=f"Follow the instructions to learn how to play the Game!",
                                                            colour=0xe91e63)
                                    embedVar.add_field(name="**Moveset**",value=f"{player1_card.move1_emoji} - **Basic Attack** *10 :zap:ST*\n{player1_card.move2_emoji} - **Special Attack** *30 :zap:ST*\n{player1_card.move3_emoji} - **Ultimate Move** *80 :zap:ST*\n🦠 - **Enhancer** *20 :zap:ST*\n🛡️ - **Block** *20 :zap:ST*\n:zap: - **Resolve** : Heal and Activate Resolve\n:dna: - **Summon** : {player1.equipped_summon}")
                                    embedVar.set_footer(text="Focus State : When card deplete to 0 stamina, they focus to Heal they also gain ATK and DEF ")
                                    await private_channel.send(embed=embedVar)
                                    await asyncio.sleep(2)
                                if _battle._is_boss:
                                    embedVar = discord.Embed(title=f"**{player2_card.name}** Boss of `{player2_card.universe}`",
                                                            description=f"*{_battle._description_boss_description}*", colour=0xe91e63)
                                    embedVar.add_field(name=f"{_battle._arena_boss_description}", value=f"{_battle._arenades_boss_description}")
                                    embedVar.add_field(name=f"Entering the {_battle._arena_boss_description}", value=f"{_battle._entrance_boss_description}", inline=False)
                                    embedVar.set_footer(text=f"{player1_card.name} waits for you to strike....")
                                    await ctx.send(embed=embedVar)
                                    await asyncio.sleep(2)
                                
                            if player1_card.stamina < 10:
                                player1_card.focusing(player1_title, player2_title, player2_card, _battle)
                                
                                if _battle._is_tutorial and tutorial_focus ==False:
                                    await ctx.send(embed=_battle._tutorial_message)
                                    await asyncio.sleep(2)

                                if _battle._is_boss:
                                    await ctx.send(embed=_boss_embed_message)
                                    
                            else:
                                if _battle._is_auto_battle:                                    
                                    player1_card.set_battle_arm_messages(player2_card)

                                    player1_card.activate_solo_leveling_trait(_battle, player2_card)
                                            
                                    embedVar = discord.Embed(title=f"➡️ **Current Turn** {_battle._turn_total}", description=textwrap.dedent(f"""\
                                    {_battle.get_previous_moves_embed()}
                                    
                                    """), color=0xe74c3c)
                                    await asyncio.sleep(2)
                                    embedVar.set_thumbnail(url=ctx.author.avatar_url)
                                    embedVar.set_footer(
                                        text=f"{_battle.get_battle_window_title_text(player2_card, player1_card)}",
                                        icon_url="https://cdn.discordapp.com/emojis/789290881654980659.gif?v=1")
                                    await battle_msg.edit(embed=embedVar, components=[])

                                    
                                    
                                    selected_move = _battle.ai_battle_command(player1_card, player2_card)
                                    
                                    if selected_move in [1, 2, 3, 4]:
                                        damage_calculation_response = player1_card.damage_cal(selected_move, _battle, player2_card)

                                    if selected_move == 5:
                                        player1_card.resolving(_battle, player2_card, player1)
                                        if _battle._is_boss:
                                            await button_ctx.send(embed=_battle._boss_embed_message)

                                    elif selected_move == 6:
                                        # Resolve Check and Calculation
                                        player1_card.use_summon(_battle, player2_card)
                                    
                                    if selected_move == 7:
                                        damage_calculation_response = player1_card.damage_cal(selected_move, _battle, player2_card)
                                        player1_card.use_block(_battle, damage_calculation_response, player2_card)
                                    
                                    if selected_move != 5 and selected_move != 6 and selected_move != 0:
                                        player1_card.damage_done(_battle, damage_calculation_response, player2_card)                                        

                                else:
                                    player1_card.set_battle_arm_messages(player2_card)

                                    player1_card.activate_solo_leveling_trait(_battle, player2_card)

                                    _battle.set_battle_options(player1_card, player2_card)

                                    battle_action_row = manage_components.create_actionrow(*_battle.battle_buttons)
                                    util_action_row = manage_components.create_actionrow(*_battle.utility_buttons)
                                    
                                    if _battle._is_co_op:
                                        coop_util_action_row = manage_components.create_actionrow(*_battle.co_op_util_buttons)
                                        player3_card.set_battle_arm_messages(player2_card)
                                        if player1_card.stamina >= 20:
                                            components = [battle_action_row, coop_util_action_row, util_action_row]
                                        else:
                                            components = [battle_action_row, util_action_row]
                                        companion_stats = f"\n{player3_card.name}: ❤️{round(player3_card.health)} 🌀{round(player3_card.stamina)} 🗡️{round(player3_card.attack)}/🛡️{round(player3_card.defense)} {player3_card._arm_message}"

                                    else:
                                        components = [battle_action_row, util_action_row]

                                    player1_card.set_battle_arm_messages(player2_card)
                                    embedVar = discord.Embed(title=f"", description=textwrap.dedent(f"""\
                                    {_battle.get_previous_moves_embed()}
                                    
                                    """), color=0xe74c3c)
                                    embedVar.set_author(name=f"{player1_card._arm_message}\n{player1_card.summon_resolve_message}\n")
                                    embedVar.add_field(name=f"➡️ **Current Turn** {_battle._turn_total}", value=f"{ctx.author.mention} Select move below!")
                                    # await asyncio.sleep(2)
                                    embedVar.set_image(url="attachment://image.png")
                                    embedVar.set_thumbnail(url=ctx.author.avatar_url)
                                    embedVar.set_footer(
                                        text=f"{_battle.get_battle_footer_text(player2_card, player1_card)}",
                                        icon_url="https://cdn.discordapp.com/emojis/789290881654980659.gif?v=1")
                                    await battle_msg.delete(delay=2)
                                    await asyncio.sleep(2)
                                    battle_msg = await private_channel.send(embed=embedVar, components=components, file=player1_card.showcard(_battle.mode, player1_arm, player1_title, _battle._turn_total, player2_card.defense))

                                    # Make sure user is responding with move
                                    def check(button_ctx):
                                        return button_ctx.author == user1 and button_ctx.custom_id in _battle.battle_options

                                    try:
                                        button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot,
                                                                                                                components=components,
                                                                                                                timeout=120,
                                                                                                                check=check)
                                        
                                        if button_ctx.custom_id == "s":
                                            try:
                                                player1_card.health = 0
                                                _battle.game_over = True
                                                await save_spot(self, ctx, _battle._selected_universe, _battle.mode, _battle._currentopponent)
                                                await battle_msg.delete(delay=1)
                                                await asyncio.sleep(1)
                                                battle_msg = await private_channel.send(content="Your game has been saved.")
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
                                                guild = self.bot.get_guild(main.guild_id)
                                                channel = guild.get_channel(main.guild_channel)
                                                await channel.send(f"'PLAYER': **{str(ctx.author)}**, 'GUILD': **{str(ctx.author.guild)}**, TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")
                                                
                                        if button_ctx.custom_id == "b":
                                            c_stamina = c_stamina + 10
                                            c_health = c_health + 50
                                            boost_message = f"**{o_card}** Boosted **{c_card}** +10 🌀 +100 :heart:"
                                            o_block_used = True
                                            player1_card.stamina = player1_card.stamina - 20
                                            o_defense = round(o_defense * 2)
                                            embedVar = discord.Embed(title=f"{boost_message}", colour=0xe91e63)

                                            previous_moves.append(f"(**{turn_total}**) {boost_message}")
                                            # await button_ctx.defer(ignore=True)
                                            turn_total = turn_total + 1
                                            turn = 1
                                        
                                        if button_ctx.custom_id == "q" or button_ctx.custom_id == "Q":
                                            player1_card.health = 0
                                            _battle.game_over = True
                                            _battle.add_battle_history_messsage(f"(**{_battle._turn_total}**) 💨 **{player1_card.name}** Fled...")
                                            await battle_msg.delete(delay=1)
                                            await asyncio.sleep(1)
                                            battle_msg = await private_channel.send(content=f"{ctx.author.mention} has fled.")
                                        
                                        if button_ctx.custom_id == "1":
                                            if _battle._is_tutorial and _battle.tutorial_basic == False:
                                                _battle.tutorial_basic =True
                                                embedVar = discord.Embed(title=f":boom:Basic Attack!",
                                                                        description=f":boom:**Basic Attack** cost **10 ST(Stamina)** to deal decent Damage!",
                                                                        colour=0xe91e63)
                                                embedVar.add_field(
                                                    name=f"Your Basic Attack: {player1_card.move1_emoji} {player1_card.move1} inflicts {player1_card.move1_element}",
                                                    value=f"**{player1_card.move1_element}** : *{element_mapping[player1_card.move1_element]}*")
                                                embedVar.set_footer(
                                                    text=f"Basic Attacks are great when you are low on stamina. Enter Focus State to Replenish!")
                                                await button_ctx.send(embed=embedVar, components=[])
                                                await asyncio.sleep(2)

                                            damage_calculation_response = player1_card.damage_cal(int(button_ctx.custom_id), _battle, player2_card)
                                        
                                        elif button_ctx.custom_id == "2":
                                            if _battle._is_tutorial and _battle.tutorial_special==False:
                                                _battle.tutorial_special = True
                                                embedVar = discord.Embed(title=f":comet:Special Attack!",
                                                                        description=f":comet:**Special Attack** cost **30 ST(Stamina)** to deal great Damage!",
                                                                        colour=0xe91e63)
                                                embedVar.add_field(
                                                    name=f"Your Special Attack: {player1_card.move2_emoji} {player1_card.move2} inflicts {player1_card.move2_element}",
                                                    value=f"**{player1_card.move2_element}** : *{element_mapping[player1_card.move2_element]}*")
                                                embedVar.set_footer(
                                                    text=f"Special Attacks are great when you need to control the Focus game! Use Them to Maximize your Focus and build stronger Combos!")
                                                await button_ctx.send(embed=embedVar)
                                                await asyncio.sleep(2)
                                            
                                            damage_calculation_response = player1_card.damage_cal(int(button_ctx.custom_id), _battle, player2_card)
                                        
                                        elif button_ctx.custom_id == "3":
                                            if _battle._is_tutorial and _battle.tutorial_ultimate==False:
                                                _battle.tutorial_ultimate=True
                                                embedVar = discord.Embed(title=f":rosette:Ultimate Move!",
                                                                        description=f":rosette:**Ultimate Move** cost **80 ST(Stamina)** to deal incredible Damage!",
                                                                        colour=0xe91e63)
                                                embedVar.add_field(
                                                    name=f"Your Ultimate: {player1_card.move3_emoji} {player1_card.move3} inflicts {player1_card.move3_element}",
                                                    value=f"**{player1_card.move3_element}** : *{element_mapping[player1_card.move3_element]}*")
                                                embedVar.add_field(name=f"Ultimate GIF",
                                                                value="Using your ultimate move also comes with a bonus GIF to deliver that final blow!\n*Enter performance mode to disable GIFs\n/performace*")
                                                embedVar.set_footer(
                                                    text=f"Ultimate moves will consume most of your ST(Stamina) for Incredible Damage! Use Them Wisely!")
                                                await button_ctx.send(embed=embedVar)
                                                await asyncio.sleep(2)
                                           
                                            damage_calculation_response = player1_card.damage_cal(int(button_ctx.custom_id), _battle, player2_card)
                                            if player1_card.gif != "N/A" and not player1.performance:
                                                # await button_ctx.defer(ignore=True)
                                                await battle_msg.delete(delay=None)
                                                # await asyncio.sleep(1)
                                                battle_msg = await private_channel.send(f"{player1_card.gif}")
                                                
                                                await asyncio.sleep(2)
                                        
                                        elif button_ctx.custom_id == "4":
                                            if _battle._is_tutorial and _battle.tutorial_enhancer==False:
                                                _battle.tutorial_enhancer = True
                                                embedVar = discord.Embed(title=f"🦠Enhancers!",
                                                                        description=f"🦠**Enhancers** cost **20 ST(Stamina)** to Boost your Card or Debuff Your Opponent!",
                                                                        colour=0xe91e63)
                                                embedVar.add_field(
                                                    name=f"Your Enhancer:🦠 {player1_card.move4} is a {player1_card.move4enh}",
                                                    value=f"**{player1_card.move4enh}** : *{enhancer_mapping[player1_card.move4enh]}*")
                                                embedVar.set_footer(
                                                    text=f"Use /enhancers to view a full list of Enhancers! Look for the {player1_card.move4enh} Enhancer")
                                                await button_ctx.send(embed=embedVar)
                                                await asyncio.sleep(2)

                                            damage_calculation_response = player1_card.damage_cal(int(button_ctx.custom_id), _battle, player2_card)

                                        elif button_ctx.custom_id == "5":
                                            # Resolve Check and Calculation
                                            if not player1_card.used_resolve and player1_card.used_focus:
                                                if _battle._is_tutorial and _battle.tutorial_resolve == False:
                                                    _battle.tutorial_resolve = True
                                                    embedVar = discord.Embed(title=f"⚡**Resolve Transformation**!",
                                                                            description=f"**Heal**, Boost **ATK**, and 🧬**Summon**!",
                                                                            colour=0xe91e63)
                                                    embedVar.add_field(name=f"Trade Offs!",
                                                                    value="Sacrifice **DEF** and **Focusing** will not increase **ATK** or **DEF**")
                                                    embedVar.add_field(name=f"🧬Your Summon",
                                                                    value=f"**{player1_card._summon_name}**")
                                                    embedVar.set_footer(
                                                        text=f"You can only enter ⚡Resolve once per match! Use the Heal Wisely!!!")
                                                    await button_ctx.send(embed=embedVar)
                                                    await asyncio.sleep(2)

                                                player1_card.resolving(_battle, player2_card, player1)
                                                if _battle._is_boss:
                                                    await button_ctx.send(embed=_battle._boss_embed_message)
                                            else:
                                                emessage = m.CANNOT_USE_RESOLVE
                                                embedVar = discord.Embed(title=emessage, colour=0xe91e63)
                                                previous_moves.append(f"(**{_battle._turn_total}**) **{player1_card.name}** cannot resolve")
                                                await button_ctx.defer(ignore=True)
                                                _battle._is_turn = _battle._repeat_turn()
                                        
                                        elif button_ctx.custom_id == "6":
                                            # Resolve Check and Calculation
                                            if player1_card.used_resolve and player1_card.used_focus and not player1_card.used_summon:
                                                if _battle._is_tutorial and _battle.tutorial_summon == False:
                                                    _battle.tutorial_summon = True
                                                    embedVar = discord.Embed(title=f"{player1_card.name} Summoned 🧬 **{player1_card._summon_name}**",colour=0xe91e63)
                                                    embedVar.add_field(name=f"🧬**Summon Enhancers**!",
                                                                    value="You can use 🧬**Summons** once per Focus without losing a turn!")
                                                    embedVar.add_field(name=f"Resting",
                                                                    value="🧬**Summons** need to rest after using their ability! **Focus** to Replenish your 🧬**Summon**")
                                                    embedVar.set_footer(
                                                        text=f"🧬Summons will Level Up and build Bond as you win battles! Train up your 🧬summons to perform better in the field!")
                                                    await button_ctx.send(embed=embedVar)
                                                    await asyncio.sleep(2)
                                            summon_response = player1_card.use_summon(_battle, player2_card)
                                            
                                            if not player1.performance and summon_response['CAN_USE_MOVE']:
                                                await battle_msg.delete(delay=2)
                                                tsummon_file = showsummon(player1_card.summon_image, player1_card.summon_name, summon_response['MESSAGE'], player1_card.summon_lvl, player1_card.summon_bond)
                                                embedVar.set_image(url="attachment://pet.png")
                                                await asyncio.sleep(2)
                                                battle_msg = await private_channel.send(embed=embedVar, file=tsummon_file)
                                                await asyncio.sleep(2)
                                                await battle_msg.delete(delay=2)

                                        elif _battle._is_co_op:
                                            if button_ctx.custom_id == "7":
                                                player1_card.use_companion_enhancer(_battle, player2_card, player3_card)
                                            
                                            elif button_ctx.custom_id == "8":
                                                # Use companion enhancer on you
                                                player3_card.use_companion_enhancer(_battle, player2_card, player1_card)

                                            elif button_ctx.custom_id == "9":
                                                player3_card.use_block(_battle, player2_card, player1_card)

                                        if button_ctx.custom_id == "0":
                                            if _battle._is_tutorial and _battle.tutorial_block==False:
                                                _battle.tutorial_block=True
                                                embedVar = discord.Embed(title=f"🛡️Blocking!",
                                                                        description=f"🛡️**Blocking** cost **20 ST(Stamina)** to Double your **DEF** until your next turn!",
                                                                        colour=0xe91e63)
                                                embedVar.add_field(name=f"**Engagements**",
                                                                value="You will take less DMG when your **DEF** is greater than your opponenents **ATK**")
                                                embedVar.add_field(name=f"**Engagement Insight**",
                                                                value="💢: %33-%50 of AP\n❕: %50-%75 AP\n‼️: %75-%120 AP\n〽️x1.5: %120-%150 AP\n❌x2: $150-%200 AP")
                                                embedVar.set_footer(
                                                    text=f"Use 🛡️Block strategically to defend against your opponents strongest abilities!")
                                                await button_ctx.send(embed=embedVar)
                                                await asyncio.sleep(2)
                                            
                                            player1_card.use_block(_battle, player2_card)                                            

                                        if button_ctx.custom_id in _battle.main_battle_options:
                                            player1_card.damage_done(_battle, damage_calculation_response, player2_card)
                                    
                                    except asyncio.TimeoutError:
                                        await battle_msg.edit(components=[])
                                        if not _battle._is_abyss and not _battle._is_scenario and not _battle._is_explore and not _battle._is_pvp_match and not _battle._is_tutorial:
                                            await save_spot(self, ctx, _battle._selected_universe, _battle.mode, _battle._currentopponent)
                                        
                                        await ctx.send(f"{ctx.author.mention} {_battle.error_end_match_message()}")
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
                                        guild = self.bot.get_guild(main.guild_id)
                                        channel = guild.get_channel(main.guild_channel)
                                        await channel.send(f"'PLAYER': **{str(ctx.author)}**, 'GUILD': **{str(ctx.author.guild)}**, TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")

                        if _battle._is_turn == 1:
                            player2_card.reset_stats_to_limiter(player1_card)

                            player2_card.yuyu_hakusho_attack_increase()

                            player2_card.activate_chainsawman_trait(_battle)

                            _battle.add_battle_history_messsage(player2_card.set_bleed_hit(_battle._turn_total, player1_card))

                            _battle.add_battle_history_messsage(player2_card.set_burn_hit(player1_card))

                            if player1_card.freeze_enh:
                                new_turn = player2_card.frozen(_battle, player1_card)
                                _battle._is_turn = new_turn['MESSAGE']
                                _battle.add_battle_history_messsage(new_turn['TURN'])
                                continue
                            player2_card.freeze_enh = False

                            _battle.add_battle_history_messsage(player2_card.set_poison_hit(player1_card))
                                
                            player2_card.set_gravity_hit()


                            player2_title.activate_title_passive(_battle, player2_card, player1_card)
                            
                            player2_card.activate_card_passive(player1_card)

                            player2_card.activate_demon_slayer_trait(_battle, player1_card)

                            player1_card.activate_demon_slayer_trait(_battle, player2_card)

                            if player2_card.used_block == True:
                                player2_card.defense = int(player2_card.defense / 2)
                                player2_card.used_block = False
                            if player2_card.used_defend == True:
                                player2_card.defense = int(player2_card.defense / 2)
                                player2_card.used_defend = False

                            player1_card.set_deathnote_message(_battle)
                            player2_card.set_deathnote_message(_battle)
                            if _battle._is_co_op:
                                player3_card.set_deathnote_message(_battle)                            
                            

                            # Focus
                            if player2_card.stamina < 10:
                                player2_card.focusing(player2_title, player1_title, player1_card, _battle)

                                if _battle._is_boss:
                                    embedVar = discord.Embed(title=f"**{player2_card.name}** Enters Focus State",
                                                            description=f"{_battle._powerup_boss_description}", colour=0xe91e63)
                                    embedVar.add_field(name=f"A great aura starts to envelop **{player2_card.name}** ",
                                                    value=f"{_battle._aura_boss_description}")
                                    embedVar.set_footer(text=f"{player2_card.name} Says: 'Now, are you ready for a real fight?'")
                                    await ctx.send(embed=embedVar)
                                    previous_moves.append(f"(**{_battle._turn_total}**) 🌀 **{player2_card.name}** focused")
                                    # await asyncio.sleep(2)
                                    if player2_card.universe == "Digimon" and player2_card.used_resolve is False:
                                        embedVar = discord.Embed(title=f"(**{_battle._turn_total}**) :zap: **{player2_card.name}** Resolved!", description=f"{_battle._rmessage_boss_description}",
                                                                colour=0xe91e63)
                                        embedVar.set_footer(text=f"{player1_card.name} this will not be easy...")
                                        await ctx.send(embed=embedVar)
                                        await asyncio.sleep(2)

                            else:
                                player2_card.set_battle_arm_messages(player1_card)

                                player2_card.activate_solo_leveling_trait(_battle, player1_card)
                                                                
                                embedVar = discord.Embed(title=f"➡️ **Opponent Turn** {_battle._turn_total}", description=textwrap.dedent(f"""\
                                {_battle.get_previous_moves_embed()}
                                
                                """), color=0xe74c3c)
                                embedVar.set_footer(
                                    text=f"{_battle.get_battle_window_title_text(player2_card, player1_card)}",
                                    icon_url="https://cdn.discordapp.com/emojis/789290881654980659.gif?v=1")


                                if _battle._is_pvp_match:
                                    _battle.set_battle_options(player1_card, player2_card)
                                    # Check If Playing Bot
                                    if not _battle.is_ai_opponent:

                                        battle_action_row = manage_components.create_actionrow(*_battle.battle_buttons)
                                        util_action_row = manage_components.create_actionrow(*_battle.utility_buttons)

                                        player2_card.set_battle_arm_messages(player2_card)

                                        components = [battle_action_row, util_action_row]
                                        embedVar = discord.Embed(title=f"", description=textwrap.dedent(f"""\
                                        {_battle.get_previous_moves_embed()}

                                        """), color=0xe74c3c)
                                        embedVar.set_author(name=f"{player2_card._arm_message}\n{player2_card.summon_resolve_message}\n")
                                        embedVar.add_field(name=f"➡️ **Current Turn** {_battle._turn_total}", value=f"{user2.mention} Select move below!")
                                        embedVar.set_image(url="attachment://image.png")
                                        embedVar.set_footer(
                                            text=f"{_battle.get_battle_footer_text(player1_card, player2_card)}",
                                            icon_url="https://cdn.discordapp.com/emojis/789290881654980659.gif?v=1")
                                        await battle_msg.delete(delay=1)
                                        await asyncio.sleep(1)
                                        battle_msg = await private_channel.send(embed=embedVar, components=components, file=player2_card.showcard(_battle.mode, player2_arm, player2_title, _battle._turn_total, player1_card.defense))

                                        # Make sure user is responding with move
                                        def check(button_ctx):
                                            return button_ctx.author == user2 and button_ctx.custom_id in options

                                        try:
                                            button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot,
                                                                                                                    components=[
                                                                                                                        battle_action_row,
                                                                                                                        util_action_row],
                                                                                                                    timeout=120,
                                                                                                                    check=check)

                                            if button_ctx.custom_id == "q" or button_ctx.custom_id == "Q":
                                                player2_card.health = 0
                                                _battle.game_over = True
                                                await battle_msg.delete(delay=1)
                                                await asyncio.sleep(1)
                                                battle_msg = await private_channel.send(content=f"{user2.mention} has fled.")

                                                #return
                                            if button_ctx.custom_id == "1":
                                                damage_calculation_response = player2_card.damage_cal(int(button_ctx.custom_id), _battle, player1_card)
                                            
                                            elif button_ctx.custom_id == "2":
                                                damage_calculation_response = player2_card.damage_cal(int(button_ctx.custom_id), _battle, player1_card)
                                            
                                            elif button_ctx.custom_id == "3":

                                                damage_calculation_response = player2_card.damage_cal(int(button_ctx.custom_id), _battle, player1_card)
                                                if player2_card.gif != "N/A" and not player1.performance:
                                                    # await button_ctx.defer(ignore=True)
                                                    await battle_msg.delete(delay=None)
                                                    # await asyncio.sleep(1)
                                                    battle_msg = await private_channel.send(f"{player2_card.gif}")
                                                    
                                                    await asyncio.sleep(2)
                                            elif button_ctx.custom_id == "4":
                                                damage_calculation_response = player2_card.damage_cal(int(button_ctx.custom_id), _battle, player1_card)
                                            
                                            elif button_ctx.custom_id == "5":
                                                player2_card.resolving(_battle, player1_card, player2)
                                            
                                            elif button_ctx.custom_id == "6" and not _battle._is_raid:
                                                player2_card.use_summon(_battle, player1_card)
                                            
                                            elif button_ctx.custom_id == "0":
                                                player2_card.use_block(_battle, player1_card)                                            

                                            if button_ctx.custom_id in _battle.main_battle_options:
                                                player2_card.damage_done(_battle, damage_calculation_response, player1_card)
                                        
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
                                            guild = self.bot.get_guild(main.guild_id)
                                            channel = guild.get_channel(main.guild_channel)
                                            await channel.send(f"'PLAYER': **{str(ctx.author)}**, 'GUILD': **{str(ctx.author.guild)}**, TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")

                                    # Play Bot
                                    else:
                                        player2_card.set_battle_arm_messages(player1_card)

                                        player2_card.activate_solo_leveling_trait(_battle, player1_card)

                                        _battle.set_battle_options(player2_card, player1_card)

                                        tembedVar = discord.Embed(title=f"_Turn_ {_battle._turn_total}", description=textwrap.dedent(f"""\
                                        {_battle.get_previous_moves_embed()}
                                        """), color=0xe74c3c)
                                        tembedVar.set_image(url="attachment://image.png")
                                        await battle_msg.delete(delay=2)
                                        await asyncio.sleep(2)
                                        battle_msg = await private_channel.send(embed=tembedVar, file=player2_card.showcard(_battle.mode, player2_arm, player2_title, _battle._turn_total, player1_card.defense))
                                        await asyncio.sleep(3)
                                        
                                        selected_move = _battle.ai_battle_command(player2_card, player1_card)

                                        damage_calculation_response = player2_card.damage_cal(selected_move, _battle, player1_card)

                                        if selected_move == 5:
                                            player2_card.resolving(_battle, player1_card, player2)
                                            if _battle._is_boss:
                                                await button_ctx.send(embed=_battle._boss_embed_message)

                                        elif selected_move == 6:
                                            # Resolve Check and Calculation
                                            player2_card.use_summon(_battle, player1_card)
                                        
                                        if selected_move == 7:
                                            player2_card.use_block(_battle, damage_calculation_response, player1_card)

                                        if selected_move != 5 and selected_move != 6 and selected_move != 0:
                                            player2_card.damage_done(_battle, damage_calculation_response, player1_card)                                        

                                if not _battle._is_pvp_match:
                                    if _battle._is_auto_battle:
                                        await asyncio.sleep(2)
                                        embedVar.set_thumbnail(url=ctx.author.avatar_url)
                                        await battle_msg.edit(embed=embedVar, components=[])
                                    
                                    if not _battle._is_auto_battle:
                                        player2_card.set_battle_arm_messages(player1_card)

                                        player2_card.activate_solo_leveling_trait(_battle, player1_card)
                                        tembedVar = discord.Embed(title=f"_Turn_ {_battle._turn_total}", description=textwrap.dedent(f"""\
                                        {_battle.get_previous_moves_embed()}
                                        """), color=0xe74c3c)
                                        tembedVar.set_image(url="attachment://image.png")
                                        await battle_msg.delete(delay=None)
                                        # await asyncio.sleep(2)
                                        battle_msg = await private_channel.send(embed=tembedVar, file=player2_card.showcard(_battle.mode, player2_arm, player2_title, _battle._turn_total, player1_card.defense))


                                    selected_move = _battle.ai_battle_command(player2_card, player1_card)
                                                                        
                                    if int(selected_move) in [1, 2, 3, 4]:
                                        damage_calculation_response = player2_card.damage_cal(selected_move, _battle, player1_card)                                    
                                        if _battle._is_auto_battle:
                                            if player2_card.gif != "N/A"  and not player1.performance:
                                                await battle_msg.delete(delay=2)
                                                await asyncio.sleep(2)
                                                battle_msg = await private_channel.send(f"{player2_card.gif}")
                                                await asyncio.sleep(2)

                                    elif int(selected_move) == 5:
                                        player2_card.resolving(_battle, player1_card)
                                        if _battle._is_boss:
                                            await button_ctx.send(embed=_battle._boss_embed_message)

                                    elif int(selected_move) == 6:
                                        # Resolve Check and Calculation
                                        if player2_card.used_resolve and player2_card.used_focus and not player2_card.used_summon:
                                            if _battle._is_co_op:
                                                if player3_card.used_defend == True:
                                                    summon_response = player2_card.use_summon(_battle, player3_card)
                                                    if not player1.performance and summon_response['CAN_USE_MOVE']:
                                                        await battle_msg.delete(delay=2)
                                                        tsummon_file = showsummon(player2_card.summon_image, player2_card.summon_name, summon_response['MESSAGE'], player2_card.summon_lvl, player2_card.summon_bond)
                                                        embedVar.set_image(url="attachment://pet.png")
                                                        await asyncio.sleep(2)
                                                        battle_msg = await private_channel.send(embed=embedVar, file=tsummon_file)
                                                        await asyncio.sleep(2)
                                                        await battle_msg.delete(delay=2)

                                                else:
                                                    summon_response = player2_card.use_summon(_battle, player1_card)
                                                    if not player1.performance and summon_response['CAN_USE_MOVE']:
                                                        await battle_msg.delete(delay=2)
                                                        tsummon_file = showsummon(player2_card.summon_image, player2_card.summon_name, summon_response['MESSAGE'], player2_card.summon_lvl, player2_card.summon_bond)
                                                        embedVar.set_image(url="attachment://pet.png")
                                                        await asyncio.sleep(2)
                                                        battle_msg = await private_channel.send(embed=embedVar, file=tsummon_file)
                                                        await asyncio.sleep(2)
                                                        await battle_msg.delete(delay=2)

                                            else:
                                                summon_response = player2_card.use_summon(_battle, player1_card)
                                                if not player1.performance and summon_response['CAN_USE_MOVE']:
                                                    await battle_msg.delete(delay=2)
                                                    tsummon_file = showsummon(player2_card.summon_image, player2_card.summon_name, summon_response['MESSAGE'], player2_card.summon_lvl, player2_card.summon_bond)
                                                    embedVar.set_image(url="attachment://pet.png")
                                                    await asyncio.sleep(2)
                                                    battle_msg = await private_channel.send(embed=embedVar, file=tsummon_file)
                                                    await asyncio.sleep(2)
                                                    await battle_msg.delete(delay=2)

                                        else:
                                            _battle.add_battle_history_messsage(f"(**{_battle._turn_total}**) {player2_card.name} Could not summon 🧬 **{player2_card.name}**. Needs rest")
                                    elif int(selected_move) == 7:
                                        player2_card.use_block(_battle, player1_card)                                            
                                    if int(selected_move) != 5 and int(selected_move) != 6 and int(selected_move) != 7:

                                        # If you have enough stamina for move, use it
                                        # if c used block
                                        if _battle._is_co_op:
                                            if player3_card.used_defend == True:
                                                player2_card.damage_done(_battle, damage_calculation_response, player3_card)
                                            else:
                                                player2_card.damage_done(_battle, damage_calculation_response, player1_card)
                                        else:
                                            player2_card.damage_done(_battle, damage_calculation_response, player1_card)


                        elif _battle._is_co_op and turn != (0 or 1):
                            if turn == 2:
                                player3_card.reset_stats_to_limiter(player2_card)

                                player3_card.yuyu_hakusho_attack_increase()

                                player3_card.activate_chainsawman_trait(_battle)

                                _battle.add_battle_history_messsage(player3_card.set_bleed_hit(_battle._turn_total, player2_card))

                                _battle.add_battle_history_messsage(player3_card.set_burn_hit(player2_card))

                                if player2_card.freeze_enh:
                                    new_turn = player3_card.frozen(_battle, player2_card)
                                    _battle._is_turn = new_turn['MESSAGE']
                                    _battle.add_battle_history_messsage(new_turn['TURN'])
                                    continue
                                player3_card.freeze_enh = False

                                _battle.add_battle_history_messsage(player3_card.set_poison_hit(player2_card))
                                    
                                player3_card.set_gravity_hit()


                                player3_title.activate_title_passive(_battle, player3_card, player2_card)
                                
                                player3_card.activate_card_passive(player1_card)

                                player3_card.activate_demon_slayer_trait(_battle, player2_card)

                                player2_card.activate_demon_slayer_trait(_battle, player3_card)

                                if player3_card.used_block == True:
                                    player3_card.defense = int(player3_card.defense / 2)
                                    player3_card.used_block = False
                                if player3_card.used_defend == True:
                                    player3_card.defense = int(player3_card.defense / 2)
                                    player3_card.used_defend = False

                                player2_card.set_deathnote_message(_battle)
                                player3_card.set_deathnote_message(_battle)


                                if c_stamina < 10:
                                    player3_card.focusing(player3_title, player2_title, player2_card, _battle)
                                else:
                                    if _battle._is_auto_battle:
                                        player3_card.set_battle_arm_messages(player2_card)

                                        player3_card.activate_solo_leveling_trait(_battle, player2_card)


                                        #await private_channel.send(file=companion_card)
                                        tembedVar = discord.Embed(title=f"_Turn_ {_battle._turn_total}", description=textwrap.dedent(f"""\
                                        {_battle.get_previous_moves_embed()}
                                        """), color=0xe74c3c)
                                        await battle_msg.edit(embed=embedVar, components=[])


                                        selected_move = _battle.ai_battle_command(player3_card, player2_card)

                                        if selected_move in [1, 2, 3, 4]:
                                            damage_calculation_response = player3_card.damage_cal(selected_move, _battle, player2_card)
                                        
                                        if selected_move == 5:
                                            player3_card.resolving(_battle, player2_card, player3)
                                        
                                        if selected_move == 6:
                                            player3_card.use_summon(_battle, player2_card)                                        
                                        
                                        elif selected_move == 8:
                                            player3_card.use_companion_enhancer(_battle, player2_card, player1_card)
                                        
                                        elif selected_move == 7:
                                            player3_card.use_defend(_battle, player1_card)

                                        if selected_move != 5 and selected_move != 6 and selected_move != 7 and selected_move != 8:
                                            player3_card.damage_done(_battle, damage_calculation_response, player2_card) 

                                    else:
                                        player3_card.set_battle_arm_messages(player2_card)

                                        player3_card.activate_solo_leveling_trait(_battle, player2_card)

                                        _battle.set_battle_options(player3_card, player2_card)

                                        battle_action_row = manage_components.create_actionrow(*_battle.battle_buttons)
                                        util_action_row = manage_components.create_actionrow(*_battle.utility_buttons)


                                        battle_action_row = manage_components.create_actionrow(*battle_buttons)
                                        util_action_row = manage_components.create_actionrow(*util_buttons)
                                        coop_util_action_row = manage_components.create_actionrow(*coop_util_buttons)

                                        embedVar = discord.Embed(title=f"", description=textwrap.dedent(f"""\
                                        {previous_moves_into_embed}
                                        
                                        """), color=0xe74c3c)
                                        embedVar.set_author(name=f"{player3_card._arm_message}\n{player3_card.summon_resolve_message}\n")
                                        embedVar.add_field(name=f"➡️ **Current Turn** {_battle._turn_total}", value=f"{user2.mention} Select move below!")
                                        # await asyncio.sleep(2)
                                        embedVar.set_image(url="attachment://image.png")
                                        embedVar.set_footer(
                                            text=f"{_battle.get_battle_footer_text(player2_card, player3_card)}",
                                            icon_url="https://cdn.discordapp.com/emojis/789290881654980659.gif?v=1")
                                        await battle_msg.delete(delay=2)
                                        await asyncio.sleep(2)
                                        battle_msg = await private_channel.send(embed=embedVar, components=[battle_action_row, util_action_row,
                                                                            coop_util_action_row], file=player3_card.showcard(_battle.mode, player3_arm, player3_title, _battle._turn_total, player2_card.defense))
                                        # Make sure user is responding with move
                                        def check(button_ctx):
                                            return button_ctx.author == user and button_ctx.custom_id in options

                                        try:
                                            button_ctx: ComponentContext = await manage_components.wait_for_component(
                                                self.bot,
                                                components=[battle_action_row, util_action_row, coop_util_action_row],
                                                timeout=120, check=check)

                                            # calculate data based on selected move
                                            if button_ctx.custom_id == "q" or button_ctx.custom_id == "Q":
                                                player3_card.health = 0
                                                _battle.game_over = True
                                                _battle.add_battle_history_messsage(f"(**{_battle._turn_total}**) 💨 **{player3_card.name}** Fled...")
                                                await asyncio.sleep(1)
                                                await battle_msg.delete(delay=1)
                                                battle_msg = await private_channel.send(content=f"{ctx.author.mention} has fled.")
                                            
                                            if button_ctx.custom_id == "1":
                                                damage_calculation_response = player3_card.damage_cal(int(button_ctx.custom_id), _battle, player2_card)
                                            
                                            elif button_ctx.custom_id == "2":
                                                damage_calculation_response = player3_card.damage_cal(int(button_ctx.custom_id), _battle, player2_card)
                                            
                                            elif button_ctx.custom_id == "3":
                                                damage_calculation_response = player3_card.damage_cal(int(button_ctx.custom_id), _battle, player2_card)
                                                if player3_card.gif != "N/A" and not player3.performance:
                                                    # await button_ctx.defer(ignore=True)
                                                    await battle_msg.delete(delay=None)
                                                    # await asyncio.sleep(1)
                                                    battle_msg = await private_channel.send(f"{player3_card.gif}")
                                                    
                                                    await asyncio.sleep(2)
                                            elif button_ctx.custom_id == "4":
                                                damage_calculation_response = player1_card.damage_cal(int(button_ctx.custom_id), _battle, player2_card)
                                            
                                            elif button_ctx.custom_id == "5":
                                                player3_card.resolving(_battle, player2_card, player3)
                                            
                                            elif button_ctx.custom_id == "6":
                                                summon_response = player3_card.use_summon(_battle, player2_card)
                                                
                                                if not player3.performance and summon_response['CAN_USE_MOVE']:
                                                    await battle_msg.delete(delay=2)
                                                    tsummon_file = showsummon(player3_card.summon_image, player3_card.summon_name, summon_response['MESSAGE'], player3_card.summon_lvl, player3_card.summon_bond)
                                                    embedVar.set_image(url="attachment://pet.png")
                                                    await asyncio.sleep(2)
                                                    battle_msg = await private_channel.send(embed=embedVar, file=tsummon_file)
                                                    await asyncio.sleep(2)
                                                    await battle_msg.delete(delay=2)
                                            
                                            elif button_ctx.custom_id == "7":
                                                player3_card.use_companion_enhancer(_battle, player2_card, player1_card)

                                            
                                            elif button_ctx.custom_id == "0":
                                                player3_card.use_block(_battle, player2_card)                                            

                                            if button_ctx.custom_id != "5" and button_ctx.custom_id != "6" and button_ctx.custom_id != "7" and button_ctx.custom_id != "0" and button_ctx.custom_id != "q" and button_ctx.custom_id in options:
                                                player3_card.damage_done(_battle, damage_calculation_response, player2_card)
                                        except asyncio.TimeoutError:
                                            await battle_msg.delete()
                                            #await battle_msg.edit(components=[])
                                            await save_spot(self, ctx, _battle._selected_universe, _battle.mode, _battle._currentopponent)
                                            await ctx.author.send(f"{ctx.author.mention} your game timed out. Your channel has been closed but your spot in the tales has been saved where you last left off.")
                                            await ctx.send(f"{ctx.author.mention} your game timed out. Your channel has been closed but your spot in the tales has been saved where you last left off.")
                                            # await discord.TextChannel.delete(private_channel, reason=None)
                                            _battle.add_battle_history_messsage(f"(**{_battle._turn_total}**) 💨 **{player3_card.name}** Fled...")
                                            # c_health = 0
                                            # o_health = 0
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
                                            guild = self.bot.get_guild(main.guild_id)
                                            channel = guild.get_channel(main.guild_channel)
                                            await channel.send(f"'PLAYER': **{str(ctx.author)}**, 'GUILD': **{str(ctx.author.guild)}**, TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")

                            # Opponent Turn Start
                            elif turn == 3:
                                player2_card.reset_stats_to_limiter(player3_card)

                                player2_card.yuyu_hakusho_attack_increase()

                                player2_card.activate_chainsawman_trait(_battle)

                                _battle.add_battle_history_messsage(player2_card.set_bleed_hit(_battle._turn_total, player3_card))

                                _battle.add_battle_history_messsage(player2_card.set_burn_hit(player3_card))

                                if player3_card.freeze_enh:
                                    new_turn = player2_card.frozen(_battle, player3_card)
                                    _battle._is_turn = new_turn['MESSAGE']
                                    _battle.add_battle_history_messsage(new_turn['TURN'])
                                    continue
                                player2_card.freeze_enh = False

                                _battle.add_battle_history_messsage(player2_card.set_poison_hit(player3_card))
                                    
                                player2_card.set_gravity_hit()


                                player2_title.activate_title_passive(_battle, player2_card, player3_card)
                                
                                player2_card.activate_card_passive(player3_card)

                                player2_card.activate_demon_slayer_trait(_battle, player3_card)

                                player3_card.activate_demon_slayer_trait(_battle, player2_card)

                                if player2_card.used_block == True:
                                    player2_card.defense = int(player2_card.defense / 2)
                                    player2_card.used_block = False
                                if player2_card.used_defend == True:
                                    player2_card.defense = int(player2_card.defense / 2)
                                    player2_card.used_defend = False

                                player3_card.set_deathnote_message(_battle)
                                player2_card.set_deathnote_message(_battle)


                                # Focus
                                if t_stamina < 10:
                                    player2_card.focusing(player2_title, player3_title, player3_card, _battle)

                                    if _battle._is_boss:
                                        embedVar = discord.Embed(title=f"**{player2_card.name}** Enters Focus State",
                                                                description=f"{_battle._powerup_boss_description}", colour=0xe91e63)
                                        embedVar.add_field(name=f"A great aura starts to envelop **{player2_card.name}** ",
                                                        value=f"{_battle._aura_boss_description}")
                                        embedVar.set_footer(text=f"{player2_card.name} Says: 'Now, are you ready for a real fight?'")
                                        await ctx.send(embed=embedVar)
                                        previous_moves.append(f"(**{_battle._turn_total}**) 🌀 **{player2_card.name}** focused")
                                        # await asyncio.sleep(2)
                                        if player2_card.universe == "Digimon" and player2_card.used_resolve is False:
                                            embedVar = discord.Embed(title=f"(**{_battle._turn_total}**) :zap: **{player2_card.name}** Resolved!", description=f"{_battle._rmessage_boss_description}",
                                                                    colour=0xe91e63)
                                            embedVar.set_footer(text=f"{player3_card.name} this will not be easy...")
                                            await ctx.send(embed=embedVar)
                                            await asyncio.sleep(2)
                                
                                else:
                                    player2_card.set_battle_arm_messages(player3_card)

                                    player2_card.activate_solo_leveling_trait(_battle, player3_card)
                                    tembedVar = discord.Embed(title=f"_Turn_ {_battle._turn_total}", description=textwrap.dedent(f"""\
                                    {_battle.get_previous_moves_embed()}
                                    """), color=0xe74c3c)
                                    tembedVar.set_image(url="attachment://image.png")
                                    await battle_msg.delete(delay=None)
                                    # await asyncio.sleep(2)
                                    battle_msg = await private_channel.send(embed=tembedVar, file=player2_card.showcard(_battle.mode, player2_arm, player2_title, _battle._turn_total, player3_card.defense))


                                    selected_move = _battle.ai_battle_command(player2_card, player3_card)
                                    
                                    damage_calculation_response = player2_card.damage_cal(selected_move, _battle, player3_card)
                                    
                                    if int(selected_move) == 3:                                    

                                        if _battle._is_auto_battle:
                                            if player2_card.gif != "N/A"  and not player1.performance:
                                                await battle_msg.delete(delay=2)
                                                await asyncio.sleep(2)
                                                battle_msg = await private_channel.send(f"{player2_card.gif}")
                                                await asyncio.sleep(2)

                                    elif int(selected_move) == 5:
                                        player2_card.resolving(_battle, player3_card, player2)
                                        if _battle._is_boss:
                                            await button_ctx.send(embed=_battle._boss_embed_message)

                                    elif int(selected_move) == 6:
                                        # Resolve Check and Calculation
                                        if player2_card.used_resolve and player2_card.used_focus and not player2_card.used_summon:
                                            if _battle._is_co_op:
                                                if player3_card.used_defend == True:
                                                    summon_response = player2_card.use_summon(_battle, player1_card)
                                                    if not player1.performance and summon_response['CAN_USE_MOVE']:
                                                        await battle_msg.delete(delay=2)
                                                        tsummon_file = showsummon(player2_card.summon_image, player2_card.summon_name, summon_response['MESSAGE'], player2_card.summon_lvl, player2_card.summon_bond)
                                                        embedVar.set_image(url="attachment://pet.png")
                                                        await asyncio.sleep(2)
                                                        battle_msg = await private_channel.send(embed=embedVar, file=tsummon_file)
                                                        await asyncio.sleep(2)
                                                        await battle_msg.delete(delay=2)

                                                else:
                                                    summon_response = player2_card.use_summon(_battle, player3_card)
                                                    if not player1.performance and summon_response['CAN_USE_MOVE']:
                                                        await battle_msg.delete(delay=2)
                                                        tsummon_file = showsummon(player2_card.summon_image, player2_card.summon_name, summon_response['MESSAGE'], player2_card.summon_lvl, player2_card.summon_bond)
                                                        embedVar.set_image(url="attachment://pet.png")
                                                        await asyncio.sleep(2)
                                                        battle_msg = await private_channel.send(embed=embedVar, file=tsummon_file)
                                                        await asyncio.sleep(2)
                                                        await battle_msg.delete(delay=2)

                                            else:
                                                summon_response = player2_card.use_summon(_battle, player3_card)
                                                if not player1.performance and summon_response['CAN_USE_MOVE']:
                                                    await battle_msg.delete(delay=2)
                                                    tsummon_file = showsummon(player2_card.summon_image, player2_card.summon_name, summon_response['MESSAGE'], player2_card.summon_lvl, player2_card.summon_bond)
                                                    embedVar.set_image(url="attachment://pet.png")
                                                    await asyncio.sleep(2)
                                                    battle_msg = await private_channel.send(embed=embedVar, file=tsummon_file)
                                                    await asyncio.sleep(2)
                                                    await battle_msg.delete(delay=2)

                                        else:
                                            _battle.add_battle_history_messsage(f"(**{_battle._turn_total}**) {player2_card.name} Could not summon 🧬 **{player2_card.name}**. Needs rest")
                                    elif int(selected_move) == 7:
                                        player2_card.use_block(_battle, player3_card)                                            
                                    if int(selected_move) != 5 and int(selected_move) != 6 and int(selected_move) != 7:

                                        # If you have enough stamina for move, use it
                                        # if c used block
                                        if _battle._is_co_op:
                                            if player3_card.used_defend == True:
                                                player2_card.damage_done(_battle, damage_calculation_response, player1_card)
                                            else:
                                                player2_card.damage_done(_battle, damage_calculation_response, player3_card)
                                        else:
                                            player2_card.damage_done(_battle, damage_calculation_response, player3_card)
                    
                    if (_battle.game_over(player1_card, player2_card) == True and not _battle._is_co_op) or (_battle.game_over(player1_card, player2_card, player3_card) == True and not _battle.is_co_op):
                        wintime = time.asctime()
                        h_playtime = int(wintime[11:13])
                        m_playtime = int(wintime[14:16])
                        s_playtime = int(wintime[17:19])
                        gameClock = getTime(int(h_gametime), int(m_gametime), int(s_gametime), h_playtime, m_playtime,
                                            s_playtime)

                        if _battle._is_pvp_match or _battle._is_raid:
                            try:

                                # put _battle.pvp_victory_embed here
                                if _battle.player1_wins:
                                    pvp_response = await _battle.pvp_victory_embed(player1, player1_card, player1_arm, player1_title, player2, player2_card)
                                else:
                                    pvp_response = await _battle.pvp_victory_embed(player2, player2_card, player2_arm, player2_title, player1, player1_card)

                                await battle_msg.delete(delay=2)
                                await asyncio.sleep(2)
                                battle_msg = await private_channel.send(embed=pvp_response)
                                continued = False
                                return


                                if _battle._is_raid:
                                    guild_query = {'FDID': oguild['FDID']}
                                    bounty = oguild['BOUNTY']
                                    bonus = oguild['STREAK']
                                    total_bounty = (bounty + ((bonus / 100) * bounty))
                                    winbonus = int(((bonus / 100) * bounty))
                                    if winbonus == 0:
                                        winbonus = bounty
                                    wage = int(total_bounty)
                                    endmessage = f":yen: SHIELD BOUNTY CLAIMED :coin: {'{:,}'.format(winbonus)}"
                                    hall_info = db.queryHall({"HALL":oguild['HALL']})
                                    fee = hall_info['FEE']
                                    if title_match_active:
                                        if shield_test_active:
                                            endmessage = f":flags: {oguild['GNAME']} DEFENSE TEST OVER!"
                                        elif shield_training_active:
                                            endmessage = f":flags: {oguild['GNAME']} TRAINING COMPLETE!"
                                        else:
                                            newshield = db.updateGuild(guild_query, {'$set': {'SHIELD': str(ctx.author)}})
                                            newshieldid = db.updateGuild(guild_query, {'$set': {'SDID': str(ctx.author.id)}})
                                            guildwin = db.updateGuild(guild_query, {'$set': {'BOUNTY': winbonus, 'STREAK': 1}})
                                            endmessage = f":flags: {oguild['GNAME']} SHIELD CLAIMED!"
                                            prev_team_update = {'$set': {'SHIELDING': False}}
                                            remove_shield = db.updateTeam({'TEAM_NAME': str(tteam)}, prev_team_update)
                                            update_shielding = {'$set': {'SHIELDING': True}}
                                            add_shield = db.updateTeam({'TEAM_NAME': str(oteam)}, update_shielding)
                                    else:
                                        guildloss = db.updateGuild(guild_query, {'$set': {'BOUNTY': fee, 'STREAK': 0}})
                                
                                    embedVar = discord.Embed(
                                        title=f"{endmessage}\n\n You have defeated the {tguild} SHIELD!\nMatch concluded in {turn_total} turns",
                                        description=textwrap.dedent(f"""
                                                                    {previous_moves_into_embed}
                                                                    
                                                                    """), colour=0xe91e63)
                                    # embedVar.set_author(name=f"{t_card} says\n{t_lose_description}")
                                    if int(gameClock[0]) == 0 and int(gameClock[1]) == 0:
                                        embedVar.set_footer(text=f"Battle Time: {gameClock[2]} Seconds.")
                                    elif int(gameClock[0]) == 0:
                                        embedVar.set_footer(text=f"Battle Time: {gameClock[1]} Minutes and {gameClock[2]} Seconds.")
                                    else:
                                        embedVar.set_footer(
                                            text=f"Battle Time: {gameClock[0]} Hours {gameClock[1]} Minutes and {gameClock[2]} Seconds.")
                                    embedVar.add_field(name="🔢 Focus Count",
                                                    value=f"**{o_card}**: {o_focus_count}\n**{t_card}**: {t_focus_count}")
                                    if o_focus_count >= t_focus_count:
                                        embedVar.add_field(name="🌀 Most Focused", value=f"**{o_card}**")
                                    else:
                                        embedVar.add_field(name="🌀 Most Focused", value=f"**{t_card}**")
                                    battle_msg = await private_channel.send(embed=embedVar)
                                    continued = False
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
                                guild = self.bot.get_guild(main.guild_id)
                                channel = guild.get_channel(main.guild_channel)
                                await channel.send(f"'PLAYER': **{str(ctx.author)}**, 'GUILD': **{str(ctx.author.guild)}**, TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")

                        else:
                            if _battle._is_explore:
                                explore_response =  await _battle.explore_embed(user1, player1, player1_card, player1_arm, player1_title)
                                await battle_msg.delete(delay=2)
                                await asyncio.sleep(2)
                                battle_msg = await private_channel.send(embed=explore_response)
                                return


                            
                            talisman_response = crown_utilities.inc_talisman(str(o_user['DID']), o_talisman)
                            corrupted_message = ""
                            if mode != "ABYSS" and mode != "SCENARIO" and mode not in RAID_MODES and mode not in PVP_MODES and difficulty != "EASY":
                                if universe['CORRUPTED']:
                                    corrupted_message = await crown_utilities.corrupted_universe_handler(ctx, selected_universe, difficulty)
                                    if not corrupted_message:
                                        corrupted_message = "You must dismantle a card from this universe to enable crafting."

                            tale_or_dungeon_only = ""
                            if mode in U_modes:
                                tale_or_dungeon_only = "Tales"
                            if mode in D_modes:
                                tale_or_dungeon_only = "Dungeon"
                            
                            if mode in B_modes:
                                uid = o_DID
                                ouser = await self.bot.fetch_user(uid)
                                wintime = time.asctime()
                                h_playtime = int(wintime[11:13])
                                m_playtime = int(wintime[14:16])
                                s_playtime = int(wintime[17:19])
                                gameClock = getTime(int(h_gametime), int(m_gametime), int(s_gametime), h_playtime, m_playtime,
                                                    s_playtime)
                                drop_response = await bossdrops(self,ctx.author, t_universe)
                                db.updateUserNoFilter({'DID': str(ctx.author.id)}, {'$set': {'BOSS_FOUGHT': True}})
                                match = await savematch(str(ouser), str(o_card), str(o_card_path), str(otitle['TITLE']),
                                                        str(oarm['ARM']), "N/A", "Boss", o['EXCLUSIVE'])
                                bank_amount = 100000
                                fam_amount = 50000
                                if difficulty == "HARD":
                                    bank_amount = 1500000
                                    fam_amount = 1000000


                                if mode == "CBoss":
                                    # cmatch = await savematch(str(user2), str(c_card), str(c_card_path), str(ctitle['TITLE']),
                                    #                         str(carm['ARM']), "N/A", "Boss", c['EXCLUSIVE'])
                                    cfambank = await crown_utilities.blessfamily(bank_amount, cfam)
                                    cteambank = await crown_utilities.blessteam(bank_amount, cteam)
                                    cpetlogger = await summonlevel(cpet_name, user2)
                                    uc = await main.bot.fetch_user(user2.id)
                                    ccardlogger = await crown_utilities.cardlevel(uc, c_card, user2.id, "Dungeon", selected_universe)
                                    await crown_utilities.bless(50000, str(user2.id))
                                    teammates = False
                                    fam_members =False
                                    stat_bonus = 0
                                    hlt_bonus = 0 
                                    if o_user['TEAM'] == c_user['TEAM'] and o_user['TEAM'] != 'PCG':
                                        teammates=True
                                        stat_bonus=50
                                    if o_user['FAMILY'] == c_user['FAMILY'] and o_user['FAMILY'] != 'PCG':
                                        fam_members=True
                                        hlt_bonus=100
                                    
                                    if teammates==True:
                                        bonus_message = f":checkered_flag:**{o_user['TEAM']}:** 🗡️**+{stat_bonus}** 🛡️**+{stat_bonus}**"
                                        if fam_members==True:
                                            bonus_message = f":family_mwgb:**{o_user['FAMILY']}:** ❤️**+{hlt_bonus}**\n:checkered_flag:**{o_user['TEAM']}:**🗡️**+{stat_bonus}** 🛡️**+{stat_bonus}**"
                                    elif fam_members==True:
                                            bonus_message = f":family_mwgb:**{o_user['FAMILY']}:** ❤️**+{hlt_bonus}**"
                                    else:
                                        bonus_message = f"Join a Guild or Create a Family for Coop Bonuses!"
                                    embedVar = discord.Embed(title=f":zap: **{o_card}** and **{c_card}** defeated the {t_universe} Boss {t_card}!\nMatch concluded in {turn_total} turns!\n\n{drop_response} + :coin: 15,000!\n\n{c_user['NAME']} got :coin: 10,000!", description=textwrap.dedent(f"""
                                    {previous_moves_into_embed}
                                    
                                    """),colour=0x1abc9c)
                                    embedVar.set_author(name=f"**{t_card}** Says: {t_concede}")
                                    embedVar.add_field(name="**Co-Op Bonus**",
                                                value=f"{bonus_message}")
                                else:
                                    embedVar = discord.Embed(title=f":zap: **{o_card}** defeated the {t_universe} Boss {t_card}!\nMatch concluded in {turn_total} turns!\n\n{drop_response} + :coin: 25,000!\n{corrupted_message}",description=textwrap.dedent(f"""
                                    {previous_moves_into_embed}
                                    
                                    """),colour=0x1abc9c)
                                await crown_utilities.bless(25000, str(ctx.author.id))
                                ofambank = await crown_utilities.blessfamily(fam_amount, ofam)
                                oteambank = await crown_utilities.blessteam(bank_amount, oteam)
                                petlogger = await summonlevel(opet_name, ouser)
                                u = await main.bot.fetch_user(ouser.id)
                                cardlogger = await crown_utilities.cardlevel(u, o_card, ouser.id, "Dungeon", selected_universe)

                                if crestsearch:
                                    await crown_utilities.blessguild(25000, oguild['GNAME'])
                                    teambank = await crown_utilities.blessteam(5000, oteam)
                                    await movecrest(selected_universe, oguild['GNAME'])
                                    embedVar.add_field(name=f"**{selected_universe} Crest Claimed**!",
                                                    value=f":flags:**{oguild['GNAME']}** earned the {selected_universe} **Crest**")
                                embedVar.set_author(name=f"{t_card} lost",
                                                    icon_url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620236432/PCG%20LOGOS%20AND%20RESOURCES/PCGBot_1.png")
                                if int(gameClock[0]) == 0 and int(gameClock[1]) == 0:
                                    embedVar.set_footer(text=f"Battle Time: {gameClock[2]} Seconds.")
                                elif int(gameClock[0]) == 0:
                                    embedVar.set_footer(text=f"Battle Time: {gameClock[1]} Minutes and {gameClock[2]} Seconds.")
                                else:
                                    embedVar.set_footer(
                                        text=f"Battle Time: {gameClock[0]} Hours {gameClock[1]} Minutes and {gameClock[2]} Seconds.")
                                # await ctx.send(embed=embedVar)
                                await battle_msg.delete(delay=2)
                                await asyncio.sleep(2)
                                battle_msg = await private_channel.send(embed=embedVar)

                                if t_card not in sowner['BOSS_WINS']:
                                    if difficulty == "HARD":
                                        await crown_utilities.bless(5000000, str(ctx.author.id))
                                    else:
                                        await crown_utilities.bless(15000000, str(ctx.author.id))
                                    if mode == "CBoss":
                                        if difficulty == "HARD":
                                            await crown_utilities.bless(5000000, str(user2.id))
                                        else:
                                            await crown_utilities.bless(15000000, str(user2.id))

                                    query = {'DISNAME': sowner['DISNAME']}
                                    new_query = {'$addToSet': {'BOSS_WINS': t_card}}
                                    resp = db.updateUserNoFilter(query, new_query)

                                # await discord.TextChannel.delete(private_channel, reason=None)
                                continued = False
                            
                            if mode == "ABYSS":
                                if currentopponent != (total_legends):
                                    embedVar = discord.Embed(title=f"VICTORY\nThe game lasted {turn_total} rounds.",description=textwrap.dedent(f"""
                                    {previous_moves_into_embed}
                                    
                                    """),colour=0x1abc9c)

                                    embedVar.set_author(name=f"{t_card} lost!")
                                    

                                    await battle_msg.delete(delay=2)
                                    await asyncio.sleep(2)
                                    battle_msg = await private_channel.send(embed=embedVar)
                                    currentopponent = currentopponent + 1
                                    continued = True
                                if currentopponent == (total_legends):
                                    uid = o_DID
                                    ouser = await self.bot.fetch_user(uid)
                                    floor = universe['FLOOR']
                                    new_level = floor + 1
                                    response = db.updateUserNoFilter({'DID': str(ctx.author.id)}, {'$set': {'LEVEL': new_level}})
                                    abyss_message = await abyss_level_up_message(str(ctx.author.id), floor, t_card, t_title, tarm_name)
                                    cardlogger = await crown_utilities.cardlevel(ouser, o_card, ctx.author.id, "Purchase", "n/a")
                                    abyss_drop_message = "\n".join(abyss_message['DROP_MESSAGE'])
                                    bless_amount = 100000 + (10000 * floor)
                                    await crown_utilities.bless(bless_amount, ctx.author.id)
                                    embedVar = discord.Embed(title=f"🌑 Floor **{floor}** Cleared\nThe game lasted {turn_total} rounds.",description=textwrap.dedent(f"""
                                    Counquer the **Abyss** to unlock **Abyssal Rewards** and **New Game Modes.**
                                    
                                    🎊**Abyss Floor Unlocks**
                                    **3** - *PvP and Guilds*
                                    **10** - *Trading*
                                    **15** - *Associations and Raids*
                                    **20** - *Gifting*
                                    **25** - *Explore Mode*
                                    **30** - *Marriage*
                                    **40** - *Dungeons*
                                    **60** - *Bosses*
                                    **100** - *Boss Soul Exchange*
                                    """),colour=0xe91e63)

                                    embedVar.set_author(name=f"{t_card} lost!")
                                    embedVar.set_footer(text=f"Traverse the **Abyss** in /solo to unlock new game modes and features!")
                                    floor_list = [0,2,3,6,7,8,9,10,20,25,40,60,100]
                                    if floor in floor_list:
                                        embedVar.add_field(
                                        name=f"Abyssal Unlock",
                                        value=f"{abyss_message['MESSAGE']}")
                                    embedVar.add_field(
                                    name=f"Abyssal Rewards",
                                    value=f"{abyss_drop_message}")
 
                                    battle_msg = await private_channel.send(embed=embedVar)

                                    continued = False

                            if mode == "SCENARIO":
                                if currentopponent != (total_legends):
                                    uid = o_DID
                                    ouser = await self.bot.fetch_user(uid)
                                    cardlogger = await crown_utilities.cardlevel(ouser, o_card, ouser.id, "Tales", universe['UNIVERSE'])

                                    embedVar = discord.Embed(title=f"VICTORY\nThe game lasted {turn_total} rounds.",description=textwrap.dedent(f"""
                                    {previous_moves_into_embed}
                                    
                                    """),colour=0x1abc9c)

                                    embedVar.set_author(name=f"{t_card} lost!")
                                    

                                    await battle_msg.delete(delay=2)
                                    await asyncio.sleep(2)
                                    battle_msg = await private_channel.send(embed=embedVar)
                                    currentopponent = currentopponent + 1
                                    continued = True
                                if currentopponent == (total_legends):
                                    uid = o_DID
                                    ouser = await self.bot.fetch_user(uid)
                                    response = await scenario_drop(self, ctx, universe, difficulty)
                                    bless_amount = 50000
                                    await crown_utilities.bless(bless_amount, ctx.author.id)
                                    embedVar = discord.Embed(title=f"Scenario Battle Cleared!\nThe game lasted {turn_total} rounds.",description=textwrap.dedent(f"""
                                    Good luck on your next adventure!
                                    """),colour=0xe91e63)

                                    embedVar.set_author(name=f"{t_card} lost!")
                                    embedVar.add_field(
                                    name=f"Scenario Reward",
                                    value=f"{response}")
 
                                    battle_msg = await private_channel.send(embed=embedVar)

                                    continued = False

                            elif mode not in B_modes and mode != "ABYSS":
                                uid = o_DID
                                ouser = await self.bot.fetch_user(uid)
                                wintime = time.asctime()
                                h_playtime = int(wintime[11:13])
                                m_playtime = int(wintime[14:16])
                                s_playtime = int(wintime[17:19])
                                gameClock = getTime(int(h_gametime), int(m_gametime), int(s_gametime), h_playtime, m_playtime,
                                                    s_playtime)

                                bank_amount = 5000
                                fam_amount = 2000
                                if mode in D_modes:
                                    bank_amount = 20000
                                    fam_amount = 5000

                                if difficulty == "HARD":
                                    bank_amount = 100000
                                    fam_amount = 50000
                                    

                                if difficulty == "EASY":
                                    bank_amount = 500
                                    fam_amount = 100

                                if mode in D_modes:
                                    teambank = await crown_utilities.blessteam(bank_amount, oteam)
                                else:
                                    teambank = await crown_utilities.blessteam(bank_amount, oteam)
                                if o_user['RIFT'] == 1:
                                    response = db.updateUserNoFilter({'DISNAME': str(o_user['DISNAME'])}, {'$set': {'RIFT': 0}})

                                if mode in D_modes:
                                    drop_response = await dungeondrops(self, ouser, selected_universe, currentopponent)
                                elif mode in U_modes:
                                    drop_response = await drops(self, ouser, selected_universe, currentopponent)
                                if mode in D_modes:
                                    ofambank = await crown_utilities.blessfamily(fam_amount, ofam)
                                else:
                                    ofambank = await crown_utilities.blessfamily(fam_amount, ofam)
                                match = await savematch(str(ouser), str(o_card), str(o_card_path), str(otitle['TITLE']),
                                                        str(oarm['ARM']), str(selected_universe), tale_or_dungeon_only,
                                                        o['EXCLUSIVE'])
                                ran_element = crown_utilities.select_random_element(difficulty, mode)
                                essence = crown_utilities.inc_essence(ouser.id, ran_element["ELEMENT"], ran_element["ESSENCE"])

                                if difficulty != "EASY":
                                    questlogger = await quest(ouser, t_card, tale_or_dungeon_only)
                                    destinylogger = await destiny(ouser, t_card, tale_or_dungeon_only)
                                    petlogger = await summonlevel(opet_name, ouser)
                                    cardlogger = await crown_utilities.cardlevel(ouser, o_card, ouser.id, tale_or_dungeon_only, selected_universe)
                                    # if questlogger:
                                    #     await private_channel.send(questlogger)
                                    # if destinylogger:
                                    #     await private_channel.send(destinylogger)
                                
                                if _battle._is_co_op and mode not in ai_co_op_modes:
                                    teammates = False
                                    fam_members =False
                                    stat_bonus = 0
                                    hlt_bonus = 0 
                                    if o_user['TEAM'] == c_user['TEAM'] and o_user['TEAM'] != 'PCG':
                                        teammates=True
                                        stat_bonus=50
                                    if o_user['FAMILY'] == c_user['FAMILY'] and o_user['FAMILY'] != 'PCG':
                                        fam_members=True
                                        hlt_bonus=100
                                    
                                    if teammates==True:
                                        bonus_message = f":checkered_flag:**{o_user['TEAM']}:** 🗡️**+{stat_bonus}** 🛡️**+{stat_bonus}**"
                                        if fam_members==True:
                                            bonus_message = f":family_mwgb:**{o_user['FAMILY']}:** ❤️**+{hlt_bonus}**\n:checkered_flag:**{o_user['TEAM']}:**🗡️**+{stat_bonus}** 🛡️**+{stat_bonus}**"
                                    elif fam_members==True:
                                            bonus_message = f":family_mwgb:**{o_user['FAMILY']}:** ❤️**+{hlt_bonus}**"
                                    else:
                                        bonus_message = f"Join a Guild or Create a Family for Coop Bonuses!"
                                    cuid = c_DID
                                    talisman_response = crown_utilities.inc_talisman(str(cuid), c_talisman)
                                    cuser = await self.bot.fetch_user(cuid)
                                    if mode in D_modes:
                                        teambank = await crown_utilities.blessteam(bank_amount, oteam)
                                        cteambank = await crown_utilities.blessteam(bank_amount, oteam)
                                    else:
                                        teambank = await crown_utilities.blessteam(bank_amount, oteam)
                                        cteambank = await crown_utilities.blessteam(bank_amount, oteam)
                                    if mode in D_modes:
                                        cdrop_response = await dungeondrops(self,user2, selected_universe, currentopponent)
                                    elif mode in U_modes:
                                        cdrop_response = await drops(self,user2, selected_universe, currentopponent)
                                    if mode in D_modes:
                                        cfambank = await crown_utilities.blessfamily(fam_amount, cfam)
                                        ofambank = await crown_utilities.blessfamily(fam_amount, ofam)
                                    else:
                                        cfambank = await crown_utilities.blessfamily(fam_amount, cfam)
                                        ofambank = await crown_utilities.blessfamily(fam_amount, ofam)
                                    # cmatch = await savematch(str(user2), str(c_card), str(c_card_path), str(ctitle['TITLE']),
                                    #                         str(carm['ARM']), str(selected_universe), tale_or_dungeon_only, c['EXCLUSIVE'])
                                    cfambank = await crown_utilities.blessfamily(fam_amount, cfam)
                                    cteambank = await crown_utilities.blessteam(bank_amount, cteam)
                                    cpetlogger = await summonlevel(cpet_name, user2)
                                    ucc = await main.bot.fetch_user(user2.id)
                                    ccardlogger = await crown_utilities.cardlevel(ucc, c_card, user2.id, tale_or_dungeon_only, selected_universe)
                                    await crown_utilities.bless(5000, str(user2.id))
                                    cessence = crown_utilities.inc_essence(cuser.id, ran_element["ELEMENT"], ran_element["ESSENCE"])
                                if currentopponent != (total_legends):
                                    if mode not in co_op_modes:
                                        embedVar = discord.Embed(title=f"🎊 VICTORY\nThe game lasted {turn_total} rounds.\n\n{drop_response}\nEarned {essence} {ran_element['ESSENCE']} Essence\n{corrupted_message}",description=textwrap.dedent(f"""
                                        {previous_moves_into_embed}
                                        
                                        """),colour=0x1abc9c)
                                        if difficulty != "EASY":
                                            if questlogger:
                                                embedVar.add_field(name="**Quest Progress**",
                                                    value=f"{questlogger}")
                                            if destinylogger:
                                                embedVar.add_field(name="**Destiny Progress**",
                                                    value=f"{destinylogger}")
                                    elif _battle._is_co_op and mode not in ai_co_op_modes:
                                        embedVar = discord.Embed(title=f"👥 CO-OP VICTORY\nThe game lasted {turn_total} rounds.\n\n👤**{o_user['NAME']}:** {drop_response}\nEarned {essence} {ran_element['ESSENCE']} Essence\n👥**{c_user['NAME']}:** {cdrop_response}\nEarned {cessence} {ran_element['ESSENCE']} Essence",description=textwrap.dedent(f"""
                                        {previous_moves_into_embed}
                                        
                                        """),colour=0x1abc9c)
                                        embedVar.add_field(name="**Co-Op Bonus**",
                                                value=f"{bonus_message}")
                                        if questlogger:
                                            embedVar.add_field(name="**Quest Progress**",
                                                value=f"{questlogger}")
                                        if destinylogger:
                                            embedVar.add_field(name="**Destiny Progress**",
                                                value=f"{destinylogger}")
                                    elif mode in ai_co_op_modes:
                                        embedVar = discord.Embed(title=f"🎊 DUO VICTORY\nThe game lasted {turn_total} rounds.\n\n{drop_response}\n{corrupted_message}",description=textwrap.dedent(f"""
                                        {previous_moves_into_embed}
                                        
                                        """),colour=0x1abc9c)
                                    if mode in D_modes:
                                        if crestsearch:
                                            await crown_utilities.blessguild(10000, oguild['GNAME'])
                                            embedVar.add_field(name=f"**{selected_universe} Crest Search!**",
                                                            value=f":flags:**{oguild['GNAME']}** earned **100,000** :coin:")
                                    embedVar.set_author(name=f"{t_card} lost!")
                                    
                                    await battle_msg.delete(delay=2)
                                    await asyncio.sleep(2)
                                    battle_msg = await private_channel.send(embed=embedVar)

                                    currentopponent = currentopponent + 1
                                    continued = True

                                if currentopponent == (total_legends):
                                    if mode in D_modes:
                                        embedVar = discord.Embed(title=f":fire: DUNGEON CONQUERED",
                                                                description=f"**{selected_universe} Dungeon** has been conquered\n\n{drop_response}\n{corrupted_message}",
                                                                colour=0xe91e63)
                                        embedVar.set_author(name=f"{selected_universe} Boss has been unlocked!")
                                        if crestsearch:
                                            await crown_utilities.blessguild(100000, oguild['GNAME'])
                                            teambank = await crown_utilities.blessteam(100000, oteam)
                                            await movecrest(selected_universe, oguild['GNAME'])
                                            embedVar.add_field(name=f"**{selected_universe}** CREST CLAIMED!",
                                                            value=f"**{oguild['GNAME']}** earned the {selected_universe} **Crest**")
                                        if questlogger:
                                            embedVar.add_field(name="**Quest Progress**",
                                                value=f"{questlogger}")
                                        if destinylogger:
                                            embedVar.add_field(name="**Destiny Progress**",
                                                value=f"{destinylogger}")
                                        embedVar.set_footer(text="Visit the /shop for a huge discount!")
                                        if difficulty != "EASY":
                                            upload_query = {'DID': str(ctx.author.id)}
                                            new_upload_query = {'$addToSet': {'DUNGEONS': selected_universe}}
                                            r = db.updateUserNoFilter(upload_query, new_upload_query)
                                        if selected_universe in o_user['DUNGEONS']:
                                            await crown_utilities.bless(300000, ctx.author.id)
                                            teambank = await crown_utilities.blessteam(bank_amount, oteam)
                                            # await crown_utilities.bless(125, user2)
                                            # await ctx.send(embed=embedVar)
                                            await battle_msg.delete(delay=2)
                                            await asyncio.sleep(2)
                                            embedVar.add_field(name="Minor Reward",
                                                        value=f"You were awarded :coin: 300,000 for completing the {selected_universe} Dungeon again!")
                                            #battle_msg = await private_channel.send(embed=embedVar)
                                        else:
                                            await crown_utilities.bless(6000000, ctx.author.id)
                                            teambank = await crown_utilities.blessteam(1500000, oteam)
                                            # await ctx.send(embed=embedVar)
                                            await battle_msg.delete(delay=2)
                                            await asyncio.sleep(2)
                                            embedVar.add_field(name="Dungeon Reward",
                                                        value=f"You were awarded :coin: 6,000,000 for completing the {selected_universe} Dungeon!")
                                            #battle_msg = await private_channel.send(embed=embedVar)
                                        if _battle._is_co_op and mode not in ai_co_op_modes:
                                            cuid = c_DID
                                            cuser = await self.bot.fetch_user(cuid)
                                            await crown_utilities.bless(500000, user2.id)
                                            teambank = await crown_utilities.blessteam(200000, cteam)
                                            # await crown_utilities.bless(125, user2)
                                            # await ctx.send(embed=embedVar)
                                            await asyncio.sleep(2)
                                            
                                            await ctx.send(
                                                f"{user2.mention} You were awarded :coin: 500,000 for  assisting in the {selected_universe} Dungeon!")
                                        battle_msg = await private_channel.send(embed=embedVar)
                                        continued = False
                                        # await discord.TextChannel.delete(private_channel, reason=None)
                                    elif mode in U_modes:
                                        embedVar = discord.Embed(title=f"🎊 UNIVERSE CONQUERED",
                                                                description=f"**{selected_universe}** has been conquered\n\n{drop_response}\n{corrupted_message}",
                                                                colour=0xe91e63)
                                        if questlogger:
                                            embedVar.add_field(name="**Quest Progress**",
                                                value=f"{questlogger}")
                                        if destinylogger:
                                            embedVar.add_field(name="**Destiny Progress**",
                                                value=f"{destinylogger}")
                                        embedVar.set_footer(text=f"You can now /craft {selected_universe} cards")
                                        if difficulty != "EASY":
                                            embedVar.set_author(name=f"{selected_universe} Dungeon has been unlocked!")
                                            upload_query = {'DID': str(ctx.author.id)}
                                            new_upload_query = {'$addToSet': {'CROWN_TALES': selected_universe}}
                                            r = db.updateUserNoFilter(upload_query, new_upload_query)
                                        if selected_universe in o_user['CROWN_TALES']:
                                            await crown_utilities.bless(100000, ctx.author.id)
                                            teambank = await crown_utilities.blessteam(25000, oteam)
                                            # await ctx.send(embed=embedVar)
                                            await battle_msg.delete(delay=2)
                                            await asyncio.sleep(2)
                                            embedVar.add_field(name="Minor Reward",
                                                        value=f"You were awarded :coin: 100,000 for completing the {selected_universe} Tale again!")
                                        else:
                                            await crown_utilities.bless(2000000, ctx.author.id)
                                            teambank = await crown_utilities.blessteam(500000, oteam)
                                            # await ctx.send(embed=embedVar)
                                            await battle_msg.delete(delay=2)
                                            await asyncio.sleep(2)
                                            
                                            embedVar.add_field(name="Conquerors Reward",
                                                        value=f"You were awarded :coin: 2,000,000 for completing the {selected_universe} Tale!")
                                            #battle_msg = await private_channel.send(embed=embedVar)
                                        if _battle._is_co_op and mode not in ai_co_op_modes:
                                            cuid = c_DID
                                            cuser = await self.bot.fetch_user(cuid)
                                            await crown_utilities.bless(250000, user2.id)
                                            teambank = await crown_utilities.blessteam(80000, cteam)
                                            # await crown_utilities.bless(125, user2)
                                            # await ctx.send(embed=embedVar)
                                            await asyncio.sleep(2)
                                            embedVar.add_field(name="Companion Reward",
                                                        value=f"{user2.mention} You were awarded :coin: 250,000 for assisting in the {selected_universe} Tale!")
                                            
                                        battle_msg = await private_channel.send(embed=embedVar)
                                        continued = False

            except asyncio.TimeoutError:
                await battle_msg.edit(components=[])
                if not _battle._is_abyss and not _battle._is_scenario and not _battle._is_explore and not _battle._is_pvp_match and not _battle._is_tutorial:
                    await save_spot(self, ctx, _battle._selected_universe, _battle.mode, _battle._currentopponent)
                
                await ctx.send(f"{ctx.author.mention} {_battle.error_end_match_message()}")
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
                    'PLAYER': str(ctx.author),
                    'type': type(ex).__name__,
                    'message': str(ex),
                    'trace': trace
                }))
                # if mode not in ai_co_op_modes:
                #     await battle_ping_message.delete()
                await battle_msg.delete()
                guild = self.bot.get_guild(main.guild_id)
                channel = guild.get_channel(main.guild_channel)
                await channel.send(f"'PLAYER': **{str(ctx.author)}**, 'GUILD': **{str(ctx.author.guild)}**, TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")
                return

    except asyncio.TimeoutError:
        await battle_msg.edit(components=[])
        if not _battle._is_abyss and not _battle._is_scenario and not _battle._is_explore and not _battle._is_pvp_match and not _battle._is_tutorial:
            await save_spot(self, ctx, _battle._selected_universe, _battle.mode, _battle._currentopponent)
        
        await ctx.send(f"{ctx.author.mention} {_battle.error_end_match_message()}")
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
            'PLAYER': str(ctx.author),
            'type': type(ex).__name__,
            'message': str(ex),
            'trace': trace
        }))
        guild = self.bot.get_guild(main.guild_id)
        channel = guild.get_channel(main.guild_channel)
        await channel.send(f"'PLAYER': **{str(ctx.author)}**, TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")
        return


async def save_spot(self, ctx, universe, mode, currentopponent):
    try:
        user = {"DID": str(ctx.author.id)}
        query = {"$addToSet": {"SAVE_SPOT": {"UNIVERSE": str(universe['TITLE']), "MODE": str(mode), "CURRENTOPPONENT": currentopponent}}}
        response = db.updateUserNoFilter(user, query)
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
            'PLAYER': str(ctx.author),
            'type': type(ex).__name__,
            'message': str(ex),
            'trace': trace
        }))
        guild = self.bot.get_guild(main.guild_id)
        channel = guild.get_channel(main.guild_channel)
        await channel.send(f"'PLAYER': **{str(ctx.author)}**, 'GUILD': **{str(ctx.author.guild)}**, TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")
        return

        

def update_arm_durability(self, vault, arm, arm_universe, arm_price, card):
    try:
        player_info = db.queryUser({'DID': str(vault['DID'])})
        if player_info['DIFFICULTY'] == "EASY":
            return
        pokemon_universes = ['Kanto Region', 'Johto Region','Hoenn Region','Sinnon Region','Kalos Region','Alola Region','Galar Region']
        if card['UNIVERSE'] == 'Crown Rift Slayers':
            arm_universe = card['UNIVERSE']
            
        if arm_universe in pokemon_universes:
            arm_universe = card['UNIVERSE']

        decrease_value = -1
        break_value = 1
        if arm_universe != card['UNIVERSE'] and arm_universe != "Unbound":
            decrease_value = -5
            break_value = 5

        for a in vault['ARMS']:
            if a['ARM'] == str(arm['ARM']):
                current_durability = a['DUR']
                if current_durability <= 0:
                    selected_arm = arm['ARM']
                    arm_name = arm['ARM']
                    selected_universe = arm_universe
                    dismantle_amount = 5000
                    current_gems = []
                    for gems in vault['GEMS']:
                        current_gems.append(gems['UNIVERSE'])

                    if selected_universe in current_gems:
                        query = {'DID': str(vault['DID'])}
                        update_query = {'$inc': {'GEMS.$[type].' + "GEMS": dismantle_amount}}
                        filter_query = [{'type.' + "UNIVERSE": selected_universe}]
                        response = db.updateVault(query, update_query, filter_query)
                    else:
                        response = db.updateVaultNoFilter({'DID': str(vault['DID'])},{'$addToSet':{'GEMS': {'UNIVERSE': selected_universe, 'GEMS': dismantle_amount, 'UNIVERSE_HEART': False, 'UNIVERSE_SOUL': False}}})


                    query = {'DID': str(vault['DID'])}
                    update_query = {'$pull': {'ARMS': {'ARM': str(arm['ARM'])}}}
                    resp = db.updateVaultNoFilter(query, update_query)

                    user_query = {'DID': str(vault['DID'])}
                    user_update_query = {'$set': {'ARM': 'Stock'}}
                    user_resp = db.updateUserNoFilter(user_query, user_update_query)
                    return {"MESSAGE": f"**{arm['ARM']}** has been dismantled after losing all ⚒️ durability, you earn 💎 {str(dismantle_amount)}. Your arm will be **Stock** after your next match."}
                else:                   
                    query = {'DID': str(vault['DID'])}
                    update_query = {'$inc': {'ARMS.$[type].' + 'DUR': decrease_value}}
                    filter_query = [{'type.' + "ARM": str(arm['ARM'])}]
                    resp = db.updateVault(query, update_query, filter_query)
                    if current_durability >= 15:
                        return {"MESSAGE": False}
                    else:
                        return {"MESSAGE": f"**{arm['ARM']}** will lose all ⚒️ durability soon! Use **/blacksmith** to repair!"}
        return {"MESSAGE": False}
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
        


def update_save_spot(self, ctx, saved_spots, selected_universe, modes):
    try:
        currentopponent = 0
        if saved_spots:
            for save in saved_spots:
                if save['UNIVERSE'] == selected_universe and save['MODE'] in modes:
                    currentopponent = save['CURRENTOPPONENT']
                    query = {'DID': str(ctx.author.id)}
                    update_query = {'$pull': {'SAVE_SPOT': {"UNIVERSE": selected_universe}}}
                    resp = db.updateUserNoFilter(query, update_query)
        return currentopponent
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
            'PLAYER': str(ctx.author),
            'type': type(ex).__name__,
            'message': str(ex),
            'trace': trace
        }))
        return



def health_and_stamina_bars(health, stamina, max_health, max_stamina, resolved):
    health_response = ""
    stamina_response = ""

    if health >= max_health:
        health_response = f"❤️❤️❤️❤️❤️"
    if health >= (max_health * .80) and health < max_health:
        health_response = f"❤️❤️❤️❤️💔"
    if health >= (max_health * .60) and health < (max_health * .80):
        health_response = f"❤️❤️❤️💔💔"
    if health >= (max_health * .40) and health < (max_health * .60):
        health_response = f"❤️❤️💔💔💔"
    if health >= (max_health * .20) and health < (max_health * .40):
        health_response = f"❤️💔💔💔💔"
    if health >= 0 and health <= (max_health * .20):
        health_response = f"💔💔💔💔💔"
    if resolved:
        if stamina >= max_stamina:
            stamina_response = f"⚡⚡⚡⚡⚡"
        if stamina >= (max_stamina * .80) and stamina < max_stamina:
            stamina_response = f"⚡⚡⚡⚡💫"
        if stamina >= (max_stamina * .60) and stamina < (max_stamina * .80):
            stamina_response = f"⚡⚡⚡💫💫"
        if stamina >= (max_stamina * .40) and stamina < (max_stamina * .60):
            stamina_response = f"⚡⚡💫💫💫"
        if stamina >= (max_stamina * .10) and stamina < (max_stamina * .40):
            stamina_response = f"⚡💫💫💫💫"
        if stamina >= 0 and stamina <= (max_stamina * .10):
            stamina_response = f"💫💫💫💫💫"
    else:
        if stamina >= max_stamina:
            stamina_response = f"🌀🌀🌀🌀🌀"
        if stamina >= (max_stamina * .80) and stamina < max_stamina:
            stamina_response = f"🌀🌀🌀🌀⚫"
        if stamina >= (max_stamina * .60) and stamina < (max_stamina * .80):
            stamina_response = f"🌀🌀🌀⚫⚫"
        if stamina >= (max_stamina * .40) and stamina < (max_stamina * .60):
            stamina_response = f"🌀🌀⚫⚫⚫"
        if stamina >= (max_stamina * .10) and stamina < (max_stamina * .40):
            stamina_response = f"🌀⚫⚫⚫⚫"
        if stamina >= 0 and stamina <= (max_stamina * .10):
            stamina_response = f"⚫⚫⚫⚫⚫"

    return {"HEALTH": health_response, "STAMINA": stamina_response}


def getTime(hgame, mgame, sgame, hnow, mnow, snow):
    hoursPassed = hnow - hgame
    minutesPassed = mnow - mgame
    secondsPassed = snow - sgame
    if hoursPassed > 0:
        minutesPassed = mnow
        if minutesPassed > 0:
            secondsPassed = snow
        else:
            secondsPassed = snow - sgame
    else:
        minutesPassed = mnow - mgame
        if minutesPassed > 0:
            secondsPassed = snow
        else:
            secondsPassed = snow - sgame
    gameTime = str(hoursPassed) + str(minutesPassed) + str(secondsPassed)
    return gameTime


async def blessteam(amount, team):
    blessAmount = amount
    posBlessAmount = 0 + abs(int(blessAmount))
    query = {'TEAM_NAME': str(team.lower())}
    team_data = db.queryTeam(query)
    if team_data:
        guild_mult = 1.0
        if team_data['GUILD'] != 'PCG':
            guild_query = {'GNAME': str(team_data['GUILD'])}
            guild_info = db.queryGuildAlt(guild_query)
            guild_hall = guild_info['HALL']
            hall_query = {'HALL': str(guild_hall)}
            hall_info = db.queryHall(hall_query)
            guild_mult = hall_info['SPLIT']
            blessAmount = amount * guild_mult
            posBlessAmount = 0 + abs(int(blessAmount))
        total_members = team_data['MEMBERS']
        headcount_bonus = 0
        bonus_percentage = 0.0
        for m in total_members:
            headcount_bonus= headcount_bonus + 1
        bonus_percentage= (headcount_bonus/25)
        if bonus_percentage >= 1:
            bonus_percentage = 1.5
        posBlessAmount = int((posBlessAmount + (bonus_percentage * posBlessAmount)))
        update_query = {"$inc": {'BANK': posBlessAmount}}
        db.updateTeam(query, update_query)



async def teamwin(team):
    query = {'TEAM_NAME': str(team.lower())}
    team_data = db.queryTeam(query)
    if team_data:
        update_query = {"$inc": {'SCRIM_WINS': 1}}
        db.updateTeam(query, update_query)
    else:
        print("Cannot find Guild")


async def teamloss(team):
    query = {'TEAM_NAME': str(team.lower())}
    team_data = db.queryTeam(query)
    if team_data:
        update_query = {"$inc": {'SCRIM_LOSSES': 1}}
        db.updateTeam(query, update_query)
    else:
        print("Cannot find Guild")


async def movecrest(universe, guild):
    guild_name = guild
    universe_name = universe
    guild_query = {'GNAME': guild_name}
    guild_info = db.queryGuildAlt(guild_query)
    if guild_info:
        alt_query = {'FDID': guild_info['FDID']}
        crest_list = guild_info['CREST']
        pull_query = {'$pull': {'CREST': universe_name}}
        pull = db.updateManyGuild(pull_query)
        update_query = {'$push': {'CREST': universe_name}}
        update = db.updateGuild(alt_query, update_query)
        universe_guild = db.updateUniverse({'TITLE': universe_name}, {'$set': {'GUILD': guild_name}})
    else:
        print("Association not found: Crest")


async def scenario_drop(self, ctx, scenario, difficulty):
    try:
        vault_query = {'DID': str(ctx.author.id)}
        vault = db.queryVault(vault_query)
        scenario_level = scenario["ENEMY_LEVEL"]
        scenario_gold = crown_utilities.scenario_gold_drop(scenario_level)
        # player_info = db.queryUser({'DID': str(vault['DID'])})
        
        owned_destinies = []
        for destiny in vault['DESTINY']:
            owned_destinies.append(destiny['NAME'])


        owned_arms = []
        for arm in vault['ARMS']:
            owned_arms.append(arm['ARM'])

        easy = "EASY_DROPS"
        normal = "NORMAL_DROPS"
        hard = "HARD_DROPS"
        rewards = []
        rewarded = ""
        mode = ""

        if difficulty == "EASY":
            rewards = scenario[easy]
            mode = "TALES"
            scenario_gold = round(scenario_gold / 3)
        if difficulty == "NORMAL":
            rewards = scenario[normal]
            mode = "TALES"
        if difficulty == "HARD":
            rewards = scenario[hard]
            mode = "DUNGEON"
            scenario_gold = round(scenario_gold * 3)
        if len(rewards) > 1:
            num_of_potential_rewards = len(rewards)
            selection = round(random.randint(0, num_of_potential_rewards))
            rewarded = rewards[selection]
        else:
            rewarded = rewards[0]
        
        await crown_utilities.bless(scenario_gold, ctx.author.id)
        # Add Card Check
        arm = db.queryArm({"ARM": rewarded})
        if arm:
            arm_name = arm['ARM']
            element_emoji = crown_utilities.set_emoji(arm['ELEMENT'])
            arm_passive = arm['ABILITIES'][0]
            arm_passive_type = list(arm_passive.keys())[0]
            arm_passive_value = list(arm_passive.values())[0]
            reward = f"{element_emoji} {arm_passive_type.title()} **{arm_name}** Attack: **{arm_passive_value}** dmg"

            if len(vault['ARMS']) >= 25:
                return f"You're maxed out on Arms! You earned :coin:**{'{:,}'.format(scenario_gold)}** instead!"
            elif rewarded in owned_arms:
                return f"You already own {reward}! You earn :coin: **{'{:,}'.format(scenario_gold)}**."
            else:
                response = db.updateVaultNoFilter(vault_query, {'$addToSet': {'ARMS': {'ARM': rewarded, 'DUR': 100}}})
                return f"You earned _Arm:_ {reward} with ⚒️**{str(100)} Durability** and :coin: **{'{:,}'.format(scenario_gold)}**!"
        else:
            card = db.queryCard({"NAME": rewarded})
            u = await main.bot.fetch_user(str(ctx.author.id))
            response = await crown_utilities.store_drop_card(u, str(ctx.author.id), card["NAME"], card["UNIVERSE"], vault, owned_destinies, 3000, 1000, mode, False, 0, "cards")
            response = f"{response}\nYou earned :coin: **{'{:,}'.format(scenario_gold)}**!"
            if not response:
                bless_amount = (5000 + (2500 * matchcount)) * (1 + rebirth)
                await crown_utilities.bless(bless_amount, str(ctx.author.id))
                return f"You earned :coin: **{'{:,}'.format(scenario_gold)}**!"
            return response

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

    

    


async def drops(self,player, universe, matchcount):
    all_available_drop_cards = db.queryDropCards(universe)
    all_available_drop_titles = db.queryDropTitles(universe)
    all_available_drop_arms = db.queryDropArms(universe)
    all_available_drop_pets = db.queryDropPets(universe)
    vault_query = {'DID': str(player.id)}
    vault = db.queryVault(vault_query)
    player_info = db.queryUser({'DID': str(vault['DID'])})

    difficulty = player_info['DIFFICULTY']

    if difficulty == "EASY":
        bless_amount = 100
        await crown_utilities.bless(bless_amount, player.id)
        return f"You earned :coin: **{bless_amount}**!"

    owned_arms = []
    for arm in vault['ARMS']:
        owned_arms.append(arm['ARM'])
        
    owned_titles = []
    owned_titles = vault['TITLES']

    user_query = {'DID': str(player.id)}
    user = db.queryUser(user_query)
    rebirth = user['REBIRTH']
    owned_destinies = []
    for destiny in vault['DESTINY']:
        owned_destinies.append(destiny['NAME'])

    cards = []
    titles = []
    arms = []
    pets = []

    # if matchcount <= 2:
    #     bless_amount = (500 + (1000 * matchcount)) * (1 + rebirth)
    #     if difficulty == "HARD":
    #         bless_amount = (5000 + (2500 * matchcount)) * (1 + rebirth)
    #     await crown_utilities.bless(bless_amount, player.id)
    #     return f"You earned :coin: **{bless_amount}**!"



    if all_available_drop_cards:
        for card in all_available_drop_cards:
            cards.append(card['NAME'])

    if all_available_drop_titles:
        for title in all_available_drop_titles:
            titles.append(title['TITLE'])

    if all_available_drop_arms:
        for arm in all_available_drop_arms:
            arms.append(arm['ARM'])
        
    if all_available_drop_pets:
        for pet in all_available_drop_pets:
            pets.append(pet['PET'])
         
    
    if len(cards)==0:
        rand_card = 0
    else:
        c = len(cards) - 1
        rand_card = random.randint(0, c)

    if len(titles)==0:
        rand_title= 0
    else:
        t = len(titles) - 1
        rand_title = random.randint(0, t)

    if len(arms)==0:
        rand_arm = 0
    else:
        a = len(arms) - 1
        rand_arm = random.randint(0, a)

    
    if len(pets)==0:
        rand_pet = 0
    else:
        p = len(pets) - 1
        rand_pet = random.randint(0, p)

    gold_drop = 125  # 125
    rift_rate = 150  # 150
    rematch_rate = 175 #175
    title_drop = 190  # 190
    arm_drop = 195  # 195
    pet_drop = 198  # 198
    card_drop = 200  # 200
    drop_rate = random.randint((0 + (rebirth * rebirth) * (1 + rebirth)), 200)
    durability = random.randint(1, 45)
    if difficulty == "HARD":
        mode = "Purchase"
        gold_drop = 30
        rift_rate = 55
        rematch_rate = 70
        title_drop = 75  
        arm_drop = 100  
        pet_drop = 180  
        card_drop = 200 
        drop_rate = random.randint((0 + (rebirth * rebirth) * (1 + rebirth)), 200)
        durability = random.randint(35, 50)
        
    try:
        if drop_rate <= gold_drop:
            bless_amount = (10000 + (1000 * matchcount)) * (1 + rebirth)
            if difficulty == "HARD":
                bless_amount = (30000 + (2500 * matchcount)) * (1 + rebirth)
            await crown_utilities.bless(bless_amount, player.id)
            return f"You earned :coin: **{bless_amount}**!"
        elif drop_rate <= rift_rate and drop_rate > gold_drop:
            response = db.updateUserNoFilter(user_query, {'$set': {'RIFT': 1}})
            bless_amount = (20000 + (1000 * matchcount)) * (1 + rebirth)
            await crown_utilities.bless(bless_amount, player.id)
            return f"A RIFT HAS OPENED! You have earned :coin: **{bless_amount}**!"
        elif drop_rate <= rematch_rate and drop_rate > rift_rate:
            response = db.updateUserNoFilter(user_query, {'$inc': {'RETRIES': 1}})
            bless_amount = (25000 + (1000 * matchcount)) * (1 + rebirth)
            await crown_utilities.bless(bless_amount, player.id)
            return f"🆚  You have earned 1 Rematch and  :coin: **{bless_amount}**!"
        elif drop_rate <= title_drop and drop_rate > rematch_rate:
            if all_available_drop_titles:
                # if len(vault['TITLES']) >= 25:
                #     await crown_utilities.bless(300, player.id)
                #     return f"You're maxed out on Titles! You earned :coin: 300 instead!"
                # if str(titles[rand_title]) in owned_titles:
                #     await crown_utilities.bless(150, player.id)
                #     return f"You already own **{titles[rand_title]}**! You earn :coin: **150**."
                # response = db.updateVaultNoFilter(vault_query, {'$addToSet': {'TITLES': str(titles[rand_title])}})
                # return f"You earned _Title:_ **{titles[rand_title]}**!"
                u = await main.bot.fetch_user(player.id)
                response = await crown_utilities.store_drop_card(u, player.id, titles[rand_title], universe, vault, owned_destinies, 150, 150, "mode", False, 0, "titles")
                return response
            else:
                await crown_utilities.bless(150, player.id)
                return f"You earned :coin: **150**!"
        elif drop_rate <= arm_drop and drop_rate > title_drop:
            if all_available_drop_arms:
                # if len(vault['ARMS']) >= 25:
                #     await crown_utilities.bless(300, player.id)
                #     return f"You're maxed out on Arms! You earned :coin: 300 instead!"
                # if str(arms[rand_arm]) in owned_arms:
                #     await crown_utilities.bless(150, player.id)
                #     return f"You already own **{arms[rand_arm]}**! You earn :coin: **150**."
                # else:
                #     response = db.updateVaultNoFilter(vault_query, {'$addToSet': {'ARMS': {'ARM': str(arms[rand_arm]), 'DUR': durability}}})
                #     return f"You earned _Arm:_ **{arms[rand_arm]}** with ⚒️**{str(durability)}**!"
                u = await main.bot.fetch_user(player.id)
                response = await crown_utilities.store_drop_card(u, player.id, arms[rand_arm], universe, vault, durability, 2000, 2000, "mode", False, 0, "arms")
            else:
                await crown_utilities.bless(150, player.id)
                return f"You earned :coin: **150**!"
        elif drop_rate <= pet_drop and drop_rate > arm_drop:
            if all_available_drop_pets:
                if len(vault['PETS']) >= 25:
                    await crown_utilities.bless(300, player.id)
                    return f"You're maxed out on Summons! You earned :coin: 300 instead!"

                pet_owned = False
                for p in vault['PETS']:
                    if p['NAME'] == pets[rand_pet]:
                        pet_owned = True

                if pet_owned:

                    await crown_utilities.bless(150, player.id)
                    return f"You own _Summon:_ **{pets[rand_pet]}**! Received extra + :coin: 150!"
                else:

                    selected_pet = db.queryPet({'PET': pets[rand_pet]})
                    pet_ability_name = list(selected_pet['ABILITIES'][0].keys())[0]
                    pet_ability_power = list(selected_pet['ABILITIES'][0].values())[0]
                    pet_ability_type = list(selected_pet['ABILITIES'][0].values())[1]

                    response = db.updateVaultNoFilter(vault_query, {'$addToSet': {
                        'PETS': {'NAME': selected_pet['PET'], 'LVL': 0, 'EXP': 0, pet_ability_name: int(pet_ability_power),
                                'TYPE': pet_ability_type, 'BOND': 0, 'BONDEXP': 0, 'PATH': selected_pet['PATH']}}})
                    await crown_utilities.bless(50, player.id)
                    return f"You earned _Summon:_ **{pets[rand_pet]}** + :coin: 50!"
            else:
                await crown_utilities.bless(150, player.id)
                return f"You earned :coin: **150**!"
        elif drop_rate <= card_drop and drop_rate > pet_drop:
            if all_available_drop_cards:
                u = await main.bot.fetch_user(player.id)
                response = await crown_utilities.store_drop_card(u, player.id, cards[rand_card], universe, vault, owned_destinies, 3000, 1000, "mode", False, 0, "cards")
                if not response:
                    bless_amount = (5000 + (2500 * matchcount)) * (1 + rebirth)
                    await crown_utilities.bless(bless_amount, player.id)
                    return f"You earned :coin: **{bless_amount}**!"
                return response
            else:
                await crown_utilities.bless(5000, player.id)
                return f"You earned :coin: **5000**!"
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
            'player': str(player),
            'type': type(ex).__name__,
            'message': str(ex),
            'trace': trace
        }))
        await crown_utilities.bless(5000, player.id)
        guild = self.bot.get_guild(main.guild_id)
        channel = guild.get_channel(main.guild_channel)
        await channel.send(f"'PLAYER': **{str(player)}**, TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")

        return f"You earned :coin: **5000**!"


async def specific_drops(self,player, card, universe):
    vault_query = {'DID': str(player)}
    vault = db.queryVault(vault_query)
    user_query = {'DID': str(player)}
    user = db.queryUser(user_query)

    if user['DIFFICULTY'] == "EASY":
        bless_amount = 100
        await crown_utilities.bless(100, player)
        return f"You earned :coin: **{bless_amount}**!"

    rebirth = user['REBIRTH']
    owned_destinies = []
    for destiny in vault['DESTINY']:
        owned_destinies.append(destiny['NAME'])

    try:
        u = await main.bot.fetch_user(player)
        response = await crown_utilities.store_drop_card(u, player, card, universe, vault, owned_destinies, 3000, 1000, "Purchase", False, 0, "cards")
        return response
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
            'player': str(player),
            'type': type(ex).__name__,
            'message': str(ex),
            'trace': trace
        }))
        await crown_utilities.bless(5000, player.id)
        guild = self.bot.get_guild(main.guild_id)
        channel = guild.get_channel(main.guild_channel)
        await channel.send(f"'PLAYER': **{str(player)}**, TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")

        return f"You earned :coin: **5000**!"


async def dungeondrops(self, player, universe, matchcount):
    all_available_drop_cards = db.queryExclusiveDropCards(universe)
    all_available_drop_titles = db.queryExclusiveDropTitles(universe)
    all_available_drop_arms = db.queryExclusiveDropArms(universe)
    all_available_drop_pets = db.queryExclusiveDropPets(universe)
    vault_query = {'DID': str(player.id)}
    vault = db.queryVault(vault_query)
    owned_arms = []
    for arm in vault['ARMS']:
        owned_arms.append(arm['ARM'])
    owned_titles = vault['TITLES']

    user_query = {'DID': str(player.id)}
    user = db.queryUser(user_query)

    player_info = db.queryUser({'DID': str(vault['DID'])})
    difficulty = player_info['DIFFICULTY']
    if difficulty == "EASY":
        bless_amount = 100
        await crown_utilities.bless(bless_amount, player.id)
        return f"You earned :coin: **{bless_amount}**!"




    rebirth = user['REBIRTH']
    owned_destinies = []
    for destiny in vault['DESTINY']:
        owned_destinies.append(destiny['NAME'])

    cards = []
    titles = []
    arms = []
    pets = []

    if matchcount <= 3:
        bless_amount = (20000 + (2000 * matchcount)) * (1 + rebirth)
        if difficulty == "HARD":
            bless_amount = (50000 + (20000 * matchcount)) * (1 + rebirth)
        await crown_utilities.bless(bless_amount, player.id)
        return f"You earned :coin: **{bless_amount}**!"


    for card in all_available_drop_cards:
        cards.append(card['NAME'])

    for title in all_available_drop_titles:
        titles.append(title['TITLE'])

    for arm in all_available_drop_arms:
        arms.append(arm['ARM'])

    for pet in all_available_drop_pets:
        pets.append(pet['PET'])
    
    if len(cards)==0:
        rand_card = 0
    else:
        c = len(cards) - 1
        rand_card = random.randint(0, c)

    if len(titles)==0:
        rand_title= 0
    else:
        t = len(titles) - 1
        rand_title = random.randint(0, t)

    if len(arms)==0:
        rand_arm = 0
    else:
        a = len(arms) - 1
        rand_arm = random.randint(0, a)

    
    if len(pets)==0:
        rand_pet = 0
    else:
        p = len(pets) - 1
        rand_pet = random.randint(0, p)


    gold_drop = 250  #
    rift_rate = 300  #
    rematch_rate = 350
    title_drop = 380  #
    arm_drop = 390  #
    pet_drop = 396  #
    card_drop = 400  #
    drop_rate = random.randint((0 + (rebirth * rebirth) * (1 + rebirth)), 400)
    durability = random.randint(10, 75)
    mode="Dungeon"
    if difficulty == "HARD":
        gold_drop = 30  
        rift_rate = 55
        rematch_rate = 70
        title_drop = 75  
        arm_drop = 100  
        pet_drop = 250  
        card_drop = 300 
        drop_rate = random.randint((0 + (rebirth * rebirth) * (1 + rebirth)), 300)
        durability = 100
        mode="Purchase"

    try:
        if drop_rate <= gold_drop:
            bless_amount = (30000 + (2000 * matchcount)) * (1 + rebirth)
            if difficulty == "HARD":
                bless_amount = (60000 + (5000 * matchcount)) * (1 + rebirth)
            await crown_utilities.bless(bless_amount, player.id)
            return f"You earned :coin: **{bless_amount}**!"
        elif drop_rate <= rift_rate and drop_rate > gold_drop:
            response = db.updateUserNoFilter(user_query, {'$set': {'RIFT': 1}})
            bless_amount = (35000 + (5000 * matchcount)) * (1 + rebirth)
            await crown_utilities.bless(bless_amount, player.id)
            return f"A RIFT HAS OPENED! You have earned :coin: **{bless_amount}**!"
        elif drop_rate <= rematch_rate and drop_rate > rift_rate:
            response = db.updateUserNoFilter(user_query, {'$inc': {'RETRIES': 3}})
            bless_amount = (40000 + (5000 * matchcount)) * (1 + rebirth)
            await crown_utilities.bless(bless_amount, player.id)
            return f"🆚  You have earned 3 Rematches and  :coin: **{bless_amount}**!"
        elif drop_rate <= title_drop and drop_rate > rematch_rate:
            # if len(vault['TITLES']) >= 25:
            #     await crown_utilities.bless(2500, player.id)
            #     return f"You're maxed out on Titles! You earned :coin: 2500 instead!"
            # if str(titles[rand_title]) in owned_titles:
            #         await crown_utilities.bless(2000, player.id)
            #         return f"You already own **{titles[rand_title]}**! You earn :coin: **2000**."
            # response = db.updateVaultNoFilter(vault_query, {'$addToSet': {'TITLES': str(titles[rand_title])}})
            # return f"You earned _Title:_ **{titles[rand_title]}**!"
            u = await main.bot.fetch_user(player.id)
            response = await crown_utilities.store_drop_card(u, player.id, titles[rand_title], universe, vault, owned_destinies, 30000, 30000,"mode", False, 0, "titles")
            return response
        elif drop_rate <= arm_drop and drop_rate > title_drop:
            # if len(vault['ARMS']) >= 25:
            #     await crown_utilities.bless(3000, player.id)
            #     return f"You're maxed out on Arms! You earned :coin: 3000 instead!"
            # if str(arms[rand_arm]) in owned_arms:
            #     await crown_utilities.bless(2500, player.id)
            #     return f"You already own **{arms[rand_arm]}**! You earn :coin: **2500**."
            # else:
            #     response = db.updateVaultNoFilter(vault_query, {'$addToSet': {'ARMS': {'ARM': str(arms[rand_arm]), 'DUR': durability}}})
            #     return f"You earned _Arm:_ **{arms[rand_arm]}** with ⚒️**{str(durability)}**!"
            u = await main.bot.fetch_user(player.id)
            response = await crown_utilities.store_drop_card(u, player.id, arms[rand_arm], universe, vault, durability, 3000, 3000,"mode", False, 0, "arms")
            return response
        elif drop_rate <= pet_drop and drop_rate > arm_drop:
            if len(vault['PETS']) >= 25:
                await crown_utilities.bless(4000, player.id)
                return f"You're maxed out on Summons! You earned :coin: 4000 instead!"
            pet_owned = False
            for p in vault['PETS']:
                if p['NAME'] == pets[rand_pet]:
                    pet_owned = True

            if pet_owned:
                await crown_utilities.bless(5000, player.id)
                return f"You own _Summon:_ **{pets[rand_pet]}**! Received extra + :coin: 5000!"
            else:
                selected_pet = db.queryPet({'PET': pets[rand_pet]})
                pet_ability_name = list(selected_pet['ABILITIES'][0].keys())[0]
                pet_ability_power = list(selected_pet['ABILITIES'][0].values())[0]
                pet_ability_type = list(selected_pet['ABILITIES'][0].values())[1]

                response = db.updateVaultNoFilter(vault_query, {'$addToSet': {
                    'PETS': {'NAME': selected_pet['PET'], 'LVL': 0, 'EXP': 0, pet_ability_name: int(pet_ability_power),
                             'TYPE': pet_ability_type, 'BOND': 0, 'BONDEXP': 0, 'PATH': selected_pet['PATH']}}})
                await crown_utilities.bless(10000, player.id)
                return f"You earned _Summon:_ **{pets[rand_pet]}** + :coin: 10000!"
        elif drop_rate <= card_drop and drop_rate > pet_drop:
            u = await main.bot.fetch_user(player.id)
            response = await crown_utilities.store_drop_card(u, player.id, cards[rand_card], universe, vault, owned_destinies, 5000, 2500,"mode", False, 0, "cards")
            return response
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
            'player': str(player),
            'type': type(ex).__name__,
            'message': str(ex),
            'trace': trace
        }))
        await crown_utilities.bless(5000, player.id)
        guild = self.bot.get_guild(main.guild_id)
        channel = guild.get_channel(main.guild_channel)
        await channel.send(f"'PLAYER': **{str(player)}**, TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")

        return f"You earned :coin: **5000**!"


async def bossdrops(self,player, universe):
    all_available_drop_cards = db.queryExclusiveDropCards(universe)
    all_available_drop_titles = db.queryExclusiveDropTitles(universe)
    all_available_drop_arms = db.queryExclusiveDropArms(universe)
    all_available_drop_pets = db.queryExclusiveDropPets(universe)
    boss = db.queryBoss({'UNIVERSE': universe})
    vault_query = {'DID': str(player.id)}
    vault = db.queryVault(vault_query)
    owned_arms = []
    for arm in vault['ARMS']:
        owned_arms.append(arm['ARM'])
    owned_titles = vault['TITLES']

    user_query = {'DID': str(player.id)}
    user = db.queryUser(user_query)
    difficulty = user['DIFFICULTY']
    rebirth = user['REBIRTH']

    owned_destinies = []
    for destiny in vault['DESTINY']:
        owned_destinies.append(destiny['NAME'])

    cards = []
    titles = []
    arms = []
    pets = []
    boss_title = boss['TITLE']
    boss_arm = boss['ARM']
    boss_pet = boss['PET']
    boss_card = boss['CARD']

    for card in all_available_drop_cards:
        cards.append(card['NAME'])

    for title in all_available_drop_titles:
        titles.append(title['TITLE'])

    for arm in all_available_drop_arms:
        arms.append(arm['ARM'])

    for pet in all_available_drop_pets:
        pets.append(pet['PET'])

    if len(cards)==0:
        rand_card = 0
    else:
        c = len(cards) - 1
        rand_card = random.randint(0, c)

    if len(titles)==0:
        rand_title= 0
    else:
        t = len(titles) - 1
        rand_title = random.randint(0, t)

    if len(arms)==0:
        rand_arm = 0
    else:
        a = len(arms) - 1
        rand_arm = random.randint(0, a)

    
    if len(pets)==0:
        rand_pet = 0
    else:
        p = len(pets) - 1
        rand_pet = random.randint(0, p)


    gold_drop = 300  #
    rematch_drop = 330 #330
    title_drop = 340  #
    arm_drop = 370  #
    pet_drop = 390  #
    card_drop = 400  #
    boss_title_drop = 450  #
    boss_arm_drop = 480  #
    boss_pet_drop = 495  #
    boss_card_drop = 500  #

    drop_rate = random.randint((0 + (rebirth * rebirth) * (1 + rebirth)), 500)
    durability = random.randint(100, 150)

    try:
        if drop_rate <= gold_drop:
            bless_amount = 1000000 * (1 + rebirth)
            if difficulty == "HARD":
                bless_amount = 5000000 * (1 + rebirth)
            await crown_utilities.bless(bless_amount, player.id)
            return f"You earned :coin: {bless_amount}!"
        elif drop_rate <= rematch_drop and drop_rate > gold_drop:
            response = db.updateUserNoFilter(user_query, {'$inc': {'RETRIES': 10}})
            bless_amount = (1000000  * (1 + rebirth))
            await crown_utilities.bless(bless_amount, player.id)
            return f"🆚  You have earned 10 Rematches and  :coin: **{bless_amount}**!"
        elif drop_rate <= title_drop and drop_rate > gold_drop:
            # if len(vault['TITLES']) >= 25:
            #     await crown_utilities.bless(500000, player.id)
            #     return f"You're maxed out on Titles! You earned :coin: **500000** instead!"
            # if str(titles[rand_title]) in owned_titles:
            #         await crown_utilities.bless(30000, player.id)
            #         return f"You already own **{titles[rand_title]}**! You earn :coin: **30000**."
            # response = db.updateVaultNoFilter(vault_query, {'$addToSet': {'TITLES': str(titles[rand_title])}})
            # return f"You earned {titles[rand_title]}!"
            u = await main.bot.fetch_user(player.id)
            response = await crown_utilities.store_drop_card(u, player.id, titles[rand_title], universe, vault, owned_destinies, 30000, 30000, "Dungeon", False, 0, "titles")
            return response
        elif drop_rate <= arm_drop and drop_rate > title_drop:
            # if len(vault['ARMS']) >= 25:
            #     await crown_utilities.bless(40000, player.id)
            #     return f"You're maxed out on Arms! You earned :coin: **40000** instead!"
            # if str(arms[rand_arm]) in owned_arms:
            #     await crown_utilities.bless(40000, player.id)
            #     return f"You already own **{arms[rand_arm]}**! You earn :coin: **40000**."
            # else:
            #     response = db.updateVaultNoFilter(vault_query, {'$addToSet': {'ARMS': {'ARM': str(arms[rand_arm]), 'DUR': durability}}})
            #     return f"You earned _Arm:_ **{arms[rand_arm]}** with ⚒️**{str(durability)}**!"
            u = await main.bot.fetch_user(player.id)
            response = await crown_utilities.store_drop_card(u, player.id, arms[rand_arm], universe, vault, durability, 40000, 40000, "Dungeon", False, 0, "arms")
            return response
        elif drop_rate <= pet_drop and drop_rate > arm_drop:
            if len(vault['PETS']) >= 25:
                await crown_utilities.bless(8000, player.id)
                return f"You're maxed out on Summons! You earned :coin: 8000 instead!"
            selected_pet = db.queryPet({'PET': pets[rand_pet]})
            pet_ability_name = list(selected_pet['ABILITIES'][0].keys())[0]
            pet_ability_power = list(selected_pet['ABILITIES'][0].values())[0]
            pet_ability_type = list(selected_pet['ABILITIES'][0].values())[1]

            response = db.updateVaultNoFilter(vault_query, {'$addToSet': {
                'PETS': {'NAME': selected_pet['PET'], 'LVL': 0, 'EXP': 0, pet_ability_name: int(pet_ability_power),
                         'TYPE': pet_ability_type, 'BOND': 0, 'BONDEXP': 0, 'PATH': selected_pet['PATH']}}})
            await crown_utilities.bless(750000, player.id)
            return f"You earned {pets[rand_pet]} + :coin: 750000!"
        elif drop_rate <= card_drop and drop_rate > pet_drop:
            u = await main.bot.fetch_user(player.id)
            response = await crown_utilities.store_drop_card(u, player.id, cards[rand_card], universe, vault, owned_destinies, 500000, 500000, "Dungeon", False, 0, "cards")
            return response
        elif drop_rate <= boss_title_drop and drop_rate > card_drop:
            # if len(vault['TITLES']) >= 25:
            #     await crown_utilities.bless(10000000, player.id)
            #     return f"You're maxed out on Titles! You earned :coin: **10,000,000** instead!"
            # response = db.updateVaultNoFilter(vault_query, {'$addToSet': {'TITLES': str(boss_title)}})
            # return f"You earned the Exclusive Boss Title: {boss_title}!"
            u = await main.bot.fetch_user(player.id)
            response = await crown_utilities.store_drop_card(u, player.id, boss_title, universe, vault, owned_destinies, 50000, 50000, "Boss", False, 0, "titles")
            return response
        elif drop_rate <= boss_arm_drop and drop_rate > boss_title_drop:
            # if len(vault['ARMS']) >= 25:
            #     await crown_utilities.bless(10000000, player.id)
            #     return f"You're maxed out on Arms! You earned :coin: **10,000,000** instead!"
            # if str(boss_arm) in owned_arms:
            #     await crown_utilities.bless(9000000, player.id)
            #     return f"You already own **{arms[rand_arm]}**! You earn :coin: **9,000,000**."
            # else:
            #     response = db.updateVaultNoFilter(vault_query, {'$addToSet': {'ARMS': {'ARM': str(boss_arm), 'DUR': durability}}})
            #     return f"You earned the Exclusive Boss Arm: **{str(boss_arm)}** with ⚒️**{str(durability)}**!"
            u = await main.bot.fetch_user(player.id)
            response = await crown_utilities.store_drop_card(u, player.id, boss_arm, universe, vault, durability, 9000000, 9000000, "Boss", False, 0, "arms")
            return response
        elif drop_rate <= boss_pet_drop and drop_rate > boss_arm_drop:
            if len(vault['PETS']) >= 25:
                await crown_utilities.bless(1500000, player.id)
                return f"You're maxed out on Summons! You earned :coin: **15,000,000** instead!"
            selected_pet = db.queryPet({'PET': boss['PET']})
            pet_ability_name = list(selected_pet['ABILITIES'][0].keys())[0]
            pet_ability_power = list(selected_pet['ABILITIES'][0].values())[0]
            pet_ability_type = list(selected_pet['ABILITIES'][0].values())[1]

            response = db.updateVaultNoFilter(vault_query, {'$addToSet': {
                'PETS': {'NAME': selected_pet['PET'], 'LVL': 0, 'EXP': 0, pet_ability_name: int(pet_ability_power),
                         'TYPE': pet_ability_type, 'BOND': 0, 'BONDEXP': 0, 'PATH': selected_pet['PATH']}}})
            await crown_utilities.bless(10000000, player.id)
            return f"You earned the Exclusive Boss Summon:  {boss['PET']} + :coin: **10,000,000**!"
        elif drop_rate <= boss_card_drop and drop_rate > boss_pet_drop:
            u = await main.bot.fetch_user(player.id)
            response = await crown_utilities.store_drop_card(u, player.id, boss_card, universe, vault, owned_destinies, 30000, 10000, "Boss", False, 0, "cards")
            return response
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
            'player': str(player),
            'type': type(ex).__name__,
            'message': str(ex),
            'trace': trace
        }))
        await crown_utilities.bless(5000, player.id)
        guild = self.bot.get_guild(main.guild_id)
        channel = guild.get_channel(main.guild_channel)
        await channel.send(f"'PLAYER': **{str(player)}**, TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")

        return f"You earned :coin: **5000**!"


enhancer_mapping = {'ATK': 'Increase Attack %',
'DEF': 'Increase Defense %',
'STAM': 'Increase Stamina',
'HLT': 'Heal yourself or companion',
'LIFE': 'Steal Health from Opponent',
'DRAIN': 'Drain Stamina from Opponent',
'FLOG': 'Steal Attack from Opponent',
'WITHER': 'Steal Defense from Opponent',
'RAGE': 'Lose Defense, Increase AP',
'BRACE': 'Lose Attack, Increase AP',
'BZRK': 'Lose Health, Increase Attack',
'CRYSTAL': 'Lose Health, Increase Defense',
'GROWTH': 'Lose 10% Max Health, Increase Attack, Defense and AP',
'STANCE': 'Swap your Attack & Defense, Increase Defense',
'CONFUSE': 'Swap Opponent Attack & Defense, Decrease Opponent Defense',
'BLINK': 'Decrease your  Stamina, Increase Target Stamina',
'SLOW': 'Increase Opponent Stamina, Decrease Your Stamina then Swap Stamina with Opponent',
'HASTE': 'Increase your Stamina, Decrease Opponent Stamina then Swap Stamina with Opponent',
'FEAR': 'Lose 10% Max Health, Decrease Opponent Attack, Defense and AP',
'SOULCHAIN': 'You and Your Opponent Stamina Link',
'GAMBLE': 'You and Your Opponent Health Link',
'WAVE': 'Deal Damage, Decreases over time',
'CREATION': 'Heals you, Decreases over time',
'BLAST': 'Deals Damage, Increases over time based on card tier',
'DESTRUCTION': 'Decreases Your Opponent Max Health, Increases over time based on card tier',
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
title_enhancer_mapping = {'ATK': 'Increase Attack',
'DEF': 'Increase Defense',
'STAM': 'Increase Stamina',
'HLT': 'Heal for AP',
'LIFE': 'Steal AP Health',
'DRAIN': 'Drain Stamina from Opponent',
'FLOG': 'Steal Attack from Opponent',
'WITHER': 'Steal Defense from Opponent',
'RAGE': 'Lose Defense, Increase AP',
'BRACE': 'Lose Attack, Increase AP',
'BZRK': 'Lose Health, Increase Attack',
'CRYSTAL': 'Lose Health, Increase Defense',
'GROWTH': 'Lose 5% Max Health, Increase Attack, Defense and AP',
'STANCE': 'Swap your Attack & Defense, Increase Defense',
'CONFUSE': 'Swap Opponent Attack & Defense, Decrease Opponent Defense',
'BLINK': 'Decrease your Stamina, Increase Target Stamina',
'SLOW': 'Decrease Turn Count by 1',
'HASTE': 'Increase Turn Count By 1',
'FEAR': 'Lose 5% MAx Health, Decrease Opponent Attack, Defense and AP',
'SOULCHAIN': 'Both players stamina regen equals AP',
'GAMBLE': 'Focusing players health regen equals to AP',
'WAVE': 'Deal Damage, Decreases over time',
'CREATION': 'Heals you, Decreases over time',
'BLAST': 'Deals Damage on your turn based on card tier',
'DESTRUCTION': 'Decreases Your Opponent Max Health, Increases over time based on card tier',
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

element_mapping = {'PHYSICAL': 'If ST(stamina) greater than 80, Deals double Damage',
'FIRE': 'Does 25% damage of previous attack over the next opponent turns, stacks',
'ICE': 'After 2 uses opponent freezes and loses 1 turn',
'WATER': 'Increases all water attack dmg by 40 Flat',
'EARTH': 'Cannot be Parried. Increases Def by 25% AP',
'ELECTRIC': 'Add 15% to Shock damage, added to each attack',
'WIND': 'Cannot Miss, boost all wind damage by 15% DMG',
'PSYCHIC': 'Penetrates Barriers. Reduce opponent ATK & DEF by 15% AP',
'DEATH': 'Adds 20% opponent max health as damage',
'LIFE': 'Heal for 20% AP',
'LIGHT': 'Regain 50% Stamina Cost, Increase ATK by 20% DMG',
'DARK': 'Penetrates shields & decrease opponent stamina by 15',
'POISON': 'Penetrates shields, Opponent takes additional 30 damage each turn stacking up to 600',
'RANGED': 'If ST(Stamina) > 30 deals 1.7x Damage',
'SPIRIT': 'Has higher chance of Crit',
'RECOIL': 'Deals 60% damage back to you, if damage would kill you reduce health to 1',
'TIME': 'IF ST(Stamina) < 80 you Focus after attacking, You Block during your Focus',
'BLEED': 'After 3 Attacks deal 10x turn count damage to opponent',
'GRAVITY': 'Disables Opponent Block and Reduce opponent DEF by 25% AP'
}

passive_enhancer_suffix_mapping = {'ATK': ' %',
'DEF': ' %',
'STAM': ' Flat',
'HLT': ' %',
'LIFE': '%',
'DRAIN': ' Flat',
'FLOG': '%',
'WITHER': '%',
'RAGE': '%',
'BRACE': '%',
'BZRK': '%',
'CRYSTAL': '%',
'GROWTH': ' Flat',
'STANCE': ' Flat',
'CONFUSE': ' Flat',
'BLINK': ' Flat',
'SLOW': ' Flat',
'HASTE': ' Flat',
'FEAR': ' Flat',
'SOULCHAIN': ' Flat',
'GAMBLE': ' Flat',
'WAVE': ' Flat',
'CREATION': '%',
'BLAST': ' Flat',
'DESTRUCTION': '%',
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
'GROWTH': ' Flat',
'STANCE': ' Flat',
'CONFUSE': ' Flat',
'BLINK': ' Flat',
'SLOW': ' Flat',
'HASTE': ' Flat',
'FEAR': ' Flat',
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
title_enhancer_suffix_mapping = {'ATK': ' Flat',
'DEF': ' Flat',
'STAM': ' Flat',
'HLT': ' %',
'LIFE': '%',
'DRAIN': ' Flat',
'FLOG': '%',
'WITHER': '%',
'RAGE': '%',
'BRACE': '%',
'BZRK': '%',
'CRYSTAL': '%',
'GROWTH': ' Flat',
'STANCE': ' Flat',
'CONFUSE': ' Flat',
'BLINK': ' Flat',
'SLOW': ' Turn',
'HASTE': ' Turn',
'FEAR': ' Flat',
'SOULCHAIN': ' Flat',
'GAMBLE': ' Flat',
'WAVE': ' Flat',
'CREATION': '%',
'BLAST': ' Flat',
'DESTRUCTION': '%',
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

abyss_floor_reward_list = [10,20,30,40,50,60,70,80,90,100]

crown_rift_universe_mappings = {'Crown Rift Awakening': 3, 'Crown Rift Slayers': 2, 'Crown Rift Madness': 5}
Healer_Enhancer_Check = ['HLT', 'LIFE']
DPS_Enhancer_Check = ['FLOG', 'WITHER']
INC_Enhancer_Check = ['ATK', 'DEF']
TRADE_Enhancer_Check = ['RAGE', 'BRACE']
Gamble_Enhancer_Check = ['GAMBLE', 'SOULCHAIN']
SWITCH_Enhancer_Check = ['STANCE', 'CONFUSE']
Time_Enhancer_Check = ['HASTE', 'SLOW','BLINK']
Support_Enhancer_Check = ['DEF', 'ATK', 'WITHER', 'FLOG']
Sacrifice_Enhancer_Check = ['BZRK', 'CRYSTAL']
FORT_Enhancer_Check = ['GROWTH', 'FEAR']
Stamina_Enhancer_Check = ['STAM', 'DRAIN']
Control_Enhancer_Check = ['SOULCHAIN']
Damage_Enhancer_Check = ['DESTRUCTION', 'BLAST']
Turn_Enhancer_Check = ['WAVE', 'CREATION']
take_chances_messages = ['You lost immediately.', 'You got smoked!', 'You fainted before the fight even started.',
                         'That... was just sad. You got dropped with ease.', 'Too bad, so sad. You took the L.',
                         'Annnd another L. You lost.', 'Annnnnnnnnnnd another L! You lost.',
                         'How many Ls you gonna take today?', 'That was worse than the last time. You got dropped.']

pokemon_universes= ['Kanto Region', 'Johnto Region', 'Hoenn Region', 'Sinnoh Region', 'Kalos Region', 'Galar Region', 'Alola Region', 'Unova Region']