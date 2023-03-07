import discord
from discord.embeds import Embed
from discord.ext import commands
import bot as main
import time
now = time.asctime()
import crown_utilities
import db
import classes as dclass
import dataclasses as data
from .classes.player_class import Player
from .classes.card_class import Card
from .classes.title_class import Title
from .classes.arm_class import Arm
from .classes.summon_class import Summon
from .classes.battle_class  import Battle
import messages as m
import numpy as np
import help_commands as h
# Converters
from discord import User
from discord import Member
from PIL import Image, ImageFont, ImageDraw
import requests
from collections import ChainMap

from io import BytesIO
import io
import unique_traits as ut
import DiscordUtils
import textwrap
from .crownunlimited import  enhancer_mapping, title_enhancer_mapping, enhancer_suffix_mapping, title_enhancer_suffix_mapping, passive_enhancer_suffix_mapping, battle_commands
from collections import Counter
from discord_slash import cog_ext, SlashContext
from dinteractions_Paginator import Paginator
from discord_slash import SlashCommand
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle
from crown_utilities import crest_dict



emojis = ['👍', '👎']

class Lookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Lookup Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    
    @cog_ext.cog_slash(description="Lookup player stats", guild_ids=main.guild_ids)
    async def player(self, ctx, player = None):
        await ctx.defer()
        a_registered_player = await crown_utilities.player_check(ctx)
        if not a_registered_player:
            return

        try:
            if player:
                player = player.replace("<","")
                player = player.replace(">","")
                player = player.replace("@","")
                player = player.replace("!","")
                
                
                user = await self.bot.fetch_user(player)
                avi = user.avatar_url
                # print(player)
                # print(str(ctx.author.id))
            else:
                player = ctx.author.id
                avi = ctx.author.avatar_url
            query = {'DID': str(player)}
            
            d = db.queryUser(query)
            
            m = db.queryManyMatchesPerPlayer({'PLAYER': d['DISNAME']})
            v = db.queryVault({'DID': str(player)})
            b = db.queryAllBosses()
            user = await self.bot.fetch_user(d['DID'])
            if d:
                balance = v['BALANCE']
                bal_icon = ":coin:"
                if balance >= 50000000:
                    bal_icon = ":money_with_wings:"
                elif balance >= 10000000:
                    bal_icon = ":moneybag:"
                elif balance >= 500000:
                    bal_icon = ":dollar:"

                bal_message = f"{bal_icon}{'{:,}'.format(balance)}"

                all_cards = len(v['CARDS'])
                all_titles = len(v['TITLES'])
                all_arms = len(v['ARMS'])
                all_pets = len(v['PETS'])
                cstorage = len(v['STORAGE'])
                astorage = len(v['ASTORAGE'])
                tstorage = len(v['TSTORAGE'])

                name = d['DISNAME'].split("#",1)[0]
                difficulty = d['DIFFICULTY']
                games = d['GAMES']
                abyss_level = d['LEVEL']
                if abyss_level > 100:
                    abyss_level = "**Conquered**"
                retries = d['RETRIES']
                card = d['CARD']
                ign = d['IGN']
                team = d['TEAM']
                guild = d['GUILD']
                patreon = d['PATRON']
                autosave_message = "🔴 Off"
                autosave = d['AUTOSAVE']
                if autosave:
                    autosave_message = "*🟢 On*"
                    
                performance_message = "🔴 Off"
                performance = d['PERFORMANCE']
                if performance:
                    performance_message = "*🟢 On*"
                    
                explore_message = "🔴 Off"
                explore = d['EXPLORE']
                if explore:
                    explore_location = d['EXPLORE_LOCATION']
                    location = "All"
                    if explore_location != "NULL":
                        location = explore_location
                    explore_message = f"🟢 *Exploring {location}*"
                if abyss_level <=25:
                    explore_message = f"*Unlock After Abyss 25*"
                    

                    
                purse_message = ""
                purse = d['TOURNAMENT_WINS']
                if purse == 1:
                    purse_message = "👛 | **Gabe's Purse** Activated"
                    
                patreon_message = ""
                if patreon == True:
                    patreon_message = "**💞 | Patreon Supporter**"
                
                rift_message = "*🔴 Closed*"
                rift = d['RIFT']
                if rift == 1:
                    rift_message = "*🟢 On*"
                if team != "PCG":
                    team_info = db.queryTeam({'TEAM_NAME' : str(team.lower())})
                    guild = team_info['GUILD']
                    guild_buff = team_info['ACTIVE_GUILD_BUFF']
                    guild_buff_active = team_info['GUILD_BUFF_ON']
                    if guild_buff == "Rift" and guild_buff_active:
                        rift_message = "*🟢 Guild Buff On*"
                
                family = d['FAMILY'] 
                family_info = db.queryFamily({"HEAD": str(family)})
                if family_info:
                    family_summon = family_info['SUMMON']
                    family_summon_name = family_summon['NAME']
                fs_message = ""
                if d['FAMILY_PET']:
                    fs_message = f":family_mwgb: | **Family Summon** *{family_summon_name}*"
                titles = d['TITLE']
                arm = d['ARM']
                battle_history = d['BATTLE_HISTORY']

                avatar = d['AVATAR']
                matches = d['MATCHES']
                crown_tales = d['CROWN_TALES']
                dungeons = d['DUNGEONS']
                bosses = d['BOSS_WINS']
                pvp_wins = d['PVP_WINS']
                pvp_loss = d['PVP_LOSS']
                pet = d['PET']
                rebirth = d['REBIRTH']
                join_raw = d['TIMESTAMP']
                year_joined = join_raw[20:]
                day_joined = join_raw[:10]
                prestige = d['PRESTIGE']
                
                aicon = ":new_moon:"
                if prestige == 1:
                    aicon = ":waxing_crescent_moon:"
                elif prestige == 2:
                    aicon = ":first_quarter_moon:"
                elif prestige == 3:
                    aicon = ":waxing_gibbous_moon:"
                elif prestige == 4:
                    aicon = ":full_moon:"
                elif prestige == 5:
                    aicon = ":waning_gibbous_moon:"
                elif prestige == 6:
                    aicon = ":last_quarter_moon:"
                elif prestige == 7:
                    aicon = ":waning_crescent_moon:"
                elif prestige == 8:
                    aicon = ":crescent_moon:"
                elif prestige == 9:
                    aicon = ":crown:"
                elif prestige >= 10:
                    aicon = ":japanese_ogre:"
                prestige_message = "*No Prestige*"
                if prestige > 0 :
                    prestige_message = f"**Prestige:** *{prestige}*"
                #print(day_joined + " " + year_joined)
                birthday = f"🎉 | Registered on {day_joined}, {year_joined}"
                icon = ':heart_on_fire:'
                if rebirth == 0:
                    icon = ':triangular_flag_on_post:'
                elif rebirth >= 6:
                    icon = '👼'
                elif rebirth >= 10:
                    icon = ':man_fairy:'
                else:
                    icon = ':man_fairy:'

                talisman = d['TALISMAN']
                talisman_message = "No Talisman Equipped"
                if talisman == "NULL":
                    talisman_message = "No Talisman Equipped"
                else:
                    for t in v["TALISMANS"]:
                        if t["TYPE"].upper() == talisman.upper():
                            talisman_emoji = crown_utilities.set_emoji(talisman.upper())
                            talisman_durability = t["DUR"]
                    talisman_message = f"📿| **{talisman_emoji} {talisman.title()}** ⚒️ {talisman_durability}"

                pvp_matches = []
                boss_matches = []
                dungeon_matches = []
                tales_matches = []
                most_played_card = []
                most_played_card_message = "_No Data For Analysis_"
                match_history_message = ""
                most_universe_played = []
                most_played_universe_message = "_No Data For Analysis_"

                wlmatches = list(d['MATCHES'][0].values())[0]
                wins = wlmatches[0]
                losses = wlmatches[1]
                if m:
                    for match in m:
                        most_played_card.append(match['CARD'])
                        if match['UNIVERSE_TYPE'] == "Tales":
                            tales_matches.append(match)
                            most_universe_played.append(match['UNIVERSE'])
                        elif match['UNIVERSE_TYPE'] == "Dungeon":
                            dungeon_matches.append(match)
                            most_universe_played.append(match['UNIVERSE'])
                        elif match['UNIVERSE_TYPE'] == "Boss":
                            boss_matches.append(match)
                            most_universe_played.append(match['UNIVERSE'])
                        elif match['UNIVERSE_TYPE'] == "PVP":
                            pvp_matches.append(match)
                            
                    
                    
                    if not most_universe_played or len(most_universe_played) < 10:
                        most_played_universe_message = "_No Data For Analysis_"
                    if not most_played_card:
                        most_played_card_message = "_No Data For Analysis_"
                    else:
                        card_main = most_frequent(most_played_card)
                        fav_uni = most_frequent(most_universe_played)
                        most_played_card_message = f"**Most Played Card: **{card_main}"
                        most_played_universe_message = f"**Favorite Universe: **{fav_uni}"
                        match_history_message = f"""
                        **Tales Played: **{'{:,}'.format(int(len(tales_matches)))}
                        **Dungeons Played: **{'{:,}'.format(len(dungeon_matches))}
                        **Bosses Played: **{'{:,}'.format(len(boss_matches))}
                        **Pvp Played: **{'{:,}'.format(len(pvp_matches))}
                        """

                crown_list = []
                for crown in crown_tales:
                    if crown != "":
                        crown_list.append(f"**{crest_dict[crown]} |** {crown}")
                
                dungeon_list = []
                for dungeon in dungeons:
                    if dungeon != "":
                        dungeon_list.append(f"**{crest_dict[dungeon]} |** {dungeon}")

                boss_list =[]
                uni = "Unbound"
                for boss in bosses:
                    if boss != "":
                        boss_info = db.queryBoss({'NAME': str(boss)})
                        uni = boss_info['UNIVERSE']
                        boss_list.append(f"**{crest_dict[uni]} |** {boss}")

                matches_to_string = dict(ChainMap(*matches))
                ign_to_string = dict(ChainMap(*ign))
                
                



                embed1 = discord.Embed(title=f"{name}'s Profile".format(self), description=textwrap.dedent(f"""\
                {aicon} | **Abyss Rank**: {abyss_level}
                :heart_on_fire: | **Rebirth**: {rebirth}
                
                :flower_playing_cards: | **Card:** {card}
                :reminder_ribbon:** | Title:** {titles}
                :mechanical_arm: | **Arm:** {arm}
                🧬 | **Summon:** {pet}
                {talisman_message}

                :flags: | **Association: ** {guild}
                :military_helmet: | **Guild:** {team} 
                :family_mwgb: | **Family:** {family}
                """), colour=discord.Color.green())
                embed1.set_thumbnail(url=avatar)
                
                embed2 = discord.Embed(title=f"{name}'s Settings".format(self), description=textwrap.dedent(f"""\
                🆚 | **Retries:** {retries} available
                :crystal_ball: | **Rift:** {rift_message}
                :milky_way: | **Explore:** {explore_message}
                
                ⚙️ | **Battle History Setting:** {str(battle_history)} messages
                ⚙️ | **Difficulty:** {difficulty.lower().capitalize()}
                ⚙️ | **Performance:** {performance_message}
                
                :floppy_disk: | **Autosave:** {autosave_message}
                """), colour=discord.Color.darker_grey())
                embed2.set_thumbnail(url=avatar)
                
                embed5 = discord.Embed(title=f"{name}'s Stats".format(self), description=textwrap.dedent(f"""\
                ⚔️ | **Tales Played: **{'{:,}'.format(int(len(tales_matches)))}
                🔥 | **Dungeons Played: **{'{:,}'.format(len(dungeon_matches))}
                👹 | **Bosses Played: **{'{:,}'.format(len(boss_matches))}
                
                🆚 | **Pvp Played: **{'{:,}'.format(len(pvp_matches))}
                📊 | **Pvp Record: ** :regional_indicator_w: **{pvp_wins}** / :regional_indicator_l: **{pvp_loss}**
                """), colour=discord.Color.red())
                embed5.set_thumbnail(url=avatar)
                
                embed3 = discord.Embed(title=f"{name}'s Vault".format(self), description=textwrap.dedent(f"""\
                **Balance** | {bal_message}
                :flower_playing_cards: | **Cards:** {all_cards} ~ :briefcase: *{cstorage}*
                :reminder_ribbon: | **Titles:** {all_titles} ~ :briefcase: *{tstorage}*
                :mechanical_arm: | **Arms:** {all_arms} ~ :briefcase: *{astorage}*
                🧬 | **Summons:** {all_pets}
                {fs_message}
                {purse_message}
                """), colour=discord.Color.dark_purple())
                embed3.set_thumbnail(url=avatar)
                
                embed6 = discord.Embed(title=f"{name}'s Avatar".format(self), description=textwrap.dedent(f"""\
                    **:bust_in_silhouette: | User:** {user.mention}
                    {aicon} | {prestige_message}
                    :military_medal: | {most_played_card_message}
                    :earth_africa: | {most_played_universe_message}
                    {patreon_message}
                """), colour=000000)
                embed6.set_image(url=avi)
                embed6.set_footer(text=f"{birthday}")
                if crown_list:
                    embed4 = discord.Embed(title=f"{name}'s Achievements".format(self), description=":bank: | Party Chat Gaming Database™️", colour=discord.Color.gold())
                    embed4.set_thumbnail(url=avatar)
                    embed4.add_field(name=":medal: | " + "Completed Tales" , value="\n".join(crown_list))
                    if dungeon_list:
                        embed4.add_field(name=":fire: | " + "Completed Dungeons", value="\n".join(dungeon_list))
                        if boss_list:
                            embed4.add_field(name=":japanese_ogre: | " + "Boss Souls",value="\n".join(boss_list))
                        else:
                            embed4.add_field(name=":japanese_ogre: | " + "Boss Souls", value="No Boss Souls Collected, yet!")
                    else:
                        embed4.add_field(name=":fire: | " + "Completed Dungeons", value="No Dungeons Completed, yet!")
                        embed4.add_field(name=":japanese_ogre: | " + "Boss Souls", value="No Boss Souls Collected, yet!")
                else:
                    embed4 = discord.Embed(title=f"{name}'s Achievements".format(self), description=":bank: Party Chat Gaming Database™️", colour=discord.Color.gold())
                    embed4.set_thumbnail(url=avatar)
                    embed4.add_field(name="Completed Tales" + " :medal:", value="No Completed Tales, yet!")
                    embed4.add_field(name="Completed Dungeons" + " :fire: ", value="No Dungeons Completed, yet!")
                    embed4.add_field(name="Boss Souls" + " :japanese_ogre: ", value="No Boss Souls Collected, yet!")

                embeds = [embed6, embed1, embed5, embed3, embed2,embed4]
                await Paginator(bot=self.bot, ctx=ctx, pages=embeds, timeout=60).run()
            else:
                await ctx.send(m.USER_NOT_REGISTERED)
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
            await ctx.send("There's an issue with your lookup command. Check with support.")
            return

    
    @cog_ext.cog_slash(description="Lookup Guild stats", guild_ids=main.guild_ids)
    async def guild(self, ctx, guild = None):
        a_registered_player = await crown_utilities.player_check(ctx)
        if not a_registered_player:
            return

        try:
            if guild:
                team_name = guild.lower()
                team_query = {'TEAM_NAME': team_name}
                team = db.queryTeam(team_query)
                team_display_name = team['TEAM_DISPLAY_NAME']
                if team:
                    team_name = team['TEAM_NAME']
                    team_display_name = team['TEAM_DISPLAY_NAME']
                else:
                    await ctx.send("Guild does not exist")
                    return
            else:
                user = db.queryUser({'DID': str(ctx.author.id)})
                team = db.queryTeam({'TEAM_NAME': user['TEAM'].lower()})
                if team:
                    team_name = team['TEAM_NAME']
                    team_display_name = team['TEAM_DISPLAY_NAME']
                else:
                    await ctx.send("You are not a part of a Guild.")
                    return

            if team:
                is_owner = False
                is_officer = False
                is_captain = False
                is_member = False
                user = db.queryUser({'DID': str(ctx.author.id)})

                owner = team['OWNER']
                shielding = team['SHIELDING']
                owner_data = db.queryUser({'DISNAME': owner})
                owner_object = await self.bot.fetch_user(owner_data['DID'])
                officers = team['OFFICERS']
                captains = team['CAPTAINS']
                members = team['MEMBERS']
                member_count = len(members)
                formatted_list_of_members = []
                formatted_list_of_officers = []
                formatted_list_of_captains = []
                formatted_owner = ""
                for member in members:
                    index = members.index(member)
                    if user['DISNAME'] == member:
                        is_member = True

                    if member in officers:
                        formatted_name = f"🅾️ [{str(index)}] **{member}**"
                        formatted_list_of_officers.append(formatted_name)
                    elif member in captains:
                        formatted_name = f"🇨 [{str(index)}] **{member}**"
                        formatted_list_of_captains.append(formatted_name)
                    elif member == owner:
                        formatted_name = f"👑 [{str(index)}] **{member}**"
                        formatted_owner = formatted_name
                    elif member not in officers and member not in captains and member != owner:
                        formatted_name = f"🔰 [{str(index)}] **{member}**"
                        formatted_list_of_members.append(formatted_name)

                members_list_joined = ", ".join(formatted_list_of_members)
                captains_list_joined = ", ".join(formatted_list_of_captains)
                officers_list_joined = ", ".join(formatted_list_of_officers)
                if user['DISNAME'] in officers:
                    is_officer = True
                elif user['DISNAME'] in captains:
                    is_captain = True
                elif user['DISNAME'] == owner:
                    is_owner = True
                elif user['DISNAME'] in  members:
                    is_member = True

                transactions = team['TRANSACTIONS']
                transactions_embed = ""
                if transactions:
                    transactions_len = len(transactions)
                    if transactions_len >= 10:
                        transactions = transactions[-10:]
                        transactions_embed = "\n".join(transactions)
                    else:
                        transactions_embed = "\n".join(transactions)
                
                storage = team['STORAGE']
                balance = team['BANK']

                guild_buff_available = team['GUILD_BUFF_AVAILABLE']
                guild_buff_on = team['GUILD_BUFF_ON']
                gbon_status = ""
                if guild_buff_on:
                    gbon_status ="🟢"
                else:
                    gbon_status ="🔴"
                guild_buffs = team['GUILD_BUFFS']
                active_guild_buff = team['ACTIVE_GUILD_BUFF']
                active_guild_buff_use_cases = ""
                guild_buff_message = ""
                guild_buff_message_active = "No Active Guild Buff"
                if guild_buff_available:
                    guild_buff_message = "Guild Buff Available"
                    if active_guild_buff:
                        for buff in guild_buffs:
                            if buff['TYPE'] == active_guild_buff:
                                active_guild_buff_use_cases = str(buff['USES'])
                        guild_buff_message_active = f"{gbon_status} {active_guild_buff} Buff: {active_guild_buff_use_cases} uses left!"

                else:
                    guild_buff_message = "No Guild Buff Available"
                
                association = team['GUILD']
                
                association_msg = f"{association}"
                
                if shielding:
                    association_msg= f":shield: {association}"
                
                hall_info = db.queryHall({'HALL': 'Mine'})
                hall_img = hall_info['PATH']
                hall_name = hall_info['HALL']
                split = hall_info['SPLIT']
                if association != "PCG":
                    association_info = db.queryGuildAlt({"GNAME" :str(association)})
                    hall = association_info['HALL']
                    hall_info = db.queryHall({'HALL':str(hall)})
                    hall_name = hall_info['HALL']
                    hall_img = hall_info['PATH']
                    split = hall_info['SPLIT']
                else:
                    association = "Not Associated */oath to create association*"

                tournament_wins = team['TOURNAMENT_WINS']
                wins = team['WINS']
                losses = team['LOSSES']
                in_war = team['WAR_FLAG']
                war_opponent = team['WAR_OPPONENT']
                war_wins = team['WAR_WINS']
                war_message = ""
                if in_war:
                    war_message = "Guild in War"
                else:
                    war_message = "No Guild War"
                


                guild_mission = team['GUILD_MISSION']
                completed_missions = team['COMPLETED_MISSIONS']
                guild_mission_message = ""
                if guild_mission:
                    guild_mission_message = "Guild Mission Active"
                else:
                    guild_mission_message = "No Active Guild Mission"


                icon = "💳"
                guild = team['GUILD']


                first_page = discord.Embed(title=f"{team_display_name}", description=textwrap.dedent(f"""
                👑 **Owner** 
                {formatted_owner}
                
                🅾️ **Officers**
                {officers_list_joined}
                
                🇨 **Captains**
                {captains_list_joined}
                
                **Guild Membership Count** 
                {member_count}
                
                **Association**
                {association_msg}
                
                **Guild Buff**
                {guild_buff_message}
                
                **Active Buff**
                {guild_buff_message_active}
                
                **Bank** 
                {icon} {'{:,}'.format(balance)}
                """), colour=0x7289da)
                # first_page.set_footer(text=f"")
                
                membership_pages = discord.Embed(title=f"Members", description=textwrap.dedent(f"""
                🔰 **Members**
                {members_list_joined}
               
                """), colour=0x7289da)

                
                guild_mission_embed = discord.Embed(title=f"Guild Missions", description=textwrap.dedent(f"""
                **Guild Mission** *Coming Soon*
                {guild_mission_message}
                **Completed Guild Missions**
                {str(completed_missions)}
               
                """), colour=0x7289da)


                war_embed = discord.Embed(title=f"Guild War", description=textwrap.dedent(f"""
                **War** *Coming Soon*
                {war_message}
                **Wars Won**
                {str(war_wins)}
               
                """), colour=0x7289da)
                
                activity_page = discord.Embed(title="Recent Guild Activity", description=textwrap.dedent(f"""
                {transactions_embed}
                """), colour=0x7289da)
                
                association_page = discord.Embed(title="Association", description=textwrap.dedent(f"""
                **:flags: Association** | {association}
                **:shinto_shrine: Hall** | {hall_name}
                **:yen: Split** | Earn **{split}x** :coin: per match!
                """), colour=0x7289da)
                association_page.set_image(url=hall_img)
                
                
                guild_explanations = discord.Embed(title=f"Information", description=textwrap.dedent(f"""
                **Buff Explanations**
                - **Quest Buff**: Start Quest from the required fight in the Tale, not for dungeons
                - **Level Buff**: Each fight will grant you a level up
                - **Stat Buff**: Add 50 ATK & DEF, 30 AP, and 100 HLT
                - **Rift Buff**: Rifts will always be available
                - **Rematch Buff**: Unlimited Rematches
                **Guild Position Explanations**
                - **Owner**:  All operations */guildoperations*
                - **Officer**:  Can Add members, Delete members, Pay members, Buy, Swap, and Toggle Buffs
                - **Captain**:  Can Toggly Buffs, Pay members
                - **Member**:  No operations
                """), colour=0x7289da)

                embed_list = [first_page, membership_pages, guild_mission_embed, war_embed, association_page, activity_page, guild_explanations]

                buttons = [] 



                

                if not is_member:
                    buttons.append(
                        manage_components.create_button(style=3, label="Apply", custom_id="guild_apply")
                    )
                
                if is_owner:
                    buttons = [
                        manage_components.create_button(style=3, label="Buff Toggle", custom_id="guild_buff_toggle"),
                        manage_components.create_button(style=3, label="Buff Swap", custom_id="guild_buff_swap"),
                        manage_components.create_button(style=3, label="Buff Shop", custom_id="guild_buff_shop"),
                    ]

                elif is_officer:
                    buttons = [
                        manage_components.create_button(style=3, label="Buff Toggle", custom_id="guild_buff_toggle"),
                        manage_components.create_button(style=3, label="Buff Swap", custom_id="guild_buff_swap"),
                        manage_components.create_button(style=3, label="Buff Shop", custom_id="guild_buff_shop"),
                    ]

                elif is_captain:
                    buttons = [
                        manage_components.create_button(style=3, label="Buff Toggle", custom_id="guild_buff_toggle"),
                    ]

                elif is_member and not is_owner and not is_captain and not is_officer:
                    buttons = [
                        manage_components.create_button(style=2, label="Close", custom_id="Q")
                    ]


                custom_action_row = manage_components.create_actionrow(*buttons)


                async def custom_function(self, button_ctx):
                    if button_ctx.author == ctx.author:
                        if button_ctx.custom_id == "guild_apply":
                            await button_ctx.defer(ignore=True)
                            await apply(self, ctx, owner_object)
                            self.stop = True
                            return
                        elif button_ctx.custom_id == "Q":
                            self.stop = True
                            return
                        elif button_ctx.custom_id == "guild_buff_toggle":
                            if guild_buff_available:
                                response = guild_buff_toggle(user, team)
                                if response:
                                    await button_ctx.send(f"{response['MSG']}")
                                else:
                                    await button_ctx.send("Error in toggling buff. Please seek support https://discord.gg/yWAD5HkDXU")
                                self.stop = True
                            else:
                                await button_ctx.send(f"No Active Guild Buff.")
                        
                        elif button_ctx.custom_id == "guild_buff_swap":
                            if guild_buff_available:
                                await button_ctx.defer(ignore=True)
                                await main.buffswap(ctx, user, team)
                                self.stop = True
                            else:
                                await button_ctx.send(f"No Active Guild Buff.")

                        elif button_ctx.custom_id == "guild_buff_shop":
                            await button_ctx.defer(ignore=True)
                            await main.buffshop(ctx, user, team)
                            self.stop = True
                        self.stop = True
                    else:
                        await button_ctx.send("Not your button bucko")
                        self.stop = True


                await Paginator(bot=self.bot, useQuitButton=True, disableAfterTimeout=True, ctx=ctx, pages=embed_list, timeout=60, customActionRow=[
                    custom_action_row,
                    custom_function,
                ]).run()
                
            else:
                await ctx.send(m.TEAM_DOESNT_EXIST)
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
    
    
    @cog_ext.cog_slash(description="Lookup Association", guild_ids=main.guild_ids)
    async def association(self, ctx, association = None):
        a_registered_player = await crown_utilities.player_check(ctx)
        if not a_registered_player:
            return
        
        in_guild = False
        is_visitor = False
        guild_query = {}
        try:
            if association:   
                guild_name = association
                guild_query = {'GNAME': guild_name}
                guild = db.queryGuildAlt(guild_query)
                founder_name = ""
                if guild:
                    guild_name = guild['GNAME']
                else:
                    await ctx.send("Association does not exist.")
                    return
            else:
                user = db.queryUser({'DID': str(ctx.author.id)})
                team = db.queryTeam({'TEAM_NAME': user['TEAM'].lower()})
                guild = db.queryGuildAlt({'GNAME': team['GUILD']})
                if guild:
                    guild_name = guild['GNAME']
                    in_guild = True
                else:
                    await ctx.send("Your Guild is not Associated.")
                    return
                
            if guild:
                is_founder = False
                is_sworn = False
                is_shield = False
                is_guild_leader = False
                member = False
                betrayed = False
                
                hall = db.queryHall({'HALL' : guild['HALL']})
                hall_name = hall['HALL']
                hall_multipler = hall['MULT']
                hall_split = hall['SPLIT']
                hall_fee = hall['FEE']
                hall_def = hall['DEFENSE']
                hall_img = hall['PATH']
                
                guild_name = guild['GNAME']
                guild_query = {'GNAME': guild_name}
                founder_name = guild['FOUNDER']
                f_DID = guild['FDID']
                w_DID = guild['WDID']
                s_DID = guild['SDID']
                sworn_name = guild['SWORN']
                if guild['WDID'] == "BETRAYED":
                    betrayed = True
                    
                shield_name = guild['SHIELD']
                shield_info = db.queryUser({'DID' : s_DID})
                shield_card = shield_info['CARD']
                shield_arm = shield_info['ARM']
                shield_title = shield_info['TITLE']
                shield_rebirth = shield_info['REBIRTH']
                
                streak = guild['STREAK']
                crest = guild['CREST']
                balance = guild['BANK']
                bounty = guild['BOUNTY']
                bonus = int((streak/100) * bounty)
                
                estates = guild['ESTATES']
                estates_list = []
                estate_data_list = []
                for halls in estates:
                    hall_data = db.queryHall({'HALL': halls})
                    estates_list.append(halls)
                    estate_data_list.append(hall_data)
                    
                estates_list_joined = ", ".join(estates_list)
                
                picon = ":shield:"
                sicon = ":beginner:"
                
                icon = ":coin:"
                if balance >= 2000000000:
                    icon = ":money_with_wings:"
                elif balance >=1000000000:
                    icon = ":moneybag:"
                elif balance >= 500000000:
                    icon = ":dollar:"
                    
                if streak >= 100:
                    sicon = ":skull_crossbones:"     
                elif streak >= 50:
                    sicon = ":skull:"
                elif streak >=25:
                    sicon = ":ghost:"
                elif streak >= 10:
                    sicon = ":diamond_shape_with_a_dot_inside:"
                    
                
                

                sword_list = []
                owner_list = []
                owner_name_list = []
                sword_member_list = []
                sword_count = 0
                blade_count = 0
                total_blade_count = 0
                for swords in guild['SWORDS']:
                    index = guild['SWORDS'].index(swords)
                    blade_count = 0
                    sword_count = sword_count + 1
                    sword_team = db.queryTeam({'TEAM_NAME': swords})
                    swords_name = sword_team['TEAM_DISPLAY_NAME']
                    dubs = sword_team['WINS']
                    els = sword_team['LOSSES']
                    owner = sword_team['OWNER']
                    owner_DID = sword_team['DID']
                    
                    officers = sword_team['OFFICERS']
                    captains = sword_team['CAPTAINS']
                    members = sword_team['MEMBERS']
                    owner_list.append(f"{owner_DID}")
                    
                    if owner_DID == f_DID:
                        owner_name_list.append(f"🪆 | [{str(index)}] **{owner}** *{sword_team['TEAM_DISPLAY_NAME']}*")
                    elif owner_DID == w_DID:
                        owner_name_list.append(f"🎎 | [{str(index)}] **{owner}** *{sword_team['TEAM_DISPLAY_NAME']}*")
                    elif owner_DID == s_DID:
                        owner_name_list.append(f"👺 | [{str(index)}] **{owner}** *{sword_team['TEAM_DISPLAY_NAME']}*")
                    else:
                        owner_name_list.append(f"👑 | [{str(index)}] **{owner}** *{sword_team['TEAM_DISPLAY_NAME']}*")
                    for blades in sword_team['MEMBERS']:
                        bindex = sword_team['MEMBERS'].index(blades)
                        blade_count = blade_count + 1
                        total_blade_count = total_blade_count + 1
                        if blades in officers:
                            formatted_name = f"**🅾️ [{str(index)}{str(bindex)}]** {blades}"
                            sword_member_list.append(formatted_name)
                        elif blades in captains:
                            formatted_name = f"**🇨 [{str(index)}{str(bindex)}** {blades}"
                            sword_member_list.append(formatted_name)
                        elif blades == owner:
                            formatted_name = f"**👑 [{str(index)}{str(bindex)}] {blades}**"
                            formatted_owner = formatted_name
                            sword_member_list.append(formatted_owner)
                        elif blades not in officers and blades not in captains and blades != owner:
                            formatted_name = f"**🔰 [{str(index)}{str(bindex)}]** *{blades}*"
                            sword_member_list.append(formatted_name)
                        #sword_member_list.append(f":knife: [{str(index)}{str(bindex)}] **{blades}**")
                    sword_bank = sword_team['BANK']
                    sword_list.append(f"~ {swords_name} ~ W**{dubs}** / L**{els}**\n:coin: | **Bank: **{'{:,}'.format(sword_bank)}\n:knife: | **Members: **{blade_count}\n_______________________")
                    
                guild_owner_list_joined = "\n".join(owner_name_list)
                members_list_joined =  " | ".join(sword_member_list)
                crest_list = []
                for c in crest:
                    crest_list.append(f"{crown_utilities.crest_dict[c]} | {c}")
                
                # print(ctx.author.id)
                # print(f_DID)
                # print(w_DID)
                # print(s_DID)
                if in_guild:
                    member = True
                
                if str(ctx.author.id) == f_DID:
                    is_founder = True
                    is_guild_leader = True
                    member = True
                elif str(ctx.author.id) == w_DID:
                    is_sworn = True
                    is_guild_leader = True
                    member = True
                elif str(ctx.author.id) == s_DID:
                    is_shield = True
                    if str(ctx.author.id) in owner_list:
                        is_guild_leader = True
                    member = True
                elif str(ctx.author.id) in owner_list:
                    is_guild_leader = True
                    member = True
                    
                elif member == False:
                    is_visitor = True

                transactions = guild['TRANSACTIONS']
                transactions_embed = ""
                if transactions:
                    transactions_len = len(transactions)
                    if transactions_len >= 10:
                        transactions = transactions[-10:]
                        transactions_embed = "\n".join(transactions)
                    else:
                        transactions_embed = "\n".join(transactions)

                # embed1 = discord.Embed(title=f":flags: {guild_name} Guild Card - {icon}{'{:,}'.format(balance)}".format(self), description=":bank: Party Chat Gaming Database", colour=000000)
                # if guild['LOGO_FLAG']:
                #     embed1.set_image(url=logo)
                # embed1.add_field(name="Founder :dolls:", value= founder_name.split("#",1)[0], inline=True)
                # embed1.add_field(name="Sworn :dolls:", value= sworn_name.split("#",1)[0], inline=True)
                main_page = discord.Embed(title= f"{guild_name}".format(self), description=textwrap.dedent(f"""\
                :flags: | **Association:** {guild_name}
                {icon} | **Bank:** {icon}{'{:,}'.format(balance)}
                :nesting_dolls: | **Founder: ~** {founder_name.split("#",1)[0]}
                :dolls: | **Sworn: ~** {sworn_name.split("#",1)[0]}
                :japanese_goblin: | **Shield: ~**{shield_name.split("#",1)[0].format(self)}
                :ninja: | **Guilds: **{sword_count}
                :secret: | **Universe Crest: **{len(crest_list)} 
                    
                :shinto_shrine: | **Hall: **{hall_name}
                """), colour=000000)
                main_page.set_image(url=hall_img)
                main_page.set_footer(text=f"/ally to join the {guild_name} Association")
                
                arena_page = discord.Embed(title= f"Hall Information".format(self), description=textwrap.dedent(f"""\
                :flags: | **{guild_name} Raid Arena**
                :coin: | **Raid Fee: **{'{:,}'.format(hall_fee)}
                :yen: | **Bounty: **{'{:,}'.format(bounty)}
                :moneybag: | **Victory Bonus: **{'{:,}'.format(bonus)}
                
                {sicon} | **Victories: **{streak}
                :japanese_goblin: | **Shield: ~**{shield_name.split("#",1)[0].format(self)}
                :flower_playing_cards: | **Card: **{shield_card}
                :reminder_ribbon: | **Title: **{shield_title}
                :mechanical_arm: | **Arm: **{shield_arm}
                    
                :shinto_shrine: | **Hall: **{hall_name} 
                :shield: | **Raid Defenses: **{hall_def} 
                """), colour=000000)
                arena_page.set_image(url=hall_img)
                arena_page.set_footer(text=f"/raid {guild_name} - Raid Association")
                
                guilds_page = discord.Embed(title=f"Guild Information".format(self), description=f":flags: |  {guild_name} **Guild** List\n⛩️ | Guilds Earn **{hall_split}x**:coin:\n:bank: |  Party Chat Gaming Database", colour=000000)
                guilds_page.add_field(name=f":military_helmet: Guilds | **:ninja: ~ {sword_count}/:knife: {total_blade_count}**", value="\n".join(f'**{t}**'.format(self) for t in sword_list), inline=False)
                guilds_page.set_footer(text=f"/guild - View Association Guild")
                
                crest_page = discord.Embed(title=f"Universe Crest".format(self), description=f":flags: |  {guild_name} **Universe Crest**\n:bank: |  Party Chat Gaming Database", colour=000000)
                crest_page.add_field(name=f":secret: | **OWNED**", value="\n".join(f'**{c}**'.format(self) for c in crest_list), inline=False)
                crest_page.set_footer(text=f"Earn Universe Crest in Dungeons and Boss Fights!")
                
                activity_page = discord.Embed(title="Recent Association Activity", description=textwrap.dedent(f"""
                {transactions_embed}
                """), colour=0x7289da)
                
                ghost_page = discord.Embed(title=f"Guild Owners", description=textwrap.dedent(f"""
                👑 **Guild Leaders** | *Guilds Sworn To {guild['GNAME']}*
                {guild_owner_list_joined}
               
                """), colour=0x7289da)
                ghost_page.set_footer(text=f"/player - Lookup Guild Owners")

                blades_page = discord.Embed(title=f"Association Members List", description=textwrap.dedent(f"""
                👑 **Owner** | Guild Owner
                🇨  **Captains** | Guild Captains
                🅾️ **Officers** | Guild Officers
                🔰 **Members** | Guild Members
    
                {members_list_joined}
               
                """), colour=0x7289da)
                blades_page.set_footer(text=f"/player - Lookup Guild Members")
                
                estates_page = discord.Embed(title=f"Halls", description=textwrap.dedent(f"""
                ⛩️ | **Halls**
                {estates_list_joined}
               
                """), colour=0x7289da)
                estates_page.set_footer(text=f"/halls - View Hall List")
                
                
                war_embed = discord.Embed(title=f"Association War", description=textwrap.dedent(f"""
                **War** *Coming Soon*
                *None*

                **Wars Won**
                0
               
                """), colour=0x7289da)
                war_embed.set_footer(text=f"Association Wars Coming Soon")
                
                association_mission_page = discord.Embed(title=f"Association Missions", description=textwrap.dedent(f"""
                **Association Mission** *Coming Soon*
                *None*

                **Completed Association Missions**
                0
               
                """), colour=0x7289da)
                association_mission_page.set_footer(text=f"Association Missions Coming Soon")
                
                association_explanations = discord.Embed(title=f"Information", description=textwrap.dedent(f"""
                **Assocation Explanations**
                - **Earnings**: Associations earn coin for every PVP Match or Dungeon/Boss Encounter
                - **Splits**: Each Guild earns a % of the Wages Earned during these battles determined by the type of Hall
                - **Sponser**: Associations Leaders can sponsor Guilds with Association Funds
                - **Fund**: Invest money into Association from Guild
                - **Halls**: Give Coin Multipliers and Wage Multiplier in all game modes towards Association Earnings
                - **Raid Fee**: Cost to Raid this Association (Determined by Hall)
                - **Hall Defense**:  Give Bonus Defense Multiplier to Shield During Raids
                - **Bounty**: Other Associated players can raid to aquire the Bounty
                - **Victory Bonus**: Each Succesful Shield Defense increases the bounty and Victory Bonus
                - **Real Estate**: Own multiple Halls, swap your current Hall buy and sell real estate.
                - **Guild Armory**: Members share the Armory: Store Cards, Titles and Arms for all Members
                - **Armory Draw**: /armory to draw items from the Armory
                

                **Association Position Explanations**
                - **Founder**:  All operations.
                - **Sworn**:  All operations
                - **Shield**: Can set Raid Bounty, Swap Hideouts, and Knight other Blades
                - **Kids**:  Can equip family summon.
                """), colour=0x7289da)
                association_explanations.set_footer(text=f"/help for more information on Associations")
                
                # if guild['LOGO_FLAG']:
                #     embed3.set_image(url=logo)
                
                embed_list = [main_page, arena_page, crest_page, guilds_page, ghost_page, blades_page, estates_page, association_mission_page, war_embed, activity_page, association_explanations]
                # paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
                # paginator.add_reaction('⏮️', "first")
                # paginator.add_reaction('⬅️', "back")
                # paginator.add_reaction('🔐', "lock")
                # paginator.add_reaction('➡️', "next")
                # paginator.add_reaction('⏭️', "last")
                # embeds = [embed1,embed2, embed3]
                # await paginator.run(embeds)
                
                buttons = [] 
                # print(member)
                # print(is_visitor)
                # print(is_founder)
                # print(is_sworn)
                # print(is_guild_leader)
                if is_visitor:
                    buttons.append(
                        manage_components.create_button(style=3, label="Say Hello", custom_id="hello"),
                        manage_components.create_button(style=3, label="Raid!", custom_id="raid")
                    )
                    
                if is_founder or is_sworn:
                    buttons = [
                        manage_components.create_button(style=3, label="Check/Purchase Halls", custom_id="property"),
                        manage_components.create_button(style=3, label="View/Update Armory", custom_id="armory"),
                        manage_components.create_button(style=3, label="Test Shield Defenses", custom_id="raid")
                    ]
                # elif is_sworn:
                #     buttons = [
                #         manage_components.create_button(style=3, label="Check Properties", custom_id="property"),
                #     ]
                    
                elif is_shield:
                    buttons = [
                        manage_components.create_button(style=3, label="View Properties", custom_id="property"),
                        manage_components.create_button(style=3, label="View/Update Armory", custom_id="armory"),
                        manage_components.create_button(style=3, label="Shield Training", custom_id="raid")
                    ]
                    
                elif is_guild_leader:
                    buttons = [
                        manage_components.create_button(style=3, label="View Properties", custom_id="property"),
                        manage_components.create_button(style=3, label="View Armory", custom_id="armory"),
                        manage_components.create_button(style=3, label="Claim The Shield!", custom_id="raid")
                    ]
                    
                custom_action_row = manage_components.create_actionrow(*buttons)
                async def custom_function(self, button_ctx):
                    try:
                        await button_ctx.defer(ignore=True)
                        if button_ctx.author == ctx.author:
                            if button_ctx.custom_id == "hello":
                                guild_query = {"GNAME": guild['GNAME']}
                                #await button_ctx.defer(ignore=True)
                                update_query = {
                                        '$push': {'TRANSACTIONS': f":wave: | {button_ctx.author} said 'Hello'!"}
                                    }
                                response = db.updateGuildAlt(guild_query, update_query)
                                await ctx.send(f"**{button_ctx.author.mention}** Said Hello to **{guild['GNAME']}**!")
                                self.stop = True
                                return
                            if button_ctx.custom_id == "raid":
                                guild_query = {"GNAME": guild['GNAME']}
                                #await button_ctx.defer(ignore=True)
                                update_query = {
                                        '$push': {'TRANSACTIONS': f":crossed_swords: | {button_ctx.author} Raided!"}
                                    }
                                response = db.updateGuildAlt(guild_query, update_query)
                                await raid(button_ctx, guild['GNAME'])
                                self.stop = True
                                return
                            elif button_ctx.custom_id == "property":
                                #await button_ctx.defer(ignore=True)
                                real_estate_message = " "
                                property_buttons = []
                                balance_message = '{:,}'.format(guild['BANK'])
                                if is_founder:
                                    real_estate_message = "\nWelcome Great Founder!\n**View Property** - View Owned Properties or make a Move!\n**Buy New Hall** - Buy a new Hall for your Association\n**Browse Hall Catalog** - View all Properties for sale"
                                    property_buttons = [
                                    manage_components.create_button(style=2, label="Owned Properties", custom_id="equip"),
                                    manage_components.create_button(style=3, label="Buy/Sell Halls", custom_id="buy"),
                                    manage_components.create_button(style=1, label="Browse Hall Catalog", custom_id="browse"),
                                    manage_components.create_button(style=ButtonStyle.red, label="Quit", custom_id="q")
                                    
                                ]
                                elif is_sworn:
                                    real_estate_message = "\nWelcome Holy Sworn!\n**View Property** - View Owned Properties or make a Move!\n**Buy New Hall** - Buy a new Hall for your Association\n**Browse Hall Catalog** - View all Properties for sale"
                                    property_buttons = [
                                    manage_components.create_button(style=2, label="Owned Properties", custom_id="equip"),
                                    manage_components.create_button(style=3, label="Buy/Sell Halls", custom_id="buy"),
                                    manage_components.create_button(style=1, label="Browse Hall Catalog", custom_id="browse"),
                                    manage_components.create_button(style=ButtonStyle.red, label="Quit", custom_id="q")
                                ]
                                elif is_shield:
                                    real_estate_message = "\nWelcome Noble Shield!\n**View Property** - View Owned Properties or make a Move!\n**Browse Hall Catalog** - View all Properties for sale"
                                    property_buttons = [
                                    manage_components.create_button(style=1, label="Owned Properties", custom_id="equip"),
                                    manage_components.create_button(style=1, label="Browse Hall Catalog", custom_id="browse"),
                                    manage_components.create_button(style=ButtonStyle.red, label="Quit", custom_id="q")
                                ]
                                elif is_guild_leader:
                                    real_estate_message = "\nWelcome Oathsworn!\n**View Property** - View Owned Properties\n**Browse Hall Catalog** - View all Properties for sale"
                                    property_buttons = [
                                    manage_components.create_button(style=1, label="View Properties", custom_id="view"),
                                    manage_components.create_button(style=1, label="Browse Hall Catalog", custom_id="browse"),
                                    manage_components.create_button(style=ButtonStyle.red, label="Quit", custom_id="q")
                                ]
                                property_action_row = manage_components.create_actionrow(*property_buttons)
                                real_estate_screen = discord.Embed(title=f"Anime VS+ Real Estate", description=textwrap.dedent(f"""\
                                {real_estate_message}
                                *Current Association Bank*:
                                :coin: **{balance_message}**
                                """), color=0xe74c3c)
                                real_estate_screen.set_image(url="https://thumbs.gfycat.com/FormalBlankGeese-max-1mb.gif")
                                
                                msg = await ctx.send(embed=real_estate_screen, components=[property_action_row])
                                def check(button_ctx):
                                    return button_ctx.author == ctx.author
                                try:
                                    hall_embed_list = []
                                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[property_action_row], timeout=120, check=check)
                                    if button_ctx.custom_id == "q":
                                        await ctx.send("Real Estate Menu Closed...")
                                        return
                                    if button_ctx.custom_id == "browse":
                                        await button_ctx.defer(ignore=True)
                                        all_halls = db.queryAllHalls()
                                        for hall in all_halls:
                                            hall_name = hall['HALL']
                                            hall_price = hall['PRICE']
                                            price_message = '{:,}'.format(hall['PRICE'])
                                            hall_img = hall['PATH']
                                            hall_multiplier = hall['MULT']    
                                            hall_fee = '{:,}'.format(hall['FEE'])
                                            hall_split = hall['SPLIT']
                                            hall_def = hall['DEFENSE']                                       
                                            embedVar = discord.Embed(title= f"{hall_name}", description=textwrap.dedent(f"""
                                            💰 | **Price**: {price_message}
                                            〽️ | **Multiplier**: {hall_multiplier}
                                            :dollar: | **Split**: {hall_split}
                                            :yen: | **Raid Fee**: {hall_fee}
                                            :shield: | **Defenses**: {hall_def}
                                            
                                            **Association** earns **{hall_multiplier}x** :coin: per match!
                                            **Raids** cost **{hall_fee}** :coin:!
                                            **Guilds** earn **{hall_split}x** :coin: per match! 
                                            **Shield** Defense Boost: :shield:**{hall_def}x**
                                            """))
                                            embedVar.set_image(url=hall_img)
                                            hall_embed_list.append(embedVar)
                                        await Paginator(bot=self.bot, ctx=ctx, useQuitButton=True, deleteAfterTimeout=True, pages=hall_embed_list).run()
                                    if button_ctx.custom_id == "view":
                                        await button_ctx.defer(ignore=True)
                                        for hall in estate_data_list:
                                            hall_name = hall['HALL']
                                            hall_price = hall['PRICE']
                                            price_message = '{:,}'.format(hall['PRICE'])
                                            hall_img = hall['PATH']
                                            hall_multiplier = hall['MULT']    
                                            hall_fee = '{:,}'.format(hall['FEE'])
                                            hall_split = hall['SPLIT']
                                            hall_def = hall['DEFENSE']                                            
                                            embedVar = discord.Embed(title= f"{hall_name}", description=textwrap.dedent(f"""
                                            💰 | **Price**: {price_message}
                                            〽️ | **Multiplier**: {hall_multiplier}
                                            :dollar: | **Split**: {hall_split}
                                            :yen: | **Raid Fee**: {hall_fee}
                                            :shield: | **Defenses**: {hall_def}
                                            
                                            **Association** earns **{hall_multiplier}x** :coin: per match!
                                            **Raids** cost **{hall_fee}** :coin:!
                                            **Guilds** earn **{hall_split}x** :coin: per match! 
                                            **Shield** Defense Boost: :shield:**{hall_def}x**
                                            """))
                                            embedVar.set_image(url=hall_img)
                                            hall_embed_list.append(embedVar)
                                        await Paginator(bot=self.bot, ctx=ctx, useQuitButton=True, deleteAfterTimeout=True, pages=hall_embed_list).run()
                                    elif button_ctx.custom_id == "equip":
                                        await button_ctx.defer(ignore=True)
                                        for hall in estate_data_list:
                                            hall_name = hall['HALL']
                                            hall_price = hall['PRICE']
                                            price_message = '{:,}'.format(hall['PRICE'])
                                            hall_img = hall['PATH']
                                            hall_multiplier = hall['MULT']    
                                            hall_fee = '{:,}'.format(hall['FEE'])
                                            hall_split = hall['SPLIT']
                                            hall_def = hall['DEFENSE']                                               
                                            embedVar = discord.Embed(title= f"{hall_name}", description=textwrap.dedent(f"""
                                            💰 | **Price**: {price_message}
                                            〽️ | **Multiplier**: {hall_multiplier}
                                            :dollar: | **Split**: {hall_split}
                                            :yen: | **Raid Fee**: {hall_fee}
                                            :shield: | **Defenses**: {hall_def}
                                            
                                            **Association** earns **{hall_multiplier}x** :coin: per match!
                                            **Raids** cost **{hall_fee}** :coin:!
                                            **Guilds** earn **{hall_split}x** :coin: per match! 
                                            **Shield** Defense Boost: :shield:**{hall_def}x**
                                            """))
                                            embedVar.set_image(url=hall_img)
                                            hall_embed_list.append(embedVar)
                                            
                                        equip_buttons = [
                                            manage_components.create_button(style=3, label="⛩️ Equip Hall", custom_id="equip"),

                                        ]
                                        equip_action_row = manage_components.create_actionrow(*equip_buttons)
                                        async def equip_function(self, button_ctx):
                                            hall_name = str(button_ctx.origin_message.embeds[0].title)
                                            guild_query = {'GNAME': guild['GNAME']}
                                            await button_ctx.defer(ignore=True)
                                            if button_ctx.author == ctx.author:
                                                if button_ctx.custom_id == "equip":
                                                    transaction_message = f"⛩️ | {ctx.author} changed the Association Hall to **{str(button_ctx.origin_message.embeds[0].title)}**."
                                                    update_query = {
                                                            '$set': {'HALL': hall_name},
                                                            '$push': {'TRANSACTIONS': transaction_message}
                                                        }
                                                    response = db.updateGuildAlt(guild_query, update_query)
                                                    await ctx.send(f"**{guild['GNAME']}** moved into their **{hall_name}**! This is much better suited for your current needs!")
                                                    self.stop = True
                                            else:
                                                await ctx.send("This is not your command.")
                                        await Paginator(bot=self.bot, ctx=ctx, useQuitButton=True, deleteAfterTimeout=True, pages=hall_embed_list, customActionRow=[
                                            equip_action_row,
                                            equip_function,
                                        ]).run()
                                                                                    
                                    elif button_ctx.custom_id == "buy":
                                        ahll_embed_list = []
                                        all_halls = db.queryAllHalls()
                                        owned = False
                                        current_savings = '{:,}'.format(guild['BANK'])
                                        for hall in all_halls:
                                            hall_name = hall['HALL']
                                            hall_price = hall['PRICE']
                                            price_message = '{:,}'.format(hall['PRICE'])
                                            hall_img = hall['PATH']
                                            hall_multiplier = hall['MULT']    
                                            hall_fee = '{:,}'.format(hall['FEE'])
                                            hall_split = hall['SPLIT']
                                            hall_def = hall['DEFENSE']       
                                            ownership_message = f"💰 **Price**: {price_message}"  
                                            sell_price = hall_price *.80
                                            sell_message = " "
                                            sell_message = f"💱 Sells for **{'{:,}'.format(hall['PRICE'])}**"                                  
                                            embedVar = discord.Embed(title= f"{hall_name}", description=textwrap.dedent(f"""
                                            **Current Bank**: :coin: **{current_savings}**                                                                    
                                            {ownership_message}
                                            
                                            💰 | **Price**: {price_message}
                                            〽️ | **Multiplier**: {hall_multiplier}
                                            :dollar: | **Split**: {hall_split}
                                            :yen: | **Raid Fee**: {hall_fee}
                                            :shield: | **Defenses**: {hall_def}
                                            
                                            **Association** earns **{hall_multiplier}x** :coin: per match!
                                            **Raids** cost **{hall_fee}** :coin:!
                                            **Guilds** earn **{hall_split}x** :coin: per match! 
                                            **Shield** Defense Boost: :shield:**{hall_def}x**
                                            
                                            {sell_message}
                                            """))
                                            embedVar.set_image(url=hall_img)
                                            hall_embed_list.append(embedVar)
                                        
                                        econ_buttons = [
                                            manage_components.create_button(style=3, label="💰 Buy Hall", custom_id="buy"),
                                            manage_components.create_button(style=3, label="💱 Sell Hall", custom_id="sell"),

                                        ]
                                        econ_action_row = manage_components.create_actionrow(*econ_buttons)
                                        
                                        async def econ_function(self, button_ctx):
                                            hall_name = str(button_ctx.origin_message.embeds[0].title)
                                            await button_ctx.defer(ignore=True)
                                            if button_ctx.author == ctx.author:
                                                if button_ctx.custom_id == "buy":
                                                    if hall_name in estates_list:
                                                        await ctx.send("You already own this Hall. Click 'Sell' to sell it!")
                                                        self.stop = True
                                                        return
                                                    if hall_name == 'Mine':
                                                        await button_ctx.send("You already own your **Memorial Mine.**")
                                                        #self.stop = True
                                                        return
                                                    try: 
                                                        hall = db.queryHall({'HALL': {"$regex": f"^{str(hall_name)}$", "$options": "i"}})
                                                        currentBalance = guild['BANK']
                                                        cost = hall['PRICE']
                                                        hall_name = hall['HALL']
                                                        if hall:
                                                            if hall_name == guild['HALL']:
                                                                await ctx.send(m.USERS_ALREADY_HAS_HALL, delete_after=5)
                                                            else:
                                                                newBalance = currentBalance - cost
                                                                if newBalance < 0 :
                                                                    await ctx.send("You have an insufficent Balance")
                                                                else:
                                                                    guild_query = {'GNAME': guild['GNAME']}
                                                                    await crown_utilities.curseguild(cost, guild['GNAME'])
                                                                    transaction_message = f":coin: | {ctx.author} bought a new **{str(button_ctx.origin_message.embeds[0].title)}**."
                                                                    response = db.updateGuildAlt(guild_query,{'$set':{'HALL': str(hall_name)},'$push': {'TRANSACTIONS': transaction_message}})
                                                                    response2 = db.updateGuildAlt(guild_query,{'$addToSet':{'ESTATES': str(hall_name)}})
                                                                    await ctx.send(m.PURCHASE_COMPLETE_H + "Enjoy your new Hall!")
                                                                    return
                                                        else:
                                                            await ctx.send("Hall does not exist")
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
                                                if button_ctx.custom_id == "sell":
                                                    hall = db.queryHall({'HALL': {"$regex": f"^{str(hall_name)}$", "$options": "i"}})
                                                    cost = hall['PRICE']
                                                    formatted_cost = '{:,}'.format(cost)
                                                    if hall_name not in guild['ESTATES']:
                                                        await ctx.send("You need to Own this Hall to to sell it!")
                                                        #self.stop = True
                                                        return
                                                    if hall_name == guild['HALL']:
                                                        await button_ctx.send("You cannot sell your **Designated Hall**.")
                                                        #self.stop = True
                                                        return
                                                    if hall_name == 'Mine':
                                                        await button_ctx.send("You cannot sell your **Memorial Mine.**")
                                                        #self.stop = True
                                                        return
                                                    elif hall_name in guild['ESTATES']:
                                                        await crown_utilities.blessGuild(cost, guild['GNAME'])
                                                        transaction_message = f":coin: | {ctx.author} sold the Association Hall: **{str(hall_name)}**."
                                                        response = db.updateGuildAlt(guild_query,{'$pull':{'ESTATES': str(hall_name)},'$push': {'TRANSACTIONS': transaction_message}})
                                                        await ctx.send(f"{guild['GNAME']} sold their **{hall_name}** for **{formatted_cost}**")
                                                        #self.stop = True
                                                        return
                                            else:
                                                await ctx.send("This is not your command.")
                                        await Paginator(bot=self.bot, ctx=ctx, useQuitButton=True, deleteAfterTimeout=True, pages=hall_embed_list, customActionRow=[
                                            econ_action_row,
                                            econ_function,
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
                            elif button_ctx.custom_id == "armory":
                                #await button_ctx.defer(ignore=True)
                                armory_message = " "
                                armory_buttons = []
                                balance_message = '{:,}'.format(guild['BANK'])
                                if is_founder:
                                    armory_message = "\nnWelcome Great Founder!\n**View Armory** - View Items in Armory\n**Upgrade Armory** - Upgrade Armory\n**Donate Gear** - Donate Cards, Titles or Arms to the Armory"
                                    armory_buttons = [
                                    manage_components.create_button(style=2, label="View Armory", custom_id="view"),
                                    manage_components.create_button(style=3, label="Upgrade Armory", custom_id="upgrade"),
                                    manage_components.create_button(style=1, label="Donate Gear", custom_id="donate"),
                                    
                                ]
                                elif is_sworn:
                                    armory_message = "\nWelcome Holy Sword!\n**View Armory** - View Items in Armory\n**Upgrade Armory** - Upgrade Armory\n**Donate Gear** - Donate Cards, Titles or Arms to the Armory"
                                    armory_buttons = [
                                    manage_components.create_button(style=2, label="View Armory", custom_id="view"),
                                    manage_components.create_button(style=3, label="Upgrade Armory", custom_id="upgrade"),
                                    manage_components.create_button(style=1, label="Donate Gear", custom_id="donate"),
                                ]
                                elif is_shield:
                                    armory_message = "\nWelcome Noble Shield!\n**View Armory** - View Items in Armory\n**Upgrade Armory** - Upgrade Armory\n**Donate Gear** - Donate Cards, Titles or Arms to the Armory"
                                    armory_buttons = [
                                    manage_components.create_button(style=2, label="View Armory", custom_id="view"),
                                    manage_components.create_button(style=3, label="Upgrade Armory", custom_id="upgrade"),
                                    manage_components.create_button(style=1, label="Donate Gear", custom_id="donate"),
                                    
                                ]
                                elif is_guild_leader:
                                    armory_message = "\nWelcome Oathsworn!\n**View Armory** - View Items in Armory\n**Donate Gear** - Donate Cards, Titles or Arms to the Armory"
                                    armory_buttons = [
                                    manage_components.create_button(style=2, label="View Armory", custom_id="view"),
                                    manage_components.create_button(style=1, label="Donate Gear", custom_id="donate"),
                                    
                                ]
                                elif member:
                                    armory_message = "\nWelcome Member!\n**View Armory** - View Items in Armory\n**Donate Gear** - Donate Cards, Titles or Arms to the Armory"
                                    armory_buttons = [
                                    manage_components.create_button(style=2, label="View Armory", custom_id="view"),
                                    manage_components.create_button(style=1, label="Donate Gear", custom_id="donate"),
                                    
                                ]
                                armory_action_row = manage_components.create_actionrow(*armory_buttons)
                                armory_screen = discord.Embed(title=f"{guild['GNAME']} Armory!", description=textwrap.dedent(f"""\
                                {armory_message}
                                 
                                🕋 **Armory Inventory** | 300
                                🎴 **Cards** |  {len(guild['CSTORAGE'])}
                                🎗️ **Titles** |  {len(guild['TSTORAGE'])}
                                🦾 **Arms** |  {len(guild['ASTORAGE'])}
                                """), color=0xe74c3c)
                                armory_screen.set_image(url="https://cdnb.artstation.com/p/assets/images/images/036/549/141/original/jonathan-dodd-mdz2-large-warehouse-port.gif?1617957276")
                                
                                msg = await ctx.send(embed=armory_screen, components=[armory_action_row])
                                def check(button_ctx):
                                    return button_ctx.author == ctx.author
                                try:
                                    #await button_ctx.defer(ignore=True)
                                    card_storage = []
                                    title_storage = []
                                    arm_storage = []
                                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[armory_action_row], timeout=120, check=check)
                                    if button_ctx.custom_id == "q":
                                        await ctx.send("Armory Menu Closed...")
                                        return
                                    if button_ctx.custom_id == "view":
                                        await msg.delete()
                                        armory_item_buttons = [
                                            manage_components.create_button(style=2, label="View Cards", custom_id="cards"),
                                            manage_components.create_button(style=3, label="View Titles", custom_id="titles"),
                                            manage_components.create_button(style=1, label="View Arms", custom_id="arms"),
                                            
                                        ]
                                        armory_item_action_row = manage_components.create_actionrow(*armory_item_buttons)
                                        armory_item_screen = discord.Embed(title=f"{guild['GNAME']} Armory!", description=textwrap.dedent(f"""\
                                        {armory_message}
                                        
                                        🕋 **Armory Inventory** | 300
                                        🎴 **Cards** |  {len(guild['CSTORAGE'])}
                                        🎗️ **Titles** |  {len(guild['TSTORAGE'])}
                                        🦾 **Arms** |  {len(guild['ASTORAGE'])}
                                        """), color=0xe74c3c)
                                        armory_item_screen.set_image(url="https://cdnb.artstation.com/p/assets/images/images/036/549/141/original/jonathan-dodd-mdz2-large-warehouse-port.gif?1617957276")
                                        
                                        msg = await ctx.send(embed=armory_item_screen, components=[armory_item_action_row])
                                        def check(button_ctx):
                                            return button_ctx.author == ctx.author
                                        try:
                                            button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[armory_item_action_row], timeout=120, check=check)
                                            if button_ctx.custom_id == "cards":
                                                try:
                                                    card_storage = guild['CSTORAGE']
                                                    if len(card_storage) > 0:
                                                        storage_allowed_amount = 300
                                                        list_of_cards = db.querySpecificCards(card_storage)
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

                                                            
                                                            universe_crest = crown_utilities.crest_dict[card['UNIVERSE']]
                                                            index = card_storage.index(card['NAME'])
                                                            level = ""
                                                            level_icon = "🔰"
                                                            for c in guild['S_CARD_LEVELS']:
                                                                if card['NAME'] == c['CARD']:
                                                                    level = str(c['LVL'])
                                                                    card_lvl = int(c['LVL'])
                                                                else:
                                                                    level = str(0)
                                                                    card_lvl = int(0)
                                                            if card_lvl >= 200:
                                                                level_icon = "🔱"
                                                            if card_lvl >= 700:
                                                                level_icon ="⚜️"
                                                            if card_lvl >=999:
                                                                level_icon ="🏅"
                                                                
                                                            available = ""
                                                            if card['EXCLUSIVE'] and not card['HAS_COLLECTION']:
                                                                dungeon_card_details.append(
                                                                    f"[{str(index)}] {universe_crest} : :mahjong: **{card['TIER']}** **{card['NAME']}** {basic_attack_emoji} {super_attack_emoji} {ultimate_attack_emoji}\n**{level_icon}**: {str(level)} :heart: {card['HLT']} :dagger: {card['ATK']}  🛡️ {card['DEF']}\n")
                                                            elif not card['HAS_COLLECTION']:
                                                                tales_card_details.append(
                                                                    f"[{str(index)}] {universe_crest} : :mahjong: **{card['TIER']}** **{card['NAME']}** {basic_attack_emoji} {super_attack_emoji} {ultimate_attack_emoji}\n**{level_icon}**: {str(level)} :heart: {card['HLT']} :dagger: {card['ATK']}  🛡️ {card['DEF']}\n")
                                                            elif card['HAS_COLLECTION']:
                                                                destiny_card_details.append(
                                                                    f"[{str(index)}] {universe_crest} : :mahjong: **{card['TIER']}** **{card['NAME']}** {basic_attack_emoji} {super_attack_emoji} {ultimate_attack_emoji}\n**{level_icon}**: {str(level)} :heart: {card['HLT']} :dagger: {card['ATK']}  🛡️ {card['DEF']}\n")

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
                                                            embedVar = discord.Embed(title=f"🕋 | {guild['GNAME']}'s Card Armory", description="\n".join(all_cards), colour=0x7289da)
                                                            embedVar.set_footer(
                                                                text=f"{total_cards} Total Cards\n{str(storage_allowed_amount - len(card_storage))} Storage Available")
                                                            await ctx.send(embed=embedVar)

                                                        embed_list = []
                                                        for i in range(0, len(cards_broken_up)):
                                                            globals()['embedVar%s' % i] = discord.Embed(
                                                                title=f"🕋 | {guild['GNAME']}'s Card Armory",
                                                                description="\n".join(cards_broken_up[i]), colour=0x7289da)
                                                            globals()['embedVar%s' % i].set_footer(
                                                                text=f"{total_cards} Total Cards\n{str(storage_allowed_amount - len(card_storage))} Storage Available")
                                                            embed_list.append(globals()['embedVar%s' % i])

                                                        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
                                                        paginator.add_reaction('⏮️', "first")
                                                        paginator.add_reaction('⬅️', "back")
                                                        paginator.add_reaction('🔐', "lock")
                                                        paginator.add_reaction('➡️', "next")
                                                        paginator.add_reaction('⏭️', "last")
                                                        embeds = embed_list
                                                        await paginator.run(embeds)
                                                    else:
                                                        await ctx.send("🕋 | Card Armory Empty...")
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
                                                
                                            if button_ctx.custom_id == "titles":
                                                title_storage = guild['TSTORAGE']
                                                storage_allowed_amount = 300
                                                if len(title_storage) > 0:
                                                    list_of_titles = db.querySpecificTitles(guild['TSTORAGE'])
                                                    titles = [x for x in list_of_titles]
                                                    dungeon_title_details = []
                                                    tales_title_details = []
                                                    boss_title_details = []
                                                    unbound_title_details = []
                                                    for title in titles:
                                                        title_title = title['TITLE']
                                                        title_show = title['UNIVERSE']
                                                        exclusive = title['EXCLUSIVE']
                                                        available = title['AVAILABLE']
                                                        title_passive = title['ABILITIES'][0]
                                                        title_passive_type = list(title_passive.keys())[0]
                                                        title_passive_value = list(title_passive.values())[0]


                                                    
                                                        universe_crest = crown_utilities.crest_dict[title_show]
                                                        index = guild['TSTORAGE'].index(title_title)

                                                        if title_show == "Unbound":
                                                            unbound_title_details.append(
                                                                f"[{str(index)}] {universe_crest} :crown: : **{title_title}**\n**🦠 {title_passive_type}**: *{title_passive_value}*\n")
                                                        elif not exclusive and not available:
                                                            boss_title_details.append(
                                                                f"[{str(index)}] {universe_crest} 👹 : **{title_title}**\n**🦠 {title_passive_type}**:  *{title_passive_value}*\n")
                                                        elif exclusive and available:
                                                            dungeon_title_details.append(
                                                                f"[{str(index)}] {universe_crest} :fire: : **{title_title}**\n**🦠 {title_passive_type}**: *{title_passive_value}*\n")
                                                        elif available and not exclusive:
                                                            tales_title_details.append(
                                                                f"[{str(index)}] {universe_crest} 🎗️ : **{title_title}**\n**🦠 {title_passive_type}**:  *{title_passive_value}*\n")

                                                    all_titles = []
                                                    
                                                    if unbound_title_details:
                                                        for u in unbound_title_details:
                                                            all_titles.append(u)
                                                            
                                                    if tales_title_details:
                                                        for t in tales_title_details:
                                                            all_titles.append(t)

                                                    if dungeon_title_details:
                                                        for d in dungeon_title_details:
                                                            all_titles.append(d)

                                                    if boss_title_details:
                                                        for de in boss_title_details:
                                                            all_titles.append(de)
                                                    
                                                    

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
                                                        # first_digit = 10
                                                        titles_broken_up = np.array_split(all_titles, first_digit)

                                                    # If it's not an array greater than 10, show paginationless embed
                                                    if len(all_titles) < 10:
                                                        embedVar = discord.Embed(title=f"🕋 | {guild['GNAME']}'s Title Armory", description="\n".join(all_titles), colour=0x7289da)
                                                        embedVar.set_footer(
                                                            text=f"{total_titles} Total Titles\n{str(storage_allowed_amount - len(guild['TSTORAGE']))} Storage Available")
                                                        await ctx.send(embed=embedVar)

                                                    embed_list = []
                                                    for i in range(0, len(titles_broken_up)):
                                                        globals()['embedVar%s' % i] = discord.Embed(
                                                            title=f"🕋 | {guild['GNAME']}'s Title Armory",
                                                            description="\n".join(titles_broken_up[i]), colour=0x7289da)
                                                        globals()['embedVar%s' % i].set_footer(
                                                            text=f"{total_titles} Total Titles\n{str(storage_allowed_amount - len(guild['TSTORAGE']))} Storage Available")
                                                        embed_list.append(globals()['embedVar%s' % i])

                                                    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
                                                    paginator.add_reaction('⏮️', "first")
                                                    paginator.add_reaction('⬅️', "back")
                                                    paginator.add_reaction('🔐', "lock")
                                                    paginator.add_reaction('➡️', "next")
                                                    paginator.add_reaction('⏭️', "last")
                                                    embeds = embed_list
                                                    await paginator.run(embeds)
                                                else:
                                                    await ctx.send("🕋 | Title Armory Empty...")
                                                    return
                                            if button_ctx.custom_id == "arms":
                                                arm_storage = guild['ASTORAGE']
                                                storage_allowed_amount = 300
                                                if len(arm_storage) > 0:
                                                    storage_card_names = []
                                                    for name in guild['ASTORAGE']:
                                                        storage_card_names.append(name['ARM'])
                                            
                                                    list_of_arms = db.querySpecificArms(storage_card_names)

                                                    arms = [x for x in list_of_arms]
                                                    dungeon_arm_details = []
                                                    tales_arm_details = []
                                                    boss_arm_details = []
                                                    unbound_arm_details = []
                                                    icon = ""
                                                    for arm in arms:
                                                        durability = 0
                                                        for name in guild['ASTORAGE']:
                                                            if name['ARM'] == arm['ARM']:
                                                                durability = int(name['DUR'])
                                                        element_available = ['BASIC', 'SPECIAL', 'ULTIMATE']
                                                        arm_name = arm['ARM']
                                                        arm_show = arm['UNIVERSE']
                                                        exclusive = arm['EXCLUSIVE']
                                                        available = arm['AVAILABLE']
                                                        element = arm['ELEMENT']
                                                        if element:
                                                            element_name = element.title()
                                                            element = crown_utilities.set_emoji(element)
                                                        else:
                                                            element = "🦠"
                                                        arm_passive = arm['ABILITIES'][0]
                                                            # Arm Passive
                                                        arm_passive_type = list(arm_passive.keys())[0]
                                                        arm_passive_value = list(arm_passive.values())[0]
                                                        
                                                        icon = element
                                                        if arm_passive_type == "SHIELD":
                                                            icon = "🌐"
                                                        if arm_passive_type == "PARRY":
                                                            icon = "🔄"
                                                        if arm_passive_type == "BARRIER":
                                                            icon = "💠"
                                                        if arm_passive_type == "SIPHON":
                                                            icon = "💉"

                                                    
                                                        universe_crest = crown_utilities.crest_dict[arm_show]
                                                        index = guild['ASTORAGE'].index({'ARM': arm_name, 'DUR' : durability})

                                                        if arm_show == "Unbound":
                                                            unbound_arm_details.append(
                                                                f"[{str(index)}] {universe_crest} :crown: {icon} : **{arm_name}** ⚒️*{durability}*\n**{arm_passive_type}** : *{arm_passive_value}*\n")
                                                        elif not exclusive and not available:
                                                            boss_arm_details.append(
                                                                f"[{str(index)}] {universe_crest} 👹 {icon} : **{arm_name}** ⚒️*{durability}*\n**{arm_passive_type}** :  *{arm_passive_value}*\n")
                                                        elif exclusive and available:
                                                            dungeon_arm_details.append(
                                                                f"[{str(index)}] {universe_crest} :fire: {icon} : **{arm_name}** ⚒️*{durability}*\n**{arm_passive_type}** : *{arm_passive_value}*\n")
                                                        elif available and not exclusive:
                                                            tales_arm_details.append(
                                                                f"[{str(index)}] {universe_crest} 🦾 {icon} : **{arm_name}** ⚒️*{durability}*\n**{arm_passive_type}** :  *{arm_passive_value}*\n")

                                                    all_arms = []
                                                    if unbound_arm_details:
                                                        for u in unbound_arm_details:
                                                            all_arms.append(u)
                                                            
                                                    if tales_arm_details:
                                                        for t in tales_arm_details:
                                                            all_arms.append(t)

                                                    if dungeon_arm_details:
                                                        for d in dungeon_arm_details:
                                                            all_arms.append(d)

                                                    if boss_arm_details:
                                                        for de in boss_arm_details:
                                                            all_arms.append(de)

                                                    

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
                                                        # first_digit = 10
                                                        arms_broken_up = np.array_split(all_arms, first_digit)

                                                    # If it's not an array greater than 10, show paginationless embed
                                                    if len(all_arms) < 10:
                                                        embedVar = discord.Embed(title=f"🕋 | {guild['GNAME']}'s Arm Armory", description="\n".join(all_arms), colour=0x7289da)
                                                        embedVar.set_footer(
                                                            text=f"{total_arms} Total Arms\n{str(storage_allowed_amount - len(guild['ASTORAGE']))} Storage Available")
                                                        await ctx.send(embed=embedVar)

                                                    embed_list = []
                                                    for i in range(0, len(arms_broken_up)):
                                                        globals()['embedVar%s' % i] = discord.Embed(
                                                            title=f"🕋 | {guild['GNAME']}'s Arm Armory",
                                                            description="\n".join(arms_broken_up[i]), colour=0x7289da)
                                                        globals()['embedVar%s' % i].set_footer(
                                                            text=f"{total_arms} Total Arms\n{str(storage_allowed_amount - len(guild['ASTORAGE']))} Storage Available")
                                                        embed_list.append(globals()['embedVar%s' % i])

                                                    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
                                                    paginator.add_reaction('⏮️', "first")
                                                    paginator.add_reaction('⬅️', "back")
                                                    paginator.add_reaction('🔐', "lock")
                                                    paginator.add_reaction('➡️', "next")
                                                    paginator.add_reaction('⏭️', "last")
                                                    embeds = embed_list
                                                    await paginator.run(embeds)
                                                else:
                                                    await ctx.send("🕋 | Arm Armory Empty...")
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
                                    if button_ctx.custom_id == "upgrade":   
                                        await msg.delete()    
                                        await ctx.send("🕋 | Armory Upgrades Coming Soon...")
                                        return
                                        #print("Armory Upgrades Coming Soon")  
                                    if button_ctx.custom_id == "donate":  
                                        # await msg.delete()    
                                        # await ctx.send("🕋 | Armory Donations Coming Soon...")
                                        # return  
                                        await msg.delete()
                                        donate_buttons = [
                                            manage_components.create_button(style=2, label="Donate Cards", custom_id="cards"),
                                            manage_components.create_button(style=3, label="Donate Titles", custom_id="titles"),
                                            manage_components.create_button(style=1, label="Donate Arms", custom_id="arms"),
                                            
                                        ]
                                        donate_action_row = manage_components.create_actionrow(*donate_buttons)
                                        donate_item_screen = discord.Embed(title=f"{guild['GNAME']} Armory!", description=textwrap.dedent(f"""\
                                        {armory_message}
                                        
                                        🕋 **Armory Inventory** | 300
                                        🎴 **Cards** |  {len(guild['CSTORAGE'])}
                                        🎗️ **Titles** |  {len(guild['TSTORAGE'])}
                                        🦾 **Arms** |  {len(guild['ASTORAGE'])}
                                        """), color=0xe74c3c)
                                        donate_item_screen.set_image(url="https://cdnb.artstation.com/p/assets/images/images/036/549/141/original/jonathan-dodd-mdz2-large-warehouse-port.gif?1617957276")
                                        
                                        msg = await ctx.send(embed=donate_item_screen, components=[donate_action_row])
                                        def check(button_ctx):
                                            return button_ctx.author == ctx.author
                                        try:
                                            button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[donate_action_row], timeout=120, check=check)
                                            if button_ctx.custom_id == "cards": 
                                                query = {'DID': str(ctx.author.id)}
                                                d = db.queryUser(query)#Storage Update
                                                storage_type = d['STORAGE_TYPE']
                                                vault = db.queryVault({'DID': d['DID']})
                                                try: 
                                                    if vault:
                                                        name = d['DISNAME'].split("#",1)[0]
                                                        avatar = d['AVATAR']
                                                        card_levels = vault['CARD_LEVELS']
                                                        current_gems = []
                                                        for gems in vault['GEMS']:
                                                            current_gems.append(gems['UNIVERSE'])
                                                        balance = vault['BALANCE']
                                                        cards_list = vault['CARDS']
                                                        total_cards = len(cards_list)
                                                        current_card = d['CARD']
                                                        storage = vault['STORAGE']
                                                        cards=[]
                                                        icon = ":coin:"
                                                        if balance >= 150000:
                                                            icon = ":money_with_wings:"
                                                        elif balance >=100000:
                                                            icon = ":moneybag:"
                                                        elif balance >= 50000:
                                                            icon = ":dollar:"
                                                        
                                                        embed_list = []

                                                        for card in cards_list:
                                                            index = cards_list.index(card)
                                                            resp = db.queryCard({"NAME": str(card)})
                                                            card_tier = 0
                                                            lvl = ""
                                                            tier = ""
                                                            speed = 0
                                                            card_tier = f":mahjong: {resp['TIER']}"
                                                            card_available = resp['AVAILABLE']
                                                            card_exclusive = resp['EXCLUSIVE']
                                                            card_collection = resp['HAS_COLLECTION']
                                                            show_img = db.queryUniverse({'TITLE': resp['UNIVERSE']})['PATH']
                                                            affinity_message = crown_utilities.set_affinities(resp)
                                                            o_show = resp['UNIVERSE']
                                                            icon = ":flower_playing_cards:"
                                                            if card_available and card_exclusive:
                                                                icon = ":fire:"
                                                            elif card_available == False and card_exclusive ==False:
                                                                if card_collection:
                                                                    icon =":sparkles:"
                                                                else:
                                                                    icon = ":japanese_ogre:"
                                                            card_lvl = 0
                                                            card_exp = 0
                                                            card_lvl_attack_buff = 0
                                                            card_lvl_defense_buff = 0
                                                            card_lvl_ap_buff = 0
                                                            card_lvl_hlt_buff = 0

                                                            for cl in card_levels:
                                                                if card == cl['CARD']:
                                                                    
                                                                    licon = "🔰"
                                                                    if cl['LVL'] >= 200:
                                                                        licon ="🔱"
                                                                    if cl['LVL'] >= 700:
                                                                        licon ="⚜️"
                                                                    if cl['LVL'] >= 999:
                                                                        licon = "🏅"
                                                                    lvl = f"{licon} **{cl['LVL']}**"
                                                                    card_lvl = cl['LVL']
                                                                    card_exp = cl['EXP']
                                                                    card_lvl_ap_buff = crown_utilities.level_sync_stats(card_lvl, "AP")
                                                                    card_lvl_attack_buff = crown_utilities.level_sync_stats(card_lvl, "ATK_DEF")
                                                                    card_lvl_defense_buff = crown_utilities.level_sync_stats(card_lvl, "ATK_DEF")
                                                                    card_lvl_hlt_buff = crown_utilities.level_sync_stats(card_lvl, "HLT")
                                                                    
                                                            
                                                            o_passive = resp['PASS'][0] 
                                                            o_moveset = resp['MOVESET']
                                                            o_1 = o_moveset[0]
                                                            o_2 = o_moveset[1]
                                                            o_3 = o_moveset[2]
                                                            o_enhancer = o_moveset[3]
                                                            
                                                            # Move 1
                                                            move1 = list(o_1.keys())[0]
                                                            move1ap = list(o_1.values())[0] + card_lvl_ap_buff
                                                            move1_stamina = list(o_1.values())[1]
                                                            move1_element = list(o_1.values())[2]
                                                            move1_emoji = crown_utilities.set_emoji(move1_element)
                                                            
                                                            # Move 2
                                                            move2 = list(o_2.keys())[0]
                                                            move2ap = list(o_2.values())[0] + card_lvl_ap_buff
                                                            move2_stamina = list(o_2.values())[1]
                                                            move2_element = list(o_2.values())[2]
                                                            move2_emoji = crown_utilities.set_emoji(move2_element)


                                                            # Move 3
                                                            move3 = list(o_3.keys())[0]
                                                            move3ap = list(o_3.values())[0] + card_lvl_ap_buff
                                                            move3_stamina = list(o_3.values())[1]
                                                            move3_element = list(o_3.values())[2]
                                                            move3_emoji = crown_utilities.set_emoji(move3_element)


                                                            # Move Enhancer
                                                            move4 = list(o_enhancer.keys())[0]
                                                            move4ap = list(o_enhancer.values())[0]
                                                            move4_stamina = list(o_enhancer.values())[1]
                                                            move4enh = list(o_enhancer.values())[2]

                                                            passive_name = list(o_passive.keys())[0]
                                                            passive_num = list(o_passive.values())[0]
                                                            passive_type = list(o_passive.values())[1]
                                                        
                                                            if passive_type:
                                                                value_for_passive = resp['TIER'] * .5
                                                                flat_for_passive = round(10 * (resp['TIER'] * .5))
                                                                stam_for_passive = 5 * (resp['TIER'] * .5)
                                                                if passive_type == "HLT":
                                                                    passive_num = value_for_passive
                                                                if passive_type == "LIFE":
                                                                    passive_num = value_for_passive
                                                                if passive_type == "ATK":
                                                                    passive_num = value_for_passive
                                                                if passive_type == "DEF":
                                                                    passive_num = value_for_passive
                                                                if passive_type == "STAM":
                                                                    passive_num = stam_for_passive
                                                                if passive_type == "DRAIN":
                                                                    passive_num = stam_for_passive
                                                                if passive_type == "FLOG":
                                                                    passive_num = value_for_passive
                                                                if passive_type == "WITHER":
                                                                    passive_num = value_for_passive
                                                                if passive_type == "RAGE":
                                                                    passive_num = value_for_passive
                                                                if passive_type == "BRACE":
                                                                    passive_num = value_for_passive
                                                                if passive_type == "BZRK":
                                                                    passive_num = value_for_passive
                                                                if passive_type == "CRYSTAL":
                                                                    passive_num = value_for_passive
                                                                if passive_type == "FEAR":
                                                                    passive_num = flat_for_passive
                                                                if passive_type == "GROWTH":
                                                                    passive_num = flat_for_passive
                                                                if passive_type == "CREATION":
                                                                    passive_num = value_for_passive
                                                                if passive_type == "DESTRUCTION":
                                                                    passive_num = value_for_passive
                                                                if passive_type == "SLOW":
                                                                    passive_num = passive_num
                                                                if passive_type == "HASTE":
                                                                    passive_num = passive_num
                                                                if passive_type == "GAMBLE":
                                                                    passive_num = passive_num
                                                                if passive_type == "SOULCHAIN":
                                                                    passive_num = passive_num + 90
                                                                if passive_type == "STANCE":
                                                                    passive_num = flat_for_passive
                                                                if passive_type == "CONFUSE":
                                                                    passive_num = flat_for_passive
                                                                if passive_type == "BLINK":
                                                                    passive_num = stam_for_passive

                                                            traits = ut.traits
                                                            mytrait = {}
                                                            traitmessage = ''
                                                            for trait in traits:
                                                                if trait['NAME'] == o_show:
                                                                    mytrait = trait
                                                                if o_show == 'Kanto Region' or o_show == 'Johto Region' or o_show == 'Kalos Region' or o_show == 'Unova Region' or o_show == 'Sinnoh Region' or o_show == 'Hoenn Region' or o_show == 'Galar Region' or o_show == 'Alola Region':
                                                                    if trait['NAME'] == 'Pokemon':
                                                                        mytrait = trait
                                                            if mytrait:
                                                                traitmessage = f"**{mytrait['EFFECT']}:** {mytrait['TRAIT']}"


                                                            embedVar = discord.Embed(title= f"{resp['NAME']}", description=textwrap.dedent(f"""\
                                                            {icon} **[{index}]** 
                                                            {card_tier}: {lvl}
                                                            :heart: **{resp['HLT']}** :dagger: **{resp['ATK']}** :shield: **{resp['DEF']}** 🏃 **{resp['SPD']}**

                                                            {move1_emoji} **{move1}:** {move1ap}
                                                            {move2_emoji} **{move2}:** {move2ap}
                                                            {move3_emoji} **{move3}:** {move3ap}
                                                            🦠 **{move4}:** {move4enh} {move4ap}{enhancer_suffix_mapping[move4enh]}

                                                            🩸 **{passive_name}:** {passive_type.title()} {passive_num}{passive_enhancer_suffix_mapping[passive_type]}
                                                            ♾️ {traitmessage}
                                                            """), colour=0x7289da)
                                                            embedVar.add_field(name="__Affinities__", value=f"{affinity_message}")
                                                            embedVar.set_thumbnail(url=show_img)
                                                            embedVar.set_footer(text=f"/enhancers - 🩸 Enhancer Menu")
                                                            embed_list.append(embedVar)

                                                        buttons = [
                                                            manage_components.create_button(style=3, label="Donate", custom_id="Donate"),
                                                        ]
                                                        custom_action_row = manage_components.create_actionrow(*buttons)
                                                        # custom_button = manage_components.create_button(style=3, label="Equip")

                                                        async def custom_function(self, button_ctx):
                                                            if button_ctx.author == ctx.author:
                                                                updated_vault = db.queryVault({'DID': d['DID']})
                                                                sell_price = 0

                                                                selected_card = str(button_ctx.origin_message.embeds[0].title)
                                                                card_levels = updated_vault['CARD_LEVELS']
                                                                for cl in card_levels:
                                                                    if selected_card == cl['CARD']:
                                                                        card_lvl = cl['LVL']
                                                                        card_tier = cl['TIER']
                                                                        card_exp = cl['EXP']
                                                                        card_lvl_ap_buff = crown_utilities.level_sync_stats(card_lvl, "AP")
                                                                        card_lvl_attack_buff = crown_utilities.level_sync_stats(card_lvl, "ATK_DEF")
                                                                        card_lvl_defense_buff = crown_utilities.level_sync_stats(card_lvl, "ATK_DEF")
                                                                        card_lvl_hlt_buff = crown_utilities.level_sync_stats(card_lvl, "HLT")
                                                                if button_ctx.custom_id == "Donate":
                                                                    #print("donate")
                                                                    guild_query = {"GNAME": guild["GNAME"]}
                                                                    if selected_card == d['CARD']:
                                                                        await ctx.send(f"🕋 | **{selected_card}** cannot donate Equipped Card")
                                                                        return
                                                                    if len(card_storage) <= 300:
                                                                        transaction_message = f":kaaba:  | {ctx.author} Donated 🎴**{selected_card}**."
                                                                        query = {'DID': str(ctx.author.id)}
                                                                        update_storage_query = {
                                                                            '$pull': {'CARDS': selected_card, 'CARD_LEVELS': {'CARD' :  selected_card}},
                                                                        }
                                                                        response = db.updateVaultNoFilter(query, update_storage_query)
                                                                        update_gstorage_query = {
                                                                            '$addToSet' : {'CSTORAGE' : str(selected_card)},
                                                                            '$push': {'TRANSACTIONS': transaction_message}                                                                         
                                                                        }
                                                                        response = db.updateGuildAlt(guild_query, update_gstorage_query)
                                                                        update_glevel_query = {
                                                                        '$addToSet' : {
                                                                                'S_CARD_LEVELS': {'CARD': str(selected_card), 'LVL': card_lvl, 'TIER': card_tier, 'EXP': card_exp,
                                                                                                'HLT': card_lvl_hlt_buff, 'ATK': card_lvl_attack_buff, 'DEF': card_lvl_defense_buff, 'AP': card_lvl_ap_buff}}
                                                                        }
                                                                        response = db.updateGuildAlt(guild_query, update_glevel_query)
                                                                        await msg.delete()
                                                                        await ctx.send(f"🕋 | **{selected_card}** has been added to the Armory")
                                                                        return
                                                                    else:
                                                                        await ctx.send("Not enough space in storage")
                                                                        return
                                                            else:
                                                                await ctx.send("This is not your card list.")
                                                        await Paginator(bot=self.bot, disableAfterTimeout=True, useQuitButton=True, ctx=ctx, pages=embed_list, timeout=60, customActionRow=[
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
                                            if button_ctx.custom_id == "titles":
                                                query = {'DID': str(ctx.author.id)}
                                                guild_query = {"GNAME": guild["GNAME"]}
                                                d = db.queryUser(query)
                                                vault = db.queryVault({'DID': d['DID']})
                                                storage_type = d['STORAGE_TYPE']
                                                if vault:
                                                    try:
                                                        name = d['DISNAME'].split("#",1)[0]
                                                        avatar = d['AVATAR']
                                                        balance = vault['BALANCE']
                                                        current_title = d['TITLE']
                                                        titles_list = vault['TITLES']
                                                        total_titles = len(titles_list)
                                                        storage = vault['TSTORAGE']
                                                        titles=[]
                                                        current_gems = []
                                                        for gems in vault['GEMS']:
                                                            current_gems.append(gems['UNIVERSE'])
                                                        icon = ":coin:"
                                                        if balance >= 150000:
                                                            icon = ":money_with_wings:"
                                                        elif balance >=100000:
                                                            icon = ":moneybag:"
                                                        elif balance >= 50000:
                                                            icon = ":dollar:"


                                                        embed_list = []
                                                        for title in titles_list:
                                                            index = titles_list.index(title)
                                                            resp = db.queryTitle({"TITLE": str(title)})
                                                            title_passive = resp['ABILITIES'][0]
                                                            title_passive_type = list(title_passive.keys())[0]
                                                            title_passive_value = list(title_passive.values())[0]
                                                            title_available = resp['AVAILABLE']
                                                            title_exclusive = resp['EXCLUSIVE']
                                                            icon = "🎗️"
                                                            if resp['UNIVERSE'] == "Unbound":
                                                                icon = ":crown:"
                                                            elif title_available and title_exclusive:
                                                                icon = ":fire:"
                                                            elif title_available == False and title_exclusive ==False:
                                                                icon = ":japanese_ogre:"
                                                            
                                                            
                                                            embedVar = discord.Embed(title= f"{resp['TITLE']}", description=textwrap.dedent(f"""
                                                            {icon} **[{index}]**
                                                            🦠 **{title_passive_type}:** {title_passive_value}
                                                            :earth_africa: **Universe:** {resp['UNIVERSE']}"""), 
                                                            colour=0x7289da)
                                                            embedVar.set_thumbnail(url=avatar)
                                                            embedVar.set_footer(text=f"{title_passive_type}: {title_enhancer_mapping[title_passive_type]}")
                                                            embed_list.append(embedVar)
                                                        
                                                        buttons = [
                                                            manage_components.create_button(style=3, label="Donate", custom_id="Donate"),
                                                        ]
                                                        custom_action_row = manage_components.create_actionrow(*buttons)

                                                        async def custom_function(self, button_ctx):
                                                            if button_ctx.author == ctx.author:
                                                                updated_vault = db.queryVault({'DID': d['DID']})
                                                                sell_price = 0
                                                                selected_title = str(button_ctx.origin_message.embeds[0].title)
                                                                if selected_title == d['TITLE']:
                                                                        await ctx.send(f"🕋 | **{selected_title}** cannot donate Equipped Title")
                                                                        return
                                                                if button_ctx.custom_id == "Donate":
                                                                    if len(title_storage) <= 300:
                                                                        transaction_message = f":kaaba:  | {ctx.author} Donated 🎗️ **{selected_title}**."
                                                                        query = {'DID': str(ctx.author.id)}
                                                                        update_storage_query = {
                                                                            '$pull': {'TITLES': selected_title},
                                                                        }
                                                                        response = db.updateVaultNoFilter(query, update_storage_query)
                                                                        update_gstorage_query = {
                                                                            '$addToSet' : {'TSTORAGE' : str(selected_title)},
                                                                            '$push': {'TRANSACTIONS': transaction_message}                                                                          
                                                                        }
                                                                        response = db.updateGuildAlt(guild_query, update_gstorage_query)
                                                                        await msg.delete()
                                                                        await ctx.send(f"🕋 | **{selected_title}** has been added to the Armory")
                                                                        return
                                                                    else:
                                                                        await ctx.send("Not enough space in storage")
                                                                        return
                                                            else:
                                                                await ctx.send("This is not your card list.")
                                                        await Paginator(bot=self.bot, disableAfterTimeout=True, useQuitButton=True, ctx=ctx, pages=embed_list, timeout=60, customActionRow=[
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
                                            if button_ctx.custom_id == "arms":
                                                guild_query = {"GNAME": guild["GNAME"]}
                                                query = {'DID': str(ctx.author.id)}
                                                d = db.queryUser(query)
                                                vault = db.queryVault({'DID': d['DID']})
                                                
                                                storage_type = d['STORAGE_TYPE']
                                                if vault:
                                                    try:
                                                        name = d['DISNAME'].split("#",1)[0]
                                                        avatar = d['AVATAR']
                                                        current_arm = d['ARM']
                                                        balance = vault['BALANCE']
                                                        arms_list = vault['ARMS']
                                                        total_arms = len(arms_list)
                                                        storage = vault['ASTORAGE']
                                                        arms=[]
                                                        current_gems = []
                                                        for gems in vault['GEMS']:
                                                            current_gems.append(gems['UNIVERSE'])

                                                        icon = ":coin:"
                                                        if balance >= 150000:
                                                            icon = ":money_with_wings:"
                                                        elif balance >=100000:
                                                            icon = ":moneybag:"
                                                        elif balance >= 50000:
                                                            icon = ":dollar:"

                                                        embed_list = []
                                                        for arm in arms_list:
                                                            index = arms_list.index(arm)
                                                            resp = db.queryArm({"ARM": str(arm['ARM'])})
                                                            element = resp['ELEMENT']
                                                            arm_passive = resp['ABILITIES'][0]
                                                            arm_passive_type = list(arm_passive.keys())[0]
                                                            arm_passive_value = list(arm_passive.values())[0]
                                                            arm_available = resp['AVAILABLE']
                                                            arm_exclusive = resp['EXCLUSIVE']
                                                            icon = "🦾"
                                                            if resp['UNIVERSE'] == "Unbound":
                                                                icon = ":crown:"
                                                            elif arm_available and arm_exclusive:
                                                                icon = ":fire:"
                                                            elif arm_available == False and arm_exclusive ==False:
                                                                icon = ":japanese_ogre:"
                                                            element_available = ['BASIC', 'SPECIAL', 'ULTIMATE']
                                                            if element and arm_passive_type in element_available:
                                                                element_name = element
                                                                element = crown_utilities.set_emoji(element)
                                                                arm_type = f"**{arm_passive_type.title()} {element_name.title()} Attack**"
                                                                arm_message = f"{element} **{resp['ARM']}:** {arm_passive_value}"
                                                                footer = f"The new {arm_passive_type.title()} attack will reflect on your card when equipped"

                                                            else:
                                                                arm_type = f"**Unique Passive**"
                                                                arm_message = f"🦠 **{arm_passive_type.title()}:** {arm_passive_value}"
                                                                footer = f"{arm_passive_type}: {enhancer_mapping[arm_passive_type]}"



                                                            embedVar = discord.Embed(title= f"{resp['ARM']}", description=textwrap.dedent(f"""
                                                            {icon} **[{index}]**

                                                            {arm_type}
                                                            {arm_message}
                                                            :earth_africa: **Universe:** {resp['UNIVERSE']}
                                                            ⚒️ {arm['DUR']}
                                                            """), 
                                                            colour=0x7289da)
                                                            embedVar.set_thumbnail(url=avatar)
                                                            embedVar.set_footer(text=f"{footer}")
                                                            embed_list.append(embedVar)
                                                        
                                                        buttons = [
                                                            manage_components.create_button(style=3, label="Donate", custom_id="Donate"),
                                                        ]
                                                        custom_action_row = manage_components.create_actionrow(*buttons)

                                                        async def custom_function(self, button_ctx):
                                                            if button_ctx.author == ctx.author:
                                                                u_vault = db.queryVault({'DID': d['DID']})
                                                                updated_vault = []
                                                                storage = u_vault['ASTORAGE']
                                                                for arm in u_vault['ARMS']:
                                                                    updated_vault.append(arm['ARM'])
                                                                
                                                                sell_price = 0
                                                                selected_arm = str(button_ctx.origin_message.embeds[0].title)
                                                                if selected_arm == d['ARM']:
                                                                        await ctx.send(f"🕋 | **{selected_arm}** cannot donate Equipped Arm")
                                                                        return
                                                                if button_ctx.custom_id == "Donate":
                                                                    durability = 0
                                                                    for names in u_vault['ARMS']:
                                                                        if names['ARM'] == selected_arm:
                                                                            durability = names['DUR']
                                                                    if len(arm_storage) <= 300:
                                                                        transaction_message = f":kaaba:  | {ctx.author} Donated 🦾 **{selected_arm}**."
                                                                        query = {'DID': str(ctx.author.id)}
                                                                        update_storage_query = {
                                                                            '$pull': {'ARMS': {'ARM' : str(selected_arm)}}
                                                                        }
                                                                        response = db.updateVaultNoFilter(query, update_storage_query)
                                                                        update_gstorage_query = {
                                                                            '$addToSet' : {'ASTORAGE': { 'ARM' : str(selected_arm), 'DUR' : int(durability)}},
                                                                            '$push': {'TRANSACTIONS': transaction_message}                                                                           
                                                                        }
                                                                        response = db.updateGuildAlt(guild_query, update_gstorage_query)
                                                                        await msg.delete()
                                                                        await ctx.send(f"🕋 | **{selected_arm}** has been added to the Armory")
                                                                        return
                                                            else:
                                                                await ctx.send("This is not your card list.")
                                                        await Paginator(bot=self.bot, disableAfterTimeout=True, useQuitButton=True, ctx=ctx, pages=embed_list, timeout=60, customActionRow=[
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
                            await ctx.send("This is not your command.")    
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
                await Paginator(bot=self.bot, useQuitButton=True, disableAfterTimeout=True, ctx=ctx, pages=embed_list, timeout=60, customActionRow=[
                    custom_action_row,
                    custom_function,
                ]).run()
            else:
                await ctx.send(m.GUILD_DOESNT_EXIST)
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


    @cog_ext.cog_slash(description="Lookup player family", guild_ids=main.guild_ids)
    async def family(self, ctx, player = None):
        a_registered_player = await crown_utilities.player_check(ctx)
        if not a_registered_player:
            return
        ctx_user = db.queryUser({'DID': str(ctx.author.id)})
        #print(ctx_user)

        try:
            if player != None:
                member = player
            if player:
                player = player.replace("<","")
                player = player.replace(">","")
                player = player.replace("@","")
                player = player.replace("!","")
                user_profile = db.queryUser({'DID': str(player)})
                family = db.queryFamily({'HEAD': user_profile['FAMILY']})
                if family:
                    family_name = family['HEAD']
                else:
                    await ctx.send("Family does not exist.")
                    return
                
            else:
                user_profile = db.queryUser({'DID': str(ctx.author.id)})
                family = db.queryFamily({'HEAD': user_profile['FAMILY']})
                if family:
                    family_name = family['HEAD']
                else:
                    await ctx.send("You are not a part of a Family.")
                    return
                
            if family:
                is_head = False
                is_partner = False
                is_kid = False
                member = False
                
                family_name = family['HEAD'] + "'s Family"
                head_name = family['HEAD']
                partner_name = family['PARTNER']
                savings = int(family['BANK'])
                head_data = db.queryUser({'DISNAME': head_name})
                head_object = await self.bot.fetch_user(head_data['DID'])
                estates = family['ESTATES']
                if partner_name:
                    partner_data = db.queryUser({'DISNAME': partner_name})
                    partner_object = await self.bot.fetch_user(partner_data['DID'])
                    partner_name_adjusted = partner_name.split("#",1)[0]
                else:
                    partner_name_adjusted = '*None*'
                house = family['HOUSE']
                house_info = db.queryHouse({'HOUSE' : house})
                house_img = house_info['PATH']
                kid_list = []
                for kids in family['KIDS']:
                    kid_list.append(kids.split("#",1)[0])
                icon = ":coin:"
                if savings >= 500000000:
                    icon = ":money_with_wings:"
                elif savings >=100000000:
                    icon = ":moneybag:"
                elif savings >= 50000000:
                    icon = ":dollar:"

                if str(ctx.author.id) == head_data['DID']:
                    is_head = True
                    member = True
                if partner_name:
                    if str(ctx.author.id) == partner_data['DID']:
                        is_partner = True
                        member = True
                if kid_list:
                    if ctx_user['NAME'] in kid_list:
                        is_kid = True
                        member = True
                #print(member)
                transactions = family['TRANSACTIONS']
                transactions_embed = ""
                if transactions:
                    transactions_len = len(transactions)
                    if transactions_len >= 10:
                        transactions = transactions[-10:]
                        transactions_embed = "\n".join(transactions)
                    else:
                        transactions_embed = "\n".join(transactions)
                
                        
                summon_object = family['SUMMON']
                summon = list(summon_object.values())[0]
                head_vault = db.queryVault({'DID' : head_data['DID']})
                pet_name = ""
                summon_bond = 0
                summon_lvl = 0
                summon_type = "Unbound"
                power = 0
                path = "N/A"
                found_summon_in_vault = False
                if head_vault:
                    vault_summons = head_vault['PETS']
                    for l in vault_summons:
                        if summon == l['NAME']:
                            found_summon_in_vault = True
                            level = l['LVL']
                            xp = l['EXP']
                            pet_ability = list(l.keys())[3]
                            pet_ability_power = list(l.values())[3]
                            power = (l['BOND'] * l['LVL']) + pet_ability_power
                            pet_info = {'NAME': l['NAME'], 'LVL': l['LVL'], 'EXP': l['EXP'], pet_ability: pet_ability_power, 'TYPE': l['TYPE'], 'BOND': l['BOND'], 'BONDEXP': l['BONDEXP'], 'PATH': l['PATH']}
                            summon_img = pet_info['PATH']
                            pet_name = pet_info["NAME"]
                            summon_bond = l["BOND"]
                            summon_lvl = level
                            summon_type = pet_info["TYPE"]
                            power = (summon_bond * summon_lvl) + int(pet_ability_power)
                            path = pet_info["PATH"]
                            summon_file = crown_utilities.showsummon(summon_img, pet_info['NAME'], enhancer_mapping[pet_info['TYPE']], pet_info['LVL'], pet_info['BOND'])
                    if found_summon_in_vault == False:
                        pet_info = db.queryPet({'PET': summon})
                        summon_img = pet_info['PATH']
                        pet_ability_power = list(pet_info['ABILITIES'][0].values())[0]
                        pet_ability = list(pet_info['ABILITIES'])[0]
                        summon_type = pet_ability['TYPE']
                        summon_bond = 0
                        pet_name = pet_info["PET"]
                        summon_lvl = 0
                        summon_img = pet_info['PATH']
                        power = (summon_bond * summon_lvl) + int(pet_ability_power)
                        path = pet_info["PATH"]
                        summon_file = crown_utilities.showsummon(summon_img, pet_info['PET'], enhancer_mapping[summon_type], 0, 0)
                else:
                    partnervault =  db.queryVault({'DID' : partner_data['DID']})
                    if partnervault:
                        vault_summons = partnervault['PETS']
                        for l in vault_summons:
                            if summon == l['NAME']:
                                found_summon_in_vault = True
                                level = l['LVL']
                                xp = l['EXP']
                                pet_ability = list(l.keys())[3]
                                pet_ability_power = list(l.values())[3]
                                power = (l['BOND'] * l['LVL']) + pet_ability_power
                                pet_info = {'NAME': l['NAME'], 'LVL': l['LVL'], 'EXP': l['EXP'], pet_ability: pet_ability_power, 'TYPE': l['TYPE'], 'BOND': l['BOND'], 'BONDEXP': l['BONDEXP'], 'PATH': l['PATH']}
                                summon_img = pet_info['PATH']
                                summon_type = pet_info["TYPE"]
                                summon_file = crown_utilities.showsummon(summon_img, pet_info['NAME'], enhancer_mapping[pet_info['TYPE']], pet_info['LVL'], pet_info['BOND'])
                                pet_name = pet_info["NAME"]
                                summon_bond = pet_info["BOND"]
                                summon_lvl = level
                                power = (summon_bond * summon_lvl) + int(pet_ability_power)
                                path = pet_info["PATH"]
                        if found_summon_in_vault == False:
                            pet_info = db.queryPet({'PET': summon})
                            summon_img = pet_info['PATH']
                            pet_ability_power = list(pet_info['ABILITIES'][0].values())[0]
                            pet_ability = list(pet_info['ABILITIES'])[0]
                            summon_type = pet_ability['TYPE']
                            summon_bond = 0
                            pet_name = pet_info["PET"]
                            summon_lvl = 0
                            summon_img = pet_info['PATH']
                            power = (summon_bond * summon_lvl) + int(pet_ability_power)
                            path = pet_info["PATH"]
                            summon_file = crown_utilities.showsummon(summon_img, pet_info['PET'], enhancer_mapping[summon_type], 0, 0)
                                
                    else:
                        pet_info = db.queryPet({'PET': summon})
                        summon_img = pet_info['PATH']
                        pet_ability_power = list(pet_info['ABILITIES'][0].values())[0]
                        pet_ability = list(pet_info['ABILITIES'])[0]
                        summon_type = pet_ability['TYPE']
                        summon_bond = 0
                        pet_name = pet_info["PET"]
                        summon_lvl = 0
                        summon_img = pet_info['PATH']
                        power = (summon_bond * summon_lvl) + int(pet_ability_power)
                        path = pet_info["PATH"]
                        summon_file = crown_utilities.showsummon(summon_img, pet_info['PET'], enhancer_mapping[summon_type], 0, 0)
                universe = family['UNIVERSE']
                universe_data = db.queryUniverse({'TITLE': universe})
                universe_img = universe_data['PATH']
                estates_list = []
                estate_data_list = []
                for houses in estates:
                    house_data = db.queryHouse({'HOUSE': houses})
                    estates_list.append(houses)
                    estate_data_list.append(house_data)
                    
                estates_list_joined = ", ".join(estates_list)
                
                
                kids_names = ", ".join(f'{k}'.format(self) for k in kid_list)
                # if summon_data:
                #     await ctx.send({summon_data})
                    
                first_page = discord.Embed(title=f":family_mwgb: | {family_name}", description=textwrap.dedent(f"""
                :brain: **Head of Household** 
                {head_name.split("#",1)[0]}

                :anatomical_heart: **Partner**
                {partner_name_adjusted}

                :baby: **Kids**
                {kids_names}

                🏦**Savings** 
                {icon} {'{:,}'.format(savings)}
                
                🏠**Primary Residence**
                {house_info['HOUSE']} - 〽️**{house_info['MULT']}x** :coin: per match!
                """), colour=0x7289da)
                first_page.set_image(url=house_img)
                
                estates_page = discord.Embed(title=f"Real Estate", description=textwrap.dedent(f"""
                🌇 **Properties**
                {estates_list_joined}
               
                """), colour=0x7289da)

                
                activity_page = discord.Embed(title="Recent Family Activity", description=textwrap.dedent(f"""
                {transactions_embed}
                """), colour=0x7289da)
                
                summon_page = discord.Embed(title="Family Summon", description=textwrap.dedent(f"""
                🧬**{pet_name}**
                *Bond* **{summon_bond}**
                *Level* **{summon_lvl}**
                :small_blue_diamond: **{summon_type}** ~ **{power}**{enhancer_suffix_mapping[summon_type]}
                🦠 : **{enhancer_mapping[summon_type]}**
                """), colour=0x7289da)
                summon_page.set_image(url=path)
                
                
                
                
                
                family_explanations = discord.Embed(title=f"Information", description=textwrap.dedent(f"""
                **Family Explanations**
                - **Earnings**: Families earn coin for every completed battle by its members
                - **Allowance**: Disperse Family Savings to a family member
                - **Invest**: Invest money into Family Bank
                - **Houses**: Give Coin Multipliers in all game modes towards Family Earnings
                - **Home Universe**: Earn Extra gold in Home Universe,
                - **Real Estate**: Own multiple houses, swap your current house buy and sell real estate
                - **Family Summon**: Each family member has access and can equip the family summon
                

                **Family Position Explanations**
                - **Head of Household**:  All operations.
                - **Partner**:  Can equip/update family summon, change equipped house and give allowances
                - **Kids**:  Can equip family summon.
                """), colour=0x7289da)

                embed_list = [first_page, estates_page, summon_page, activity_page, family_explanations]

                buttons = []
                
                if not member:
                    buttons.append(
                        manage_components.create_button(style=3, label="Say Hello", custom_id="hello")
                    )
                    
                if is_head:
                    buttons = [
                        manage_components.create_button(style=3, label="Check/Purchase Properties", custom_id="property"),
                        manage_components.create_button(style=3, label="Equip/Set Family Summon", custom_id="summon"),
                    ]
                elif is_partner:
                    buttons = [
                        manage_components.create_button(style=3, label="Check Properties", custom_id="property"),
                        manage_components.create_button(style=3, label="Equip/Set Family Summon", custom_id="summon"),
                    ]
                    
                elif is_kid:
                    buttons = [
                        manage_components.create_button(style=3, label="View Properties", custom_id="property"),
                        manage_components.create_button(style=3, label="Equip Family Summon", custom_id="summon"),
                    ]
                    
                custom_action_row = manage_components.create_actionrow(*buttons)
                
                async def custom_function(self, button_ctx):
                    try:
                        if button_ctx.author == ctx.author:
                            if button_ctx.custom_id == "hello":
                                await button_ctx.defer(ignore=True)
                                update_query = {
                                        '$push': {'TRANSACTIONS': f"{button_ctx.author} said 'Hello'!"}
                                    }
                                response = db.updateFamily({'HEAD': family['HEAD']}, update_query)
                                await ctx.send(f"**{button_ctx.author.mention}** Said Hello! to {family_name}!")
                                self.stop = True
                                return
                            elif button_ctx.custom_id == "property":
                                await button_ctx.defer(ignore=True)
                                real_estate_message = " "
                                property_buttons = []
                                balance_message = '{:,}'.format(savings)
                                if is_head:
                                    real_estate_message = "\nWelcome Head of Household!\n**View Property** - View Owned Properties or make a Move!\n**Buy New Home** - Buy a new Home for your Family\n**Browse Housing Catalog** - View all Properties for sale"
                                    property_buttons = [
                                    manage_components.create_button(style=2, label="Owned Properties", custom_id="equip"),
                                    manage_components.create_button(style=3, label="Buy/Sell Houses", custom_id="buy"),
                                    manage_components.create_button(style=1, label="Browse Housing Catalog", custom_id="browse"),
                                    manage_components.create_button(style=ButtonStyle.red, label="Quit", custom_id="q")
                                    
                                ]
                                if is_partner:
                                    real_estate_message = "\nWelcome Partner!\n**View Property** - View Owned Properties or make a Move!\n**Browse Housing Catalog** - View all Properties for sale"
                                    property_buttons = [
                                    manage_components.create_button(style=1, label="Owned Properties", custom_id="equip"),
                                    manage_components.create_button(style=1, label="Browse Housing Catalog", custom_id="browse"),
                                    manage_components.create_button(style=ButtonStyle.red, label="Quit", custom_id="q")
                                ]
                                if is_kid:
                                    real_estate_message = "\nWelcome Kids!\n**View Property** - View Owned Properties"
                                    property_buttons = [
                                    manage_components.create_button(style=1, label="View Properties", custom_id="view"),
                                    manage_components.create_button(style=ButtonStyle.red, label="Quit", custom_id="q")
                                ]
                                property_action_row = manage_components.create_actionrow(*property_buttons)
                                real_estate_screen = discord.Embed(title=f"Anime VS+ Real Estate", description=textwrap.dedent(f"""\
                                {real_estate_message}
                                *Current Savings*: 
                                :coin: **{balance_message}**
                                """), color=0xe74c3c)
                                real_estate_screen.set_image(url="https://thumbs.gfycat.com/FormalBlankGeese-max-1mb.gif")
                                
                                msg = await ctx.send(embed=real_estate_screen, components=[property_action_row])
                                def check(button_ctx):
                                    return button_ctx.author == ctx.author
                                try:
                                    house_embed_list = []
                                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[property_action_row], timeout=120, check=check)
                                    if button_ctx.custom_id == "q":
                                        await ctx.send("Real Estate Menu Closed...")
                                        return
                                    if button_ctx.custom_id == "browse":
                                        await button_ctx.defer(ignore=True)
                                        all_houses = db.queryAllHouses()
                                        for houses in all_houses:
                                            house_name = houses['HOUSE']
                                            house_price = houses['PRICE']
                                            price_message = '{:,}'.format(houses['PRICE'])
                                            house_img = houses['PATH']
                                            house_multiplier = houses['MULT']                                            
                                            embedVar = discord.Embed(title= f"{house_name}", description=textwrap.dedent(f"""
                                            💰 **Price**: {price_message}
                                            〽️ **Multiplier**: {house_multiplier}
                                            Family earns **{house_multiplier}x** :coin: per match!
                                            """))
                                            embedVar.set_image(url=house_img)
                                            house_embed_list.append(embedVar)
                                        await Paginator(bot=self.bot, ctx=ctx, useQuitButton=True, deleteAfterTimeout=True, pages=house_embed_list).run()
                                    if button_ctx.custom_id == "view":
                                        await button_ctx.defer(ignore=True)
                                        for houses in estate_data_list:
                                            house_name = houses['HOUSE']
                                            house_price = houses['PRICE']
                                            price_message = '{:,}'.format(houses['PRICE'])
                                            house_img = houses['PATH']
                                            house_multiplier = houses['MULT']                                            
                                            embedVar = discord.Embed(title= f"{house_name}", description=textwrap.dedent(f"""
                                            💰 **Price**: {price_message}
                                            〽️ **Multiplier**: {house_multiplier} 
                                            Family earns **{house_multiplier}x** :coin: per match!
                                            """))
                                            embedVar.set_image(url=house_img)
                                            house_embed_list.append(embedVar)
                                        await Paginator(bot=self.bot, ctx=ctx, useQuitButton=True, deleteAfterTimeout=True, pages=house_embed_list).run()
                                    elif button_ctx.custom_id == "equip":
                                        await button_ctx.defer(ignore=True)
                                        for houses in estate_data_list:
                                            house_name = houses['HOUSE']
                                            house_price = houses['PRICE']
                                            price_message = '{:,}'.format(houses['PRICE'])
                                            house_img = houses['PATH']
                                            house_multiplier = houses['MULT']                                            
                                            embedVar = discord.Embed(title= f"{house_name}", description=textwrap.dedent(f"""
                                            💰 **Price**: {price_message}
                                            〽️ **Multiplier**: {house_multiplier} 
                                            Family earns **{house_multiplier}x** :coin: per match!
                                            """))
                                            embedVar.set_image(url=house_img)
                                            house_embed_list.append(embedVar)
                                            
                                        equip_buttons = [
                                            manage_components.create_button(style=3, label="🏠 Equip House", custom_id="equip"),

                                        ]
                                        equip_action_row = manage_components.create_actionrow(*equip_buttons)
                                        async def equip_function(self, button_ctx):
                                            house_name = str(button_ctx.origin_message.embeds[0].title)
                                            await button_ctx.defer(ignore=True)
                                            if button_ctx.author == ctx.author:
                                                if button_ctx.custom_id == "equip":
                                                    transaction_message = f"🏠 | {ctx.author} changed the family house to **{str(button_ctx.origin_message.embeds[0].title)}**."
                                                    update_query = {
                                                            '$set': {'HOUSE': house_name},
                                                            '$push': {'TRANSACTIONS': transaction_message}
                                                        }
                                                    response = db.updateFamily({'HEAD': family['HEAD']}, update_query)
                                                    await ctx.send(f"**{family_name}** moved into their **{house_name}**! Enjoy your new Home!")
                                                    self.stop = True
                                            else:
                                                await ctx.send("This is not your command.")
                                        await Paginator(bot=self.bot, ctx=ctx, useQuitButton=True, deleteAfterTimeout=True, pages=house_embed_list, customActionRow=[
                                            equip_action_row,
                                            equip_function,
                                        ]).run()
                                                                                    
                                    elif button_ctx.custom_id == "buy":
                                        house_embed_list = []
                                        all_houses = db.queryAllHouses()
                                        owned = False
                                        current_savings = '{:,}'.format(savings)
                                        for houses in all_houses:
                                            house_name = houses['HOUSE']
                                            house_price = houses['PRICE']
                                            price_message = '{:,}'.format(houses['PRICE'])
                                            house_img = houses['PATH']
                                            house_multiplier = houses['MULT']       
                                            ownership_message = f"💰 **Price**: {price_message}"  
                                            sell_price = house_price *.80
                                            sell_message = " "
                                            sell_message = f"💱 Sells for **{'{:,}'.format(houses['PRICE'])}**"                                  
                                            embedVar = discord.Embed(title= f"{house_name}", description=textwrap.dedent(f"""
                                            **Current Savings**: :coin: **{current_savings}**                                                                    
                                            {ownership_message}
                                            〽️ **Multiplier**: {house_multiplier}
                                            {sell_message}
                                            Family earns **{house_multiplier}x** :coin: per match!
                                            """))
                                            embedVar.set_image(url=house_img)
                                            house_embed_list.append(embedVar)
                                        
                                        econ_buttons = [
                                            manage_components.create_button(style=3, label="💰 Buy House", custom_id="buy"),
                                            manage_components.create_button(style=3, label="💱 Sell House", custom_id="sell"),

                                        ]
                                        econ_action_row = manage_components.create_actionrow(*econ_buttons)
                                        
                                        async def econ_function(self, button_ctx):
                                            house_name = str(button_ctx.origin_message.embeds[0].title)
                                            await button_ctx.defer(ignore=True)
                                            if button_ctx.author == ctx.author:
                                                if button_ctx.custom_id == "buy":
                                                    if house_name in estates_list:
                                                        await ctx.send("You already own this House. Click 'Sell' to sell it!")
                                                        self.stop = True
                                                        return
                                                    if house_name == 'Cave':
                                                        await button_ctx.send("You already own your **Ancestral Cave.**")
                                                        #self.stop = True
                                                        return
                                                    try: 
                                                        house = db.queryHouse({'HOUSE': {"$regex": f"^{str(house_name)}$", "$options": "i"}})
                                                        currentBalance = family['BANK']
                                                        cost = house['PRICE']
                                                        house_name = house['HOUSE']
                                                        if house:
                                                            if house_name == family['HOUSE']:
                                                                await ctx.send(m.USERS_ALREADY_HAS_HOUSE, delete_after=5)
                                                            else:
                                                                newBalance = currentBalance - cost
                                                                if newBalance < 0 :
                                                                    await ctx.send("You have an insufficent Balance")
                                                                else:
                                                                    await crown_utilities.cursefamily(cost, family['HEAD'])
                                                                    transaction_message = f":coin: | {ctx.author} bought a new **{str(button_ctx.origin_message.embeds[0].title)}**."
                                                                    response = db.updateFamily({'HEAD': family['HEAD']},{'$set':{'HOUSE': str(house_name)},'$push': {'TRANSACTIONS': transaction_message}})
                                                                    response2 = db.updateFamily({'HEAD': family['HEAD']},{'$addToSet':{'ESTATES': str(house_name)}})
                                                                    await ctx.send(m.PURCHASE_COMPLETE_H + "Enjoy your new Home!")
                                                                    return
                                                        else:
                                                            await ctx.send(m.HOUSE_DOESNT_EXIST)
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
                                                if button_ctx.custom_id == "sell":
                                                    house = db.queryHouse({'HOUSE': {"$regex": f"^{str(house_name)}$", "$options": "i"}})
                                                    cost = house['PRICE']
                                                    formatted_cost = '{:,}'.format(cost)
                                                    if house_name not in family['ESTATES']:
                                                        await ctx.send("You need to Own this House to to sell it!")
                                                        #self.stop = True
                                                        return
                                                    if house_name == family['HOUSE']:
                                                        await button_ctx.send("You cannot sell your **Primary Residence**.")
                                                        #self.stop = True
                                                        return
                                                    if house_name == 'Cave':
                                                        await button_ctx.send("You cannot sell your **Ancestral Cave.**")
                                                        #self.stop = True
                                                        return
                                                    elif house_name in family['ESTATES']:
                                                        await crown_utilities.blessfamily(cost, family['HEAD'])
                                                        transaction_message = f":coin: | {ctx.author} sold the family home: **{str(house_name)}**."
                                                        response = db.updateFamily({'HEAD': family['HEAD']},{'$pull':{'ESTATES': str(house_name)},'$push': {'TRANSACTIONS': transaction_message}})
                                                        await ctx.send(f'{family_name} sold their **{house_name}** for **{formatted_cost}**')
                                                        #self.stop = True
                                                        return
                                            else:
                                                await ctx.send("This is not your command.")
                                        await Paginator(bot=self.bot, ctx=ctx, useQuitButton=True, deleteAfterTimeout=True, pages=house_embed_list, customActionRow=[
                                            econ_action_row,
                                            econ_function,
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
                            elif button_ctx.custom_id == "summon":
                                await button_ctx.defer(ignore=True)
                                summon_object = family['SUMMON']
                                summon = list(summon_object.values())[0]
                                head_vault = db.queryVault({'DID' : head_data['DID']})
                                pet_name = ""
                                summon_bond = 0
                                summon_lvl = 0
                                summon_type = "Unbound"
                                power = 0
                                path = "N/A"
                                found_summon_in_vault = False
                                if head_vault:
                                    vault_summons = head_vault['PETS']
                                    for l in vault_summons:
                                        if summon == l['NAME']:
                                            found_summon_in_vault = True
                                            level = l['LVL']
                                            xp = l['EXP']
                                            pet_ability = list(l.keys())[3]
                                            pet_ability_power = list(l.values())[3]
                                            power = (l['BOND'] * l['LVL']) + pet_ability_power
                                            pet_info = {'NAME': l['NAME'], 'LVL': l['LVL'], 'EXP': l['EXP'], pet_ability: pet_ability_power, 'TYPE': l['TYPE'], 'BOND': l['BOND'], 'BONDEXP': l['BONDEXP'], 'PATH': l['PATH']}
                                            summon_img = pet_info['PATH']
                                            pet_name = pet_info["NAME"]
                                            summon_bond = l["BOND"]
                                            summon_lvl = level
                                            summon_type = pet_info["TYPE"]
                                            power = (summon_bond * summon_lvl) + int(pet_ability_power)
                                            path = pet_info["PATH"]
                                            summon_file = crown_utilities.showsummon(summon_img, pet_info['NAME'], enhancer_mapping[pet_info['TYPE']], pet_info['LVL'], pet_info['BOND'])
                                    if found_summon_in_vault == False:
                                        pet_info = db.queryPet({'PET': summon})
                                        summon_img = pet_info['PATH']
                                        pet_ability_power = list(pet_info['ABILITIES'][0].values())[0]
                                        pet_ability = list(pet_info['ABILITIES'])[0]
                                        summon_type = pet_ability['TYPE']
                                        summon_bond = 0
                                        pet_name = pet_info["PET"]
                                        summon_lvl = 0
                                        summon_img = pet_info['PATH']
                                        power = (summon_bond * summon_lvl) + int(pet_ability_power)
                                        path = pet_info["PATH"]
                                        summon_file = crown_utilities.showsummon(summon_img, pet_info['PET'], enhancer_mapping[summon_type], 0, 0)
                                else:
                                    partnervault =  db.queryVault({'DID' : partner_data['DID']})
                                    if partnervault:
                                        vault_summons = partnervault['PETS']
                                        for l in vault_summons:
                                            if summon == l['NAME']:
                                                found_summon_in_vault = True
                                                level = l['LVL']
                                                xp = l['EXP']
                                                pet_ability = list(l.keys())[3]
                                                pet_ability_power = list(l.values())[3]
                                                power = (l['BOND'] * l['LVL']) + pet_ability_power
                                                pet_info = {'NAME': l['NAME'], 'LVL': l['LVL'], 'EXP': l['EXP'], pet_ability: pet_ability_power, 'TYPE': l['TYPE'], 'BOND': l['BOND'], 'BONDEXP': l['BONDEXP'], 'PATH': l['PATH']}
                                                summon_img = pet_info['PATH']
                                                summon_type = pet_info["TYPE"]
                                                summon_file = crown_utilities.showsummon(summon_img, pet_info['NAME'], enhancer_mapping[pet_info['TYPE']], pet_info['LVL'], pet_info['BOND'])
                                                pet_name = pet_info["NAME"]
                                                summon_bond = pet_info["BOND"]
                                                summon_lvl = level
                                                power = (summon_bond * summon_lvl) + int(pet_ability_power)
                                                path = pet_info["PATH"]
                                        if found_summon_in_vault == False:
                                            pet_info = db.queryPet({'PET': summon})
                                            summon_img = pet_info['PATH']
                                            pet_ability_power = list(pet_info['ABILITIES'][0].values())[0]
                                            pet_ability = list(pet_info['ABILITIES'])[0]
                                            summon_type = pet_ability['TYPE']
                                            summon_bond = 0
                                            pet_name = pet_info["PET"]
                                            summon_lvl = 0
                                            summon_img = pet_info['PATH']
                                            power = (summon_bond * summon_lvl) + int(pet_ability_power)
                                            path = pet_info["PATH"]
                                            summon_file = crown_utilities.showsummon(summon_img, pet_info['PET'], enhancer_mapping[summon_type], 0, 0)

                                    else:
                                        pet_info = db.queryPet({'PET': summon})
                                        summon_img = pet_info['PATH']
                                        pet_ability_power = list(pet_info['ABILITIES'][0].values())[0]
                                        pet_ability = list(pet_info['ABILITIES'])[0]
                                        summon_type = pet_ability['TYPE']
                                        summon_bond = 0
                                        pet_name = pet_info["PET"]
                                        summon_lvl = 0
                                        summon_img = pet_info['PATH']
                                        power = (summon_bond * summon_lvl) + int(pet_ability_power)
                                        path = pet_info["PATH"]
                                        summon_file = crown_utilities.showsummon(summon_img, pet_info['PET'], enhancer_mapping[summon_type], 0, 0)
                                summon_buttons = []
                                if is_head:
                                    summon_message = "Welcome Head of Household! Equip or Change Family Summon Here!"
                                    summon_buttons = [
                                    manage_components.create_button(style=2, label="Change Summon", custom_id="change"),
                                    manage_components.create_button(style=3, label="Equip Family Summon", custom_id="equip"),
                                    
                                ]
                                if is_partner:
                                    summon_message = "Welcome Partner! Equip or Change Family Summon Here!"
                                    summon_buttons = [
                                    manage_components.create_button(style=1, label="Change Summon", custom_id="change"),
                                    manage_components.create_button(style=1, label="Equip Family Summon", custom_id="equip"),
                                ]
                                if is_kid:
                                    summon_message = "Welcome Kids! Equip Family Summon Here!"
                                    summon_buttons = [
                                    manage_components.create_button(style=1, label="Equip Family Summon", custom_id="equip"),
                                ]
                                summon_action_row = manage_components.create_actionrow(*summon_buttons)
                                summon_screen = discord.Embed(title=f"Anime VS+ Family", description=textwrap.dedent(f"""\
                                {summon_message}
                                :dna: : **{pet_name}**
                                *Bond* **{summon_bond}**
                                *Level* **{summon_lvl}**
                                :small_blue_diamond: **{summon_type}** ~ **{power}**{enhancer_suffix_mapping[summon_type]}
                                🦠 : **{enhancer_mapping[summon_type]}**
                                """), color=0xe74c3c)
                                summon_screen.set_image(url=path)
                                
                                msg = await ctx.send(embed=summon_screen, components=[summon_action_row])
                                def check(button_ctx):
                                    return button_ctx.author == ctx.author
                                try:
                                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[summon_action_row], timeout=120, check=check)
                                    
                                    if button_ctx.custom_id == "change":
                                        await button_ctx.defer(ignore=True)
                                        query = {'DID': str(button_ctx.author.id)}
                                        d = db.queryUser(query)
                                        vault = db.queryVault({'DID': d['DID']})
                                        if vault:
                                            name = d['DISNAME'].split("#",1)[0]
                                            avatar = d['AVATAR']
                                            balance = vault['BALANCE']
                                            current_summon = d['PET']
                                            pets_list = vault['PETS']
                                            
                                            total_pets = len(pets_list)

                                            pets=[]
                                            bond_message = ""
                                            lvl_message = ""
                                            embed_list = []
                                            for pet in pets_list:
                                                #cpetmove_ap= (cpet_bond * cpet_lvl) + list(cpet.values())[3] # Ability Power
                                                bond_message = ""
                                                if pet['BOND'] == 3:
                                                    bond_message = ":star2:"
                                                lvl_message = ""
                                                if pet['LVL'] == 10:
                                                    lvl_message = ":star:"
                                                
                                                pet_ability = list(pet.keys())[3]
                                                pet_ability_power = list(pet.values())[3]
                                                power = (pet['BOND'] * pet['LVL']) + pet_ability_power
                                                dash_pet_info = db.queryPet({'PET' : pet['NAME']})
                                                if dash_pet_info:
                                                    pet_available = dash_pet_info['AVAILABLE']
                                                    pet_exclusive = dash_pet_info['EXCLUSIVE']
                                                    pet_universe = dash_pet_info['UNIVERSE']
                                                icon = "🧬"
                                                if pet_available and pet_exclusive:
                                                    icon = ":fire:"
                                                elif pet_available == False and pet_exclusive ==False:
                                                    icon = ":japanese_ogre:"

                                                embedVar = discord.Embed(title= f"{pet['NAME']}", description=textwrap.dedent(f"""
                                                {icon}
                                                _Bond_ **{pet['BOND']}** {bond_message}
                                                _Level_ **{pet['LVL']} {lvl_message}**
                                                :small_blue_diamond: **{pet_ability}:** {power}{enhancer_suffix_mapping[pet['TYPE']]}
                                                🦠 **Type:** {pet['TYPE']}"""), 
                                                colour=0x7289da)
                                                embedVar.set_thumbnail(url=avatar)
                                                embedVar.set_footer(text=f"{pet['TYPE']}: {enhancer_mapping[pet['TYPE']]}")
                                                embed_list.append(embedVar)
                                            
                                            buttons = [
                                                manage_components.create_button(style=3, label="Share Summon", custom_id="share"),
                                            ]
                                            custom_action_row = manage_components.create_actionrow(*buttons)

                                            async def custom_function(self, button_ctx):
                                                if button_ctx.author == ctx.author:
                                                    updated_vault = db.queryVault({'DID': d['DID']})
                                                    sell_price = 0
                                                    selected_summon = str(button_ctx.origin_message.embeds[0].title)
                                                    user_query = {'DID': str(ctx.author.id)}
                                                    user_vault = db.queryVault(user_query)

                                                    vault_summons = user_vault['PETS']
                                                    for l in vault_summons:
                                                        if selected_summon == l['NAME']:
                                                            level = l['LVL']
                                                            xp = l['EXP']
                                                            pet_ability = list(l.keys())[3]
                                                            pet_ability_power = list(l.values())[3]
                                                            power = (l['BOND'] * l['LVL']) + pet_ability_power
                                                            pet_info = {'NAME': l['NAME'], 'LVL': l['LVL'], 'EXP': l['EXP'], pet_ability: pet_ability_power, 'TYPE': l['TYPE'], 'BOND': l['BOND'], 'BONDEXP': l['BONDEXP'], 'PATH': l['PATH']}
                                                    if button_ctx.custom_id == "share":
                                                        #update_query = {'$set': {'SUMMON': }}
                                                        #filter_query = [{'type.' + "NAME": str(pet)}]
                                                        #response = db.updateVault(query, update_query, filter_query)
                                                        transaction_message = f":dna: | {ctx.author} changed the family summon to **{str(button_ctx.origin_message.embeds[0].title)}**."
                                                        response = db.updateFamily({'HEAD': family['HEAD']}, {'$set': {'SUMMON': pet_info}, '$push': {'TRANSACTIONS': transaction_message}})
                                                        await button_ctx.send(f"🧬 **{str(button_ctx.origin_message.embeds[0].title)}** is now the {family_name} **Summon**.")
                                                        self.stop = True
                                                        return
                                                else:
                                                    await ctx.send("This is not your Summons list.")
                                            await Paginator(bot=self.bot, ctx=ctx, pages=embed_list, timeout=60, customActionRow=[
                                                custom_action_row,
                                                custom_function,
                                            ]).run()

                                    elif button_ctx.custom_id == "equip":
                                        try:
                                            await button_ctx.defer(ignore=True)
                                            transaction_message = f"{ctx.author} equipped the family summon : **{str(pet_info['NAME'])}**."
                                            response = db.updateUserNoFilter({'DID': str(button_ctx.author.id)}, {'$set' : {'PET': pet_info['NAME'], 'FAMILY_PET': True}})
                                            response2 = db.updateFamily({'HEAD': family['HEAD']}, {'$push': {'TRANSACTIONS': transaction_message}})
                                            await button_ctx.send(f"🧬 **{str(pet_info['NAME'])}** is now your **Summon**.")
                                            self.stop = True
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
                
                await Paginator(bot=self.bot, useQuitButton=True, disableAfterTimeout=True, ctx=ctx, pages=embed_list, timeout=60, customActionRow=[
                    custom_action_row,
                    custom_function,
                ]).run()  
            else:
                await ctx.send(m.FAMILY_DOESNT_EXIST)
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

async def raid(ctx, guild):
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
            await battle_commands(main, ctx, battle, p1, None, p2, player3=None)
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

def setup(bot):
    bot.add_cog(Lookup(bot))

def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]

def guild_buff_toggle(player, team):
    guild_buff_on = team['GUILD_BUFF_ON']
    team_query = {'TEAM_NAME': team['TEAM_NAME']}
    return_message = {}
    
    if guild_buff_on:
        transaction_message = f"🔴 | {player['DISNAME']} turned off Guild Buff."
        new_value_query = {
            '$set': {'GUILD_BUFF_ON': False},
            '$push': {'TRANSACTIONS': transaction_message}
            }
        response = db.updateTeam(team_query, new_value_query)
        if response:
            return {"MSG": "Guild Buff has been turned off."}
        else:
            return False
    else:
        transaction_message = f"🟢 | {player['DISNAME']} turned on Guild Buff."
        new_value_query = {
            '$set': {'GUILD_BUFF_ON': True},
            '$push': {'TRANSACTIONS': transaction_message}
            }
        response = db.updateTeam(team_query, new_value_query)
        if response:
            return {"MSG": "Guild Buff has been turned on."}
        else:
            return False


async def apply(self, ctx, owner: User):
    owner_profile = db.queryUser({'DID': str(owner.id)})
    team_profile = db.queryTeam({'TEAM_NAME': owner_profile['TEAM'].lower()})

    if owner_profile['TEAM'] == 'PCG':
        await ctx.send(m.USER_NOT_ON_TEAM, delete_after=5)
    else:

        if owner_profile['DISNAME'] == team_profile['OWNER']:
            member_profile = db.queryUser({'DID': str(ctx.author.id)})
            if member_profile['LEVEL'] < 4:
                await ctx.send(f"🔓 Unlock Guilds by completing Floor 3 of the 🌑 Abyss! Use /solo to enter the abyss.")
                return

            # If user is part of a team you cannot add them to your team
            if member_profile['TEAM'] != 'PCG':
                await ctx.send("You're already in a Guild. You may not join another guild.")
                return
            else:
                team_buttons = [
                    manage_components.create_button(
                        style=ButtonStyle.blue,
                        label="Accept",
                        custom_id="Yes"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red,
                        label="Deny",
                        custom_id="No"
                    )
                ]
                team_buttons_action_row = manage_components.create_actionrow(*team_buttons)
                enhancer_mapping
                msg = await ctx.send(f"{ctx.author.mention}  applies to join **{team_profile['TEAM_DISPLAY_NAME']}**. Owner, Officers, or Captains - Please accept or deny".format(self), components=[team_buttons_action_row])

                def check(button_ctx):
                    return str(button_ctx.author) == str(owner)

                try:
                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[team_buttons_action_row], timeout=120, check=check)
                    
                    if button_ctx.custom_id == "No":
                        await button_ctx.send("Application Denied.")
                        await msg.delete()
                        return

                    if button_ctx.custom_id == "Yes":
                        team_query = {'TEAM_NAME': team_profile['TEAM_NAME'].lower()}
                        new_value_query = {'$push': {'MEMBERS': member_profile['DISNAME']}}
                        response = db.addTeamMember(team_query, new_value_query, owner_profile['DISNAME'], member_profile['DISNAME'])
                        await button_ctx.send(response)
                except:
                    await msg.delete()
        else:
            await ctx.send(m.OWNER_ONLY_COMMAND, delete_after=5)


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