import time
from operator import floordiv
from discord import guild, message
from re import T
import discord
from discord.ext import commands
import db
import dataclasses as data
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
        self._cd = commands.CooldownMapping.from_cooldown(1, 900, commands.BucketType.member)  # Change accordingly. Currently every 8 minutes (3600 seconds == 60 minutes)
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
        try:
            if message.author == main.bot.user:
                return #
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
                p = Player(player['AUTOSAVE'], player['DISNAME'], player['DID'], player['AVATAR'], player['GUILD'], player['TEAM'], player['FAMILY'], player['TITLE'], player['CARD'], player['ARM'], player['PET'], player['TALISMAN'], player['CROWN_TALES'], player['DUNGEONS'], player['BOSS_WINS'], player['RIFT'], player['REBIRTH'], player['LEVEL'], player['EXPLORE'], player['SAVE_SPOT'], player['PERFORMANCE'], player['TRADING'], player['BOSS_FOUGHT'], player['DIFFICULTY'], player['STORAGE_TYPE'], player['USED_CODES'], player['BATTLE_HISTORY'], player['PVP_WINS'], player['PVP_LOSS'], player['RETRIES'], player['PRESTIGE'], player['PATRON'], player['FAMILY_PET'], player['EXPLORE_LOCATION'])    
           
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
                selected_card = Card(cards[rand_card]['NAME'], cards[rand_card]['PATH'], cards[rand_card]['PRICE'], cards[rand_card]['EXCLUSIVE'], cards[rand_card]['AVAILABLE'], cards[rand_card]['IS_SKIN'], cards[rand_card]['SKIN_FOR'], cards[rand_card]['HLT'], cards[rand_card]['HLT'], cards[rand_card]['STAM'], cards[rand_card]['STAM'], cards[rand_card]['MOVESET'], cards[rand_card]['ATK'], cards[rand_card]['DEF'], cards[rand_card]['TYPE'], cards[rand_card]['PASS'][0], cards[rand_card]['SPD'], cards[rand_card]['UNIVERSE'], cards[rand_card]['HAS_COLLECTION'], cards[rand_card]['TIER'], cards[rand_card]['COLLECTION'], cards[rand_card]['WEAKNESS'], cards[rand_card]['RESISTANT'], cards[rand_card]['REPEL'], cards[rand_card]['ABSORB'], cards[rand_card]['IMMUNE'], cards[rand_card]['GIF'], cards[rand_card]['FPATH'], cards[rand_card]['RNAME'], cards[rand_card]['RPATH'], False)
                selected_card.set_affinity_message()
                selected_card.set_explore_bounty_and_difficulty(battle)
    
                battle.set_explore_config(universe, selected_card)
                battle.bounty = selected_card.bounty
    
                random_battle_buttons = [
                    manage_components.create_button(
                        style=ButtonStyle.blue,
                        label="🪙 Gold",
                        custom_id="gold"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.green,
                        label="👑 Glory",
                        custom_id="glory"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red,
                        label="Ignore",
                        custom_id="ignore"
                    )
                ]
    
                random_battle_buttons_action_row = manage_components.create_actionrow(*random_battle_buttons)
    
    
                # Send Message
                embedVar = discord.Embed(title=f"**{selected_card.approach_message}{selected_card.name}** has a bounty!",
                                         description=textwrap.dedent(f"""\
                **Bounty** **{selected_card.bounty_message}**
                {selected_card.battle_message}
                """), colour=0xf1c40f)
             
                embedVar.set_image(url="attachment://image.png")
                embedVar.set_thumbnail(url=message.author.avatar_url)
                embedVar.set_footer(text=f"Use /explore to exit Explore Mode",icon_url="https://cdn.discordapp.com/emojis/877233426770583563.gif?v=1")
                
    
                setchannel = discord.utils.get(channel_list, name=server_channel)
                await setchannel.send(f":milky_way:{message.author.mention}") 
                msg = await setchannel.send(embed=embedVar, file=selected_card.showcard("non-battle", "none", {'TITLE': 'EXPLORE TITLE'}, 0, 0), components=[random_battle_buttons_action_row])     
    
                def check(button_ctx):
                    return button_ctx.author == message.author
    
                try:
                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[
                        random_battle_buttons_action_row], timeout=300, check=check)
    
                    if button_ctx.custom_id == "glory":
                        await button_ctx.defer(ignore=True)
                        battle.explore_type = "glory"
                        await battle_commands(self, button_ctx, battle, p, selected_card, player2=None, player3=None)
                        await msg.edit(components=[])
    
                    if button_ctx.custom_id == "gold":
                        await button_ctx.defer(ignore=True)
                        battle.explore_type = "gold"
                        await battle_commands(self, button_ctx, battle, p, selected_card, player2=None, player3=None)
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


    @cog_ext.cog_slash(description="Toggle Explore Mode On/Off or explore a universe", options=[
        # create_option(
        #     name="toggle",
        #     description="Turn explore off or keep on",
        #     option_type=3,
        #     required=False,
        #     choices=[
        #         create_choice(
        #             name="Turn Explore Mode Off",
        #             value="off"
        #         ),
        #         create_choice(
        #             name="Turn Explore Mode On",
        #             value="on"
        #         ),
        #     ]
        # ),
        create_option(
            name="universe",
            description="Type universe you want to explore, or type 'all' to explore all universes",
            option_type=3,
            required=False
        )
    ], guild_ids=main.guild_ids)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def explore(self, ctx: SlashContext, universe=None):
        try:
            player = db.queryUser({"DID": str(ctx.author.id)})
            p = Player(player['AUTOSAVE'],
                player['DISNAME'], player['DID'], player['AVATAR'], player['GUILD'], player['TEAM'], player['FAMILY'],
                player['TITLE'], player['CARD'], player['ARM'], player['PET'], player['TALISMAN'], player['CROWN_TALES'],
                player['DUNGEONS'], player['BOSS_WINS'], player['RIFT'], player['REBIRTH'], player['LEVEL'],
                player['EXPLORE'], player['SAVE_SPOT'], player['PERFORMANCE'], player['TRADING'], player['BOSS_FOUGHT'],
                player['DIFFICULTY'], player['STORAGE_TYPE'], player['USED_CODES'], player['BATTLE_HISTORY'], player['PVP_WINS'],
                player['PVP_LOSS'], player['RETRIES'], player['PRESTIGE'], player['PATRON'], player['FAMILY_PET'],
                player['EXPLORE_LOCATION']
            )
            message = None
            if p.explore == 0:
                db.updateUserNoFilter({'DID': str(p.did)}, {'$set': {'EXPLORE': True}})
                message = f":milky_way: | Entering Explore Mode"
            elif p.explore == 1:
                db.updateUserNoFilter({'DID': str(p.did)}, {'$set': {'EXPLORE': False, 'EXPLORE_LOCATION': "NULL"}})
                message = ":rotating_light: | Exiting Explore Mode"
                    
            # if toggle is not None:
            #     if toggle.lower() == "on":
            #         db.updateUserNoFilter({'DID': str(p.did)}, {'$set': {'EXPLORE': True}})
            #         message = f"You are now entering Explore Mode :milky_way: "
            #     elif toggle.lower() == "off":
            #         db.updateUserNoFilter({'DID': str(p.did)}, {'$set': {'EXPLORE': False, 'EXPLORE_LOCATION': "NULL"}})
            #         message = "Exiting Exploration Mode :rotating_light:"

            if universe is not None:
                message = p.set_explore(universe)

            if message is not None:
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
                                   ),create_choice(
                                       name="Preset 4",
                                       value="4"
                                   ),
                                   create_choice(
                                       name="Preset 5",
                                       value="5"
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

        try:
            # await ctx.defer()
            deck = int(deck)
            if deck != 1 and deck != 2 and deck != 3 and deck != 4 and deck != 5:
                await ctx.send("Not a valid Deck Option")
                return
            deckNumber = deck - 1

            player = db.queryUser({'DID': str(ctx.author.id)})
            
            if not player['U_PRESET'] and int(deck) > 3:
                await ctx.send(":coin: Purchase additional **/preset** slots at the **/blacksmith**")
                return

            p = Player(player['AUTOSAVE'], player['DISNAME'], player['DID'], player['AVATAR'], player['GUILD'], player['TEAM'], player['FAMILY'], player['TITLE'], player['CARD'], player['ARM'],player['PET'], player['TALISMAN'], player['CROWN_TALES'], player['DUNGEONS'],
            player['BOSS_WINS'], player['RIFT'], player['REBIRTH'], player['LEVEL'], player['EXPLORE'], player['SAVE_SPOT'], player['PERFORMANCE'], player['TRADING'], player['BOSS_FOUGHT'], player['DIFFICULTY'], player['STORAGE_TYPE'], player['USED_CODES'], player['BATTLE_HISTORY'], player['PVP_WINS'], player['PVP_LOSS'], player['RETRIES'], player['PRESTIGE'], player['PATRON'], player['FAMILY_PET'], player['EXPLORE_LOCATION'])

            p3 = Player(player['AUTOSAVE'], player['DISNAME'], player['DID'], player['AVATAR'], player['GUILD'], player['TEAM'], player['FAMILY'], player['TITLE'], player['CARD'], player['ARM'],player['PET'], player['TALISMAN'], player['CROWN_TALES'], player['DUNGEONS'],
            player['BOSS_WINS'], player['RIFT'], player['REBIRTH'], player['LEVEL'], player['EXPLORE'], player['SAVE_SPOT'], player['PERFORMANCE'], player['TRADING'], player['BOSS_FOUGHT'], player['DIFFICULTY'], player['STORAGE_TYPE'], player['USED_CODES'], player['BATTLE_HISTORY'], player['PVP_WINS'], player['PVP_LOSS'], player['RETRIES'], player['PRESTIGE'], player['PATRON'], player['FAMILY_PET'], player['EXPLORE_LOCATION'])

            p3.set_deck_config(deckNumber)

            if p.get_locked_feature(mode):
                await ctx.send(p._locked_feature_message)
                return

            universe_selection = await select_universe(self, ctx, p, mode, None)
            if not universe_selection:
                return
            battle = Battle(mode, p)

            battle.set_universe_selection_config(universe_selection)
            battle.is_duo_mode = True
                
            await battle_commands(self, ctx, battle, p, None, player2=None, player3=p3)
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
            player3 = db.queryUser({'DID': str(user.id)})
            p1 = Player(player['AUTOSAVE'], player['DISNAME'], player['DID'], player['AVATAR'], player['GUILD'], player['TEAM'], player['FAMILY'], player['TITLE'], player['CARD'], player['ARM'], player['PET'], player['TALISMAN'], player['CROWN_TALES'], player['DUNGEONS'], player['BOSS_WINS'], player['RIFT'], player['REBIRTH'], player['LEVEL'], player['EXPLORE'], player['SAVE_SPOT'], player['PERFORMANCE'], player['TRADING'], player['BOSS_FOUGHT'], player['DIFFICULTY'], player['STORAGE_TYPE'], player['USED_CODES'], player['BATTLE_HISTORY'], player['PVP_WINS'], player['PVP_LOSS'], player['RETRIES'], player['PRESTIGE'], player['PATRON'], player['FAMILY_PET'], player['EXPLORE_LOCATION'])    
            p3 = Player(player3['AUTOSAVE'], player3['DISNAME'], player3['DID'], player3['AVATAR'], player3['GUILD'], player3['TEAM'], player3['FAMILY'], player3['TITLE'], player3['CARD'], player3['ARM'], player3['PET'], player3['TALISMAN'], player3['CROWN_TALES'], player3['DUNGEONS'], player3['BOSS_WINS'], player3['RIFT'], player3['REBIRTH'], player3['LEVEL'], player3['EXPLORE'], player3['SAVE_SPOT'], player3['PERFORMANCE'], player3['TRADING'], player3['BOSS_FOUGHT'], player3['DIFFICULTY'], player3['STORAGE_TYPE'], player3['USED_CODES'], player3['BATTLE_HISTORY'], player3['PVP_WINS'], player3['PVP_LOSS'], player3['RETRIES'], player3['PRESTIGE'], player3['PATRON'], player3['FAMILY_PET'], player3['EXPLORE_LOCATION'])    
            battle = Battle(mode, p1)


            universe_selection = await select_universe(self, ctx, p1, mode, p3)
            if not universe_selection:
                return
            battle.set_universe_selection_config(universe_selection)
            battle.is_co_op_mode = True

            await battle_commands(self, ctx, battle, p1, None, None, p3)
        
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
        await ctx.defer()
        a_registered_player = await crown_utilities.player_check(ctx)
        if not a_registered_player:
            return
        
        try:
            player = db.queryUser({'DID': str(ctx.author.id)})
            p = Player(player['AUTOSAVE'],player['DISNAME'], player['DID'], player['AVATAR'], player['GUILD'], player['TEAM'], player['FAMILY'], player['TITLE'], player['CARD'], player['ARM'],player['PET'], player['TALISMAN'], player['CROWN_TALES'], player['DUNGEONS'],
            player['BOSS_WINS'], player['RIFT'], player['REBIRTH'], player['LEVEL'], player['EXPLORE'], player['SAVE_SPOT'], player['PERFORMANCE'], player['TRADING'], player['BOSS_FOUGHT'], player['DIFFICULTY'], player['STORAGE_TYPE'], player['USED_CODES'], player['BATTLE_HISTORY'], player['PVP_WINS'], player['PVP_LOSS'], player['RETRIES'], player['PRESTIGE'], player['PATRON'], player['FAMILY_PET'], player['EXPLORE_LOCATION'])

            if mode == "Abyss":
                await abyss(self, ctx, p, mode)
                return

            if mode == "Tutorial":
                await tutorial(self, ctx, p, mode)
                return


            if p.get_locked_feature(mode):
                await ctx.send(p._locked_feature_message)
                return

            universe_selection = await select_universe(self, ctx, p, mode, None)
            
            if universe_selection == None:
                return

            battle = Battle(mode, p)

            battle.set_universe_selection_config(universe_selection)
                
            await battle_commands(self, ctx, battle, p, None, player2=None, player3=None)
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
            p1 = Player(player['AUTOSAVE'], player['DISNAME'], player['DID'], player['AVATAR'], player['GUILD'], player['TEAM'], player['FAMILY'], player['TITLE'], player['CARD'], player['ARM'], player['PET'], player['TALISMAN'], player['CROWN_TALES'], player['DUNGEONS'], player['BOSS_WINS'], player['RIFT'], player['REBIRTH'], player['LEVEL'], player['EXPLORE'], player['SAVE_SPOT'], player['PERFORMANCE'], player['TRADING'], player['BOSS_FOUGHT'], player['DIFFICULTY'], player['STORAGE_TYPE'], player['USED_CODES'], player['BATTLE_HISTORY'], player['PVP_WINS'], player['PVP_LOSS'], player['RETRIES'], player['PRESTIGE'], player['PATRON'], player['FAMILY_PET'], player['EXPLORE_LOCATION'])    
            p2 = Player(player2['AUTOSAVE'], player2['DISNAME'], player2['DID'], player2['AVATAR'], player2['GUILD'], player2['TEAM'], player2['FAMILY'], player2['TITLE'], player2['CARD'], player2['ARM'], player2['PET'], player2['TALISMAN'], player2['CROWN_TALES'], player2['DUNGEONS'], player2['BOSS_WINS'], player2['RIFT'], player2['REBIRTH'], player2['LEVEL'], player2['EXPLORE'], player2['SAVE_SPOT'], player2['PERFORMANCE'], player2['TRADING'], player2['BOSS_FOUGHT'], player2['DIFFICULTY'], player2['STORAGE_TYPE'], player2['USED_CODES'], player2['BATTLE_HISTORY'], player2['PVP_WINS'], player2['PVP_LOSS'], player2['RETRIES'], player2['PRESTIGE'], player2['PATRON'], player2['FAMILY_PET'], player2['EXPLORE_LOCATION'])    
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

            await battle_commands(self, ctx, battle, p1, None, p2, None)

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
            await channel.send(f"'PLAYER': **{str(ctx.author)}**, 'GUILD': **{str(ctx.author.guild)}**,  TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {tracplayer1e}")
            return


    #@cog_ext.cog_slash(description="Start an Association Raid", guild_ids=main.guild_ids)
    async def raid(self, ctx, guild):
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

            guild = sowner['TEAM']
            guild_info = db.queryTeam({'TEAM_NAME': guild.lower()})
            oguild_name = "PCG"
            shield_test_active = False
            shield_training_active = False
            if guild_info:
                oguild_name = guild_info['GUILD']
                oassociation = db.queryGuildAlt({'GNAME': oguild_name})
            player_guild = sowner['GUILD']

            if oguild_name == "PCG":
                await ctx.send(m.NO_GUILD, delete_after=5)
                return
            if oassociation['SHIELD'] == sowner['DISNAME']:
                shield_training_active = True
            elif player_guild == guildname:
                shield_test_active = True
                

            guild_query = {'GNAME': guildname}
            association_info = db.queryGuildAlt(guild_query)
            guild_shield = ""

            if not association_info:
                await ctx.send(m.GUILD_DOESNT_EXIST, delete_after=5)
                return
            guild_shield = association_info['SHIELD']
            shield_id = association_info['SDID']
            guild_hall = association_info['HALL']
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
            
            # Guild Fees
            title_match_active = False
            fee = hall_info['FEE']
            if oguild_name == tguild:
                title_match_active = True
            
            
            mode = "RAID"
            
            player = sowner
            player2 = t_user
            p1 = Player(player['AUTOSAVE'], player['DISNAME'], player['DID'], player['AVATAR'], oguild_name, player['TEAM'], player['FAMILY'], player['TITLE'], player['CARD'], player['ARM'], player['PET'], player['TALISMAN'], player['CROWN_TALES'], player['DUNGEONS'], player['BOSS_WINS'], player['RIFT'], player['REBIRTH'], player['LEVEL'], player['EXPLORE'], player['SAVE_SPOT'], player['PERFORMANCE'], player['TRADING'], player['BOSS_FOUGHT'], player['DIFFICULTY'], player['STORAGE_TYPE'], player['USED_CODES'], player['BATTLE_HISTORY'], player['PVP_WINS'], player['PVP_LOSS'], player['RETRIES'], player['PRESTIGE'], player['PATRON'], player['FAMILY_PET'], player['EXPLORE_LOCATION'])    
            p2 = Player(player2['AUTOSAVE'], player2['DISNAME'], player2['DID'], player2['AVATAR'], tteam, player2['TEAM'], player2['FAMILY'], player2['TITLE'], player2['CARD'], player2['ARM'], player2['PET'], player2['TALISMAN'], player2['CROWN_TALES'], player2['DUNGEONS'], player2['BOSS_WINS'], player2['RIFT'], player2['REBIRTH'], player2['LEVEL'], player2['EXPLORE'], player2['SAVE_SPOT'], player2['PERFORMANCE'], player2['TRADING'], player2['BOSS_FOUGHT'], player2['DIFFICULTY'], player2['STORAGE_TYPE'], player2['USED_CODES'], player2['BATTLE_HISTORY'], player2['PVP_WINS'], player2['PVP_LOSS'], player2['RETRIES'], player2['PRESTIGE'], player2['PATRON'], player2['FAMILY_PET'], player2['EXPLORE_LOCATION'])  
            battle = Battle(mode, p1)
            battle.create_raid(title_match_active, shield_test_active, shield_training_active, association_info, hall_info, tteam, oguild_name)
            


            

            # o = db.queryCard({'NAME': sowner['CARD']})
            # otitle = db.queryTitle({'TITLE': sowner['TITLE']})

            # t = db.queryCard({'NAME': t_user['CARD']})
            # ttitle = db.queryTitle({'TITLE': t_user['TITLE']})
            
            if private_channel:
                await battle_commands(self, ctx, battle, p1, None, p2, player3=None)
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
            universe_data = list(db.queryAllUniverse())
            #universe_count = 0
            #for uni in universe_data:
                #universe_count = universe_count + 1
            #if universe_count > 25:
                #universe_subset = random.sample(universe_data, k=min(len(universe_data), 25))
            #else:
            universe_subset = random.sample(universe_data, k=min(len(universe_data), 25))

            # user = db.queryUser({'DID': str(ctx.author.id)})
            universe_embed_list = []
            for uni in universe_subset:
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


async def tutorial(self, ctx, player, mode):
    try:
        await ctx.defer()
        a_registered_player = await crown_utilities.player_check(ctx)
        if not a_registered_player:
            return

        await ctx.send("🆚 Building Tutorial Match...", delete_after=10)

        tutorial_did = '837538366509154407'
        battle = Battle(mode, player)
        battle.set_tutorial(tutorial_did)
        battle.mode = "PVP"
        opponent = db.queryUser({'DID': tutorial_did})
        player2 = Player(opponent['AUTOSAVE'], opponent['DISNAME'], opponent['DID'], opponent['AVATAR'], opponent['GUILD'], opponent['TEAM'], opponent['FAMILY'], opponent['TITLE'], opponent['CARD'], opponent['ARM'],opponent['PET'], opponent['TALISMAN'], opponent['CROWN_TALES'], opponent['DUNGEONS'], opponent['BOSS_WINS'], opponent['RIFT'], opponent['REBIRTH'], opponent['LEVEL'], opponent['EXPLORE'], opponent['SAVE_SPOT'], opponent['PERFORMANCE'], opponent['TRADING'], opponent['BOSS_FOUGHT'], opponent['DIFFICULTY'], opponent['STORAGE_TYPE'], opponent['USED_CODES'], opponent['BATTLE_HISTORY'], opponent['PVP_WINS'], opponent['PVP_LOSS'], opponent['RETRIES'], opponent['PRESTIGE'], opponent['PATRON'], opponent['FAMILY_PET'], opponent['EXPLORE_LOCATION'])
        

        await battle_commands(self, ctx, battle, player, None, player2, None)
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
        familysummon = family_info['SUMMON']
        if familysummon['NAME'] == str(pet):
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



async def abyss(self, ctx: SlashContext, _player, mode):
    await ctx.defer()
    a_registered_player = await crown_utilities.player_check(ctx)
    if not a_registered_player:
        return

    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(m.SERVER_FUNCTION_ONLY)
        return

    try:
        abyss = Battle(mode, _player)

        abyss_embed = abyss.set_abyss_config(_player)

        if not abyss_embed:
            await ctx.send(f"{abyss.abyss_message}")
            return

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
                        f":x: We're sorry! :flower_playing_cards: | **{_player.equipped_card}** is banned on floor {abyss.abyss_floor}. Please, try again with another card.")
                    return
                
                await battle_commands(self, ctx, abyss, _player, None, player2=None, player3=None)

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
        scenario.selected_universe = universe
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
                    await battle_commands(self, ctx, scenario, _player, None, player2=None, player3=None)
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
    
    if mode in crown_utilities.CO_OP_M and mode not in crown_utilities.DUO_M:
        user2 = await main.bot.fetch_user(p2.did)
        opponent_ping = user2.mention
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
        msg = await ctx.send(f"{user2.mention} Do you accept the **Coop Invite**?", components=[coop_buttons_action_row])
        def check(button_ctx):
            print(button_ctx.author.id )
            print(user2)
            return button_ctx.author == user2
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
        available_universes = p.set_selectable_universes(ctx, mode, None)


        if not available_universes:
            if mode in crown_utilities.DUNGEON_M:
                universe_embed_list = discord.Embed(title= f":fire: There are no available Dungeons at this time.", description=textwrap.dedent(f"""
                __:fire: How to unlock Dungeons?__
                You unlock Dungeons by Completing the Universe Tale. Once a Dungeon is unlocked you can enter it forever.
                
                Conquer Dungeons for High Tier Loot Drops and Increased Gold!
                """))
                await ctx.send(embed=universe_embed_list)
                return
        label_text = "Start Battle!"
        scenario_text = "View Available Scenario Battles!"
        if mode in crown_utilities.CO_OP_M:
            label_text = "Start CO-OP Battle!"
            scenario_text = "View Available Scenario Battles!"
            if mode in crown_utilities.DUO_M:
                label_text = "Start Duo Battle!"
                scenario_text = "View Available Scenario Battles!"
        if mode in crown_utilities.CO_OP_M:
            if mode in crown_utilities.TALE_M:
                buttons = [
                    manage_components.create_button(style=3, label=label_text, custom_id="start"),
                ]
            if  mode in crown_utilities.DUNGEON_M:
                buttons = [
                    manage_components.create_button(style=3, label=label_text, custom_id="start"),
                ]
        else:
            if mode in crown_utilities.TALE_M:
                buttons = [
                    manage_components.create_button(style=3, label=label_text, custom_id="start"),
                    manage_components.create_button(style=1, label=scenario_text, custom_id="scenario"),
                ]
            if  mode in crown_utilities.DUNGEON_M:
                buttons = [
                    manage_components.create_button(style=3, label=label_text, custom_id="start"),
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
            if mode != "EASY":
                currentopponent = update_save_spot(self, ctx, p.save_spot, selected_universe, crown_utilities.TALE_M)
                if mode in crown_utilities.DUNGEON_M:
                    currentopponent = update_save_spot(self, ctx, p.save_spot, selected_universe, crown_utilities.DUNGEON_M)
            else:
                currentopponent = 0
            if p.rift_on:
                update_team_response = db.updateTeam(p.guild_query, p.guild_buff_update_query)

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
        l = []
        for uni in p.completed_tales:
            if uni != "":
                l.append(uni)
        available_dungeons_list = "\n".join(l)
        available_bosses = p.set_selectable_bosses(ctx, mode)

        if type(available_bosses) is not list:
            await ctx.send(embed=available_bosses)
            return
        
        custom_button = manage_components.create_button(style=3, label="Enter Boss Arena")

        async def custom_function(self, button_ctx):
            if button_ctx.author == ctx.author:
                # if p.boss_fought:

                #     boss_key_embed = discord.Embed(title= f"🗝️  Boss Arena Key Required!", description=textwrap.dedent(f"""
                #     __🗝️  How to get Arena Keys?__
                #     Conquer any Universe Dungeon to gain a Boss Arena Key
                    
                #     ☀️ | You also earn 1 Boss Key per /daily !

                #     __🌍 Available Universe Dungeons__
                #     {available_dungeons_list}
                #     """))
                #     boss_key_embed.set_thumbnail(url=ctx.author.avatar_url)
                #     # embedVar.set_footer(text="Use /tutorial")
                #     await ctx.send(embed=boss_key_embed)
                #     self.stop = True
                #     return    
                await button_ctx.defer(ignore=True)
                selected_universe = custom_function
                custom_function.selected_universe = str(button_ctx.origin_message.embeds[0].title)
                self.stop = True
            else:
                await ctx.send("This is not your button.", hidden=True)
        await Paginator(bot=self.bot, ctx=ctx, useQuitButton=True, deleteAfterTimeout=True, pages=available_bosses, timeout=120,  customButton=[
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
            if selected_universe in p.crestlist:
                await ctx.send(f"{crown_utilities.crest_dict[selected_universe]} | :flags: {p.association} {selected_universe} Crest Activated! No entrance fee!")
            else:
                if p._balance <= entrance_fee:
                    await ctx.send(f"Bosses require an :coin: {'{:,}'.format(entrance_fee)} entrance fee!", delete_after=5)
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
        except asyncio.TimeoutError:
            await ctx.send(f"**{str(ctx.author)}** Boss Arena Timed Out", hidden=True)
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
        


async def battle_commands(self, ctx, battle_config, _player, _custom_explore_card, player2=None, player3=None):
    private_channel = ctx.channel


    try:
        starttime = time.asctime()
        h_gametime = starttime[11:13]
        m_gametime = starttime[14:16]
        s_gametime = starttime[17:19]

        while battle_config.continue_fighting:
            opponent_talisman_emoji = ""
            player1 = _player
            player1.get_battle_ready()
            
            player1_card = Card(player1._equipped_card_data['NAME'], player1._equipped_card_data['PATH'], player1._equipped_card_data['PRICE'], player1._equipped_card_data['EXCLUSIVE'], player1._equipped_card_data['AVAILABLE'], player1._equipped_card_data['IS_SKIN'], player1._equipped_card_data['SKIN_FOR'], player1._equipped_card_data['HLT'], player1._equipped_card_data['HLT'], player1._equipped_card_data['STAM'], player1._equipped_card_data['STAM'], player1._equipped_card_data['MOVESET'], player1._equipped_card_data['ATK'], player1._equipped_card_data['DEF'], player1._equipped_card_data['TYPE'], player1._equipped_card_data['PASS'][0], player1._equipped_card_data['SPD'], player1._equipped_card_data['UNIVERSE'], player1._equipped_card_data['HAS_COLLECTION'], player1._equipped_card_data['TIER'], player1._equipped_card_data['COLLECTION'], player1._equipped_card_data['WEAKNESS'], player1._equipped_card_data['RESISTANT'], player1._equipped_card_data['REPEL'], player1._equipped_card_data['ABSORB'], player1._equipped_card_data['IMMUNE'], player1._equipped_card_data['GIF'], player1._equipped_card_data['FPATH'], player1._equipped_card_data['RNAME'], player1._equipped_card_data['RPATH'], battle_config._ai_is_boss)
            player1_title = Title(player1._equipped_title_data['TITLE'], player1._equipped_title_data['UNIVERSE'], player1._equipped_title_data['PRICE'], player1._equipped_title_data['EXCLUSIVE'], player1._equipped_title_data['AVAILABLE'], player1._equipped_title_data['ABILITIES'])            
            player1_arm = Arm(player1._equipped_arm_data['ARM'], player1._equipped_arm_data['UNIVERSE'], player1._equipped_arm_data['PRICE'], player1._equipped_arm_data['ABILITIES'], player1._equipped_arm_data['EXCLUSIVE'], player1._equipped_arm_data['AVAILABLE'], player1._equipped_arm_data['ELEMENT'])
            
            player1.getsummon_ready(player1_card)
            player1_arm.set_durability(player1.equipped_arm, player1._arms)
            player1_card.set_card_level_buffs(player1._card_levels)

            player1_card.set_arm_config(player1_arm.passive_type, player1_arm.name, player1_arm.passive_value, player1_arm.element)
            player1_card.set_affinity_message()
            player1.get_talisman_ready(player1_card)

            if battle_config.mode in crown_utilities.PVP_M:
                player2 = player2
                player2.get_battle_ready()
                player2_card = Card(player2._equipped_card_data['NAME'], player2._equipped_card_data['PATH'], player2._equipped_card_data['PRICE'], player2._equipped_card_data['EXCLUSIVE'], player2._equipped_card_data['AVAILABLE'], player2._equipped_card_data['IS_SKIN'], player2._equipped_card_data['SKIN_FOR'], player2._equipped_card_data['HLT'], player2._equipped_card_data['HLT'], player2._equipped_card_data['STAM'], player2._equipped_card_data['STAM'], player2._equipped_card_data['MOVESET'], player2._equipped_card_data['ATK'], player2._equipped_card_data['DEF'], player2._equipped_card_data['TYPE'], player2._equipped_card_data['PASS'][0], player2._equipped_card_data['SPD'], player2._equipped_card_data['UNIVERSE'], player2._equipped_card_data['HAS_COLLECTION'], player2._equipped_card_data['TIER'], player2._equipped_card_data['COLLECTION'], player2._equipped_card_data['WEAKNESS'], player2._equipped_card_data['RESISTANT'], player2._equipped_card_data['REPEL'], player2._equipped_card_data['ABSORB'], player2._equipped_card_data['IMMUNE'], player2._equipped_card_data['GIF'], player2._equipped_card_data['FPATH'], player2._equipped_card_data['RNAME'], player2._equipped_card_data['RPATH'], battle_config._ai_is_boss)
                player2_title = Title(player2._equipped_title_data['TITLE'], player2._equipped_title_data['UNIVERSE'], player2._equipped_title_data['PRICE'], player2._equipped_title_data['EXCLUSIVE'], player2._equipped_title_data['AVAILABLE'], player2._equipped_title_data['ABILITIES'])            
                player2_arm = Arm(player2._equipped_arm_data['ARM'], player2._equipped_arm_data['UNIVERSE'], player2._equipped_arm_data['PRICE'], player2._equipped_arm_data['ABILITIES'], player2._equipped_arm_data['EXCLUSIVE'], player2._equipped_arm_data['AVAILABLE'], player2._equipped_arm_data['ELEMENT'])
                opponent_talisman_emoji = crown_utilities.set_emoji(player2.equipped_talisman)

                
                player2.getsummon_ready(player2_card)
                player2_arm.set_durability(player2.equipped_arm, player2._arms)
                player2_card.set_card_level_buffs(player2._card_levels)
                player2_card.set_arm_config(player2_arm.passive_type, player2_arm.name, player2_arm.passive_value, player2_arm.element)
                player2_card.set_solo_leveling_config(player1_card._shield_active, player1_card._shield_value, player1_card._barrier_active, player1_card._barrier_value, player1_card._parry_active, player1_card._parry_value)
                player2_card.set_affinity_message()
                player2.get_talisman_ready(player2_card)
                player1_card.set_solo_leveling_config(player2_card._shield_active, player2_card._shield_value, player2_card._barrier_active, player2_card._barrier_value, player2_card._parry_active, player2_card._parry_value)
            
            if battle_config.mode in crown_utilities.RAID_M:
                player2 = player2
                player2.get_battle_ready()
                player2_card = Card(player2._equipped_card_data['NAME'], player2._equipped_card_data['PATH'], player2._equipped_card_data['PRICE'], player2._equipped_card_data['EXCLUSIVE'], player2._equipped_card_data['AVAILABLE'], player2._equipped_card_data['IS_SKIN'], player2._equipped_card_data['SKIN_FOR'], player2._equipped_card_data['HLT'], player2._equipped_card_data['HLT'], player2._equipped_card_data['STAM'], player2._equipped_card_data['STAM'], player2._equipped_card_data['MOVESET'], player2._equipped_card_data['ATK'], player2._equipped_card_data['DEF'], player2._equipped_card_data['TYPE'], player2._equipped_card_data['PASS'][0], player2._equipped_card_data['SPD'], player2._equipped_card_data['UNIVERSE'], player2._equipped_card_data['HAS_COLLECTION'], player2._equipped_card_data['TIER'], player2._equipped_card_data['COLLECTION'], player2._equipped_card_data['WEAKNESS'], player2._equipped_card_data['RESISTANT'], player2._equipped_card_data['REPEL'], player2._equipped_card_data['ABSORB'], player2._equipped_card_data['IMMUNE'], player2._equipped_card_data['GIF'], player2._equipped_card_data['FPATH'], player2._equipped_card_data['RNAME'], player2._equipped_card_data['RPATH'], battle_config._ai_is_boss)
                player2_title = Title(player2._equipped_title_data['TITLE'], player2._equipped_title_data['UNIVERSE'], player2._equipped_title_data['PRICE'], player2._equipped_title_data['EXCLUSIVE'], player2._equipped_title_data['AVAILABLE'], player2._equipped_title_data['ABILITIES'])            
                player2_arm = Arm(player2._equipped_arm_data['ARM'], player2._equipped_arm_data['UNIVERSE'], player2._equipped_arm_data['PRICE'], player2._equipped_arm_data['ABILITIES'], player2._equipped_arm_data['EXCLUSIVE'], player2._equipped_arm_data['AVAILABLE'], player2._equipped_arm_data['ELEMENT'])
                opponent_talisman_emoji = crown_utilities.set_emoji(player2.equipped_talisman)

                
                player2.getsummon_ready(player2_card)
                player2_arm.set_durability(player2.equipped_arm, player2._arms)
                player2_card.set_card_level_buffs(player2._card_levels)
                player2_card.set_arm_config(player2_arm.passive_type, player2_arm.name, player2_arm.passive_value, player2_arm.element)
                player2_card.set_solo_leveling_config(player1_card._shield_active, player1_card._shield_value, player1_card._barrier_active, player1_card._barrier_value, player1_card._parry_active, player1_card._parry_value)
                player2_card.set_affinity_message()
                player2_card.set_raid_defense_buff(battle_config._hall_defense)
                player2.get_talisman_ready(player2_card)
                player1_card.set_solo_leveling_config(player2_card._shield_active, player2_card._shield_value, player2_card._barrier_active, player2_card._barrier_value, player2_card._parry_active, player2_card._parry_value)

            if battle_config.mode in crown_utilities.CO_OP_M or battle_config.is_duo_mode:
                player3.get_battle_ready()
                player3_card = Card(player3._equipped_card_data['NAME'], player3._equipped_card_data['PATH'], player3._equipped_card_data['PRICE'], player3._equipped_card_data['EXCLUSIVE'], player3._equipped_card_data['AVAILABLE'], player3._equipped_card_data['IS_SKIN'], player3._equipped_card_data['SKIN_FOR'], player3._equipped_card_data['HLT'], player3._equipped_card_data['HLT'], player3._equipped_card_data['STAM'], player3._equipped_card_data['STAM'], player3._equipped_card_data['MOVESET'], player3._equipped_card_data['ATK'], player3._equipped_card_data['DEF'], player3._equipped_card_data['TYPE'], player3._equipped_card_data['PASS'][0], player3._equipped_card_data['SPD'], player3._equipped_card_data['UNIVERSE'], player3._equipped_card_data['HAS_COLLECTION'], player3._equipped_card_data['TIER'], player3._equipped_card_data['COLLECTION'], player3._equipped_card_data['WEAKNESS'], player3._equipped_card_data['RESISTANT'], player3._equipped_card_data['REPEL'], player3._equipped_card_data['ABSORB'], player3._equipped_card_data['IMMUNE'], player3._equipped_card_data['GIF'], player3._equipped_card_data['FPATH'], player3._equipped_card_data['RNAME'], player3._equipped_card_data['RPATH'], battle_config._ai_is_boss)
                player3_title = Title(player3._equipped_title_data['TITLE'], player3._equipped_title_data['UNIVERSE'], player3._equipped_title_data['PRICE'], player3._equipped_title_data['EXCLUSIVE'], player3._equipped_title_data['AVAILABLE'], player3._equipped_title_data['ABILITIES'])            
                player3_arm = Arm(player3._equipped_arm_data['ARM'], player3._equipped_arm_data['UNIVERSE'], player3._equipped_arm_data['PRICE'], player3._equipped_arm_data['ABILITIES'], player3._equipped_arm_data['EXCLUSIVE'], player3._equipped_arm_data['AVAILABLE'], player3._equipped_arm_data['ELEMENT'])
                player3_talisman_emoji = crown_utilities.set_emoji(player3.equipped_talisman)
                
                player3.getsummon_ready(player3_card)
                player3_arm.set_durability(player3.equipped_arm, player3._arms)
                player3_card.set_card_level_buffs(player3._card_levels)
                player3_card.set_arm_config(player3_arm.passive_type, player3_arm.name, player3_arm.passive_value, player3_arm.element)
                player3_card.set_solo_leveling_config(player1_card._shield_active, player1_card._shield_value, player1_card._barrier_active, player1_card._barrier_value, player1_card._parry_active, player1_card._parry_value)
                player3_card.set_affinity_message()
                player3.get_talisman_ready(player3_card)
            
            if battle_config.is_ai_opponent and not battle_config.is_raid_game_mode:
                if battle_config.is_scenario_game_mode:
                    battle_config.is_tales_game_mode = False
                if battle_config.is_explore_game_mode:
                    player2_card = _custom_explore_card
                else:
                    battle_config.get_ai_battle_ready(player1_card.card_lvl)
                    player2_card = Card(battle_config._ai_opponent_card_data['NAME'], battle_config._ai_opponent_card_data['PATH'], battle_config._ai_opponent_card_data['PRICE'], battle_config._ai_opponent_card_data['EXCLUSIVE'], battle_config._ai_opponent_card_data['AVAILABLE'], battle_config._ai_opponent_card_data['IS_SKIN'], battle_config._ai_opponent_card_data['SKIN_FOR'], battle_config._ai_opponent_card_data['HLT'], battle_config._ai_opponent_card_data['HLT'], battle_config._ai_opponent_card_data['STAM'], battle_config._ai_opponent_card_data['STAM'], battle_config._ai_opponent_card_data['MOVESET'], battle_config._ai_opponent_card_data['ATK'], battle_config._ai_opponent_card_data['DEF'], battle_config._ai_opponent_card_data['TYPE'], battle_config._ai_opponent_card_data['PASS'][0], battle_config._ai_opponent_card_data['SPD'], battle_config._ai_opponent_card_data['UNIVERSE'], battle_config._ai_opponent_card_data['HAS_COLLECTION'], battle_config._ai_opponent_card_data['TIER'], battle_config._ai_opponent_card_data['COLLECTION'], battle_config._ai_opponent_card_data['WEAKNESS'], battle_config._ai_opponent_card_data['RESISTANT'], battle_config._ai_opponent_card_data['REPEL'], battle_config._ai_opponent_card_data['ABSORB'], battle_config._ai_opponent_card_data['IMMUNE'], battle_config._ai_opponent_card_data['GIF'], battle_config._ai_opponent_card_data['FPATH'], battle_config._ai_opponent_card_data['RNAME'], battle_config._ai_opponent_card_data['RPATH'], battle_config._ai_is_boss)
                    player2_card.set_ai_card_buffs(battle_config._ai_opponent_card_lvl, battle_config.stat_buff, battle_config.stat_debuff, battle_config.health_buff, battle_config.health_debuff, battle_config.ap_buff, battle_config.ap_debuff, _player.prestige, _player.rebirth, battle_config.mode)
                if battle_config.abyss_player_card_tier_is_banned:
                    await ctx.send(f"Tier {str(player1_card.tier)} cards are banned on Floor {str(battle_config.abyss_floor)} of the abyss. Please try again with another card.")
                    return
                if not any((battle_config.is_abyss_game_mode, battle_config.is_explore_game_mode, battle_config.is_scenario_game_mode)):
                    battle_config.set_corruption_config()
                player2_title = Title(battle_config._ai_opponent_title_data['TITLE'], battle_config._ai_opponent_title_data['UNIVERSE'], battle_config._ai_opponent_title_data['PRICE'], battle_config._ai_opponent_title_data['EXCLUSIVE'], battle_config._ai_opponent_title_data['AVAILABLE'], battle_config._ai_opponent_title_data['ABILITIES'])            
                player2_arm = Arm(battle_config._ai_opponent_arm_data['ARM'], battle_config._ai_opponent_arm_data['UNIVERSE'], battle_config._ai_opponent_arm_data['PRICE'], battle_config._ai_opponent_arm_data['ABILITIES'], battle_config._ai_opponent_arm_data['EXCLUSIVE'], battle_config._ai_opponent_arm_data['AVAILABLE'], battle_config._ai_opponent_arm_data['ELEMENT'])
                player2_card.set_talisman(battle_config)
                opponent_talisman_emoji = ""
                player2_card.set_arm_config(player2_arm.passive_type, player2_arm.name, player2_arm.passive_value, player2_arm.element)
                player2_card.set_affinity_message()
                player2_card.set_solo_leveling_config(player1_card._shield_active, player1_card._shield_value, player1_card._barrier_active, player1_card._barrier_value, player1_card._parry_active, player1_card._parry_value)
                player1_card.set_solo_leveling_config(player2_card._shield_active, player2_card._shield_value, player2_card._barrier_active, player2_card._barrier_value, player2_card._parry_active, player2_card._parry_value)
                battle_config.get_aisummon_ready(player2_card)
                player2_card.get_boss_tactics(battle_config)

                if battle_config.mode in crown_utilities.CO_OP_M:
                    player2_card.set_solo_leveling_config(player3_card._shield_active, player3_card._shield_value, player3_card._barrier_active, player3_card._barrier_value, player3_card._parry_active, player3_card._parry_value)
            
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

            if battle_config.can_auto_battle and not battle_config.is_co_op_mode and not battle_config.is_duo_mode:
                start_tales_buttons.append(
                    manage_components.create_button(
                        style=ButtonStyle.grey,
                        label="Auto Battle",
                        custom_id="start_auto_tales"
                    )

                )
            
            if not battle_config.is_tutorial_game_mode and battle_config.save_match_turned_on():
                if battle_config.current_opponent_number > 0:
                    start_tales_buttons.append(
                        manage_components.create_button(
                            style=ButtonStyle.green,
                            label="Save Game",
                            custom_id="save_tales_yes"
                        )
                    )

            start_tales_buttons_action_row = manage_components.create_actionrow(*start_tales_buttons)          
            
            battle_config.set_who_starts_match(player1_card.speed, player2_card.speed, battle_config.mode)
            user1 = await main.bot.fetch_user(player1.did)

            opponent_card = player2_card
            opponent_arm = player2_arm
            opponent_title = player2_title
            if battle_config.is_pvp_game_mode:
                user2 = await main.bot.fetch_user(player2.did)
                opponent_ping = user2.mention
            elif battle_config.is_co_op_mode:
                user2 = await main.bot.fetch_user(player3.did)
                opponent_ping = user2.mention
            else:
                opponent_ping = "..."

            if battle_config.is_co_op_mode or battle_config.is_duo_mode:
                title_lvl_msg = f"{battle_config.set_levels_message(player1_card, player2_card, player3_card)}"
            else:
                title_lvl_msg = f"{battle_config.set_levels_message(player1_card, player2_card)}"

            # if battle_config.is_pvp_game_mode and not battle_config.is_tutorial_game_mode:
            #     battle_ping_message = await private_channel.send(f"{user1.mention} 🆚 {opponent_ping} ")

            embed = discord.Embed(title=f"{battle_config.get_starting_match_title()}\n{title_lvl_msg}")
            embed.add_field(name=f"__Your Affinities:__", value=f"{player1_card.affinity_message}")
            if battle_config.is_co_op_mode or battle_config.is_duo_mode:
                embed.add_field(name=f"__Companion Affinities:__", value=f"{player3_card.affinity_message}")
            embed.add_field(name=f"__Opponent Affinities:__", value=f"{opponent_card.affinity_message}")
            embed.set_image(url="attachment://image.png")
            if battle_config.is_pvp_game_mode:
                embed.set_thumbnail(url=user2.avatar_url)
            else:
                embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text="🩸 card passives and 🎗️ titles are applied every turn or Focus.")

            battle_msg = await private_channel.send(
                content=f"{ctx.author.mention} 🆚 {opponent_ping}",
                embed=embed,
                components=[start_tales_buttons_action_row],
                file=opponent_card.showcard(battle_config.mode, opponent_arm, opponent_title, battle_config.turn_total, player1_card.defense)
            )
                 
            def check(button_ctx):
                if battle_config.is_pvp_game_mode:
                    if battle_config.is_tutorial_game_mode:
                        return button_ctx.author == ctx.author
                    else:
                        return button_ctx.author == player2.did
                elif battle_config.is_co_op_mode:
                    return button_ctx.author == ctx.author
                else:
                    return button_ctx.author == ctx.author

            try:
                button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[
                            start_tales_buttons_action_row], timeout=300, check=check)

                if button_ctx.custom_id == "start_tales_no":
                    #await button_ctx.defer()
                    await battle_msg.delete()
                    if player1.autosave and battle_config.match_can_be_saved:
                        await button_ctx.send(embed = battle_config.saved_game_embed(player1_card, player2_card))
                    elif not battle_config.is_pvp_game_mode:
                        await button_ctx.send(embed = battle_config.close_pve_embed(player1_card, player2_card))
                    else:
                        await button_ctx.send(embed = battle_config.close_pvp_embed(player1, player2))
                    return

                if button_ctx.custom_id == "save_tales_yes":
                    await button_ctx.defer()
                    await battle_msg.edit(components=[])
                    await save_spot(self, player1.did, battle_config.selected_universe, battle_config.mode, battle_config.current_opponent_number)
                    await button_ctx.send(embed = battle_config.saved_game_embed(player1_card, player2_card))
                    return
                
                if button_ctx.custom_id == "start_tales_yes" or button_ctx.custom_id == "start_auto_tales":
                    if battle_config.match_can_be_saved and player1.autosave == True:
                        await save_spot(self, player1.did, battle_config.selected_universe, battle_config.mode, battle_config.current_opponent_number)
                    if button_ctx.custom_id == "start_auto_tales":
                        await button_ctx.defer()
                        battle_config.is_auto_battle_game_mode = True
                        embedVar = discord.Embed(title=f"Auto Battle has started", color=0xe74c3c)
                        embedVar.set_thumbnail(url=ctx.author.avatar_url)
                        await battle_msg.delete(delay=2)
                        await asyncio.sleep(2)
                        battle_msg = await private_channel.send(embed=embedVar)

                    tactics_set_base_stats(player2_card)
                    game_over_check = False
                    battle_config.turn_total = 50
                    player2_card.health = 1000
                    while not game_over_check:
                        if battle_config.is_duo_mode or battle_config.is_co_op_mode:
                            game_over_check = battle_config.set_game_over(player1_card, player2_card, player3_card)
                        else:
                            game_over_check = battle_config.set_game_over(player1_card, player2_card, None)
                        if game_over_check:
                            break

                        if battle_config.previous_moves:
                            battle_config.previous_moves_len = len(battle_config.previous_moves)
                            if battle_config.previous_moves_len >= player1.battle_history:
                                battle_config.previous_moves = battle_config.previous_moves[-player1.battle_history:]

                        if battle_config.is_co_op_mode:
                            pre_turn_zero = beginning_of_turn_stat_trait_affects(player1_card, player1_title, player2_card, battle_config, player3_card)
                        else:
                            pre_turn_zero = beginning_of_turn_stat_trait_affects(player1_card, player1_title, player2_card, battle_config)
                        
                        tactics_petrified_fear_check(player2_card, player1_card, battle_config)
                        tactics_bloodlust_check(player2_card, battle_config)
                        tactics_enrage_check(player2_card, battle_config)
                        tactics_damage_check(player2_card, battle_config)
                        tactics_stagger_check(player2_card, player1_card, battle_config)
                        tactics_almighty_will_check(player2_card, battle_config)
                        tactics_death_blow_check(player2_card, player1_card, battle_config)
                        tactics_intimidation_check(player2_card, player1_card, battle_config)
                        if battle_config.is_turn == 0:
                            if player1_card.health == 0:
                                continue
                            player1_card.set_deathnote_message(battle_config)
                            player2_card.set_deathnote_message(battle_config)
                            if battle_config.is_co_op_mode:
                                player3_card.set_deathnote_message(battle_config)                            

                            if battle_config.turn_total == 0:
                                if battle_config.is_tutorial_game_mode:
                                    embedVar = discord.Embed(title=f"Welcome to **Anime VS+**!",
                                                            description=f"Follow the instructions to learn how to play the Game!",
                                                            colour=0xe91e63)
                                    embedVar.add_field(name="**Moveset**",value=f"{player1_card.move1_emoji} - **Basic Attack** *10 :zap:ST*\n{player1_card.move2_emoji} - **Special Attack** *30 :zap:ST*\n{player1_card.move3_emoji} - **Ultimate Move** *80 :zap:ST*\n🦠 - **Enhancer** *20 :zap:ST*\n🛡️ - **Block** *20 :zap:ST*\n:zap: - **Resolve** : Heal and Activate Resolve\n:dna: - **Summon** : {player1.equippedsummon}")
                                    embedVar.set_footer(text="Focus State : When Stamina = 0, You will focus to Heal and gain ATK and DEF ")
                                    await private_channel.send(embed=embedVar)
                                    await asyncio.sleep(2)

                                
                            if player1_card.stamina < 10:
                                player1_card.focusing(player1_title, player2_title, player2_card, battle_config)
                                
                                if battle_config.is_tutorial_game_mode and not battle_config.tutorial_focus:
                                    await private_channel.send(embed=battle_config._tutorial_message)
                                    battle_config.tutorial_focus = True
                                    await asyncio.sleep(2)

                                if battle_config.is_boss_game_mode:
                                    await private_channel.send(embed=battle_config._boss_embed_message)
                                
                                #continue 
                            else:
                                if battle_config.is_auto_battle_game_mode:                                    
                                    embedVar = await auto_battle_embed_and_starting_traits(ctx, player1_card, player2_card, battle_config, None)
                                    if battle_msg is None:
                                        # If the message does not exist, send a new message
                                        battle_msg = await private_channel.send(embed=embedVar, components=[])
                                    else:
                                        # If the message exists, edit it
                                        await battle_msg.edit(embed=embedVar, components=[])

                                    selected_move = battle_config.ai_battle_command(player1_card, player2_card)

                                    if selected_move in [1, 2, 3, 4, 7]:
                                        damage_calculation_response = player1_card.damage_cal(selected_move, battle_config, player2_card)
                                        if selected_move != 7:
                                            player1_card.damage_done(battle_config, damage_calculation_response, player2_card)

                                    if selected_move == 5:
                                        player1_card.resolving(battle_config, player2_card, player1)
                                        if battle_config.is_boss_game_mode:
                                            await button_ctx.send(embed=battle_config._boss_embed_message)

                                    elif selected_move == 6:
                                        player1_card.usesummon(battle_config, player2_card)

                                    elif selected_move == 0:
                                        player1_card.use_block(battle_config, damage_calculation_response, player2_card)                                
                                
                                else:
                                    player1_card.set_battle_arm_messages(player2_card)
                                    player1_card.set_stat_icons()

                                    player1_card.activate_solo_leveling_trait(battle_config, player2_card)
                                    if battle_config.is_co_op_mode:
                                        battle_config.set_battle_options(player1_card, player2_card,player3_card)
                                    else:
                                        battle_config.set_battle_options(player1_card, player2_card)

                                    battle_action_row = manage_components.create_actionrow(*battle_config.battle_buttons)
                                    util_action_row = manage_components.create_actionrow(*battle_config.utility_buttons)
                                    
                                    if battle_config.is_co_op_mode:
                                        player3_card.set_battle_arm_messages(player2_card)
                                        player3_card.set_stat_icons()
                                        if player1_card.stamina >= 20:
                                            coop_util_action_row = manage_components.create_actionrow(*battle_config.co_op_buttons)
                                            components = [battle_action_row, coop_util_action_row, util_action_row]
                                        else:
                                            components = [battle_action_row, util_action_row]
                                        companion_stats = f"\n{player3_card.name}: ❤️{round(player3_card.health)} 🌀{round(player3_card.stamina)} 🗡️{round(player3_card.attack)}/🛡️{round(player3_card.defense)} {player3_card._arm_message}"

                                    else:
                                        components = [battle_action_row, util_action_row]

                                    player1_card.set_battle_arm_messages(player2_card)
                                    player1_card.set_stat_icons()

                                    if battle_config.is_duo_mode or battle_config.is_co_op_mode:
                                        footer_text = battle_config.get_battle_footer_text(player2_card, player1_card, player3_card)
                                    else:
                                        footer_text = battle_config.get_battle_footer_text(player2_card, player1_card)
                                    embedVar = discord.Embed(title=f"", description=textwrap.dedent(f"""\
                                    {battle_config.get_previous_moves_embed()}
                                    
                                    """), color=0xe74c3c)
                                    embedVar.set_author(name=f"{player1_card._arm_message}\n{player1_card.summon_resolve_message}\n")
                                    if player1.performance:
                                        embedVar.add_field(name=f"➡️ **Current Turn** {battle_config.turn_total}", value=f"{ctx.author.mention} Select move below!\n{player1_card.get_performance_stats()}\n{player1_title.get_title_icon(player1_card.universe)} | {player1_title.passive_type} {player1_title.passive_value}")
                                    else:
                                        embedVar.add_field(name=f"➡️ **Current Turn** {battle_config.turn_total}", value=f"{ctx.author.mention} Select move below!")
                                    # await asyncio.sleep(2)
                                    embedVar.set_image(url="attachment://image.png")
                                    embedVar.set_thumbnail(url=ctx.author.avatar_url)
                                    embedVar.set_footer(
                                        text=f"{footer_text}",
                                        icon_url="https://cdn.discordapp.com/emojis/789290881654980659.gif?v=1")
  
                                    await battle_msg.delete(delay=2)
                                    await asyncio.sleep(2)
                                    if player1.performance:
                                        embedVar.add_field(name=f":sunny: | **Move Set**", value=f"{player1_card.resolve_icon} | {player1_card.stamina} *Stamina*\n{player1_card.move1_emoji} | {player1_card.move1ap} *-10 ST {player1_card.resolve_icon}*\n{player3_card.move2_emoji} | {player1_card.move2ap} *-30 ST {player1_card.resolve_icon}*\n{player1_card.move3_emoji} | {player1_card.move3ap} *-80 ST {player1_card.resolve_icon}*\n:microbe: | {player1_card.move4enh} {player1_card.move4ap} *-20 ST {player1_card.resolve_icon}*")
                                        battle_msg = await private_channel.send(embed=embedVar, components=components)
                                    else:
                                        battle_msg = await private_channel.send(embed=embedVar, components=components, file=player1_card.showcard(battle_config.mode, player1_arm, player1_title, battle_config.turn_total, player2_card.defense))

                                    # Make sure user is responding with move
                                    def check(button_ctx):
                                        return button_ctx.author == user1 and button_ctx.custom_id in battle_config.battle_options

                                    try:
                                        button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot,
                                                                                                                components=components,
                                                                                                                timeout=300,
                                                                                                                check=check)
                                        

                                        if button_ctx.custom_id == "s":
                                            try:
                                                player1_card.health = 0
                                                battle_config.game_over = True
                                                await save_spot(self, player1.did, battle_config.selected_universe, battle_config.mode, battle_config.current_opponent_number)
                                                await battle_msg.delete(delay=1)
                                                await asyncio.sleep(1)
                                                if battle_config.is_co_op_mode:
                                                    battle_msg = await private_channel.send(embed=battle_config.saved_game_embed(player1_card,player2_card, player3_card))
                                                else:
                                                    battle_msg = await private_channel.send(embed=battle_config.saved_game_embed(player1_card,player2_card))
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
                                            if battle_config.is_co_op_mode:
                                                battle_config.use_boost(battle_config, player3_card)
                                            else:
                                                battle_config.use_boost(battle_config)
                                        
                                        if button_ctx.custom_id == "q" or button_ctx.custom_id == "Q":
                                            player1_card.health = 0
                                            battle_config.game_over = True
                                            battle_config.add_battle_history_message(f"(**{battle_config.turn_total}**) 💨 **{player1_card.name}** Fled...")
                                            await battle_msg.delete(delay=1)
                                            await asyncio.sleep(1)
                                            battle_msg = await private_channel.send(content=f"{ctx.author.mention} has fled.")
                                        
                                        if button_ctx.custom_id == "1":
                                            if battle_config.is_tutorial_game_mode and battle_config.tutorial_basic == False:
                                                battle_config.tutorial_basic =True
                                                embedVar = discord.Embed(title=f":boom:Basic Attack!",
                                                                        description=f":boom:**Basic Attack** cost **10 ST(Stamina)** to deal decent Damage!",
                                                                        colour=0xe91e63)
                                                embedVar.add_field(
                                                    name=f"Your Basic Attack: {player1_card.move1_emoji} {player1_card.move1} inflicts {player1_card.move1_element}",
                                                    value=f"**{player1_card.move1_element}** : *{element_mapping[player1_card.move1_element]}*")
                                                embedVar.set_footer(
                                                    text=f"Basic Attacks are great when you are low on stamina. Enter Focus State to Replenish!")
                                                await private_channel.send(embed=embedVar, components=[])
                                                await asyncio.sleep(2)

                                            damage_calculation_response = player1_card.damage_cal(int(button_ctx.custom_id), battle_config, player2_card)
                                        
                                        elif button_ctx.custom_id == "2":
                                            if battle_config.is_tutorial_game_mode and battle_config.tutorial_special==False:
                                                battle_config.tutorial_special = True
                                                embedVar = discord.Embed(title=f":comet:Special Attack!",
                                                                        description=f":comet:**Special Attack** cost **30 ST(Stamina)** to deal great Damage!",
                                                                        colour=0xe91e63)
                                                embedVar.add_field(
                                                    name=f"Your Special Attack: {player1_card.move2_emoji} {player1_card.move2} inflicts {player1_card.move2_element}",
                                                    value=f"**{player1_card.move2_element}** : *{element_mapping[player1_card.move2_element]}*")
                                                embedVar.set_footer(
                                                    text=f"Special Attacks are great when you need to control the Focus game! Use Them to Maximize your Focus and build stronger Combos!")
                                                await private_channel.send(embed=embedVar)
                                                await asyncio.sleep(2)
                                            
                                            damage_calculation_response = player1_card.damage_cal(int(button_ctx.custom_id), battle_config, player2_card)
                                        
                                        elif button_ctx.custom_id == "3":
                                            if battle_config.is_tutorial_game_mode and battle_config.tutorial_ultimate==False:
                                                battle_config.tutorial_ultimate=True
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
                                                await private_channel.send(embed=embedVar)
                                                await asyncio.sleep(2)
                                           
                                            damage_calculation_response = player1_card.damage_cal(int(button_ctx.custom_id), battle_config, player2_card)
                                            if player1_card.gif != "N/A" and not player1.performance:
                                                # await button_ctx.defer(ignore=True)
                                                await battle_msg.delete(delay=None)
                                                # await asyncio.sleep(1)
                                                battle_msg = await private_channel.send(f"{player1_card.gif}")
                                                
                                                await asyncio.sleep(2)
                                        
                                        elif button_ctx.custom_id == "4":
                                            if battle_config.is_tutorial_game_mode and battle_config.tutorial_enhancer==False:
                                                battle_config.tutorial_enhancer = True
                                                embedVar = discord.Embed(title=f"🦠Enhancers!",
                                                                        description=f"🦠**Enhancers** cost **20 ST(Stamina)** to Boost your Card or Debuff Your Opponent!",
                                                                        colour=0xe91e63)
                                                embedVar.add_field(
                                                    name=f"Your Enhancer:🦠 {player1_card.move4} is a {player1_card.move4enh}",
                                                    value=f"**{player1_card.move4enh}** : *{enhancer_mapping[player1_card.move4enh]}*")
                                                embedVar.set_footer(
                                                    text=f"Use /enhancers to view a full list of Enhancers! Look for the {player1_card.move4enh} Enhancer")
                                                await private_channel.send(embed=embedVar)
                                                await asyncio.sleep(2)

                                            damage_calculation_response = player1_card.damage_cal(int(button_ctx.custom_id), battle_config, player2_card)

                                        elif button_ctx.custom_id == "5":
                                            # Resolve Check and Calculation
                                            if not player1_card.used_resolve and player1_card.used_focus:
                                                if battle_config.is_tutorial_game_mode and battle_config.tutorial_resolve == False:
                                                    battle_config.tutorial_resolve = True
                                                    embedVar = discord.Embed(title=f"⚡**Resolve Transformation**!",
                                                                            description=f"**Heal**, Boost **ATK**, and 🧬**Summon**!",
                                                                            colour=0xe91e63)
                                                    embedVar.add_field(name=f"Trade Offs!",
                                                                    value="Sacrifice **DEF** and **Focusing** will not increase **ATK** or **DEF**")
                                                    embedVar.add_field(name=f"🧬Your Summon",
                                                                    value=f"**{player1_card.summon_name}**")
                                                    embedVar.set_footer(
                                                        text=f"You can only enter ⚡Resolve once per match! Use the Heal Wisely!!!")
                                                    await private_channel.send(embed=embedVar)
                                                    await asyncio.sleep(2)

                                                player1_card.resolving(battle_config, player2_card, player1)
                                                if battle_config.is_boss_game_mode:
                                                    await button_ctx.send(embed=battle_config._boss_embed_message)
                                            else:
                                                emessage = m.CANNOT_USE_RESOLVE
                                                embedVar = discord.Embed(title=emessage, colour=0xe91e63)
                                                battle_config.add_battle_history_message(f"(**{battle_config.turn_total}**) **{player1_card.name}** cannot resolve")
                                                await private_channel.defer(ignore=True)
                                                battle_config.is_turn = battle_config._repeat_turn()
                                        
                                        elif button_ctx.custom_id == "6":
                                            # Resolve Check and Calculation
                                            if player1_card.used_resolve and player1_card.used_focus and not player1_card.usedsummon:
                                                if battle_config.is_tutorial_game_mode and battle_config.tutorialsummon == False:
                                                    battle_config.tutorialsummon = True
                                                    embedVar = discord.Embed(title=f"{player1_card.name} Summoned 🧬 **{player1_card.summon_name}**",colour=0xe91e63)
                                                    embedVar.add_field(name=f"🧬**Summon Enhancers**!",
                                                                    value="You can use 🧬**Summons** once per Focus without losing a turn!")
                                                    embedVar.add_field(name=f"Resting",
                                                                    value="🧬**Summons** need to rest after using their ability! **Focus** to Replenish your 🧬**Summon**")
                                                    embedVar.set_footer(
                                                        text=f"🧬Summons will Level Up and build Bond as you win battles! Train up your 🧬summons to perform better in the field!")
                                                    await private_channel.send(embed=embedVar)
                                                    await asyncio.sleep(2)
                                            summon_response = player1_card.usesummon(battle_config, player2_card)
                                            
                                            if not player1.performance and summon_response['CAN_USE_MOVE']:
                                                await battle_msg.delete(delay=2)
                                                tsummon_file = showsummon(player1_card.summon_image, player1_card.summon_name, summon_response['MESSAGE'], player1_card.summon_lvl, player1_card.summon_bond)
                                                embedVar.set_image(url="attachment://pet.png")
                                                await asyncio.sleep(2)
                                                battle_msg = await private_channel.send(embed=embedVar, file=tsummon_file)
                                                await asyncio.sleep(2)
                                                await battle_msg.delete(delay=2)

                                        elif battle_config.is_co_op_mode:
                                            if button_ctx.custom_id == "7":
                                                player1_card.use_companion_enhancer(battle_config, player2_card, player3_card)
                                            
                                            elif button_ctx.custom_id == "8":
                                                # Use companion enhancer on you
                                                player3_card.use_companion_enhancer(battle_config, player2_card, player1_card)

                                            elif button_ctx.custom_id == "9":
                                                player3_card.use_block(battle_config, player2_card, player1_card)

                                        if button_ctx.custom_id == "0":
                                            if battle_config.is_tutorial_game_mode and battle_config.tutorial_block==False:
                                                battle_config.tutorial_block=True
                                                embedVar = discord.Embed(title=f"🛡️Blocking!",
                                                                        description=f"🛡️**Blocking** cost **20 ST(Stamina)** to Double your **DEF** until your next turn!",
                                                                        colour=0xe91e63)
                                                embedVar.add_field(name=f"**Engagements**",
                                                                value="You will take less DMG when your **DEF** is greater than your opponenents **ATK**")
                                                embedVar.add_field(name=f"**Engagement Insight**",
                                                                value="💢: %33-%50 of AP\n❕: %50-%75 AP\n‼️: %75-%120 AP\n〽️x1.5: %120-%150 AP\n❌x2: $150-%200 AP")
                                                embedVar.set_footer(
                                                    text=f"Use 🛡️Block strategically to defend against your opponents strongest abilities!")
                                                await private_channel.send(embed=embedVar)
                                                await asyncio.sleep(2)
                                            if battle_config.is_co_op_mode:
                                                player1_card.use_block(battle_config, player2_card, player3_card)  
                                            else:
                                                player1_card.use_block(battle_config, player2_card)                                            

                                        if button_ctx.custom_id in battle_config.main_battle_options:
                                            player1_card.damage_done(battle_config, damage_calculation_response, player2_card)
                                    
                                    except asyncio.TimeoutError:
                                        await battle_msg.edit(components=[])
                                        if not any((battle_config.is_abyss_game_mode, 
                                                    battle_config.is_scenario_game_mode, 
                                                    battle_config.is_explore_game_mode, 
                                                    battle_config.is_pvp_game_mode, 
                                                    battle_config.is_tutorial_game_mode,
                                                    battle_config.is_boss_game_mode)):
                                            await save_spot(self, player1.did, battle_config.selected_universe, battle_config.mode, battle_config.current_opponent_number)
                                            await ctx.send(embed = battle_config.saved_game_embed(player1_card,player2_card))
                                        elif any((battle_config.is_pvp_game_mode, 
                                                    battle_config.is_tutorial_game_mode
                                                                )):
                                            await ctx.send(embed = battle_config.close_pvp_embed(player1_card,player2_card))
                                        else:
                                            await ctx.send(embed = battle_config.close_pve_embed(player1_card,player2_card))
                                        # if not battle_config.is_abyss_game_mode and not battle_config.is_scenario_game_mode and not battle_config.is_explore_game_mode and not battle_config.is_pvp_game_mode and not battle_config.is_tutorial_game_mode:
                                        #     await save_spot(self, player1.did, battle_config.selected_universe, battle_config.mode, battle_config.current_opponent_number)
                                        #     await ctx.send(embed = battle_config.saved_game_embed(player1_card,player2_card))
                                        await ctx.send(f"{ctx.author.mention} {battle_config.error_end_match_message()}")
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
                        
                        if battle_config.is_duo_mode or battle_config.is_co_op_mode:
                            game_over_check = battle_config.set_game_over(player1_card, player2_card, player3_card)
                        else:
                            game_over_check = battle_config.set_game_over(player1_card, player2_card, None)
                        if game_over_check:
                            break
                        if battle_config.is_co_op_mode:
                            pre_turn_one = beginning_of_turn_stat_trait_affects(player2_card, player2_title, player1_card, battle_config, player3_card)
                        else:
                            pre_turn_one = beginning_of_turn_stat_trait_affects(player2_card, player2_title, player1_card, battle_config)
                        
                        if battle_config.is_turn == 1:
                            # tactics_death_blow_check(player2_card, player1_card, battle_config)                    
                            if player1_card.health == 0:
                                continue
                            if(player2_card.damage_check_activated):
                                battle_config.is_turn = 0
                                continue

                            player1_card.set_deathnote_message(battle_config)
                            player2_card.set_deathnote_message(battle_config)
                            if battle_config.is_co_op_mode:
                                player3_card.set_deathnote_message(battle_config)                            
                            
                            if battle_config.turn_total == 0:
                                if battle_config.is_boss_game_mode:
                                    embedVar = discord.Embed(title=f"**{player2_card.name}** Boss of `{player2_card.universe}`",
                                                            description=f"*{battle_config._description_boss_description}*", colour=0xe91e63)
                                    embedVar.add_field(name=f"{battle_config._arena_boss_description}", value=f"{battle_config._arenades_boss_description}")
                                    embedVar.add_field(name=f"Entering the {battle_config._arena_boss_description}", value=f"{battle_config._entrance_boss_description}", inline=False)
                                    embedVar.set_footer(text=f"{player2_card.name} waits for you to strike....")
                                    await private_channel.send(embed=embedVar)
                                    await asyncio.sleep(2)
                            
                            # Focus
                            if player2_card.stamina < 10:
                                player2_card.focusing(player2_title, player1_title, player1_card, battle_config)

                                if battle_config.is_boss_game_mode:
                                    embedVar = discord.Embed(title=f"**{player2_card.name}** Enters Focus State",
                                                            description=f"{battle_config._powerup_boss_description}", colour=0xe91e63)
                                    embedVar.add_field(name=f"A great aura starts to envelop **{player2_card.name}** ",
                                                    value=f"{battle_config._aura_boss_description}")
                                    embedVar.set_footer(text=f"{player2_card.name} Says: 'Now, are you ready for a real fight?'")
                                    await ctx.send(embed=embedVar)
                                    # await asyncio.sleep(2)
                                    if player2_card.universe == "Digimon" and player2_card.used_resolve is False:
                                        embedVar = discord.Embed(title=f"(**{battle_config.turn_total}**) :zap: **{player2_card.name}** Resolved!", description=f"{battle_config._rmessage_boss_description}",
                                                                colour=0xe91e63)
                                        embedVar.set_footer(text=f"{player1_card.name} this will not be easy...")
                                        await private_channel.send(embed=embedVar)
                                        await asyncio.sleep(2)

                            else:
                                player2_card.set_battle_arm_messages(player1_card)
                                player2_card.set_stat_icons()

                                player2_card.activate_solo_leveling_trait(battle_config, player1_card)
                                                                
                                embedVar = discord.Embed(title=f"➡️ **Opponent Turn** {battle_config.turn_total}", description=textwrap.dedent(f"""\
                                {battle_config.get_previous_moves_embed()}
                                
                                """), color=0xe74c3c)
                                if battle_config.is_duo_mode or battle_config.is_co_op_mode:
                                    footer_text = battle_config.get_battle_footer_text(player2_card, player1_card, player3_card)
                                else:
                                    footer_text = battle_config.get_battle_footer_text(player2_card, player1_card)
                                embedVar.set_footer(
                                    text=f"{footer_text}",
                                    icon_url="https://cdn.discordapp.com/emojis/789290881654980659.gif?v=1")


                                if battle_config.is_pvp_game_mode and not battle_config.is_tutorial_game_mode:
                                    battle_config.set_battle_options(player2_card, player1_card)
                                    # Check If Playing Bot
                                    if not battle_config.is_ai_opponent:

                                        battle_action_row = manage_components.create_actionrow(*battle_config.battle_buttons)
                                        util_action_row = manage_components.create_actionrow(*battle_config.utility_buttons)

                                        player2_card.set_battle_arm_messages(player2_card)
                                        player2_card.set_stat_icons()

                                        components = [battle_action_row, util_action_row]
                                        embedVar = discord.Embed(title=f"", description=textwrap.dedent(f"""\
                                        {battle_config.get_previous_moves_embed()}

                                        """), color=0xe74c3c)
                                        embedVar.set_author(name=f"{player2_card._arm_message}\n{player2_card.summon_resolve_message}\n")
                                        if player2.performance:
                                            embedVar.add_field(name=f"➡️ **Current Turn** {battle_config.turn_total}", value=f"{user2.mention} Select move below!\n{player2_card.get_performance_stats()}\n{player2_title.get_title_icon(player2_card.universe)} | {player2_title.passive_type} {player2_title.passive_value}")
                                        else:
                                            embedVar.add_field(name=f"➡️ **Current Turn** {battle_config.turn_total}", value=f"{user2.mention} Select move below!")
                                        #embedVar.add_field(name=f"➡️ **Current Turn** {battle_config.turn_total}", value=f"{user2.mention} Select move below!")
                                        embedVar.set_image(url="attachment://image.png")
                                        if battle_config.is_duo_mode or battle_config.is_co_op_mode:
                                            footer_text = battle_config.get_battle_footer_text(player2_card, player1_card, player3_card)
                                        else:
                                            footer_text = battle_config.get_battle_footer_text(player2_card, player1_card)
                                        embedVar.set_footer(
                                            text=f"{footer_text}",
                                            icon_url="https://cdn.discordapp.com/emojis/789290881654980659.gif?v=1")
                                        await battle_msg.delete(delay=1)
                                        await asyncio.sleep(1)
                                        if player2.performance:
                                            embedVar.add_field(name=f":sunny: | **Move Set**", value=f"{player2_card.resolve_icon} | {player2_card.stamina} *Stamina*\n{player2_card.move1_emoji} | {player2_card.move1ap} *-10 ST {player2_card.resolve_icon}*\n{player2_card.move2_emoji} | {player2_card.move2ap} *-30 ST {player2_card.resolve_icon}*\n{player2_card.move3_emoji} | {player2_card.move3ap} *-80 ST {player2_card.resolve_icon}*\n:microbe: | {player2_card.move4enh} {player2_card.move4ap} *-20 ST {player2_card.resolve_icon}*")
                                            battle_msg = await private_channel.send(embed=embedVar, components=components)
                                        else:
                                            battle_msg = await private_channel.send(embed=embedVar, components=components, file=player2_card.showcard(battle_config.mode, player2_arm, player2_title, battle_config.turn_total, player1_card.defense))

                                        # Make sure user is responding with move
                                        def check(button_ctx):
                                            return button_ctx.author == user2 and button_ctx.custom_id in options

                                        try:
                                            button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot,
                                                                                                                    components=[
                                                                                                                        battle_action_row,
                                                                                                                        util_action_row],
                                                                                                                    timeout=300,
                                                                                                                    check=check)

                                            if button_ctx.custom_id == "q" or button_ctx.custom_id == "Q":
                                                player2_card.health = 0
                                                battle_config.game_over = True
                                                await battle_msg.delete(delay=1)
                                                await asyncio.sleep(1)
                                                battle_msg = await private_channel.send(content=f"{user2.mention} has fled.")

                                                #return
                                            if button_ctx.custom_id == "1":
                                                damage_calculation_response = player2_card.damage_cal(int(button_ctx.custom_id), battle_config, player1_card)
                                            
                                            elif button_ctx.custom_id == "2":
                                                damage_calculation_response = player2_card.damage_cal(int(button_ctx.custom_id), battle_config, player1_card)
                                            
                                            elif button_ctx.custom_id == "3":

                                                damage_calculation_response = player2_card.damage_cal(int(button_ctx.custom_id), battle_config, player1_card)
                                                if player2_card.gif != "N/A" and not player1.performance:
                                                    # await button_ctx.defer(ignore=True)
                                                    await battle_msg.delete(delay=None)
                                                    # await asyncio.sleep(1)
                                                    battle_msg = await private_channel.send(f"{player2_card.gif}")
                                                    
                                                    await asyncio.sleep(2)
                                            elif button_ctx.custom_id == "4":
                                                damage_calculation_response = player2_card.damage_cal(int(button_ctx.custom_id), battle_config, player1_card)
                                            
                                            elif button_ctx.custom_id == "5":
                                                player2_card.resolving(battle_config, player1_card)
                                            
                                            elif button_ctx.custom_id == "6" and not battle_config.is_raid_game_mode:
                                                player2_card.usesummon(battle_config, player1_card)
                                            
                                            elif button_ctx.custom_id == "0":
                                                player2_card.use_block(battle_config, player1_card)                                            

                                            if button_ctx.custom_id in battle_config.main_battle_options:
                                                player2_card.damage_done(battle_config, damage_calculation_response, player1_card)
                                        
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
                                        player2_card.set_stat_icons()

                                        player2_card.activate_solo_leveling_trait(battle_config, player1_card)

                                        battle_config.set_battle_options(player2_card, player1_card)

                                        
                                        tembedVar = discord.Embed(title=f"_Turn_ {battle_config.turn_total}", description=textwrap.dedent(f"""\
                                        {battle_config.get_previous_moves_embed()}
                                        """), color=0xe74c3c)
                                        tembedVar.set_image(url="attachment://image.png")
                                        await battle_msg.delete(delay=2)
                                        await asyncio.sleep(2) 
                                        if player1.performance:
                                            embedVar.add_field(name=f"➡️ **Enemy Turn** {battle_config.turn_total}", value=f"Enemy {player2_card.name}'s Turn!\n{player2_card.get_performance_stats()}\n{player2_title.get_title_icon(player2_card.universe)} | {player2_title.passive_type} {player2_title.passive_value}")
                                            embedVar.add_field(name=f":sunny: | **Move Set**", value=f"{player2_card.resolve_icon} | {player2_card.stamina} *Stamina*\n{player2_card.move1_emoji} | {player2_card.move1ap} *-10 ST {player2_card.resolve_icon}*\n{player2_card.move2_emoji} | {player2_card.move2ap} *-30 ST {player2_card.resolve_icon}*\n{player2_card.move3_emoji} | {player2_card.move3ap} *-80 ST {player2_card.resolve_icon}*\n:microbe: | {player2_card.move4enh} {player2_card.move4ap} *-20 ST {player2_card.resolve_icon}*")
                                            battle_msg = await private_channel.send(embed=tembedVar)
                                        else:
                                            battle_msg = await private_channel.send(embed=tembedVar,file=player2_card.showcard(battle_config.mode, player2_arm, player2_title, battle_config.turn_total, player1_card.defense))
                                        await asyncio.sleep(3)
                                        
                                        selected_move = battle_config.ai_battle_command(player2_card, player1_card)

                                        damage_calculation_response = player2_card.damage_cal(selected_move, battle_config, player1_card)

                                        if selected_move == 5:
                                            player2_card.resolving(battle_config, player1_card, player2)
                                            if battle_config.is_boss_game_mode:
                                                await private_channel.send(embed=battle_config._boss_embed_message)

                                        elif selected_move == 6:
                                            # Resolve Check and Calculation
                                            player2_card.usesummon(battle_config, player1_card)
                                        
                                        if selected_move == 0:
                                            player2_card.use_block(battle_config, damage_calculation_response, player1_card)

                                        if selected_move != 5 and selected_move != 6 and selected_move != 0:
                                            player2_card.damage_done(battle_config, damage_calculation_response, player1_card)                                        

                                if not battle_config.is_pvp_game_mode or battle_config.is_tutorial_game_mode:
                                    if battle_config.is_auto_battle_game_mode:
                                        embedVar = await auto_battle_embed_and_starting_traits(ctx, player2_card, player1_card, battle_config, None)
                                        if battle_msg is None:
                                            # If the message does not exist, send a new message
                                            battle_msg = await private_channel.send(embed=embedVar, components=[])
                                        else:
                                            # If the message exists, edit it
                                            await battle_msg.edit(embed=embedVar, components=[])
                                        await asyncio.sleep(2)

                                    if not battle_config.is_auto_battle_game_mode:
                                        await battle_msg.delete(delay=2)
                                        if battle_config.is_co_op_mode or battle_config.is_duo_mode:
                                            embedVar = await auto_battle_embed_and_starting_traits(ctx, player2_card, player1_card, battle_config, player3_card)
                                        else:
                                            embedVar = await auto_battle_embed_and_starting_traits(ctx, player2_card, player1_card, battle_config, None)
                                        if player1.performance:
                                            embedVar.add_field(name=f"➡️ **Enemy Turn** {battle_config.turn_total}", value=f"Enemy {player2_card.name}'s Turn!\n{player2_card.get_performance_stats()}\n{player2_title.get_title_icon(player2_card.universe)} | {player2_title.passive_type} {player2_title.passive_value}")
                                            embedVar.add_field(name=f":sunny: | **Move Set**", value=f"{player2_card.resolve_icon} | {player2_card.stamina} *Stamina*\n{player2_card.move1_emoji} | {player2_card.move1ap} *-10 ST {player2_card.resolve_icon}*\n{player2_card.move2_emoji} | {player2_card.move2ap} *-30 ST {player2_card.resolve_icon}*\n{player2_card.move3_emoji} | {player2_card.move3ap} *-80 ST {player2_card.resolve_icon}*\n:microbe: | {player2_card.move4enh} {player2_card.move4ap} *-20 ST {player2_card.resolve_icon}*")
                                            battle_msg = await private_channel.send(embed=embedVar)
                                        else:
                                            battle_msg = await private_channel.send(embed=embedVar, file=player2_card.showcard(battle_config.mode, player2_arm, player2_title, battle_config.turn_total, player1_card.defense))


                                    selected_move = battle_config.ai_battle_command(player2_card, player1_card)
                                                                        
                                    if int(selected_move) in [1, 2, 3, 4]:
                                        damage_calculation_response = player2_card.damage_cal(selected_move, battle_config, player1_card)                                    
                                        if not battle_config.is_auto_battle_game_mode and int(selected_move) == 3:
                                            if player2_card.gif != "N/A"  and not player1.performance:
                                                await battle_msg.delete(delay=2)
                                                await asyncio.sleep(2)
                                                battle_msg = await private_channel.send(f"{player2_card.gif}")
                                                await asyncio.sleep(2)

                                    elif int(selected_move) == 5:
                                        player2_card.resolving(battle_config, player1_card)
                                        if battle_config.is_boss_game_mode:
                                            await private_channel.send(embed=battle_config._boss_embed_message)

                                    elif int(selected_move) == 6:
                                        # Resolve Check and Calculation
                                        if player2_card.used_resolve and player2_card.used_focus and not player2_card.usedsummon:
                                            if battle_config.is_co_op_mode:
                                                if player3_card.used_defend == True:
                                                    summon_response = player2_card.usesummon(battle_config, player3_card)
                                                    if not player1.performance and summon_response['CAN_USE_MOVE']:
                                                        await battle_msg.delete(delay=2)
                                                        tsummon_file = showsummon(player2_card.summon_image, player2_card.summon_name, summon_response['MESSAGE'], player2_card.summon_lvl, player2_card.summon_bond)
                                                        embedVar.set_image(url="attachment://pet.png")
                                                        await asyncio.sleep(2)
                                                        battle_msg = await private_channel.send(embed=embedVar, file=tsummon_file)
                                                        await asyncio.sleep(2)
                                                        await battle_msg.delete(delay=2)

                                                else:
                                                    summon_response = player2_card.usesummon(battle_config, player1_card)
                                                    if not player1.performance and summon_response['CAN_USE_MOVE']:
                                                        await battle_msg.delete(delay=2)
                                                        tsummon_file = showsummon(player2_card.summon_image, player2_card.summon_name, summon_response['MESSAGE'], player2_card.summon_lvl, player2_card.summon_bond)
                                                        embedVar.set_image(url="attachment://pet.png")
                                                        await asyncio.sleep(2)
                                                        battle_msg = await private_channel.send(embed=embedVar, file=tsummon_file)
                                                        await asyncio.sleep(2)
                                                        await battle_msg.delete(delay=2)

                                            else:
                                                summon_response = player2_card.usesummon(battle_config, player1_card)
                                                if not player1.performance and summon_response['CAN_USE_MOVE']:
                                                    await battle_msg.delete(delay=2)
                                                    tsummon_file = showsummon(player2_card.summon_image, player2_card.summon_name, summon_response['MESSAGE'], player2_card.summon_lvl, player2_card.summon_bond)
                                                    embedVar.set_image(url="attachment://pet.png")
                                                    await asyncio.sleep(2)
                                                    battle_msg = await private_channel.send(embed=embedVar, file=tsummon_file)
                                                    await asyncio.sleep(2)
                                                    await battle_msg.delete(delay=2)

                                        else:
                                            battle_config.add_battle_history_message(f"(**{battle_config.turn_total}**) {player2_card.name} Could not summon 🧬 **{player2_card.name}**. Needs rest")
                                    elif int(selected_move) == 0:
                                        player2_card.use_block(battle_config, player1_card)                                            
                                    if int(selected_move) != 5 and int(selected_move) != 6 and int(selected_move) != 0:

                                        # If you have enough stamina for move, use it
                                        # if c used block
                                        if battle_config.is_co_op_mode:
                                            if player3_card.used_defend == True:
                                                player2_card.damage_done(battle_config, damage_calculation_response, player3_card)
                                            else:
                                                player2_card.damage_done(battle_config, damage_calculation_response, player1_card)
                                        else:
                                            player2_card.damage_done(battle_config, damage_calculation_response, player1_card)


                        elif battle_config.is_co_op_mode and battle_config.is_turn != (0 or 1):
                            if battle_config.is_duo_mode or battle_config.is_co_op_mode:
                                game_over_check = battle_config.set_game_over(player1_card, player2_card, player3_card)
                            else:
                                game_over_check = battle_config.set_game_over(player1_card, player2_card, None)
                            if game_over_check:
                                break
                            if battle_config.is_co_op_mode:
                                pre_turn_two = beginning_of_turn_stat_trait_affects(player3_card, player3_title, player2_card, battle_config, player1_card)
                            else:
                                pre_turn_two = beginning_of_turn_stat_trait_affects(player3_card, player3_title, player2_card, battle_config)
                            if battle_config.is_turn == 2:
                                player2_card.set_deathnote_message(battle_config)
                                player3_card.set_deathnote_message(battle_config)


                                if player3_card.stamina < 10:
                                    player3_card.focusing(player3_title, player2_title, player2_card, battle_config)
                                else:
                                    if battle_config.is_auto_battle_game_mode or battle_config.is_duo_mode:
                                        if battle_config.is_duo_mode:
                                            embedVar = discord.Embed(title=f"", description=textwrap.dedent(f"""\
                                            {battle_config.get_previous_moves_embed()}
                                            
                                            """), color=0xe74c3c)
                                            embedVar.set_author(name=f"{player3_card._arm_message}\n{player3_card.summon_resolve_message}\n")
                                            if player1.performance:
                                                embedVar.add_field(name=f"➡️ **Current Turn** {battle_config.turn_total}", value=f"Ally {player3_card.name}'s Turn!\n{player3_card.get_performance_stats()}\n{player3_title.get_title_icon(player3_card.universe)} | {player3_title.passive_type} {player3_title.passive_value}")
                                            else:
                                                embedVar.add_field(name=f"➡️ **Current Turn** {battle_config.turn_total}", value=f"Ally {player3_card.name}'s Turn!")
                                            #embedVar.add_field(name=f"➡️ **Current Turn** {battle_config.turn_total}", value=f"Ally {player3_card.name}'s Turn!")
                                            # await asyncio.sleep(2)
                                            embedVar.set_image(url="attachment://image.png")
                                            if battle_config.is_duo_mode or battle_config.is_co_op_mode:
                                                footer_text = battle_config.get_battle_footer_text(player2_card, player1_card, player3_card)
                                            else:
                                                footer_text = battle_config.get_battle_footer_text(player2_card, player1_card)
                                            embedVar.set_footer(
                                                text=f"{footer_text}",
                                                icon_url="https://cdn.discordapp.com/emojis/789290881654980659.gif?v=1")
                                            await battle_msg.delete(delay=2)
                                            await asyncio.sleep(2)
                                            if player1.performance:
                                                embedVar.add_field(name=f":sunny: | **Move Set**", value=f"{player3_card.resolve_icon} | {player3_card.stamina} *Stamina*\n{player3_card.move1_emoji} | {player3_card.move1ap} *-10 ST {player3_card.resolve_icon}*\n{player3_card.move2_emoji} | {player3_card.move2ap} *-30 ST {player3_card.resolve_icon}*\n{player3_card.move3_emoji} | {player3_card.move3ap} *-80 ST {player3_card.resolve_icon}*\n:microbe: | {player3_card.move4enh} {player3_card.move4ap} *-20 ST {player3_card.resolve_icon}*")
                                                battle_msg = await private_channel.send(embed=embedVar)
                                            else:
                                                battle_msg = await private_channel.send(embed=embedVar, file=player3_card.showcard(battle_config.mode, player3_arm, player3_title, battle_config.turn_total, player2_card.defense))
                                            # Make sure user is responding with move
                                        else:
                                            embedVar = await auto_battle_embed_and_starting_traits(ctx, player3_card, player2_card, battle_config, player1_card)
                                            await battle_msg.edit(embed=embedVar, components=[])


                                        selected_move = battle_config.ai_battle_command(player3_card, player2_card)

                                        if selected_move in [1, 2, 3, 4]:
                                            damage_calculation_response = player3_card.damage_cal(selected_move, battle_config, player2_card)
                                        
                                        if selected_move == 5:
                                            player3_card.resolving(battle_config, player2_card, player3)
                                        
                                        if selected_move == 6:
                                            player3_card.usesummon(battle_config, player2_card)                                        
                                        
                                        elif selected_move == 8:
                                            player3_card.use_companion_enhancer(battle_config, player2_card, player1_card)
                                        
                                        elif selected_move == 0:
                                            player3_card.use_defend(battle_config, player1_card)

                                        if selected_move != 5 and selected_move != 6 and selected_move != 7 and selected_move != 8 and selected_move != 0:
                                            player3_card.damage_done(battle_config, damage_calculation_response, player2_card) 
                                    else:
                                        player3_card.set_battle_arm_messages(player2_card)
                                        player3_card.set_stat_icons()

                                        player3_card.activate_solo_leveling_trait(battle_config, player2_card)

                                        #battle_config.set_battle_options(player3_card, player2_card)
                                        if battle_config.is_co_op_mode:
                                            battle_config.set_battle_options(player3_card, player2_card,player1_card)
                                        else:
                                            battle_config.set_battle_options(player3_card, player2_card)

                                        battle_action_row = manage_components.create_actionrow(*battle_config.battle_buttons)
                                        util_action_row = manage_components.create_actionrow(*battle_config.utility_buttons)
                                        coop_util_action_row = manage_components.create_actionrow(*battle_config.co_op_buttons)




                                        embedVar = discord.Embed(title=f"", description=textwrap.dedent(f"""\
                                        {battle_config.get_previous_moves_embed()}
                                        
                                        """), color=0xe74c3c)
                                        embedVar.set_author(name=f"{player3_card._arm_message}\n{player3_card.summon_resolve_message}\n")
                                        if player3.performance:
                                            embedVar.add_field(name=f"➡️ **Current Turn** {battle_config.turn_total}", value=f"{user2.mention} Select move below!\n{player3_card.get_performance_stats()}\n{player3_title.get_title_icon(player3_card.universe)} | {player3_title.passive_type} {player3_title.passive_value}")
                                        else:
                                            embedVar.add_field(name=f"➡️ **Current Turn** {battle_config.turn_total}", value=f"{user2.mention} Select move below!")
                                        # embedVar.add_field(name=f"➡️ **Current Turn** {battle_config.turn_total}", value=f"{user2.mention} Select move below!")
                                        # await asyncio.sleep(2)
                                        embedVar.set_image(url="attachment://image.png")
                                        if battle_config.is_duo_mode or battle_config.is_co_op_mode:
                                            footer_text = battle_config.get_battle_footer_text(player2_card, player1_card, player3_card)
                                        else:
                                            footer_text = battle_config.get_battle_footer_text(player2_card, player1_card)
                                        embedVar.set_footer(
                                            text=f"{footer_text}",
                                            icon_url="https://cdn.discordapp.com/emojis/789290881654980659.gif?v=1")
                                        await battle_msg.delete(delay=2)
                                        await asyncio.sleep(2)
                                        if player3.performance:
                                            embedVar.add_field(name=f":sunny: | **Move Set**", value=f"{player3_card.resolve_icon} | {player3_card.stamina} *Stamina*\n{player3_card.move1_emoji} | {player3_card.move1ap} *-10 ST {player3_card.resolve_icon}*\n{player3_card.move2_emoji} | {player3_card.move2ap} *-30 ST {player3_card.resolve_icon}*\n{player3_card.move3_emoji} | {player3_card.move3ap} *-80 ST {player3_card.resolve_icon}*\n:microbe: | {player3_card.move4enh} {player3_card.move4ap} *-20 ST {player3_card.resolve_icon}*")
                                            battle_msg = await private_channel.send(embed=embedVar, components=components)
                                        else:
                                            battle_msg = await private_channel.send(embed=embedVar, components=[battle_action_row, util_action_row, coop_util_action_row], file=player3_card.showcard(battle_config.mode, player3_arm, player3_title, battle_config.turn_total, player2_card.defense))
                                        # Make sure user is responding with move
                                        def check(button_ctx):
                                            return button_ctx.author == user2

                                        try:
                                            button_ctx: ComponentContext = await manage_components.wait_for_component(
                                                self.bot,
                                                components=[battle_action_row, util_action_row, coop_util_action_row],
                                                timeout=300, check=check)

                                            # calculate data based on selected move
                                            if button_ctx.custom_id == "q" or button_ctx.custom_id == "Q":
                                                player3_card.health = 0
                                                battle_config.game_over = True
                                                battle_config.add_battle_history_message(f"(**{battle_config.turn_total}**) 💨 **{player3_card.name}** Fled...")
                                                await asyncio.sleep(1)
                                                await battle_msg.delete(delay=1)
                                                battle_msg = await private_channel.send(content=f"{ctx.author.mention} has fled.")
                                            
                                            if button_ctx.custom_id == "1":
                                                damage_calculation_response = player3_card.damage_cal(int(button_ctx.custom_id), battle_config, player2_card)
                                            
                                            elif button_ctx.custom_id == "2":
                                                damage_calculation_response = player3_card.damage_cal(int(button_ctx.custom_id), battle_config, player2_card)
                                            
                                            elif button_ctx.custom_id == "3":
                                                damage_calculation_response = player3_card.damage_cal(int(button_ctx.custom_id), battle_config, player2_card)
                                                if player3_card.gif != "N/A" and not player3.performance:
                                                    # await button_ctx.defer(ignore=True)
                                                    await battle_msg.delete(delay=None)
                                                    # await asyncio.sleep(1)
                                                    battle_msg = await private_channel.send(f"{player3_card.gif}")
                                                    
                                                    await asyncio.sleep(2)
                                            elif button_ctx.custom_id == "4":
                                                damage_calculation_response = player1_card.damage_cal(int(button_ctx.custom_id), battle_config, player2_card)
                                            
                                            elif button_ctx.custom_id == "5":
                                                player3_card.resolving(battle_config, player2_card, player3)
                                            
                                            elif button_ctx.custom_id == "6":
                                                summon_response = player3_card.usesummon(battle_config, player2_card)
                                                
                                                if not player3.performance and summon_response['CAN_USE_MOVE']:
                                                    await battle_msg.delete(delay=2)
                                                    tsummon_file = showsummon(player3_card.summon_image, player3_card.summon_name, summon_response['MESSAGE'], player3_card.summon_lvl, player3_card.summon_bond)
                                                    embedVar.set_image(url="attachment://pet.png")
                                                    await asyncio.sleep(2)
                                                    battle_msg = await private_channel.send(embed=embedVar, file=tsummon_file)
                                                    await asyncio.sleep(2)
                                                    await battle_msg.delete(delay=2)
                                            
                                        
                                                
                                            elif button_ctx.custom_id == "0":
                                                player3_card.use_block(battle_config, player2_card, player1_card)
                                            
                                            elif button_ctx.custom_id == "7":
                                                player3_card.use_companion_enhancer(battle_config, player2_card, player1_card)

                                            #Use Companion on yourself
                                            elif button_ctx.custom_id == "8":
                                                player1_card.use_companion_enhancer(battle_config, player2_card, player3_card)
                                                    
                                            elif button_ctx.custom_id == "9":
                                                player1_card.use_block(battle_config, player2_card, player3_card)                                           

                                            if button_ctx.custom_id != "5" and button_ctx.custom_id != "6" and button_ctx.custom_id != "7" and button_ctx.custom_id != "8" and button_ctx.custom_id != "0" and button_ctx.custom_id != "q":
                                                player3_card.damage_done(battle_config, damage_calculation_response, player2_card)
                                        except asyncio.TimeoutError:
                                            await battle_msg.delete()
                                            #await battle_msg.edit(components=[])
                                            if not any((battle_config.is_abyss_game_mode, 
                                                        battle_config.is_scenario_game_mode, 
                                                        battle_config.is_explore_game_mode, 
                                                        battle_config.is_pvp_game_mode, 
                                                        battle_config.is_tutorial_game_mode,
                                                        battle_config.is_boss_game_mode)):
                                                await save_spot(self, player1.did, battle_config.selected_universe, battle_config.mode, battle_config.current_opponent_number)
                                                await ctx.send(embed = battle_config.saved_game_embed(player1_card,player2_card))
                                            elif any((battle_config.is_pvp_game_mode, 
                                                        battle_config.is_tutorial_game_mode
                                                                    )):
                                                await ctx.send(embed = battle_config.close_pvp_embed(player1_card,player2_card))
                                            else:
                                                await ctx.send(embed = battle_config.close_pve_embed(player1_card,player2_card))
                                            # await save_spot(self, player1.did, battle_config.selected_universe, battle_config.mode, battle_config.current_opponent_number)
                                            # await ctx.send(embed = battle_config.saved_game_embed(player1_card,player2_card))
                                            await ctx.author.send(f"{ctx.author.mention} your game timed out. Your channel has been closed but your spot in the tales has been saved where you last left off.")
                                            await ctx.send(f"{ctx.author.mention} your game timed out. Your channel has been closed but your spot in the tales has been saved where you last left off.")
                                            # await discord.TextChannel.delete(private_channel, reason=None)
                                            battle_config.add_battle_history_message(f"(**{battle_config.turn_total}**) 💨 **{player3_card.name}** Fled...")
                                            # player3_card.health = 0
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
                            if battle_config.is_duo_mode or battle_config.is_co_op_mode:
                                game_over_check = battle_config.set_game_over(player1_card, player2_card, player3_card)
                            else:
                                game_over_check = battle_config.set_game_over(player1_card, player2_card, None)
                            if game_over_check:
                                break
                            if battle_config.is_co_op_mode:
                                pre_turn_three = beginning_of_turn_stat_trait_affects(player2_card, player2_title, player3_card, battle_config, player1_card)
                            else:
                                pre_turn_three =beginning_of_turn_stat_trait_affects(player2_card, player2_title, player3_card, battle_config)

                            if battle_config.is_turn == 3:
                                player3_card.set_deathnote_message(battle_config)
                                player2_card.set_deathnote_message(battle_config)


                                # Focus
                                if player2_card.stamina < 10:
                                    player2_card.focusing(player2_title, player3_title, player3_card, battle_config)

                                    if battle_config.is_boss_game_mode:
                                        embedVar = discord.Embed(title=f"**{player2_card.name}** Enters Focus State",
                                                                description=f"{battle_config._powerup_boss_description}", colour=0xe91e63)
                                        embedVar.add_field(name=f"A great aura starts to envelop **{player2_card.name}** ",
                                                        value=f"{battle_config._aura_boss_description}")
                                        embedVar.set_footer(text=f"{player2_card.name} Says: 'Now, are you ready for a real fight?'")
                                        await ctx.send(embed=embedVar)
                                        # await asyncio.sleep(2)
                                        if player2_card.universe == "Digimon" and player2_card.used_resolve is False:
                                            embedVar = discord.Embed(title=f"(**{battle_config.turn_total}**) :zap: **{player2_card.name}** Resolved!", description=f"{battle_config._rmessage_boss_description}",
                                                                    colour=0xe91e63)
                                            embedVar.set_footer(text=f"{player3_card.name} this will not be easy...")
                                            await ctx.send(embed=embedVar)
                                            await asyncio.sleep(2)
                                
                                else:
                                    await battle_msg.delete(delay=2)
                                    embedVar = await auto_battle_embed_and_starting_traits(ctx, player2_card, player3_card, battle_config, player1_card)
                                    if player3.performance:
                                        embedVar.add_field(name=f"➡️ **Enemy Turn** {battle_config.turn_total}", value=f"Enemy {player2_card.name}'s Turn!\n{player2_card.get_performance_stats()}\n{player2_title.get_title_icon(player2_card.universe)} | {player2_title.passive_type} {player2_title.passive_value}")
                                        embedVar.add_field(name=f":sunny: | **Move Set**", value=f"{player2_card.resolve_icon} | {player2_card.stamina} *Stamina*\n{player2_card.move1_emoji} | {player2_card.move1ap} *-10 ST {player2_card.resolve_icon}*\n{player2_card.move2_emoji} | {player2_card.move2ap} *-30 ST {player2_card.resolve_icon}*\n{player2_card.move3_emoji} | {player2_card.move3ap} *-80 ST {player2_card.resolve_icon}*\n:microbe: | {player2_card.move4enh} {player2_card.move4ap} *-20 ST {player2_card.resolve_icon}*")
                                        battle_msg = await private_channel.send(embed=embedVar)
                                    else:
                                        battle_msg = await private_channel.send(embed=embedVar,file=player2_card.showcard(battle_config.mode, player2_arm, player2_title, battle_config.turn_total, player3_card.defense))


                                    selected_move = battle_config.ai_battle_command(player2_card, player3_card)
                                    
                                    
                                    if int(selected_move) == 3:                                    

                                        if battle_config.is_auto_battle_game_mode:
                                            if player2_card.gif != "N/A"  and not player1.performance:
                                                await battle_msg.delete(delay=2)
                                                await asyncio.sleep(2)
                                                battle_msg = await private_channel.send(f"{player2_card.gif}")
                                                await asyncio.sleep(2)

                                    elif int(selected_move) == 5:
                                        player2_card.resolving(battle_config, player3_card, player2)
                                        if battle_config.is_boss_game_mode:
                                            await button_ctx.send(embed=battle_config._boss_embed_message)

                                    elif int(selected_move) == 6:
                                        # Resolve Check and Calculation
                                        if player2_card.used_resolve and player2_card.used_focus and not player2_card.usedsummon:
                                            if battle_config.is_co_op_mode:
                                                if player3_card.used_defend == True:
                                                    summon_response = player2_card.usesummon(battle_config, player1_card)
                                                    if not player1.performance and summon_response['CAN_USE_MOVE']:
                                                        await battle_msg.delete(delay=2)
                                                        tsummon_file = showsummon(player2_card.summon_image, player2_card.summon_name, summon_response['MESSAGE'], player2_card.summon_lvl, player2_card.summon_bond)
                                                        embedVar.set_image(url="attachment://pet.png")
                                                        await asyncio.sleep(2)
                                                        battle_msg = await private_channel.send(embed=embedVar, file=tsummon_file)
                                                        await asyncio.sleep(2)
                                                        await battle_msg.delete(delay=2)

                                                else:
                                                    summon_response = player2_card.usesummon(battle_config, player3_card)
                                                    if not player1.performance and summon_response['CAN_USE_MOVE']:
                                                        await battle_msg.delete(delay=2)
                                                        tsummon_file = showsummon(player2_card.summon_image, player2_card.summon_name, summon_response['MESSAGE'], player2_card.summon_lvl, player2_card.summon_bond)
                                                        embedVar.set_image(url="attachment://pet.png")
                                                        await asyncio.sleep(2)
                                                        battle_msg = await private_channel.send(embed=embedVar, file=tsummon_file)
                                                        await asyncio.sleep(2)
                                                        await battle_msg.delete(delay=2)

                                            else:
                                                summon_response = player2_card.usesummon(battle_config, player3_card)
                                                if not player1.performance and summon_response['CAN_USE_MOVE']:
                                                    await battle_msg.delete(delay=2)
                                                    tsummon_file = showsummon(player2_card.summon_image, player2_card.summon_name, summon_response['MESSAGE'], player2_card.summon_lvl, player2_card.summon_bond)
                                                    embedVar.set_image(url="attachment://pet.png")
                                                    await asyncio.sleep(2)
                                                    battle_msg = await private_channel.send(embed=embedVar, file=tsummon_file)
                                                    await asyncio.sleep(2)
                                                    await battle_msg.delete(delay=2)

                                        else:
                                            battle_config.add_battle_history_message(f"(**{battle_config.turn_total}**) {player2_card.name} Could not summon 🧬 **{player2_card.name}**. Needs rest")
                                    elif int(selected_move) == 0:
                                        player2_card.use_block(battle_config, player3_card) 
                                    if int(selected_move) == 10:
                                        player2_card.use_boost(battle_config)     
                                                                                 
                                    if int(selected_move) != 5 and int(selected_move) != 6 and int(selected_move) != 0 and int(selected_move) != 10:
                                        damage_calculation_response = player2_card.damage_cal(selected_move, battle_config, player3_card)
                                        if battle_config.is_co_op_mode:
                                            if player3_card.used_defend == True:
                                                player2_card.damage_done(battle_config, damage_calculation_response, player1_card)
                                            else:
                                                player2_card.damage_done(battle_config, damage_calculation_response, player3_card)
                                        else:
                                            player2_card.damage_done(battle_config, damage_calculation_response, player3_card)
                    
                    if game_over_check:
                        wintime = time.asctime()
                        h_playtime = int(wintime[11:13])
                        m_playtime = int(wintime[14:16])
                        s_playtime = int(wintime[17:19])
                        gameClock = getTime(int(h_gametime), int(m_gametime), int(s_gametime), h_playtime, m_playtime,
                                            s_playtime)
                        player1_card.damage_dealt = round(player1_card.damage_dealt)
                        player2_card.damage_dealt = round(player2_card.damage_dealt)
                        player1_card.damage_healed = round(player1_card.damage_healed)
                        player2_card.damage_healed = round(player2_card.damage_healed)
                        try:
                            
                            if battle_config.is_pvp_game_mode:
                                if battle_config.player1_wins:
                                    pvp_response = await battle_config.pvp_victory_embed(player1, player1_card, player1_arm, player1_title, player2, player2_card)

                                else:
                                    pvp_response = await battle_config.pvp_victory_embed(player2, player2_card, player2_arm, player2_title, player1, player1_card)

                                await battle_msg.delete(delay=2)
                                await asyncio.sleep(2)
                                battle_msg = await private_channel.send(embed=pvp_response)
                                battle_config.continue_fighting = False
                                return
                        

                            # If you lose non pvp it sends message from here. Everything else is winning stuff.
                            if battle_config.player2_wins and not battle_config.is_pvp_game_mode:
                                # if not battle_config.is_abyss_game_mode:
                                play_again_buttons = [
                                    manage_components.create_button(
                                        style=ButtonStyle.blue,
                                        label="Start Over",
                                        custom_id="Yes"
                                    ),
                                    manage_components.create_button(
                                        style=ButtonStyle.red,
                                        label="End",
                                        custom_id="No"
                                    )
                                ]
                                
                                battle_config.rematch_buff = False
                                
                                if player1.guild != 'PCG':
                                    team_info = db.queryTeam({'TEAM_NAME': str(player1.guild.lower())})
                                    guild_buff_info = team_info['ACTIVE_GUILD_BUFF']
                                    if guild_buff_info == 'Rematch':
                                        battle_config.rematch_buff =True
                                
                                if battle_config.rematch_buff: #rematch update
                                    play_again_buttons.append(
                                        manage_components.create_button(
                                            style=ButtonStyle.green,
                                            label=f"Guild Rematches Available!",
                                            custom_id="grematch"
                                        )
                                    )
                                
                                elif player1.retries >= 1:
                                    play_again_buttons.append(
                                        manage_components.create_button(
                                            style=ButtonStyle.green,
                                            label=f"{player1.retries} Rematches Available!",
                                            custom_id="rematch"
                                        )
                                    )

                                else:
                                    battle_config.rematch_buff = False


                                play_again_buttons_action_row = manage_components.create_actionrow(*play_again_buttons)
                                if battle_config.is_duo_mode or battle_config.is_co_op_mode:
                                    loss_response = battle_config.you_lose_embed(player1_card, player2_card, player3_card)
                                else:
                                    loss_response = battle_config.you_lose_embed(player1_card, player2_card, None)
                                await battle_msg.delete(delay=2)
                                await asyncio.sleep(2)
                                battle_msg = await private_channel.send(embed=loss_response, components=[play_again_buttons_action_row])
    
                                def check(button_ctx):
                                    return button_ctx.author == user1

                                try:
                                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[
                                        play_again_buttons_action_row], timeout=300, check=check)

                                    if button_ctx.custom_id == "No":
                                        await battle_msg.edit(components=[])
                                        # await button_ctx.defer(ignore=True)
                                        if battle_config.is_duo_mode or battle_config.is_co_op_mode:
                                            loss_response = battle_config.you_lose_embed(player1_card, player2_card, player3_card)
                                        else:
                                            loss_response = battle_config.you_lose_embed(player1_card, player2_card, None)
                                        await battle_msg.delete(delay=2)
                                        await asyncio.sleep(2)
                                        battle_msg = await private_channel.send(embed=loss_response)
                                        battle_config.continue_fighting = False
                                        
                                        if player1.autosave and battle_config.match_can_be_saved:
                                            await button_ctx.send(embed = battle_config.saved_game_embed(player1_card, player2_card))
                                        else:
                                            await button_ctx.send(embed = battle_config.close_pve_embed(player1_card, player2_card))
                                        return

                                    if button_ctx.custom_id == "Yes":
                                        battle_config.current_opponent_number = 0
                                        battle_config.reset_game()
                                        # print(f"CURRENT OPPONENT {battle_config.current_opponent_number}")
                                        battle_config.continue_fighting = True
                                        
                                    if button_ctx.custom_id == "rematch":
                                        new_info = await crown_utilities.updateRetry(button_ctx.author.id, "U","DEC")
                                        battle_config.reset_game()
                                        battle_config.continue_fighting = True
                                    
                                    if button_ctx.custom_id == "grematch":
                                        battle_config.reset_game()
                                        new_info = await crown_utilities.guild_buff_update_function(str(player1.guild.lower()))
                                        update_team_response = db.updateTeam(new_info['QUERY'], new_info['UPDATE_QUERY'])
                                        battle_config.continue_fighting = True
                                except asyncio.TimeoutError:
                                    battle_config.continue_fighting = False
                                    if not any((battle_config.is_abyss_game_mode, 
                                                battle_config.is_scenario_game_mode, 
                                                battle_config.is_explore_game_mode, 
                                                battle_config.is_pvp_game_mode, 
                                                battle_config.is_tutorial_game_mode,
                                                battle_config.is_boss_game_mode)):
                                        await save_spot(self, player1.did, battle_config.selected_universe, battle_config.mode, battle_config.current_opponent_number)
                                        await ctx.send(embed = battle_config.saved_game_embed(player1_card,player2_card))
                                    elif any((battle_config.is_pvp_game_mode, 
                                                battle_config.is_tutorial_game_mode
                                                            )):
                                        await ctx.send(embed = battle_config.close_pvp_embed(player1_card,player2_card))
                                    else:
                                        await ctx.send(embed = battle_config.close_pve_embed(player1_card,player2_card))
                                    # if player1.autosave and battle_config.match_can_be_saved:
                                    #     await button_ctx.send(embed = battle_config.saved_game_embed(player1_card, player2_card))
                                    # else:
                                    #     await button_ctx.send(embed = battle_config.close_pve_embed(player1_card, player2_card))
                                    # return

                                # else:
                                #     if battle_config.is_duo_mode or battle_config.is_co_op_mode:
                                #         loss_response = battle_config.you_lose_embed(player1_card, player2_card, player3_card)
                                #     else:
                                #         loss_response = battle_config.you_lose_embed(player1_card, player2_card, None)
                                #     await battle_msg.delete(delay=2)
                                #     await asyncio.sleep(2)
                                #     battle_msg = await private_channel.send(embed=loss_response)
                                #     battle_config.continue_fighting = False
                                #     return

                            if battle_config.player1_wins and not battle_config.is_pvp_game_mode:
                                if any((battle_config.is_tales_game_mode, battle_config.is_dungeon_game_mode, battle_config.is_boss_game_mode)):
                                    if battle_config.is_dungeon_game_mode:
                                        drop_response = await dungeondrops(self, user1, battle_config.selected_universe, battle_config.current_opponent_number)
                                    if battle_config.is_tales_game_mode:
                                        drop_response = await drops(self, user1, battle_config.selected_universe, battle_config.current_opponent_number)
                                    if battle_config.is_boss_game_mode:
                                        drop_response = await bossdrops(self,ctx.author, battle_config.selected_universe)
                                        await battle_config.save_boss_win(player1, player1_card, player1_title, player1_arm)

                                    p1_win_rewards = await battle_config.get_win_rewards(player1)
                                    corruption_message = await battle_config.get_corruption_message(ctx)
                                    questlogger = await quest(user1, player2_card, battle_config.mode)
                                    destinylogger = await destiny(user1, player2_card, battle_config.mode)
                                    petlogger = await crown_utilities.summonlevel(player1, player1_card)
                                    cardlogger = await crown_utilities.cardlevel(user1, player1_card.name, player1.did, battle_config.mode, battle_config.selected_universe)

                                    if not battle_config.is_easy_difficulty:
                                        questlogger = await quest(user1, player2_card, battle_config.mode)
                                        destinylogger = await destiny(user1, player2_card, battle_config.mode)
                                        petlogger = await crown_utilities.summonlevel(player1, player1_card)
                                        cardlogger = await crown_utilities.cardlevel(user1, player1_card.name, player1.did, battle_config.mode, battle_config.selected_universe)
                            

                                    if battle_config.is_co_op_mode and not battle_config.is_duo_mode:
                                        if battle_config.is_dungeon_game_mode:
                                            cdrop_response = await dungeondrops(self, user2, battle_config.selected_universe, battle_config.current_opponent_number)
                                        elif battle_config.is_tales_game_mode:
                                            cdrop_response = await drops(self, user2, battle_config.selected_universe, battle_config.current_opponent_number)

                                        co_op_bonuses = battle_config.get_co_op_bonuses(player1, player3)
                                        p3_win_rewards = await battle_config.get_win_rewards(player3)
                                        p3_questlogger = await quest(user2, player2_card, battle_config.mode)
                                        p3_destinylogger = await destiny(user2, player2_card, battle_config.mode)
                                        p3_petlogger = await crown_utilities.summonlevel(player3, player3_card)
                                        p3_cardlogger = await crown_utilities.cardlevel(user2, player1_card.name, player1.did, battle_config.mode, battle_config.selected_universe)
                                        p3_co_op_bonuses = battle_config.get_co_op_bonuses(player3, player1)


                                    if battle_config.current_opponent_number != (battle_config.total_number_of_opponents):
                                        if not battle_config.is_co_op_mode:
                                            embedVar = discord.Embed(title=f"🎊 VICTORY\nThe game lasted {battle_config.turn_total} rounds.\n\n{drop_response}\nEarned {p1_win_rewards['ESSENCE']} {p1_win_rewards['RANDOM_ELEMENT']} Essence\n{corruption_message}",description=textwrap.dedent(f"""
                                            {battle_config.get_previous_moves_embed()}
                                            
                                            """),colour=0x1abc9c)
                                            if not battle_config.is_easy_difficulty:
                                                if questlogger:
                                                    embedVar.add_field(name="**Quest Progress**",
                                                        value=f"{questlogger}")
                                                if destinylogger:
                                                    embedVar.add_field(name="**Destiny Progress**",
                                                        value=f"{destinylogger}")
                                            f_message = battle_config.get_most_focused(player1_card, player2_card)
                                            embedVar.add_field(name=f"🌀 | Focus Count",
                                                            value=f"**{player2_card.name}**: {player2_card.focus_count}\n**{player1_card.name}**: {player1_card.focus_count}")
                                            #Most Damage Dealth
                                            d_message = battle_config.get_most_damage_dealt(player1_card, player2_card)
                                            embedVar.add_field(name=f":boom: | Damage Dealt",
                                                            value=f"**{player2_card.name}**: {player2_card.damage_dealt}\n**{player1_card.name}**: {player1_card.damage_dealt}")
                                            #Most Healed
                                            h_message = battle_config.get_most_damage_healed(player1_card, player2_card)
                                            embedVar.add_field(name=f":mending_heart: | Healing",
                                                            value=f"**{player2_card.name}**: {player2_card.damage_healed}\n**{player1_card.name}**: {player1_card.damage_healed}")

                                        elif battle_config.is_co_op_mode and not battle_config.is_duo_mode:
                                            embedVar = discord.Embed(title=f"👥 CO-OP VICTORY\nThe game lasted {battle_config.turn_total} rounds.\n\n👤**{player1.disname}:** {drop_response}\nEarned {p1_win_rewards['ESSENCE']} {p1_win_rewards['RANDOM_ELEMENT']} Essence\n👥**{player3.disname}:** {cdrop_response}\nEarned {p3_win_rewards['ESSENCE']} {p3_win_rewards['RANDOM_ELEMENT']} Essence",description=textwrap.dedent(f"""
                                            {battle_config.get_previous_moves_embed()}
                                            
                                            """),colour=0x1abc9c)
                                            embedVar.add_field(name="**Co-Op Bonus**",
                                                    value=f"{co_op_bonuses}")
                                            if questlogger:
                                                embedVar.add_field(name="**Quest Progress**",
                                                    value=f"{questlogger}")
                                            if destinylogger:
                                                embedVar.add_field(name="**Destiny Progress**",
                                                    value=f"{destinylogger}")
                                        
                                        elif battle_config.is_duo_mode:
                                            embedVar = discord.Embed(title=f"🎊 DUO VICTORY\nThe game lasted {battle_config.turn_total} rounds.\n\n{drop_response}\n{corruption_message}",description=textwrap.dedent(f"""
                                            {battle_config.get_previous_moves_embed()}
                                            
                                            """),colour=0x1abc9c)
                                            
                                        if battle_config.is_co_op_mode:
                                            player3_card.damage_dealt = round(player3_card.damage_dealt)
                                            player3_card.damage_healed = round(player3_card.damage_healed)
                                            f_message = battle_config.get_most_focused(player1_card, player2_card, player3_card)
                                            embedVar.add_field(name=f"🌀 | Focus Count",
                                                            value=f"**{player2_card.name}**: {player2_card.focus_count}\n**{player1_card.name}**: {player1_card.focus_count}\n**{player3_card.name}**: {player3_card.focus_count}")
                                            #Most Damage Dealth
                                            d_message = battle_config.get_most_damage_dealt(player1_card, player2_card, player3_card)
                                            embedVar.add_field(name=f":anger_right: | Damage Dealt",
                                                            value=f"**{player2_card.name}**: {player2_card.damage_dealt}\n**{player1_card.name}**: {player1_card.damage_dealt}\n**{player3_card.name}**: {player3_card.damage_dealt}")
                                            #Most Healed
                                            h_message = battle_config.get_most_damage_healed(player1_card, player2_card, player3_card)
                                            embedVar.add_field(name=f":mending_heart: | Healing",
                                                            value=f"**{player2_card.name}**: {player2_card.damage_healed}\n**{player1_card.name}**: {player1_card.damage_healed}\n**{player3_card.name}**: {player3_card.damage_healed}")

                                        if battle_config.is_dungeon_game_mode:
                                            if battle_config.crestsearch:
                                                await crown_utilities.blessguild(10000, player1.association)
                                                embedVar.add_field(name=f"**{battle_config.selected_universe} Crest Search!**",
                                                                value=f":flags:**{player1.association}** earned **100,000** :coin:")
                                        embedVar.set_author(name=f"{player2_card.name} lost!")
                                        
                                        await battle_msg.delete(delay=2)
                                        await asyncio.sleep(2)
                                        battle_msg = await private_channel.send(embed=embedVar)
                                        battle_config.reset_game()
                                        battle_config.current_opponent_number = battle_config.current_opponent_number + 1
                                        battle_config.continue_fighting = True


                                    if battle_config.current_opponent_number == (battle_config.total_number_of_opponents):
                                        if battle_config.is_dungeon_game_mode:
                                            embedVar = discord.Embed(title=f":fire: DUNGEON CONQUERED",description=f"**{battle_config.selected_universe} Dungeon** has been conquered\n\n{drop_response}\n{corruption_message}",
                                                                    colour=0xe91e63)
                                            embedVar.set_author(name=f"{battle_config.selected_universe} Boss has been unlocked!")
                                            if battle_config.crestsearch:
                                                await crown_utilities.blessguild(100000, player1.association)
                                                teambank = await crown_utilities.blessteam(100000, player1.guild)
                                                await movecrest(battle_config.selected_universe, player1.association)
                                                embedVar.add_field(name=f"**{battle_config.selected_universe}** CREST CLAIMED!",
                                                                value=f"**{player1.association}** earned the {battle_config.selected_universe} **Crest**")
                                            if questlogger:
                                                embedVar.add_field(name="**Quest Progress**",
                                                    value=f"{questlogger}")
                                            if destinylogger:
                                                embedVar.add_field(name="**Destiny Progress**",
                                                    value=f"{destinylogger}")
                                            embedVar.set_footer(text="Visit the /shop for a huge discount!")
                                            if not battle_config.is_easy_difficulty:
                                                upload_query = {'DID': str(ctx.author.id)}
                                                new_upload_query = {'$addToSet': {'DUNGEONS': battle_config.selected_universe}}
                                                r = db.updateUserNoFilter(upload_query, new_upload_query)
                                            if battle_config.selected_universe in player1.completed_dungeons:
                                                await crown_utilities.bless(300000, ctx.author.id)
                                                await battle_msg.delete(delay=2)
                                                await asyncio.sleep(2)
                                                embedVar.add_field(name="Minor Reward",
                                                            value=f"You were awarded :coin: 300,000 for completing the {battle_config.selected_universe} Dungeon again!")
                                                embedVar.add_field(name="Boss Key Aquired!",
                                                            value=f"The Boss Arena has been Unlocked!")
                                            else:
                                                await crown_utilities.bless(6000000, ctx.author.id)
                                                await battle_msg.delete(delay=2)
                                                await asyncio.sleep(2)
                                                embedVar.add_field(name="Dungeon Reward",
                                                            value=f"You were awarded :coin: 6,000,000 for completing the {battle_config.selected_universe} Dungeon!")
                                            if battle_config.is_co_op_mode and not battle_config.is_duo_mode:
                                                await crown_utilities.bless(500000, player3.did)
                                                await asyncio.sleep(2)
                                                
                                                await ctx.send(
                                                    f"{user2.mention} You were awarded :coin: 500,000 for  assisting in the {battle_config.selected_universe} Dungeon!")
                                            battle_msg = await private_channel.send(embed=embedVar)
                                            battle_config.continue_fighting = False
                                            # await discord.TextChannel.delete(private_channel, reason=None)
                                        elif battle_config.is_tales_game_mode:
                                            embedVar = discord.Embed(title=f"🎊 UNIVERSE CONQUERED",
                                                                    description=f"**{battle_config.selected_universe}** has been conquered\n\n{drop_response}\n{corruption_message}",
                                                                    colour=0xe91e63)
                                            if questlogger:
                                                embedVar.add_field(name="**Quest Progress**",
                                                    value=f"{questlogger}")
                                            if destinylogger:
                                                embedVar.add_field(name="**Destiny Progress**",
                                                    value=f"{destinylogger}")
                                            embedVar.set_footer(text=f"You can now /craft {battle_config.selected_universe} cards")
                                            if not battle_config.is_easy_difficulty:
                                                embedVar.set_author(name=f"{battle_config.selected_universe} Dungeon has been unlocked!")
                                                upload_query = {'DID': str(ctx.author.id)}
                                                new_upload_query = {'$addToSet': {'CROWN_TALES': battle_config.selected_universe}}
                                                r = db.updateUserNoFilter(upload_query, new_upload_query)
                                            if battle_config.selected_universe in player1.completed_tales:
                                                await crown_utilities.bless(100000, ctx.author.id)
                                                # await ctx.send(embed=embedVar)
                                                await battle_msg.delete(delay=2)
                                                await asyncio.sleep(2)
                                                embedVar.add_field(name="Minor Reward",
                                                            value=f"You were awarded :coin: 100,000 for completing the {battle_config.selected_universe} Tale again!")
                                            else:
                                                await crown_utilities.bless(2000000, ctx.author.id)
                                                # await ctx.send(embed=embedVar)
                                                await battle_msg.delete(delay=2)
                                                await asyncio.sleep(2)
                                                
                                                embedVar.add_field(name="Conquerors Reward",
                                                            value=f"You were awarded :coin: 2,000,000 for completing the {battle_config.selected_universe} Tale!")
                                                #battle_msg = await private_channel.send(embed=embedVar)
                                            if battle_config.is_co_op_mode and not battle_config.is_duo_mode:
                                
                                                await crown_utilities.bless(250000, player3.did)
                                                # await crown_utilities.bless(125, user2)
                                                # await ctx.send(embed=embedVar)
                                                await asyncio.sleep(2)
                                                embedVar.add_field(name="Companion Reward",
                                                            value=f"{user2.mention} You were awarded :coin: 250,000 for assisting in the {battle_config.selected_universe} Tale!")
                                                
                                            battle_msg = await private_channel.send(embed=embedVar)
                                            battle_config.continue_fighting = False


                                    if battle_config.is_boss_game_mode:
                                        wintime = time.asctime()
                                        h_playtime = int(wintime[11:13])
                                        m_playtime = int(wintime[14:16])
                                        s_playtime = int(wintime[17:19])
                                        gameClock = getTime(int(h_gametime), int(m_gametime), int(s_gametime), h_playtime, m_playtime,
                                                            s_playtime)

                                        await battle_config.save_boss_win(player1, player1_card, player1_title, player1_arm)

                                        if battle_config.is_co_op_mode:
                                            embedVar = discord.Embed(title=f":zap: **{player1_card.name}** and **{player3_card}** defeated the {battle_config.selected_universe} Boss {player2_card.name}!\nMatch concluded in {battle_config.turn_total} turns!\n\n{drop_response} + :coin: 15,000!\n\n{player3_card.name} got :coin: 10,000!", description=textwrap.dedent(f"""
                                            {battle_config.get_previous_moves_embed()}
                                            
                                            """),colour=0x1abc9c)
                                            embedVar.set_author(name=f"**{player2_card.name}** Says: {battle_config._concede_boss_description}")
                                            embedVar.add_field(name="**Co-Op Bonus**",
                                                        value=f"{p3_co_op_bonuses}")
                                        else:
                                            embedVar = discord.Embed(title=f":zap: **{player1_card.name}** defeated the {battle_config.selected_universe} Boss {player2_card.name}!\nMatch concluded in {battle_config.turn_total} turns!\n\n{drop_response} + :coin: 25,000!\n{corruption_message}",description=textwrap.dedent(f"""
                                            {battle_config.get_previous_moves_embed()}
                                            
                                            """),colour=0x1abc9c)
                                        await crown_utilities.bless(25000, str(ctx.author.id))

                                        if battle_config.crestsearch:
                                            await crown_utilities.blessguild(25000, player1.association)
                                            teambank = await crown_utilities.blessteam(5000, player1.guild)
                                            await movecrest(battle_config.selected_universe, player1.association)
                                            embedVar.add_field(name=f"**{battle_config.selected_universe} Crest Claimed**!",
                                                            value=f":flags:**{player1.association}** earned the {battle_config.selected_universe} **Crest**")
                                        embedVar.set_author(name=f"{player2_card.name} lost",
                                                            icon_url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620236432/PCG%20LOGOS%20AND%20RESOURCES/PCGBot_1.png")
                                        if int(gameClock[0]) == 0 and int(gameClock[1]) == 0:
                                            embedVar.set_footer(text=f"Battle Time: {gameClock[2]} Seconds.")
                                        elif int(gameClock[0]) == 0:
                                            embedVar.set_footer(text=f"Battle Time: {gameClock[1]} Minutes and {gameClock[2]} Seconds.")
                                        else:
                                            embedVar.set_footer(
                                                text=f"Battle Time: {gameClock[0]} Hours {gameClock[1]} Minutes and {gameClock[2]} Seconds.")
                                        # await ctx.send(embed=embedVar)
                                        # await battle_msg.delete(delay=2)
                                        # await asyncio.sleep(2)
                                        # battle_msg = await private_channel.send(embed=embedVar)


                                        await battle_config.set_boss_win(player1, player2_card)
                                        if battle_config.is_co_op_mode:
                                            await battle_config.set_boss_win(player1, player2_card, player3)
                                        battle_config.continue_fighting = False
                                    
                                    
                                if battle_config.is_abyss_game_mode:
                                    if battle_config.current_opponent_number != (battle_config.total_number_of_opponents):
                                        embedVar = discord.Embed(title=f"VICTORY\nThe game lasted {battle_config.turn_total} rounds.",description=textwrap.dedent(f"""
                                        {battle_config.get_previous_moves_embed()}
                                        
                                        """),colour=0x1abc9c)

                                        embedVar.set_author(name=f"{player2_card.name} lost!")
                                        

                                        await battle_msg.delete(delay=2)
                                        await asyncio.sleep(2)
                                        battle_msg = await private_channel.send(embed=embedVar)
                                        battle_config.reset_game()
                                        battle_config.current_opponent_number = battle_config.current_opponent_number + 1
                                        battle_config.continue_fighting = True
                                    if battle_config.current_opponent_number == (battle_config.total_number_of_opponents):
                                        await battle_config.save_abyss_win(user1, player1, player1_card)
                                        abyss_message = await abyss_level_up_message(player1.did, battle_config.abyss_floor, player2_card.name, player2_title.name, player2_arm.name)
                                        abyss_drop_message = "\n".join(abyss_message['DROP_MESSAGE'])
                                        embedVar = discord.Embed(title=f"🌑 Floor **{battle_config.abyss_floor}** Cleared\nThe game lasted {battle_config.turn_total} rounds.",description=textwrap.dedent(f"""
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

                                        embedVar.set_author(name=f"{player2_card.name} lost!")
                                        embedVar.set_footer(text=f"Traverse the **Abyss** in /solo to unlock new game modes and features!")
                                        floor_list = [0,2,3,6,7,8,9,10,20,25,40,60,100]
                                        if battle_config.abyss_floor in floor_list:
                                            embedVar.add_field(
                                            name=f"Abyssal Unlock",
                                            value=f"{abyss_message['MESSAGE']}")
                                        embedVar.add_field(
                                        name=f"Abyssal Rewards",
                                        value=f"{abyss_drop_message}")

                                        battle_msg = await private_channel.send(embed=embedVar)
                                        battle_config.continue_fighting = False

                                
                                if battle_config.is_scenario_game_mode:
                                    if battle_config.current_opponent_number != (battle_config.total_number_of_opponents):
                                        cardlogger = await crown_utilities.cardlevel(user1, player1_card.name, player1.did, "Tales", battle_config.selected_universe)

                                        embedVar = discord.Embed(title=f"VICTORY\nThe game lasted {battle_config.turn_total} rounds.",description=textwrap.dedent(f"""
                                        {battle_config.get_previous_moves_embed()}
                                        
                                        """),colour=0x1abc9c)

                                        embedVar.set_author(name=f"{player2_card.name} lost!")
                                        

                                        await battle_msg.delete(delay=2)
                                        await asyncio.sleep(2)
                                        battle_msg = await private_channel.send(embed=embedVar)
                                        battle_config.current_opponent_number = battle_config.current_opponent_number + 1
                                        battle_config.reset_game()
                                        battle_config.continue_fighting = True
                                    if battle_config.current_opponent_number == (battle_config.total_number_of_opponents):
                                        response = await scenario_drop(self, ctx, battle_config.scenario_data, battle_config.difficulty)
                                        bless_amount = 50000
                                        await crown_utilities.bless(bless_amount, player1.did)
                                        embedVar = discord.Embed(title=f"Scenario Battle Cleared!\nThe game lasted {battle_config.turn_total} rounds.",description=textwrap.dedent(f"""
                                        Good luck on your next adventure!
                                        """),colour=0xe91e63)

                                        embedVar.set_author(name=f"{player2_card.name} lost!")
                                        embedVar.add_field(
                                        name=f"Scenario Reward",
                                        value=f"{response}")

                                        await private_channel.send(embed=embedVar)

                                        battle_config.continue_fighting = False


                                if battle_config.is_explore_game_mode:
                                    explore_response =  await battle_config.explore_embed(user1, player1, player1_card, player2_card)
                                    await battle_msg.delete(delay=2)
                                    await asyncio.sleep(2)
                                    battle_msg = await private_channel.send(embed=explore_response)
                                    return

                                if battle_config.is_raid_game_mode:
                                    shield_response = battle_config.raid_victory()
                                    raid_response = await battle_config.pvp_victory_embed(player1, player1_card, player1_arm, player1_title, player2, player2_card)
                                    await battle_msg.delete(delay=2)
                                    await asyncio.sleep(2)
                                    battle_msg = await private_channel.send(embed=raid_response)
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

            except asyncio.TimeoutError:
                await battle_msg.edit(components=[])
                if not any((battle_config.is_abyss_game_mode, 
                            battle_config.is_scenario_game_mode, 
                            battle_config.is_explore_game_mode, 
                            battle_config.is_pvp_game_mode, 
                            battle_config.is_tutorial_game_mode,
                            battle_config.is_boss_game_mode)):
                    await save_spot(self, player1.did, battle_config.selected_universe, battle_config.mode, battle_config.current_opponent_number)
                    await ctx.send(embed = battle_config.saved_game_embed(player1_card,player2_card))
                elif any((battle_config.is_pvp_game_mode, 
                            battle_config.is_tutorial_game_mode
                                        )):
                    await ctx.send(embed = battle_config.close_pvp_embed(player1_card,player2_card))
                else:
                    await ctx.send(embed = battle_config.close_pve_embed(player1_card,player2_card))
                await ctx.send(f"{ctx.author.mention} {battle_config.error_end_match_message()}")
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
                # await battle_msg.delete()
                guild = self.bot.get_guild(main.guild_id)
                channel = guild.get_channel(main.guild_channel)
                await channel.send(f"'PLAYER': **{str(ctx.author)}**, 'GUILD': **{str(ctx.author.guild)}**, TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")
                return

    except asyncio.TimeoutError:
        await battle_msg.edit(components=[])
        if not any((battle_config.is_abyss_game_mode, 
                    battle_config.is_scenario_game_mode, 
                    battle_config.is_explore_game_mode, 
                    battle_config.is_pvp_game_mode, 
                    battle_config.is_tutorial_game_mode,
                    battle_config.is_boss_game_mode)):
            await save_spot(self, player1.did, battle_config.selected_universe, battle_config.mode, battle_config.current_opponent_number)
            await ctx.send(embed = battle_config.saved_game_embed(player1_card,player2_card))
        elif any((battle_config.is_pvp_game_mode, 
                    battle_config.is_tutorial_game_mode
                                )):
            await ctx.send(embed = battle_config.close_pvp_embed(player1_card,player2_card))
        else:
            await ctx.send(embed = battle_config.close_pve_embed(player1_card,player2_card))
            
        await ctx.send(f"{ctx.author.mention} {battle_config.error_end_match_message()}")
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
        #await battle_msg.delete()
        guild = self.bot.get_guild(main.guild_id)
        channel = guild.get_channel(main.guild_channel)
        await channel.send(f"'PLAYER': **{str(ctx.author)}**, 'GUILD': **{str(ctx.author.guild)}**, TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")
        return


def tactics_set_base_stats(boss_card):
    boss_card.max_base_health = boss_card.max_health


def tactics_petrified_fear_check(boss_card, player_card, battle_config):
    if boss_card.petrified_fear and boss_card.petrified_fear_counter < boss_card.petrified_fear_turns:
        boss_card.petrified_fear_counter = boss_card.petrified_fear_counter + 1
        battle_config.is_turn = 1
        petrified_fear_message = f"*{player_card.name} is petrified with fear and cannot move for [{str((boss_card.petrified_fear_turns - boss_card.petrified_fear_counter) + 1)}] turns!*"
        battle_config.add_battle_history_message(petrified_fear_message)


def tactics_bloodlust_check(boss_card, battle_config):
    if boss_card.bloodlust:
        if not boss_card.bloodlust_activated:
            if boss_card.health <= (0.75 * boss_card.max_base_health):
                print("bloodlust check")
                boss_card.bloodlust_activated = True
                boss_card.attack = boss_card.attack + 3000
                bloodlust_message = f"*{boss_card.name} is bloodlusted! Attacks will now lifesteal!*"
                battle_config.add_battle_history_message(bloodlust_message)


def tactics_enrage_check(boss_card, battle_config):
    if boss_card.enraged:
        if not boss_card.enrage_activated:
            if boss_card.health <= (0.60 * boss_card.max_base_health):
                print("enrage check")
                boss_card.enrage_activated = True
                boss_card.attack = boss_card.attack + 9999
                boss_card.defense = boss_card.defense + 3000
                boss_card.arbitrary_ap_buff = boss_card.arbitrary_ap_buff + 600
                enrage_message = f"*{boss_card.name} is enraged! Attacks will now deal much more damage to the enemy!*"
                battle_config.add_battle_history_message(enrage_message)


def tactics_intimidation_check(boss_card, player_card, battle_config):
    if boss_card.intimidation:
        if not boss_card.intimidation_activated:
            if boss_card.health <= (0.50 * boss_card.max_base_health):
                print("intimidation check")
                boss_card.intimidation_activated = True
                player_card.temporary_attack = player_card.attack
                player_card.temporary_defense = player_card.defense
                player_card.attack = 0
                player_card.defense = 0
                intimidation_message = f"*{player_card.name} is intimidated by {boss_card.name} for {str(boss_card.intimidation_turns + 1)} turns!*"
                battle_config.add_battle_history_message(intimidation_message)
        if boss_card.intimidation_activated:
            if boss_card.intimidation_turns > 0:
                boss_card.intimidation_turns = boss_card.intimidation_turns - 1
                player_card.attack = 0
                player_card.defense = 0
                intimidation_message = f"*{player_card.name} is intimidated by {boss_card.name} for {str(boss_card.intimidation_turns + 1)} turns!*"
                battle_config.add_battle_history_message(intimidation_message)
            else:
                player_card.attack = player_card.temporary_attack
                player_card.defense = player_card.temporary_defense
                boss_card.intimidation_activated = False
                boss_card.intimidation = False
                boss_card.intimidation_counter = 0
                intimidation_message = f"*{player_card.name} is no longer intimidated by {boss_card.name}!*"
                battle_config.add_battle_history_message(intimidation_message)


def tactics_damage_check(boss_card, battle_config):
    if boss_card.damage_check:
        if not boss_card.damage_check_activated:
            if boss_card.focus_count in [5]:
                boss_card.damage_check_activated = True
                boss_card.damage_check_limit = round(boss_card.max_health * .20)
                boss_card.damage_check_turns = 5
                damage_check_message = f"*{boss_card.name} is charging a fatal blow, damage it to stop the attack!\nDeal [{str(boss_card.damage_check_limit)}] damage to stop it!*"
                battle_config.add_battle_history_message(damage_check_message)
        if boss_card.damage_check_activated:
            battle_config.is_turn = 0
            battle_config.add_battle_history_message(f"*{boss_card.name} is charging a fatal blow, damage it to stop the attack!\n[{str(boss_card.damage_check_counter)} / {str(boss_card.damage_check_limit)}]\n[{str(boss_card.damage_check_turns)}] turns to go!*")


def tactics_regeneration_check(boss_card, battle_config):
    if boss_card.regeneration:
        if not boss_card.regeneration_activated:
            if battle_config.turn_total >= 50 and boss_card.health <= 0:
                print("regeneration check")
                battle_config.game_over_check = False
                boss_card.regeneration_activated = True
                boss_card.health = boss_card.max_base_health
                regeneration_message = f"*{boss_card.name} has regenerated!*"
                battle_config.add_battle_history_message(regeneration_message)


def tactics_death_blow_check(boss_card, player_card, battle_config):
    if boss_card.death_blow:
        if battle_config.turn_total in [1, 30, 60, 90, 120, 150]:
            boss_card.death_blow_activated = True

        if battle_config.turn_total in [0, 28, 29, 58, 59, 88, 89, 118, 119, 148, 149]:
            warning_message = f"*{boss_card.name} is preparing a death blow! Protect yourself with shields, parries, or barriers!*"
            battle_config.add_battle_history_message(warning_message)

        if boss_card.death_blow_activated:
            if any({player_card._shield_active, player_card._parry_active, player_card._barrier_active}):
                player_card._shield_active = False
                player_card._parry_active = False
                player_card._barrier_active = False
                player_card._shield_value = 0
                player_card._parry_value = 0
                player_card._barrier_value = 0
                player_card._arm_message = ""
                death_blow_message = f"*{boss_card.name} destroyed {player_card.name} protections with a destructive blow!*"
                battle_config.add_battle_history_message(death_blow_message)
                boss_card.death_blow_activated = False
            else:
                player_card.health = 0
                death_blow_message = f"*{boss_card.name} dealt a fatal blow to {player_card.name}!*"
                battle_config.add_battle_history_message(death_blow_message)
                boss_card.death_blow_activated = False


def tactics_stagger_check(boss_card, player_card, battle_config):
    if boss_card.stagger:
        if boss_card.stagger_activated:
            battle_config.is_turn = 1
            stagger_message = f"*{player_card.name} is staggered and cannot move!*"
            battle_config.add_battle_history_message(stagger_message)
            boss_card.stagger_activated = False



def tactics_almighty_will_check(boss_card, battle_config):
    if boss_card.almighty_will:
        if battle_config.turn_total in boss_card.almighty_will_turns:
            battle_config.is_turn = random.randint(3, 80)
            boss_card.focus_count = random.randint(3, 30)
            almighty_will_message = f"*{boss_card.name} manipulated the flow of battle!\nIt is now turn {str(battle_config.is_turn)}* and {boss_card.name} has focused {str(boss_card.focus_count)} times!"
            battle_config.add_battle_history_message(almighty_will_message)


def run_boss_tactics(player2_card, player1_card, battle_config):
    tactics_regeneration_check(player2_card, battle_config)
    tactics_death_blow_check(player2_card, player1_card, battle_config)
    tactics_stagger_check(player2_card, player1_card, battle_config)
    tactics_almighty_will_check(player2_card, battle_config)
    tactics_bloodlust_check(player2_card, battle_config)
    tactics_petrified_fear_check(player2_card, player1_card, battle_config)
    tactics_enrage_check(player2_card, battle_config)
    tactics_intimidation_check(player2_card, player1_card, battle_config)


def beginning_of_turn_stat_trait_affects(player_card, player_title, opponent_card, battle_config, companion = None):
    #If any damage happened last turn that would kill
    player_card.reset_stats_to_limiter(opponent_card)
    battle_config.add_battle_history_message(player_card.set_poison_hit(opponent_card))
    burn_turn = player_card.set_burn_hit(opponent_card)
    if burn_turn != None:
        battle_config.add_battle_history_message(player_card.set_burn_hit(opponent_card))
    battle_config.add_battle_history_message(player_card.set_bleed_hit(battle_config.turn_total, opponent_card))
    player_card.damage_dealt = round(player_card.damage_dealt)
    opponent_card.damage_dealt = round(opponent_card.damage_dealt)
    player_card.damage_healed = round(player_card.damage_healed)
    opponent_card.damage_healed = round(opponent_card.damage_healed)
    # if player_card.health <= 0:
    #     if battle_config.is_co_op_mode:
    #         if battle_config.is_turn == 0 or battle_config.is_turn == 2:
    #             return battle_config.set_game_over(player_card,opponent_card, companion)
    #         else:
    #             return battle_config.set_game_over(opponent_card,player_card, companion)
    #     else:
    #         if battle_config.is_turn == 0:
    #             return battle_config.set_game_over(player_card,opponent_card)
    #         else:
    #             return battle_config.set_game_over(opponent_card,player_card)
    #If contiune to play
    player_card.yuyu_hakusho_attack_increase()
    player_card.activate_chainsawman_trait(battle_config)
    if opponent_card.freeze_enh:
        new_turn = player_card.frozen(battle_config, opponent_card)
        battle_config.is_turn = new_turn['TURN']
        battle_config.add_battle_history_message(new_turn['MESSAGE'])
        opponent_card.freeze_enh = False
        # return new_turn
    
    player_card.set_gravity_hit()
    if not opponent_card.wind_element_activated:
        player_title.activate_title_passive(battle_config, player_card, opponent_card)
        player_card.activate_card_passive(opponent_card, battle_config)
    opponent_card.wind_element_activated = False
    player_card.activate_demon_slayer_trait(battle_config, opponent_card)
    opponent_card.activate_demon_slayer_trait(battle_config, player_card)
    player_card.activate_observation_haki_trait(battle_config, opponent_card)
    opponent_card.activate_observation_haki_trait(battle_config, player_card)
    if player_card.used_block == True:
        player_card.defense = int(player_card.defense / 2)
        player_card.used_block = False
    if player_card.used_defend == True:
        player_card.defense = int(player_card.defense / 2)
        player_card.used_defend = False
    return False



async def auto_battle_embed_and_starting_traits(ctx, player_card, opponent_card, battle_config, companion_card):
    player_card.set_battle_arm_messages(opponent_card)
    player_card.set_stat_icons()

    player_card.activate_solo_leveling_trait(battle_config, opponent_card)
            
    embedVar = discord.Embed(title=f"➡️ **Current Turn** {battle_config.turn_total}", description=textwrap.dedent(f"""\
    {battle_config.get_previous_moves_embed()}
    
    """), color=0xe74c3c)
    await asyncio.sleep(2)
    embedVar.set_thumbnail(url=ctx.author.avatar_url)
    if battle_config.is_co_op_mode or battle_config.is_duo_mode:
        footer_text = battle_config.get_battle_window_title_text(player_card,opponent_card, companion_card)
    else:
        footer_text = battle_config.get_battle_window_title_text(player_card,opponent_card)
    embedVar.set_footer(
        text=f"{footer_text}",
        icon_url="https://cdn.discordapp.com/emojis/789290881654980659.gif?v=1")

    if not battle_config.is_auto_battle_game_mode:
        embedVar.set_image(url="attachment://image.png")

    
    return embedVar


async def save_spot(self, player_id, universe, mode, currentopponent):
    try:
        user = {"DID": str(player_id)}
        query = {"$addToSet": {"SAVE_SPOT": {"UNIVERSE": universe, "MODE": str(mode), "CURRENTOPPONENT": currentopponent}}}
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
    pokemon_universes = ['Kanto Region', 'Johto Region','Hoenn Region','Sinnon Region','Kalos Region','Alola Region','Galar Region']
    decrease_value = -1
    break_value = 1
    dismantle_amount = 5000

    # Check if the difficulty is easy, return if so
    player_info = db.queryUser({'DID': str(vault['DID'])})
    if player_info['DIFFICULTY'] == "EASY":
        return

    # Set arm universe to card universe if it is part of the pokemon universes
    if card['UNIVERSE'] in pokemon_universes:
        arm_universe = card['UNIVERSE']

    # Increase decrease value and break value if arm universe doesn't match card universe
    if arm_universe != card['UNIVERSE'] and arm_universe != "Unbound":
        decrease_value = -5
        break_value = 5

    # Check if arm exists in the player's vault
    for a in vault['ARMS']:
        if a['ARM'] == str(arm['ARM']):
            current_durability = a['DUR']
            
            # Dismantle arm if its durability is 0 or below
            if current_durability <= 0:
                selected_arm = arm['ARM']
                arm_name = arm['ARM']
                selected_universe = arm_universe
                current_gems = [gems['UNIVERSE'] for gems in vault['GEMS']]

                # Update gems if selected universe exists in current gems
                if selected_universe in current_gems:
                    db.updateVault({'DID': str(vault['DID'])}, 
                                   {'$inc': {'GEMS.$[type].GEMS': dismantle_amount}},
                                   [{'type.UNIVERSE': selected_universe}])
                else:
                    db.updateVaultNoFilter({'DID': str(vault['DID'])},
                                           {'$addToSet':{'GEMS': {'UNIVERSE': selected_universe, 
                                                                  'GEMS': dismantle_amount, 
                                                                  'UNIVERSE_HEART': False, 
                                                                  'UNIVERSE_SOUL': False}}})

                # Remove arm from player's vault
                db.updateVaultNoFilter({'DID': str(vault['DID'])},
                                       {'$pull': {'ARMS': {'ARM': str(arm['ARM'])}}})

                # Update player's arm to "Stock"
                db.updateUserNoFilter({'DID': str(vault['DID'])},
                                      {'$set': {'ARM': 'Stock'}})

                return {"MESSAGE": f"**{arm['ARM']}** has been dismantled after losing all ⚒️ durability, you earn 💎 {str(dismantle_amount)}. Your arm will be **Stock** after your next match."}       


async def save_spot(self, player_id, universe, mode, currentopponent):
    try:
        user = {"DID": str(player_id)}
        query = {"$addToSet": {"SAVE_SPOT": {"UNIVERSE": universe, "MODE": str(mode), "CURRENTOPPONENT": currentopponent}}}
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
        fight_count = len(scenario['ENEMIES'])
        scenario_gold = crown_utilities.scenario_gold_drop(scenario_level,fight_count)
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
            num_of_potential_rewards = (len(rewards) - 1)
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
                return f"You're maxed out on Arms! You earned :coin:**{scenario_gold}** instead!"
            elif rewarded in owned_arms:
                return f"You already own {reward}! You earn :coin: **{scenario_gold}**."
            else:
                response = db.updateVaultNoFilter(vault_query, {'$addToSet': {'ARMS': {'ARM': rewarded, 'DUR': 100}}})
                return f"You earned _Arm:_ {reward} with ⚒️**{str(100)} Durability** and :coin: **{scenario_gold}**!"
        else:
            card = db.queryCard({"NAME": rewarded})
            u = await main.bot.fetch_user(str(ctx.author.id))
            response = await crown_utilities.store_drop_card(str(ctx.author.id), card["NAME"], card["UNIVERSE"], vault, owned_destinies, 3000, 1000, mode, False, 0, "cards")
            response = f"{response}\nYou earned :coin: **{scenario_gold}**!"
            if not response:
                await crown_utilities.bless(15000, str(ctx.author.id))
                return f"You earned :coin: **{scenario_gold}**!"
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


async def drops(self, player, universe, matchcount):
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
    rift_rate = 140  # 150
    rematch_rate = 175 #175
    title_drop = 190  # 190
    arm_drop = 195  # 195
    pet_drop = 198  # 198
    card_drop = 200  # 200
    drop_rate = random.randint((0 + (rebirth * 10) ), 200)
    durability = random.randint(1, 45)
    if difficulty == "HARD":
        mode = "Purchase"
        gold_drop = 60
        rift_rate = 80
        rematch_rate = 100
        title_drop = 150  
        arm_drop = 170
        pet_drop = 190  
        card_drop = 200 
        drop_rate = random.randint(0 + (rebirth * 15), 200)
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
                response = await crown_utilities.store_drop_card(player.id, titles[rand_title], universe, vault, owned_destinies, 150, 150, "mode", False, 0, "titles")
                return response
            else:
                await crown_utilities.bless(150, player.id)
                return f"You earned :coin: **150**!"
        elif drop_rate <= arm_drop and drop_rate > title_drop:
            if all_available_drop_arms:
                response = await crown_utilities.store_drop_card(player.id, arms[rand_arm], universe, vault, durability, 2000, 2000, "mode", False, 0, "arms")
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
                response = await crown_utilities.store_drop_card(player.id, cards[rand_card], universe, vault, owned_destinies, 3000, 1000, "mode", False, 0, "cards")
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


    gold_drop = 125  #
    rift_rate = 150  #
    rematch_rate = 250
    title_drop = 300  #
    arm_drop = 350  #
    pet_drop = 380  #
    card_drop = 400  #
    drop_rate = random.randint((0 + (rebirth * 20) ), 400)
    durability = random.randint(10, 75)
    mode="Dungeon"
    if difficulty == "HARD":
        gold_drop = 30  
        rift_rate = 55
        rematch_rate = 180
        title_drop = 210  
        arm_drop = 240  
        pet_drop = 270  
        card_drop = 300 
        drop_rate = random.randint((0 + (rebirth * 15)), 300)
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
            response = await crown_utilities.store_drop_card(player.id, titles[rand_title], universe, vault, owned_destinies, 30000, 30000,"mode", False, 0, "titles")
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
            response = await crown_utilities.store_drop_card(player.id, arms[rand_arm], universe, vault, durability, 3000, 3000,"mode", False, 0, "arms")
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
            response = await crown_utilities.store_drop_card(player.id, cards[rand_card], universe, vault, owned_destinies, 5000, 2500,"mode", False, 0, "cards")
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

    drop_rate = random.randint((0 + (rebirth * 25)), 500)
    durability = random.randint(100, 150)
    if difficulty == "HARD":
        gold_drop = 125  #
        rematch_drop = 150 #330
        title_drop = 200  #
        arm_drop = 230  #
        pet_drop = 270  #
        card_drop = 310  #
        boss_title_drop = 350  #
        boss_arm_drop = 370  #
        boss_pet_drop = 395  #
        boss_card_drop = 400  #

        drop_rate = random.randint((0 + (rebirth * 25)), 400)
    durability = random.randint(150, 200)

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
            response = await crown_utilities.store_drop_card(player.id, titles[rand_title], universe, vault, owned_destinies, 30000, 30000, "Dungeon", False, 0, "titles")
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
            response = await crown_utilities.store_drop_card(player.id, arms[rand_arm], universe, vault, durability, 40000, 40000, "Dungeon", False, 0, "arms")
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
            response = await crown_utilities.store_drop_card(player.id, cards[rand_card], universe, vault, owned_destinies, 500000, 500000, "Dungeon", False, 0, "cards")
            return response
        elif drop_rate <= boss_title_drop and drop_rate > card_drop:
            # if len(vault['TITLES']) >= 25:
            #     await crown_utilities.bless(10000000, player.id)
            #     return f"You're maxed out on Titles! You earned :coin: **10,000,000** instead!"
            # response = db.updateVaultNoFilter(vault_query, {'$addToSet': {'TITLES': str(boss_title)}})
            # return f"You earned the Exclusive Boss Title: {boss_title}!"
            u = await main.bot.fetch_user(player.id)
            response = await crown_utilities.store_drop_card(player.id, boss_title, universe, vault, owned_destinies, 50000, 50000, "Boss", False, 0, "titles")
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
            response = await crown_utilities.store_drop_card(player.id, boss_arm, universe, vault, durability, 9000000, 9000000, "Boss", False, 0, "arms")
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
            response = await crown_utilities.store_drop_card(player.id, boss_card, universe, vault, owned_destinies, 30000, 10000, "Boss", False, 0, "cards")
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
'GROWTH': 'Lose 10% Max Health, Increase Attack, Defense and AP Buffs',
'STANCE': 'Swap your Attack & Defense, Increase Defense',
'CONFUSE': 'Swap Opponent Attack & Defense, Decrease Opponent Defense',
'BLINK': 'Decrease your  Stamina, Increase Target Stamina',
'SLOW': 'Increase Opponent Stamina, Decrease Your Stamina then Swap Stamina with Opponent',
'HASTE': 'Increase your Stamina, Decrease Opponent Stamina then Swap Stamina with Opponent',
'FEAR': 'Lose 10% Max Health, Decrease Opponent Attack, Defense and AP Buffs',
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


element_mapping = {
'PHYSICAL': 'If ST(stamina) greater than 80, Deals Bonus Damage. After 3 Strike gain a Parry',
'FIRE': 'Does 50% damage of previous attack over the next opponent turns, stacks.',
'ICE': 'Every 2 attacks, opponent freezes and loses 1 turn.',
'WATER': 'Increases all water move AP by 100 Flat.',
'EARTH': 'Cannot be Parried. Increases Def by 25% AP. Grants Shield - Increase by 50% DMG',
'ELECTRIC': 'Add 35% DMG Dealt to Shock damage, added to all Move AP.',
'WIND': 'On Miss, Use Wind Attack, boosts all wind damage by 35% of damage dealt.',
'PSYCHIC': 'Penetrates Barriers. Reduce opponent ATK & DEF by 35% DMG. After 3 Hits Gain a Barrier',
'DEATH': 'Deals 45% DMG to opponent max health. Gain Attack equal to that amount.',
'LIFE': 'Create Max Health and Heal for 35% DMG.',
'LIGHT': 'Regain 50% ST(Stamina) Cost, Illumination Increases ATK by 50% of DMG.',
'DARK': 'Penetrates Shields, Barriers and Parries & decreases opponent ST(Stamina) by 15.',
'POISON': 'Penetrates shields, Poison 30 damage stacking up to (150 * Card Tier).',
'RANGED': 'If ST(stamina) greater than 30, Deals 1.7x Damage. Every 4 Ranged Attacks Increase Hit Chance by 5%',
'SPIRIT': 'Has higher 35% higher chance of Crit.',
'RECOIL': 'Deals Incredible Bonus Damage, take 60% as recoil. If Recoil would kill you reduce HP to 1',
'TIME': 'Block and Increase Turn Count by 3, If ST(Stamina) is < 50, Focus for 1 Turn.',
'BLEED': 'Every 2 Attacks deal 10x turn count damage to opponent.',
'GRAVITY': 'Disables Opponent Block, Reduce opponent DEF by 50% DMG, Decrease Turn Count By 3.'
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
