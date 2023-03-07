from numpy import save
import db
import crown_utilities
import discord
from discord import Embed
import textwrap
import random


class Player:
    def __init__(self, auto_save, disname, did, avatar, association, guild, family, equipped_title, equipped_card, equipped_arm, equippedsummon, equipped_talisman,completed_tales, completed_dungeons, boss_wins, rift, rebirth, level, explore, save_spot, performance, trading, boss_fought, difficulty, storage_type, used_codes, battle_history, pvp_wins, pvp_loss, retries, prestige, patron, family_pet, explore_location):
        self.disname = disname
        self.did = did
        self.avatar = avatar
        self.association = association
        self.guild = guild
        self.family = family
        self.equipped_title = equipped_title
        self.equipped_card = equipped_card
        self.equipped_arm = equipped_arm
        self.equippedsummon = equippedsummon
        self.equipped_talisman = equipped_talisman
        self.completed_tales = completed_tales
        self.completed_dungeons = completed_dungeons
        self.boss_wins = boss_wins
        self.rift = rift
        self.rebirth = rebirth
        self.rebirthBonus = rebirth * 10
        self.level = level
        self.explore = explore
        self.save_spot = save_spot
        self.performance = performance
        self.trading = trading
        self.boss_fought = boss_fought
        self.difficulty = difficulty
        self.storage_type = storage_type
        self.used_codes = used_codes
        self.battle_history = battle_history
        self.pvp_wins = pvp_wins
        self.pvp_loss = pvp_loss
        self.retries = retries
        self.prestige = prestige
        self.patron = True
        self.family_pet = family_pet
        self._is_locked_feature = False
        self._locked_feature_message = ""
        self.explore_location = explore_location
        self.autosave = auto_save

        self.owned_destinies = []

        self.talisman_message = "📿 | No Talisman Equipped"

        self.summon_power_message = ""
        self.summon_lvl_message = ""
        self.rift_on = False
        self.auto_battle = False
        
        # Guild Config
        self._default_guild = ""
        self.guild_info = "" 
        self.guild_buff = ""
        self.guild_query = ""
        self.guild_buff_update_query = ""
        self.filter_query = ""

        # Association Config
        self.association_info = ""
        self.crestlist = ""
        self.crestsearch = False
        

        # Vault Infoo
        self.vault = db.queryVault({'DID': str(self.did)})
        if self.vault:
            self._balance = self.vault['BALANCE']
            self._cards = self.vault['CARDS']
            self._titles = self.vault['TITLES']
            self._arms = self.vault['ARMS']
            self.summons = self.vault['PETS']
            self._deck = self.vault['DECK']
            self._card_levels = self.vault['CARD_LEVELS']
            self._quests = self.vault['QUESTS']
            self._destiny = self.vault['DESTINY']
            self._gems = self.vault['GEMS']
            self._storage = self.vault['STORAGE']
            self._talismans = self.vault['TALISMANS']
            self._essence = self.vault['ESSENCE']
            self._tstorage = self.vault['TSTORAGE']
            self._astorage = self.vault['ASTORAGE']
            
            if self._destiny:
                for destiny in self._destiny:
                    self.owned_destinies.append(destiny['NAME'])

            self.list_of_cards = ""

        self._deck_card = ""
        self._deck_title = ""
        self._deck_arm = ""
        self._decksummon = ""
        self._deck_talisman = ""

        self._equipped_card_data = ""
        self._equipped_title_data = ""
        self._equipped_arm_data = ""
        self._equippedsummon_data = ""
        self._equippedsummon_power = 0
        self._equippedsummon_bond = 0
        self._equippedsummon_bondexp = 0
        self._equippedsummon_exp = 0
        self._equippedsummon_lvl = 0
        self._equippedsummon_type = ""
        self._equippedsummon_name = ""
        self._equippedsummon_ability_name = ""
        self._equippedsummon_image = ""
        self._equippedsummon_universe = ""
        
        self._universe_buff_msg = ""


    def set_talisman_message(self):
        try:
            print(self.equipped_talisman)
            if self.equipped_talisman != "NULL":
                for t in self._talismans:
                    if t["TYPE"].upper() == self.equipped_talisman.upper():
                        talisman_emoji = crown_utilities.set_emoji(self.equipped_talisman.upper())
                        talisman_durability = t["DUR"]
                        self.talisman_message = f"{talisman_emoji} | {self.equipped_talisman.title()} Talisman Equipped ⚒️ {talisman_durability}"
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
            print("Error setting talisman message.")
            return self.talisman_message
        

    def setsummon_messages(self):
        try:
            for summon in self.summons:
                if summon['NAME'] == self.equippedsummon:
                    activesummon = summon

            power = list(activesummon.values())[3]
            bond = activesummon['BOND']
            lvl = activesummon['LVL']
            s_type = activesummon['TYPE']
            if bond == 3:
                bond_message = "🌟"
            else:
                bond_message = " "
            
            if lvl == 10:
                lvl_message = "⭐"
            else:
                lvl_message = " "

            summon_ability_power = (bond * lvl) + power

            self.summon_power_message = f"🧬 | {self.equippedsummon}: {s_type.title()}: {summon_ability_power}{crown_utilities.enhancer_suffix_mapping[s_type]}"


            self.summon_lvl_message = f"🧬 | Bond {bond_message}{str(bond)} & Level {lvl_message}{str(lvl)}"

        except:
            print("Error setting summon message")
            return "Error"

    def set_explore(self, universe):
        
        if self.level < 25 and self.prestige == 0:             
            return "🔓 Unlock the Explore Mode by completing Floor 25 of the 🌑 Abyss! Use **Abyss** in /solo to enter the abyss."
        
        if universe.lower() == "all":
            db.updateUserNoFilter({'DID': str(self.did)}, {'$set': {'EXPLORE': True, 'EXPLORE_LOCATION': 'NULL'}})
            return f":milky_way: | Exploring **All universes!**"

        universe_selected = db.queryUniverse({"TITLE": {"$regex": f"^{universe}$", "$options": "i"}})

        if universe_selected:
            db.updateUserNoFilter({'DID': str(self.did)}, {'$set': {'EXPLORE': True, 'EXPLORE_LOCATION': universe_selected['TITLE']}})
            return f":milky_way: | You are Exploring **{universe_selected['TITLE']}**"

    
    def set_rift_on(self):
        if self.rift == 1:
            self.rift_on = True
        return self.rift_on


    async def set_guild_data(self):
        if self.guild != "PCG":
            self.guild_info = db.queryTeam({'TEAM_NAME': self.guild.lower()})
            self.guild_buff = await crown_utilities.guild_buff_update_function(self.guild)
            if self.guild_buff:
                if self.guild_buff['Rift'] is True:
                    self.rift_on = True
                    self.guild_query = self.guild_buff['QUERY']
                    self.guild_buff_update_query = self.guild_buff['UPDATE_QUERY']
                    self.filter_query = self.guild_buff['FILTER_QUERY']
                

            if self.association != "PCG":
                self.association_info = db.queryGuildAlt({'GNAME': self.association})
                if self.association_info:
                    self.crestlist = self.association_info['CREST']
                    self.crestsearch = True


    def set_auto_battle_on(self, mode):
        if self.patron != True and mode in crown_utilities.AUTO_BATTLE_M:
            self.auto_battle = True
        return self.auto_battle

    def set_selectable_bosses(self, ctx, mode):
        _all_universes = db.queryAllUniverse()
        
        
        def get_bosses(universes):
            all_universes = []
            for uni in universes:
                if uni["TITLE"] in self.completed_dungeons:
                    all_universes.append(uni)
                    #print(uni["TITLE"])
            if not all_universes:
                return None
            else:
                return all_universes
        all_universes = get_bosses(_all_universes)
        #print(all_universes)
        available_universes = []
        selected_universe = ""
        universe_menu = []
        universe_embed_list = []
        available_dungeons_list = "Sadly, you have no available dungeons at this time!\n🌍 To unlock a Universe Dungeon you must first complete the Universe Tale!"
        can_fight_boss = False
        can_fight_message = "🗝️ | Conquer A Dungeon to Gain a Boss Key"
        if self.boss_fought == False:
            can_fight_boss = True
            can_fight_message = "📿| Boss Talismans ignore all Affinities. Be Prepared"
        difficulty = self.difficulty
        prestige_slider = 0
        p_message = ""
        aicon = crown_utilities.prestige_icon(self.prestige)
        if self.prestige > 0:
            prestige_slider = ((((self.prestige + 1) * (10 + self.rebirth)) /100))
            p_percent = (prestige_slider * 100)
            p_message = f"*{aicon} x{round(p_percent)}%*"
        if self.completed_tales:
            l = []
            for uni in self.completed_tales:
                if uni != "":
                    l.append(uni)
            available_dungeons_list = "\n".join(l)
        
        
        if len(self.completed_dungeons) > 25:
            all_universes = random.sample(all_universes, min(len(all_universes), 25))
            #print(all_universes)
        for uni in all_universes:
            if uni['TITLE'] in self.completed_dungeons:
                if uni != "":
                    if uni['GUILD'] != "PCG":
                        owner_message = f"{crown_utilities.crest_dict[uni['TITLE']]} **Crest Owned**: {uni['GUILD']}"
                    else: 
                        owner_message = f"{crown_utilities.crest_dict[uni['TITLE']]} *Crest Unclaimed*"
                    if uni['UNIVERSE_BOSS'] != "":
                        boss_info = db.queryBoss({"NAME": uni['UNIVERSE_BOSS']})
                        if boss_info:
                            if boss_info['NAME'] in self.boss_wins:
                                completed = "🟢"
                            else:
                                completed = "🔴"
                            embedVar = discord.Embed(title= f"{uni['TITLE']}", description=textwrap.dedent(f"""
                            {crown_utilities.crest_dict[uni['TITLE']]} **Boss**: :japanese_ogre: **{boss_info['NAME']}**
                            🎗️ **Boss Title**: {boss_info['TITLE']}
                            🦾 **Boss Arm**: {boss_info['ARM']}
                            🧬 **Boss Summon**: {boss_info['PET']}
                            
                            **Difficulty**: ⚙️ {difficulty.lower().capitalize()} {p_message}
                            **Soul Aquired**: {completed}
                            {owner_message}
                            """))
                            embedVar.set_image(url=boss_info['PATH'])
                            #embedVar.set_thumbnail(url=ctx.author.avatar_url)
                            embedVar.set_footer(text=f"{can_fight_message}")
                            universe_embed_list.append(embedVar)

        if not universe_embed_list:
            universe_embed_list = discord.Embed(title= f"👹 There are no available Bosses at this time.", description=textwrap.dedent(f"""
            __👹 How to unlock Bosses?__
            You unlock Bosses by completing the Universe Dungeon. Once a Dungeon has been completed the boss for that universe will be unlocked for you to fight!
            
            A Boss Key is required to Enter the Boss Arena.
            Earn Boss Keys by completing any Universe Dungeon

            __🌍 Available Universe Dungeons__
            {available_dungeons_list}
            """))
            # embedVar.set_image(url=boss_info['PATH'])
            universe_embed_list.set_thumbnail(url=ctx.author.avatar_url)
            # embedVar.set_footer(text="Use /tutorial")


        return universe_embed_list


    def set_selectable_universes(self, ctx, mode, fight_number = None):
        try:
            
            completed_message = f"**Completed**: 🔴"
            save_spot_text = "No Save Data"
            corruption_message = "📢 Not Corrupted"
            title = "UTITLE"
            title_message = "Universe Title"
            arm_message = "Universe Arm"
            summon_message = "Universe Summon"
            arm = "UARM"
            summon = "UPET"
            fight_emoji = ":crossed_swords:"
            list_of_opponents = "CROWN_TALES"
            save_spot_check = crown_utilities.TALE_M
            mode_check = "HAS_CROWN_TALES"
            completed_check = self.completed_tales
            all_universes = ""
            
            prestige_slider = 0
            p_message = ""
            aicon = crown_utilities.prestige_icon(self.prestige)
            if self.prestige > 0:
                prestige_slider = ((((self.prestige + 1) * (10 + self.rebirth)) /100))
                p_percent = (prestige_slider * 100)
                p_message = f"*{aicon} x{round(p_percent)}%*"
            if mode in crown_utilities.DUNGEON_M:
                title = "DTITLE"
                title_message = "Dungeon Title"
                arm_message = "Dungeon Arm"
                summon_message = "Dungeon Summon"
                fight_emoji = ":fire:"
                arm = "DARM"
                summon = "DPET"
                list_of_opponents = "DUNGEONS"
                save_spot_check = crown_utilities.DUNGEON_M
                mode_check = "HAS_DUNGEON"
                completed_check = self.completed_dungeons

            def get_dungeons(universes):
                all_universes = []
                for uni in universes:
                    if uni['TITLE'] in self.completed_tales:
                        all_universes.append(uni)
                if not all_universes:
                    return None
                else:
                    return all_universes
                
            def get_tales(universes):
                all_universes = []
                for uni in universes:
                    all_universes.append(uni)
                if not all_universes:
                    return None
                else:
                    return all_universes
                    
            def get_rifts(universes):
                rift_universes = []
                for uni in universes:
                    if uni['TIER'] == 9:
                        rift_universes.append(uni)
                return rift_universes
                
            if self.rift_on:
                if mode in crown_utilities.DUNGEON_M:
                    _all_universes = db.queryDungeonAllUniverse()
                    all_universes = get_dungeons(_all_universes)
                    if not all_universes:
                        return None
                if mode in crown_utilities.TALE_M:
                    _all_universes = db.queryTaleAllUniverse()
                    all_universes = get_tales(_all_universes)
                rift_universes = get_rifts(all_universes)
                num_rift_universes = len(rift_universes)
                if len(rift_universes) > 1:
                    num_rift_universes = random.randint(1, min(len(rift_universes), 3))
                selected_universes = random.sample(rift_universes, num_rift_universes)

                max_non_rift_universes = 25 - num_rift_universes
                non_rift_universes = [uni for uni in all_universes if uni['TIER'] != 9]
                selected_universes.extend(random.sample(non_rift_universes, min(len(non_rift_universes), max_non_rift_universes)))
                
                corruption_message = "📢 Not Corrupted | 🔮 *Crown Rifts*"

            if not self.rift_on:
                if mode in crown_utilities.DUNGEON_M:
                    _all_universes = db.queryDungeonUniversesNotRift()
                    all_universes = get_dungeons(_all_universes)
                    if not all_universes:
                        return None
                if mode in crown_utilities.TALE_M:
                    _all_universes = db.queryTaleUniversesNotRift()
                    all_universes = get_tales(_all_universes)
                selected_universes = random.sample(all_universes, min(len(all_universes), 25))
                    

        
                

            universe_embed_list = []
            can_fight_message = ""
            for uni in selected_universes:
                save_spot_text = "No Save Data"
                can_fight_message = f"🔥 Dungeon | {uni['TITLE']} : /universes to view all Dungeon Drops."
                if uni[mode_check] == True:
                    if uni['TITLE'] in completed_check:
                        completed_message = f"**Completed**: 🟢"
                        can_fight_message = f"🔥 Dungeon | Conquer {uni['TITLE']} Dungeon again for a Boss Key and Minor Reward."

                    if self.difficulty != "EASY":
                        for save in self.save_spot:
                            if save['UNIVERSE'] == uni['TITLE'] and save['MODE'] in save_spot_check:
                                save_spot_text = str((int(save['CURRENTOPPONENT']) + 1))
                    
                    if uni['CORRUPTED']:
                        corruption_message = "👾 **Corrupted**"

                    if uni['GUILD'] != "PCG":
                        owner_message = f"{crown_utilities.crest_dict[uni['TITLE']]} **Crest Owned**: {uni['GUILD']}"
                    else: 
                        owner_message = f"{crown_utilities.crest_dict[uni['TITLE']]} *Crest Unclaimed*"


                    embedVar = discord.Embed(title= f"{uni['TITLE']}", description=textwrap.dedent(f"""
                    {crown_utilities.crest_dict[uni['TITLE']]} **Number of Fights**: {fight_emoji} **{len(uni[list_of_opponents])}**
                    🎗️ **{title_message}**: {uni[title]}
                    🦾 **{arm_message}**: {uni[arm]}
                    🧬 **{summon_message}**: {uni[summon]}

                    **Saved Game**: :crossed_swords: *{save_spot_text}*
                    **Difficulty**: ⚙️ {self.difficulty.lower().capitalize()} {p_message}
                    {completed_message}
                    {corruption_message}
                    {owner_message}
                    """))
                    embedVar.set_image(url=uni['PATH'])
                    embedVar.set_thumbnail(url=ctx.author.avatar_url)
                    if mode not in crown_utilities.DUNGEON_M:
                        if self.rift_on:
                            if uni['TIER'] == 9:
                                embedVar.set_footer(text=f"🔮 Rift | Traverse {uni['TITLE']} : /universes to view all Rift Drops.")
                            else:
                                embedVar.set_footer(text=f"⚔️ Tales | Traverse {uni['TITLE']} : /universes to view all Tales Drops.")
                        else:
                            embedVar.set_footer(text=f"⚔️ Tales | Traverse {uni['TITLE']} : /universes to view all Tales Drops.")
                    else:
                        embedVar.set_footer(text=f"{can_fight_message}")
                        
                    universe_embed_list.append(embedVar)
                        

            return universe_embed_list

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

        
    async def set_guild_buff(self):
        guild_buff = await crown_utilities.guild_buff_update_function(self.guild.lower())
        if guild_buff['Auto Battle']:
            self.auto_battle = True
            update_team_response = db.updateTeam(guild_buff['QUERY'], guild_buff['UPDATE_QUERY'])


    def get_locked_feature(self, mode):
        if self.difficulty == "EASY" and mode in crown_utilities.EASY_BLOCKED:
            self._locked_feature_message = "Dungeons, Boss, PVP, Expplore, and Abyss fights are unavailable on Easy Mode! Use /difficulty to change your difficulty setting."
            self._is_locked_feature = True
            return
        
        if self.level < 26 and mode == "EXPLORE":
            self._locked_feature_message = "Explore fights are blocked until level 26"
            self._is_locked_feature = True
            return

        if mode in crown_utilities.DUNGEON_M and self.level < 41 and int(self.prestige) == 0:
            self._locked_feature_message = "🔓 Unlock **Dungeons** by completing **Floor 40** of the 🌑 **Abyss**! Use **Abyss** in /solo to enter the abyss."
            self._is_locked_feature = True
            return

        if mode in crown_utilities.BOSS_M and self.level < 61 and int(self.prestige) == 0:
            self._locked_feature_message = "🔓 Unlock **Boss Fights** by completing **Floor 60** of the 🌑 **Abyss**! Use **Abyss** in /solo to enter the abyss."
            self._is_locked_feature = True
            return

        if self.level < 4:
            self._locked_feature_message = f"🔓 Unlock **PVP** by completing **Floor 3** of the 🌑 Abyss! Use **Abyss** in /solo to enter the abyss."
            self._is_locked_feature = True
            return
            
        return self._is_locked_feature


    def get_battle_ready(self):
        try:
            if self._deck_card:
                self._equipped_card_data = self._deck_card
                self._equipped_title_data = self._deck_title
                self._equipped_arm_data = self._deck_arm
                self.equippedsummon = self._decksummon['PET']
                self.equipped_talisman = self._deck_talisman
            else:
                self._equipped_card_data = db.queryCard({'NAME': self.equipped_card})
                self._equipped_title_data = db.queryTitle({'TITLE': self.equipped_title})
                self._equipped_arm_data = db.queryArm({'ARM': self.equipped_arm})

            for summon in self.summons:
                if summon['NAME'] == self.equippedsummon:
                    activesummon = summon
            self._equippedsummon_ability_name = list(activesummon.keys())[3]
            self._equippedsummon_power = list(activesummon.values())[3]
            self._equippedsummon_bond = activesummon['BOND']
            self._equippedsummon_bondexp = activesummon['BONDEXP']
            self._equippedsummon_lvl = activesummon['LVL']
            self._equippedsummon_type = activesummon['TYPE']
            self._equippedsummon_name = activesummon['NAME']
            self._equippedsummon_image = activesummon['PATH']
            self._equippedsummon_exp = activesummon['EXP']
            self._equippedsummon_universe = db.queryPet({'PET': activesummon['NAME']})['UNIVERSE']
        except:
            print("Failed to get battle ready")

    def getsummon_ready(self, _card):
        _card.summon_ability_name = self._equippedsummon_ability_name
        _card.summon_power = self._equippedsummon_power
        _card.summon_lvl = self._equippedsummon_lvl
        _card.summon_type = self._equippedsummon_type
        _card.summon_bond = self._equippedsummon_bond
        _card.summon_bondexp = self._equippedsummon_bondexp
        _card.summon_exp = self._equippedsummon_exp
        _card.summon_name = self._equippedsummon_name
        _card.summon_image = self._equippedsummon_image
        _card.summon_universe = self._equippedsummon_universe
    
    def get_talisman_ready(self, card):
        if self.equipped_talisman:
            card._talisman = self.equipped_talisman
        else:
            card._talisman = "None"

        if self.equipped_talisman == "NULL":
            card._talisman = "None"


    def has_storage(self):
        if self._storage:
            return True
        else:
            return False


    def set_list_of_cards(self):
        cards = db.querySpecificCards(self._storage)
        self.list_of_cards = [x for x in cards]
        return self.list_of_cards


    def set_deck_config(self, selected_deck):
        try:
            active_deck = self._deck[selected_deck]
            self._deck_card = db.queryCard({'NAME': str(active_deck['CARD'])})
            self._deck_title = db.queryTitle({'TITLE': str(active_deck['TITLE'])})
            self._deck_arm = db.queryArm({'ARM': str(active_deck['ARM'])})
            self._decksummon = db.queryPet({'PET': str(active_deck['PET'])})
            self._deck_talisman = str(active_deck['TALISMAN'])
            self._equipped_card_data = self._deck_card
            self._equipped_title_data = self._deck_title
            self._equipped_arm_data = self._deck_arm
            self._equippedsummon_data = self._decksummon
            self.equipped_talisman = self._deck_talisman
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



