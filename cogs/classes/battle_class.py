import db
import crown_utilities
import discord
import textwrap
import time
now = time.asctime()
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_commands import create_option, create_choice
import unique_traits as ut

class Battle:
    def __init__(self, mode, _player):
        self.player = _player

        self.mode = mode
        self.is_tales_game_mode = False
        self.is_dungeon_game_mode = False
        self.is_explore_game_mode = False
        self.is_abyss_game_mode = False
        self.is_boss_game_mode = False
        self.is_tutorial_game_mode = False
        self.is_raid_game_mode = False
        self.is_scenario_game_mode = False
        self.is_pvp_game_mode = False
        self.is_available = True
        self.is_corrupted = False
        self.match_can_be_saved = False
        self.is_free_battle_game_mode = False
        self.is_co_op_mode = False
        self.is_duo_mode = False
        self.is_ai_opponent = False

        self.is_auto_battle_game_mode = False
        self.can_auto_battle = False

        self.list_of_opponents_by_name = []
        self.total_number_of_opponents = 0
        self.current_opponent_number = 0
        self.match_lineup = ""
        self.is_turn = 0
        self.turn_total = 0
        self.turn_zero_has_happened = False
        self.max_turns_allowed = 250
        self.previous_moves = ["Match has started"]
        self.previous_moves_len = 0
        self.main_battle_options = ["1", "2", "3", "4"]
        self.battle_options = ["1", "2", "3", "4"]
        self.battle_buttons = []
        self.co_op_buttons = []
        self.utility_buttons = []
        self.rematch_buff = False

        self.continue_fighting = True

        self.selected_universe = ""
        self.selected_universe_full_data = ""

        self._ai_title = ""
        self._ai_arm = ""
        self._ai_summon = ""
        self._ai_opponent_card_data = ""
        self._ai_opponent_title_data = ""
        self._ai_opponent_arm_data = ""
        self._ai_opponentsummon_data = ""
        self._ai_opponentsummon_power = 0
        self._ai_opponentsummon_bond = 0
        self._ai_opponentsummon_lvl = 0
        self._ai_opponentsummon_type = ""
        self._ai_opponentsummon_name = ""
        self._ai_opponentsummon_universe = ""
        self._ai_opponentsummon_ability_name = ""
        self._ai_opponentsummon_image = ""
        self._deck_selection = 0
        self._previous_ai_move = ""
        self._boss_tactics = []

        self.difficulty = _player.difficulty
        self.is_easy_difficulty = False
        self.is_hard_difficulty = False
        self.is_normal_difficulty = False

        self.health_buff = 0
        self.health_debuff = 0
        self.stat_buff = 0
        self.stat_debuff = 0
        self.ap_buff = 0
        self.ap_debuff = 0
        self.co_op_stat_bonus = 0
        self.co_op_health_bonus = 0
        self.are_teammates = False
        self.are_family_members = False

        # Universal Elemetal Buffs
        self._wind_buff = 0

        self._ai_opponent_card_lvl = 0
        self._ai_opponentsummon_bond = 0
        self._ai_can_usesummon = False
        self._ai_combo_counter = 0

        self._boss_fought_already = False
        self._boss_data = ""

        self.completed_tales = self.player.completed_tales
        self.completed_dungeons = self.player.completed_dungeons
        self._player_association = ""
        self.name_of_boss = ""
        self._ai_opponent_card_lvl = 0
        self.match_has_ended = False

        self.bank_amount = 0
        self.fam_reward_amount = 0

        # Messages
        self.abyss_message = ""

        # Abyss / Scenario / Explore Config
        self.abyss_floor = ""
        self.abyss_card_to_earn = ""
        self.abyss_banned_card_tiers = ""
        self.abyss_player_card_tier_is_banned = False
        self.scenario_data = ""
        self.scenario_easy_drops = []
        self.scenario_normal_drops = []
        self.scenario_hard_drops = []
        self.explore_type = ""
        self.bounty = ""

        # Boss Important Descriptions
        self._arena_boss_description = ""
        self._arenades_boss_description = ""
        self._entrance_boss_description = ""
        self._description_boss_description = ""
        self._welcome_boss_description = ""
        self._feeling_boss_description = ""
        self._powerup_boss_description = ""
        self._aura_boss_description = ""
        self._assault_boss_description = ""
        self._world_boss_description = ""
        self._punish_boss_description = ""
        self._rmessage_boss_description = ""
        self._rebuke_boss_description = ""
        self._concede_boss_description = ""
        self._wins_boss_description = ""
        self._boss_embed_message = ""
        self._ai_is_boss = False

        # Boss Specific Moves
        self._turns_to_skip = 0
        self._damage_check_count = 0
        self._has_resurrect = False

        # AI Tutorial Config
        self.raidActive = False
        self.tutorial_basic = False
        self.tutorial_special = False
        self.tutorial_ultimate = False
        self.tutorial_enhancer = False
        self.tutorial_block = False
        self.tutorial_resolve = False
        self.tutorial_focus = False
        self.tutorialsummon = False
        self.tutorial_opponent_focus = False
        self.tutorial_message = ""
        self.tutorial_did = 0
        
        #Raid Config
        self._is_title_match = False
        self._is_training_match = False
        self._is_test_match = False
        self._is_bounty_match = False
        self._shield_name = ""
        self._hall_info = ""
        self._raid_hall = ""
        self._shield_guild = ""
        self._player_guild = ""
        self._association_info = ""
        self._association_name = ""
        self._raid_end_message = ""
        self._raid_fee = 0
        self._raid_bounty = 0
        self._raid_bonus = 0
        self._victory_streak = 0
        self._hall_defense = 0
        self._raid_bounty_plus_bonus = 0
        
        self.blocking_traits = ['Attack On Titan',
                           'Bleach',
                           'Black Clover',
                           'Death Note'
        ]
        self.focus_traits = ['Black Clover', 
                        'Dragon Ball Z',
                        'One Punch Man',
                        'League Of Legends',
                        'Solo Leveling',
                        'One Piece',
                        'Naruto',
                        'Digimon',
                        'Crown Rift Madness'
        ]
        self.opponent_focus_traits = ['7ds',
                                 'Souls',
                                 'One Punch Man',
                                 
            
        ]
        self.resolve_traits = ['My Hero Academia',
                          'One Piece',
                          'Pokemon',
                          'Digimon',
                          'Fate',
                          'League Of Legends',
                          'Bleach',
                          'Naruto',
                          'Attack On Titan',
                          'God Of War',
                          'Souls',
                          'Crown Rift Madness'
            
        ]
        self.set_up_traits = ['Demon Slayer',
                         'Solo Leveling',
                         'Crown Rift Slayers',
                         'Crown Rift Awakening',
                         'YuYu Hakusho',
                         'Death Note',
                         'Chainsawman',
                         'Dragon Ball Z'
                        
        ]
        
        self.summon_traits = ['7ds',
                         'Persona'
            
        ]
        

        self.player1_wins = False
        self.player2_wins = False


        if self.mode in crown_utilities.PVP_M:
            self.is_pvp_game_mode = True
            self.total_number_of_opponents = 1

        if self.mode in crown_utilities.AUTO_BATTLE_M:
            self.is_auto_battle_game_mode = True
            self.is_ai_opponent = True

        if self.mode in crown_utilities.DUO_M:
            self.is_duo_mode = True
            self.is_ai_opponent = True
            self.starting_match_title = f"Duo Battle! ({self.current_opponent_number + 1}/{self.total_number_of_opponents})"

        if self.mode in crown_utilities.CO_OP_M:
            self.is_co_op_mode = True
            self.is_ai_opponent = True
            self.starting_match_title = f"Co-op Battle! ({self.current_opponent_number + 1}/{self.total_number_of_opponents})"

        if self.mode in crown_utilities.RAID_M:
            self.is_raid_game_mode = True
            self.is_ai_opponent = True
            self.total_number_of_opponents = 1
            self.starting_match_title = f"Raid Battle!"

        if self.mode in crown_utilities.TALE_M:
            self.is_tales_game_mode = True
            self.is_ai_opponent = True
            self._ai_opponentsummon_lvl = 5
            self._ai_opponentsummon_bond = 1
            self._ai_opponent_card_lvl = 30
            self.can_auto_battle = True
            self.bank_amount = 5000
            self.fam_reward_amount = 5000

        
        if self.mode in crown_utilities.DUNGEON_M:
            self.is_dungeon_game_mode = True
            self.is_ai_opponent = True
            self._ai_opponentsummon_lvl = 10
            self._ai_opponentsummon_bond = 3
            self._ai_opponent_card_lvl = 400
            self.health_buff = self.health_buff + 2000
            self.stat_buff = self.stat_buff + 100
            self.ap_buff = self.ap_buff + 80
            self.bank_amount = 20000
            self.fam_reward_amount = 20000


        if self.mode in crown_utilities.BOSS_M:
            self.is_boss_game_mode = True
            self.is_ai_opponent = True
            self._ai_opponentsummon_lvl = 15
            self._ai_opponentsummon_bond = 4
            self._ai_opponent_card_lvl = 1000
            self.health_buff = self.health_buff + 5000
            self.stat_buff = self.stat_buff + 250
            self.ap_buff = self.ap_buff + 250
            self.total_number_of_opponents = 1
            self.starting_match_title = "👿 BOSS BATTLE!"
            self.bank_amount = 5000000
            self.fam_reward_amount = 5000000


        if self.mode == crown_utilities.ABYSS:
            self.is_abyss_game_mode = True
            self.is_ai_opponent = True

        
        if self.mode == crown_utilities.SCENARIO:
            self.is_scenario_game_mode = True
            self.is_ai_opponent = True

        
        if self.mode == crown_utilities.EXPLORE:
            self.is_explore_game_mode = True
            self.is_ai_opponent = True
            self.can_auto_battle = True
            self.total_number_of_opponents = 1
            self.starting_match_title = f"✅ Explore Battle is about to begin!"

        if self.difficulty == "EASY":
            self.is_easy_difficulty = True
            self.health_debuff = self.health_debuff + -500
            self.stat_debuff = self.stat_debuff + 100
            self.ap_debuff = self.ap_debuff + 15
            self.bank_amount = 500
            self.fam_reward_amount = 100

        
        if self.difficulty == "NORMAL":
            self.is_normal_difficulty = True
            self.bank_amount = 2500
            self.fam_reward_amount = 1500
        
        if self.difficulty == "HARD":
            self.is_hard_difficulty = True
            self.health_buff = self.health_buff + 3000
            self.stat_buff = self.stat_buff + 200
            self.ap_buff = self.ap_buff + 150
            self.bank_amount = self.bank_amount + 25000
            self.fam_reward_amount = self.fam_reward_amount + 25000

        if self.is_ai_opponent:
            self._ai_can_usesummon = True
            
        if self.is_raid_game_mode:
            self._ai_can_usesummon = False

        if self.is_tutorial_game_mode:
            self.starting_match_title = "Click Start Match to Begin the Tutorial!"
        

        
    def set_universe_selection_config(self, universe_selection):
        if universe_selection:
            self.selected_universe = universe_selection['SELECTED_UNIVERSE']
            self.selected_universe_full_data = universe_selection['UNIVERSE_DATA']
            self.crestlist = universe_selection['CREST_LIST']
            self.crestsearch = universe_selection['CREST_SEARCH']
            self.current_opponent_number =  universe_selection['CURRENTOPPONENT']

            if self.mode in crown_utilities.DUNGEON_M:
                self.list_of_opponents_by_name = self.selected_universe_full_data['DUNGEONS']
                self.total_number_of_opponents = len(self.list_of_opponents_by_name)
            if self.mode in crown_utilities.TALE_M:
                self.list_of_opponents_by_name = self.selected_universe_full_data['CROWN_TALES']
                self.total_number_of_opponents = len(self.list_of_opponents_by_name)

            if self.mode in crown_utilities.BOSS_M:
                self.name_of_boss = universe_selection['BOSS_NAME']
                self._player_association = universe_selection['OGUILD']
                if self.player.boss_fought:
                    self._boss_fought_already = True
                    

            if self.crestsearch:
                self._player_association = universe_selection['OGUILD']
            else:
                self._player_association = "PCG"
            self.starting_match_title = f"✅ Start Battle!  ({self.current_opponent_number + 1}/{self.total_number_of_opponents})"


    def get_starting_match_title(self):
        return   f"✅ Start Battle!  ({self.current_opponent_number + 1}/{self.total_number_of_opponents})"

    def set_abyss_config(self, player):
        try:
            if self.is_easy_difficulty:
                self.abyss_message = "The Abyss is unavailable on Easy self.mode! Use /difficulty to change your difficulty setting."
                return

            checks = db.queryCard({'NAME': player.equipped_card})
            abyss = db.queryAbyss({'FLOOR': player.level})

            if not abyss:
                self.abyss_message = "You have climbed out of :new_moon: **The Abyss**! Use /exchange to **Prestige**!"
                return

            self.is_ai_opponent = True
            self.is_abyss_game_mode = True
            self.list_of_opponents_by_name = abyss['ENEMIES']
            card_to_earn = self.list_of_opponents_by_name[-1] 
            self.total_number_of_opponents = len(self.list_of_opponents_by_name)
            self._ai_opponent_card_lvl = int(abyss['SPECIAL_BUFF'])
            self.abyss_floor = abyss['FLOOR']
            self.abyss_card_to_earn = self.list_of_opponents_by_name[-1] 
            self._ai_title = abyss['TITLE']
            self._ai_arm = abyss['ARM']
            self._ai_summon = abyss['PET']
            self.abyss_banned_card_tiers = abyss['BANNED_TIERS']
            self.abyss_banned_tier_conversion_to_string = [str(tier) for tier in self.abyss_banned_card_tiers]

            if self.abyss_floor in crown_utilities.ABYSS_REWARD_FLOORS:
                unlockable_message = f"⭐ Drops on this Floor\nUnlockable Card: **{card_to_earn}**\nUnlockable Title: **{self._ai_title}**\nUnlockable Arm: **{self._ai_arm}**\n"
            else:
                unlockable_message = ""

            if checks['TIER'] in self.abyss_banned_card_tiers:
                self.abyss_player_card_tier_is_banned = True


            embedVar = discord.Embed(title=f":new_moon: Abyss Floor {str(self.abyss_floor)}  ⚔️{len(self.list_of_opponents_by_name)}", description=textwrap.dedent(f"""
            {unlockable_message}
            """))
            if self.abyss_banned_card_tiers:
                embedVar.add_field(name="🀄 Banned Card Tiers", value="\n".join(self.abyss_banned_tier_conversion_to_string),
                                inline=True)
            embedVar.set_footer(text="Each floor must be completed all the way through to advance to the next floor.")

            return embedVar

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

    
    def set_scenario_selection(self):
        try:
            scenarios = db.queryAllScenariosByUniverse(str(self.selected_universe))
            embed_list = []
            for scenario in scenarios:
                if scenario['AVAILABLE']:
                    title = scenario['TITLE']
                    enemies = scenario['ENEMIES']
                    number_of_fights = len(enemies)
                    enemy_level = scenario['ENEMY_LEVEL']
                    scenario_gold = crown_utilities.scenario_gold_drop(enemy_level, number_of_fights)
                    universe = scenario['UNIVERSE']
                    scenario_image = scenario['IMAGE']
                    reward_list = []
                    if self.is_easy_difficulty:
                        rewards = scenario['EASY_DROPS']
                        scenario_gold = round(scenario_gold / 3)
                    if self.is_normal_difficulty:
                        rewards = scenario['NORMAL_DROPS']
                    if self.is_hard_difficulty:
                        rewards = scenario['HARD_DROPS']
                        scenario_gold = round(scenario_gold * 3)

                    for reward in rewards:
                        # Add Check for Cards and make Cards available in Easy Drops
                        arm = db.queryArm({"ARM": reward})
                        if arm:
                            arm_name = arm['ARM']
                            element_emoji = crown_utilities.set_emoji(arm['ELEMENT'])
                            arm_passive = arm['ABILITIES'][0]
                            arm_passive_type = list(arm_passive.keys())[0]
                            arm_passive_value = list(arm_passive.values())[0]
                            if arm_passive_type == "SHIELD":
                                reward_list.append(f":globe_with_meridians: {arm_passive_type.title()} **{arm_name}** Shield: Absorbs **{arm_passive_value}** Damage.")
                            elif arm_passive_type == "BARRIER":
                                reward_list.append(f":diamond_shape_with_a_dot_inside:  {arm_passive_type.title()} **{arm_name}** Negates: **{arm_passive_value}** attacks.")
                            elif arm_passive_type == "PARRY":
                                reward_list.append(f":repeat: {arm_passive_type.title()} **{arm_name}** Parry: **{arm_passive_value}** attacks.")
                            elif arm_passive_type == "SIPHON":
                                reward_list.append(f":syringe: {arm_passive_type.title()} **{arm_name}** Siphon: **{arm_passive_value}** + 10% Health.")
                            elif arm_passive_type == "MANA":
                                reward_list.append(f"🦠 {arm_passive_type.title()} **{arm_name}** Mana: Multiply Enhancer by **{arm_passive_value}**%.")
                            elif arm_passive_type == "ULTIMAX":
                                reward_list.append(f"〽️ {arm_passive_type.title()} **{arm_name}** Ultimax: Increase all move AP by **{arm_passive_value}**.")
                            else:
                                reward_list.append(f"{element_emoji} {arm_passive_type.title()} **{arm_name}** Attack: **{arm_passive_value}** Damage.")
                        else:
                            card = db.queryCard({"NAME": reward})
                            moveset = card['MOVESET']
                            move3 = moveset[2]
                            move2 = moveset[1]
                            move1 = moveset[0]
                            basic_attack_emoji = crown_utilities.set_emoji(list(move1.values())[2])
                            super_attack_emoji = crown_utilities.set_emoji(list(move2.values())[2])
                            ultimate_attack_emoji = crown_utilities.set_emoji(list(move3.values())[2])
                            reward_list.append(f":mahjong: {card['TIER']} **{card['NAME']}** {basic_attack_emoji} {super_attack_emoji} {ultimate_attack_emoji}\n:heart: {card['HLT']} :dagger: {card['ATK']}  🛡️ {card['DEF']}")
        
                    reward_message = "\n\n".join(reward_list)
                    embedVar = discord.Embed(title= f"{title}", description=textwrap.dedent(f"""
                    📽️ **{universe} Scenario Battle!**
                    🔱 **Enemy Level:** {enemy_level}
                    :coin: **Reward** {'{:,}'.format(scenario_gold)}

                    ⚙️ **Difficulty:** {self.difficulty.title()}

                    :crossed_swords: {str(number_of_fights)}
                    """), 
                    colour=0x7289da)
                    embedVar.add_field(name="__**Potential Rewards**__", value=f"{reward_message}")
                    embedVar.set_image(url=scenario_image)
                    # embedVar.set_footer(text=f"")
                    embed_list.append(embedVar)

            return embed_list
        except:
            print("Error setting scenario selection config")


    def set_scenario_config(self, scenario_data):
        try:
            self.scenario_data = scenario_data
            self.is_scenario_game_mode = True
            self.list_of_opponents_by_name = scenario_data['ENEMIES']
            self.total_number_of_opponents = len(self.list_of_opponents_by_name)
            self._ai_opponent_card_lvl = int(scenario_data['ENEMY_LEVEL'])
            self.selected_universe = scenario_data['UNIVERSE']
            self.is_available = scenario_data['AVAILABLE']
            self.scenario_easy_drops = scenario_data['EASY_DROPS']
            self.scenario_normal_drops = scenario_data['NORMAL_DROPS']
            self.scenario_hard_drops = scenario_data['HARD_DROPS']

            self.starting_match_title = f"🎞️ Scenario Battle Confirm Start! ({self.current_opponent_number + 1}/{self.total_number_of_opponents})"
        except:
            print("unable to set scenario config")


    def set_tutorial(self, opponent_did):
        bot_dids = ['837538366509154407', '845672426113466395']
        if opponent_did in bot_dids:
            self.is_tutorial_game_mode = True
            self.is_pvp_game_mode = True
            # self.is_ai_opponent = True
            self.is_turn = 0
            
    def create_raid(self, title_match, test_match, training_match, association, hall_info, shield_guild, player_guild): #findme
        if title_match:
            self._is_title_match = True
        if test_match:
            self._is_test_match = True
        if training_match:
            self._is_training_match = True
        if not training_match and not test_match and not title_match:
            self._is_bounty_match = True
        self._hall_info = hall_info
        self._raid_hall = hall_info['HALL']
        self._association_info = association
        self._association_name = association['GNAME']
        self._shield_name = association['SHIELD']
        self._shield_guild = shield_guild
        self._player_guild = player_guild
        self._raid_fee = int(hall_info['FEE'])
        self._raid_bounty = int(association['BOUNTY'])
        self._victory_streak = int(association['STREAK'])
        self._hall_defense = hall_info['DEFENSE']
        self._raid_bonus = int(((self._victory_streak / 100) * self._raid_bounty))
        
    def raid_victory(self):
        guild_query = {'GNAME': self._association_name}
        guild_info = db.queryGuildAlt(guild_query)
        bounty = guild_info['BOUNTY']
        bonus = guild_info['STREAK']
        total_bounty = int((bounty + ((bonus / 100) * bounty)))
        winbonus = int(((bonus / 100) * bounty))
        if winbonus == 0:
            winbonus = int(bounty)
        wage = int(total_bounty)
        bounty_drop = winbonus + total_bounty
        self._raid_bounty_plus_bonus = int(bounty_drop)
        self._raid_end_message = f":yen: SHIELD BOUNTY CLAIMED :coin: {'{:,}'.format(self._raid_bounty_plus_bonus)}"
        hall_info = db.queryHall({"HALL":self._raid_hall})
        fee = hall_info['FEE']
        transaction_message = f":shield: {self._shield_name} loss to {self.player.name}!"
        update_query = {'$push': {'TRANSACTIONS': transaction_message}}
        response = db.updateGuildAlt(guild_query, update_query)
        if self._is_title_match:
            if self._is_test_match:
                self._raid_end_message  = f":flags: {self._association_name} DEFENSE TEST OVER!"
            elif self._is_training_match:
                self._raid_end_message  = f":flags: {self._association_name} TRAINING COMPLETE!"
            else:
                transaction_message = f":shield:{self.player.name} becomes the new Shield!"
                update_query = {'$push': {'TRANSACTIONS': transaction_message}}
                response = db.updateGuildAlt(guild_query, update_query)
                newshield = db.updateGuild(guild_query, {'$set': {'SHIELD': str(self._player.disname)}})
                newshieldid = db.updateGuild(guild_query, {'$set': {'SDID': str(self._player.id)}})
                guildwin = db.updateGuild(guild_query, {'$set': {'BOUNTY': winbonus, 'STREAK': 1}})
                self._raid_end_message  = f":flags: {self._association_name} SHIELD CLAIMED!"
                prev_team_update = {'$set': {'SHIELDING': False}}
                remove_shield = db.updateTeam({'TEAM_NAME': str(self._shield_guild)}, prev_team_update)
                update_shielding = {'$set': {'SHIELDING': True}}
                add_shield = db.updateTeam({'TEAM_NAME': str(self._player_guild)}, update_shielding)
        else:
            transaction_message = f":vs: {self.player.name} defeated {self._shield_name}! They claimed the :coin: {'{:,}'.format(self._raid_bounty_plus_bonus)} Bounty!"
            update_query = {'$push': {'TRANSACTIONS': transaction_message}}
            response = db.updateGuildAlt(guild_query, update_query)
            guildloss = db.updateGuild(guild_query, {'$set': {'BOUNTY': fee, 'STREAK': 0}})
            
        
            
    # def set_hall(self, hall_info):
        


    def set_explore_config(self, universe_data, card_data):
        try:
            self.selected_universe_full_data = universe_data
            self._ai_opponent_card_data = card_data
            self.selected_universe = universe_data['TITLE']


            if self.mode in crown_utilities.DUNGEON_M or self._ai_opponent_card_lvl >= 350:
                title = 'DTITLE'
                arm = 'DARM'
                summon = 'DPET'
            if self.mode in crown_utilities.TALE_M or self._ai_opponent_card_lvl < 350:
                title = 'UTITLE'
                arm = 'UARM'
                summon = 'UPET'

            self._ai_opponent_title_data = db.queryTitle({'TITLE': self.selected_universe_full_data[title]})
            self._ai_opponent_arm_data = db.queryArm({'ARM': self.selected_universe_full_data[arm]})
            self._ai_opponentsummon_data = db.queryPet({'PET': self.selected_universe_full_data[summon]})
            self._ai_opponentsummon_image = self._ai_opponentsummon_data['PATH']
            self._ai_opponentsummon_name = self._ai_opponentsummon_data['PET']
            self._ai_opponentsummon_universe = self._ai_opponentsummon_data['UNIVERSE']

            summon_passive = self._ai_opponentsummon_data['ABILITIES'][0]
            self._ai_opponentsummon_power = list(summon_passive.values())[0]
            self._ai_opponentsummon_ability_name = list(summon_passive.keys())[0]
            self._ai_opponentsummon_type = summon_passive['TYPE']

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


    def set_corruption_config(self):
        if self.selected_universe_full_data['CORRUPTED']:
            self.is_corrupted = True
            self.ap_buff = 30
            self.stat_buff = 50
            self.health_buff = 300
            if self.difficulty == "HARD":
                self.ap_buff = 60
                self.stat_buff = 100
                self.health_buff = 1300

    # def get_tutorial_message(self, card, option):
    #     traits = ut.traits
    #     mytrait = {}
    #     traitmessage = ''
    #     for trait in traits:
    #         if trait['NAME'] == card.universe:
    #             mytrait = trait
    #         if card.universe in crown_utilities.pokemon_universes:
    #             if trait['NAME'] == 'Pokemon':
    #                 mytrait = trait
    #     if mytrait:
    #         traitmessage = f"{mytrait['T1']}"

    #     if option == "Start":
    #         if card.universe in self.set_up_traits:
    #             #do 
    #     if option == "Focus":
    #         if card.universe in self.focus_traits:
    #             #do
    #     if option == "b":
    #         if card.universe in self.blocking_traits:
    #             #do
    #     if option == "5":
    #         if card.universe in self.resolve_traits:
    #             #do
    #     if option == "6":
    #         if card.universe in self.summon_traits:
    #             #do
                

    def set_who_starts_match(self, player1_speed, player2_speed, mode):
        boss_modes = ['Boss','Cboss', 'BOSS', 'CBoss', 'CBOSS']
        if mode in boss_modes:
            self.is_turn = 0
        elif player1_speed >= player2_speed:
            self.is_turn = 0
        elif player2_speed > player1_speed:
            self.is_turn = 1
        else:
            self.is_turn = 0


    def get_lineup(self):
        self.match_lineup = f"{str(self.current_opponent_number + 1)}/{str(self.total_number_of_opponents)}"


    def save_match_turned_on(self):
        if self.mode not in crown_utilities.NOT_SAVE_MODES and self.difficulty != "EASY":
            self.match_can_be_saved = True
        return self.match_can_be_saved


    def get_ai_battle_ready(self, player1_card_level):
        try:
            if not self.is_boss_game_mode:
                if any((self.is_tales_game_mode, self.is_dungeon_game_mode, self. is_explore_game_mode, self.is_scenario_game_mode, self.is_abyss_game_mode)):
                    self._ai_opponent_card_data = db.queryCard({'NAME': self.list_of_opponents_by_name[self.current_opponent_number]})
                    universe_data = db.queryUniverse({'TITLE': {"$regex": str(self._ai_opponent_card_data['UNIVERSE']), "$options": "i"}})

                    if self.mode in crown_utilities.DUNGEON_M:
                        self._ai_title = universe_data['DTITLE']
                        self._ai_arm = universe_data['DARM']
                        self._ai_summon = universe_data['DPET']
                        if player1_card_level >= 600:
                            self._ai_opponent_card_lvl = 650
                        else:
                            self._ai_opponent_card_lvl = 50 + min(max(350, player1_card_level), 600) if not self.is_scenario_game_mode else self._ai_opponent_card_lvl                    
                    
                    if self.mode in crown_utilities.TALE_M:
                        self._ai_title = universe_data['UTITLE']
                        self._ai_arm = universe_data['UARM']
                        self._ai_summon = universe_data['UPET']
                        if player1_card_level <= 20 and player1_card_level >=10:
                            self._ai_opponent_card_lvl = 10
                        elif player1_card_level >= 0 and player1_card_level <=10:
                            self._ai_opponent_card_lvl = min(200, player1_card_level) if not self.is_scenario_game_mode else self._ai_opponent_card_lvl    
                        else:
                            self._ai_opponent_card_lvl = min(200, player1_card_level) if not self.is_scenario_game_mode else self._ai_opponent_card_lvl - 10
                        #self._ai_opponent_card_lvl = min(200, player1_card_level) if not self.is_scenario_game_mode else self._ai_opponent_card_lvl            

                    if any((self.is_scenario_game_mode, self.is_explore_game_mode)):
                        if self._ai_opponent_card_lvl < 150:
                            self._ai_title = universe_data['UTITLE']
                            self._ai_arm = universe_data['UARM']
                            self._ai_summon = universe_data['UPET']
                        if self._ai_opponent_card_lvl >= 150:
                            self._ai_title = universe_data['DTITLE']
                            self._ai_arm = universe_data['DARM']
                            self._ai_summon = universe_data['DPET']
                self._ai_opponent_title_data = db.queryTitle({'TITLE': self._ai_title})
                self._ai_opponent_arm_data = db.queryArm({'ARM': self._ai_arm})
                self._ai_opponentsummon_data = db.queryPet({'PET': self._ai_summon})
                self._ai_opponentsummon_image = self._ai_opponentsummon_data['PATH']
                self._ai_opponentsummon_name = self._ai_opponentsummon_data['PET']
                self._ai_opponentsummon_universe = self._ai_opponentsummon_data['UNIVERSE']

                summon_passive = self._ai_opponentsummon_data['ABILITIES'][0]
                self._ai_opponentsummon_power = list(summon_passive.values())[0]
                self._ai_opponentsummon_ability_name = list(summon_passive.keys())[0]
                self._ai_opponentsummon_type = summon_passive['TYPE']#
                
            else:
                self._boss_data = db.queryBoss({"UNIVERSE": self.selected_universe, "AVAILABLE": True})
                self._boss_tactics = self._boss_data['TACTICS']
                self._ai_opponent_card_data = db.queryCard({'NAME': self._boss_data['CARD']})
                self._ai_opponent_title_data = db.queryTitle({'TITLE': self._boss_data['TITLE']})
                self._ai_opponent_arm_data = db.queryArm({'ARM': self._boss_data['ARM']})
                self._ai_opponentsummon_data = db.queryPet({'PET': self._boss_data['PET']})
                self._ai_opponentsummon_image = self._ai_opponentsummon_data['PATH']
                self._ai_opponentsummon_name = self._ai_opponentsummon_data['PET']
                self._ai_opponentsummon_universe = self._ai_opponentsummon_data['UNIVERSE']
                self._ai_is_boss = True

                summon_passive = self._ai_opponentsummon_data['ABILITIES'][0]
                self._ai_opponentsummon_power = list(summon_passive.values())[0]
                self._ai_opponentsummon_ability_name = list(summon_passive.keys())[0]
                self._ai_opponentsummon_type = summon_passive['TYPE']
                
                self._arena_boss_description = self._boss_data['DESCRIPTION'][0]
                self._arenades_boss_description = self._boss_data['DESCRIPTION'][1]
                self._entrance_boss_description = self._boss_data['DESCRIPTION'][2]
                self._description_boss_description = self._boss_data['DESCRIPTION'][3]
                self._welcome_boss_description = self._boss_data['DESCRIPTION'][4]
                self._feeling_boss_description = self._boss_data['DESCRIPTION'][5]
                self._powerup_boss_description = self._boss_data['DESCRIPTION'][6]
                self._aura_boss_description = self._boss_data['DESCRIPTION'][7]
                self._assault_boss_description = self._boss_data['DESCRIPTION'][8]
                self._world_boss_description = self._boss_data['DESCRIPTION'][9]
                self._punish_boss_description = self._boss_data['DESCRIPTION'][10]
                self._rmessage_boss_description = self._boss_data['DESCRIPTION'][11]
                self._rebuke_boss_description = self._boss_data['DESCRIPTION'][12]
                self._concede_boss_description = self._boss_data['DESCRIPTION'][13]
                self._wins_boss_description = self._boss_data['DESCRIPTION'][14]
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


    def get_aisummon_ready(self, _card):
        _card.summon_ability_name = self._ai_opponentsummon_ability_name
        _card.summon_power = self._ai_opponentsummon_power
        _card.summon_lvl = self._ai_opponentsummon_lvl
        _card.summon_type = self._ai_opponentsummon_type
        _card.summon_bond = self._ai_opponentsummon_bond
        _card.summon_name = self._ai_opponentsummon_name
        _card.summon_image = self._ai_opponentsummon_image
        _card.summon_universe = self._ai_opponentsummon_universe


    def set_game_over(self, player1_card, player2_card, player3_card=None):
        if player1_card.health <= 0:
            self.match_has_ended = True
            self.player2_wins = True
        
        if player2_card.health <= 0:
            self.match_has_ended = True
            self.player1_wins = True

        if self.is_co_op_mode or self.is_duo_mode:
            if player3_card.health <= 0:
                self.match_has_ended = True
                self.player2_wins = True
            if player2_card.health <= 0:
                self.match_has_ended = True
                self.player1_wins = True

        if self.is_auto_battle_game_mode:
            if self.turn_total >= 250:
                self.previous_moves.append(f"⚙️**{player1_card.name}** could not defeat {player2_card.name} before the turn Limit...")
                player1_card.health = 0
        return self.match_has_ended

    

    def reset_game(self):
        self.match_has_ended = False
        self.player1_wins = False
        self.player2_wins = False
        self.turn_total = 0
        self.previous_moves = []
        self.is_auto_battle_game_mode = False


    def get_previous_moves_embed(self):
        msg = "\n\n".join(self.previous_moves)
        if msg:
            return msg
        else:
            return ""
    

    def get_battle_window_title_text(self, opponent_card, your_card, partner_card=None):
        o_resolve = '🌀'
        y_resolve = '🌀'
        p_resolve = '🌀'
        o_focus = '❤️'
        y_focus = '❤️'
        p_focus = '❤️'
        
        if opponent_card.used_focus:
            o_focus = '💖'
        if your_card.used_focus:
            y_focus = '💖'
        if opponent_card.used_resolve:
            o_resolve = '⚡'
        if your_card.used_resolve:
            y_resolve = '⚡'
            
        if partner_card:
            if partner_card.used_focus:
                p_focus = '💖'
            if partner_card.used_resolve:
                p_resolve = '⚡'
        #return f"{opponent_card.name}: {o_focus}{round(opponent_card.health)} {o_resolve}{round(opponent_card.stamina)} 🗡️{round(opponent_card.attack)}/🛡️{round(opponent_card.defense)} {opponent_card._arm_message}\n{your_card.name}: {y_focus}{round(your_card.health)} {y_resolve}{round(your_card.stamina)} 🗡️{round(your_card.attack)}/🛡️{round(your_card.defense)} {your_card._arm_message}"
        if self.is_turn == 1:
            if self.is_co_op_mode or self.is_duo_mode:
                return f"{opponent_card.name}: {o_focus}{round(opponent_card.health)} {o_resolve}{round(opponent_card.stamina)} 🗡️{round(opponent_card.attack)}/🛡️{round(opponent_card.defense)} {opponent_card._arm_message}\n{partner_card.name}: {p_focus}{round(partner_card.health)} {p_resolve}{round(partner_card.stamina)} 🗡️{round(partner_card.attack)}/🛡️{round(partner_card.defense)} {partner_card._arm_message}\n{your_card.name}: {y_focus}{round(your_card.health)} {y_resolve}{round(your_card.stamina)} 🗡️{round(your_card.attack)}/🛡️{round(your_card.defense)} {your_card._arm_message}"
            else:
                return f"{your_card.name}: {y_focus}{round(your_card.health)} {y_resolve}{round(your_card.stamina)} 🗡️{round(your_card.attack)}/🛡️{round(your_card.defense)} {your_card._arm_message}\n{opponent_card.name}: {o_focus}{round(opponent_card.health)} {o_resolve}{round(opponent_card.stamina)} 🗡️{round(opponent_card.attack)}/🛡️{round(opponent_card.defense)} {opponent_card._arm_message}"
        elif self.is_turn ==3:
            return f"{opponent_card.name}: {o_focus}{round(opponent_card.health)} {o_resolve}{round(opponent_card.stamina)} 🗡️{round(opponent_card.attack)}/🛡️{round(opponent_card.defense)} {opponent_card._arm_message}\n{your_card.name}: {y_focus}{round(your_card.health)} {y_resolve}{round(your_card.stamina)} 🗡️{round(your_card.attack)}/🛡️{round(your_card.defense)} {your_card._arm_message}\n{partner_card.name}: {p_focus}{round(partner_card.health)} {p_resolve}{round(partner_card.stamina)} 🗡️{round(partner_card.attack)}/🛡️{round(partner_card.defense)} {partner_card._arm_message}"
        elif self.is_turn ==0:
            if self.is_co_op_mode or self.is_duo_mode:
                return f"{opponent_card.name}: {o_focus}{round(opponent_card.health)} {o_resolve}{round(opponent_card.stamina)} 🗡️{round(opponent_card.attack)}/🛡️{round(opponent_card.defense)} {opponent_card._arm_message}\n{partner_card.name}: {p_focus}{round(partner_card.health)} {p_resolve}{round(partner_card.stamina)} 🗡️{round(partner_card.attack)}/🛡️{round(partner_card.defense)} {partner_card._arm_message}\n{your_card.name}: {y_focus}{round(your_card.health)} {y_resolve}{round(your_card.stamina)} 🗡️{round(your_card.attack)}/🛡️{round(your_card.defense)} {your_card._arm_message}"
            else:
                return f"{opponent_card.name}: {o_focus}{round(opponent_card.health)} {o_resolve}{round(opponent_card.stamina)} 🗡️{round(opponent_card.attack)}/🛡️{round(opponent_card.defense)} {opponent_card._arm_message}\n{your_card.name}: {y_focus}{round(your_card.health)} {y_resolve}{round(your_card.stamina)} 🗡️{round(your_card.attack)}/🛡️{round(your_card.defense)} {your_card._arm_message}"
        else:
            return f"{opponent_card.name}: {o_focus}{round(opponent_card.health)} {o_resolve}{round(opponent_card.stamina)} 🗡️{round(opponent_card.attack)}/🛡️{round(opponent_card.defense)} {opponent_card._arm_message}\n{your_card.name}: {y_focus}{round(your_card.health)} {y_resolve}{round(your_card.stamina)} 🗡️{round(your_card.attack)}/🛡️{round(your_card.defense)} {your_card._arm_message}\n{partner_card.name}: {y_focus}{round(partner_card.health)} {p_resolve}{round(partner_card.stamina)} 🗡️{round(partner_card.attack)}/🛡️{round(partner_card.defense)} {partner_card._arm_message}"


    def get_battle_footer_text(self, opponent_card, your_card, partner_card=None):
        o_resolve = '🌀'
        y_resolve = '🌀'
        p_resolve = '🌀'
        o_focus = '❤️'
        y_focus = '❤️'
        p_focus = '❤️'
        
        if opponent_card.used_focus:
            o_focus = '💖'
        if your_card.used_focus:
            y_focus = '💖'
        
        if opponent_card.used_resolve:
            o_resolve = '⚡'
        if your_card.used_resolve:
            y_resolve = '⚡'
            
        if partner_card:
            if partner_card.used_focus:
                p_focus = '💖'
            if partner_card.used_resolve:
                p_resolve = '⚡'
            
            
        if self.is_co_op_mode or self.is_duo_mode:
            return f"{opponent_card.name}: {o_focus}{round(opponent_card.health)} {o_resolve}{round(opponent_card.stamina)} 🗡️{round(opponent_card.attack)}/🛡️{round(opponent_card.defense)} {opponent_card._arm_message}\n{partner_card.name}: {p_focus}{round(partner_card.health)} {p_resolve}{round(partner_card.stamina)} 🗡️{round(partner_card.attack)}/🛡️{round(partner_card.defense)} {partner_card._arm_message}\n{your_card.name}: {y_focus}{round(your_card.health)} {y_resolve}{round(your_card.stamina)} 🗡️{round(your_card.attack)}/🛡️{round(your_card.defense)} {your_card._arm_message}"
        else:
            return f"{opponent_card.name}: {o_focus}{round(opponent_card.health)} {o_resolve}{round(opponent_card.stamina)} 🗡️{round(opponent_card.attack)}/🛡️{round(opponent_card.defense)} {opponent_card._arm_message}\n{your_card.name}: {y_focus}{round(your_card.health)} {y_resolve}{round(your_card.stamina)} 🗡️{round(your_card.attack)}/🛡️{round(your_card.defense)} {your_card._arm_message}"


    def ai_battle_command(self, your_card, opponent_card):
        aiMove = 0
        
        if your_card.used_resolve and not your_card.usedsummon and your_card.stamina >= 30:
            aiMove = 6
        elif your_card.move4enh == "WAVE" and (self.turn_total % 10 == 0 or self.turn_total == 0 or self.turn_total == 1):
            if your_card.stamina >=20:
                aiMove =4
            else:
                aiMove = 1
        elif your_card._barrier_active: #Ai Barrier Checks
            if your_card.stamina >=20: #Stamina Check For Enhancer
                aiMove = ai_enhancer_moves(your_card, opponent_card)
            else:
                aiMove = 1
        elif opponent_card.health <=350: #Killing Blow
            if your_card.move4enh == "BLAST":
                if your_card.stamina >=20:
                    aiMove =4
                else:
                    aiMove =1
            elif your_card.move4enh == "WAVE" and (self.turn_total % 10 == 0 or self.turn_total == 0 or self.turn_total == 1):
                if your_card.stamina >=20:
                    aiMove =4
                else:
                    aiMove =1
            else:
                if your_card.stamina >= 90:
                    aiMove = 1
                elif your_card.stamina >= 80:
                    aiMove =3
                elif your_card.stamina >=30:
                    aiMove=2
                else:
                    aiMove=1
        elif opponent_card.stamina < 10:
            if your_card.move4enh in crown_utilities.Gamble_Enhancer_Check:
                if your_card.stamina >= 20:
                    aiMove = 4
                else:
                    aiMove = 1
            else:
                aiMove = 1
        elif your_card.health <= (.50 * your_card.max_health) and your_card.used_resolve == False and your_card.used_focus:
            aiMove = 5
        elif your_card.universe in self.blocking_traits and your_card.stamina ==20:
            if opponent_card.attack >= your_card.defense and opponent_card.attack <= (your_card.defense * 2):
                aiMove = 0
            elif your_card.universe == "Attack On Titan" and your_card.health <= (your_card.max_health * .50):
                aiMove = 0
            elif opponent_card._barrier_active and opponent_card.stamina <= 20 and your_card.universe == "Bleach":
                aiMove = 0
            else:
                aiMove = 1
        elif your_card.stamina >= 160 and (your_card.health >= opponent_card.health):
            aiMove = 3
        elif your_card.stamina >= 160:
            aiMove = 3
        elif your_card.stamina >= 150 and (your_card.health >= opponent_card.health):
            aiMove = 1
        elif your_card.stamina >= 150:
            aiMove = 1
        elif your_card.stamina >= 140 and (your_card.health >= opponent_card.health):
            aiMove = 1
        elif your_card.stamina >= 140:
            aiMove = 3
        elif your_card.stamina >= 130 and (your_card.health >= opponent_card.health):
            aiMove = 1
        elif your_card.stamina >= 130:
            aiMove = 3
        elif your_card.stamina >= 120 and (your_card.health >= opponent_card.health):
            aiMove = 2
        elif your_card.stamina >= 120:
            aiMove = 3
        elif your_card.stamina >= 110 and (your_card.health >= opponent_card.health):
            aiMove = 1
        elif your_card.stamina >= 110:
            aiMove = 2
        elif your_card.stamina >= 100 and (your_card.health >= opponent_card.health):
            if your_card.move4enh in crown_utilities.Gamble_Enhancer_Check or your_card.move4enh in crown_utilities.Healer_Enhancer_Check:
                aiMove = 3
            elif your_card.move4enh in crown_utilities.Support_Enhancer_Check or your_card.move4enh in crown_utilities.Stamina_Enhancer_Check or your_card.move4enh in crown_utilities.Turn_Enhancer_Check:
                aiMove = 4
            else:
                aiMove = 1
        elif your_card.stamina >= 100:
            if your_card.universe in self.blocking_traits:
                aiMove = 0
            else:
                aiMove = 1
        elif your_card.stamina >= 90 and (your_card.health >= opponent_card.health):
            aiMove = 3
        elif your_card.stamina >= 90:
            if your_card.used_resolve == True and your_card.universe in self.blocking_traits:
                aiMove = 0
            elif your_card.move4enh in crown_utilities.Gamble_Enhancer_Check:
                aiMove = 3
            elif your_card.move4enh in crown_utilities.Support_Enhancer_Check or your_card.move4enh in crown_utilities.Stamina_Enhancer_Check or your_card.move4enh in crown_utilities.Sacrifice_Enhancer_Check:
                aiMove = 4
            else:
                aiMove = 1
        elif your_card.stamina >= 80 and (your_card.health >= opponent_card.health):
            aiMove = 1
        elif your_card.stamina >= 80:
            aiMove = 3
        elif your_card.stamina >= 70 and (your_card.health >= opponent_card.health):
            if your_card.move4enh in crown_utilities.Gamble_Enhancer_Check:
                aiMove = 1
            else:
                aiMove = ai_enhancer_moves(your_card, opponent_card)
        elif your_card.stamina >= 70:
            aiMove = 1
        elif your_card.stamina >= 60 and (your_card.health >= opponent_card.health):
            if your_card.used_resolve == False and your_card.used_focus:
                aiMove = 5
            elif your_card.used_focus == False:
                aiMove = 2
            else:
                aiMove = 1
        elif your_card.stamina >= 60:
            if your_card.used_resolve == False and your_card.used_focus:
                aiMove = 5
            elif your_card.universe in self.blocking_traits:
                aiMove = 0
            elif your_card.used_focus == False:
                aiMove = 2
            else:
                aiMove = 1
        elif your_card.stamina >= 50 and (your_card.health >= opponent_card.health):
            if your_card.used_resolve == False and your_card.used_focus:
                aiMove = 5
            elif your_card.used_focus == False:
                aiMove = 2
            else:
                aiMove = 1
        elif your_card.stamina >= 50:
            if your_card.used_resolve == False and your_card.used_focus:
                aiMove = 5
            elif your_card.used_focus == False:
                aiMove = 2
            elif your_card.move4enh in crown_utilities.Support_Enhancer_Check or your_card.move4enh in crown_utilities.Stamina_Enhancer_Check:
                aiMove = 4
            else:
                aiMove = 1
        elif your_card.stamina >= 40 and (your_card.health >= opponent_card.health):
            aiMove = 1
        elif your_card.stamina >= 40:
            aiMove = 2
        elif your_card.stamina >= 30 and (your_card.health >= opponent_card.health):
            if your_card.move4enh in crown_utilities.Gamble_Enhancer_Check:
                aiMove = 1
            elif your_card.move4enh in crown_utilities.Support_Enhancer_Check or your_card.move4enh in crown_utilities.Stamina_Enhancer_Check:
                aiMove = 2
            else:
                aiMove = ai_enhancer_moves(your_card, opponent_card)
        elif your_card.stamina >= 30:
            aiMove = 2
        elif your_card.stamina >= 20 and (your_card.health >= opponent_card.health):
            aiMove = 1
        elif your_card.stamina >= 20:
            if your_card.move4enh in crown_utilities.Gamble_Enhancer_Check:
                aiMove = 1
            elif your_card.move4enh in crown_utilities.Support_Enhancer_Check or your_card.move4enh in crown_utilities.Stamina_Enhancer_Check:
                aiMove = 1
            else:
                aiMove = 4
        elif your_card.stamina >= 10:
            aiMove = 1
        else:
            aiMove = 0
            
        #Hard Mode Ai
        if self.is_hard_difficulty:
            self._combo_counter = 0
            if aiMove == self._previous_ai_move:
                self._combo_counter = self._combo_counter + 1
                if self._combo_counter == 2:
                    self._combo_counter = 0
                    #Try to select a different move
                    if self._previous_ai_move == 0:
                        if your_card.stamina >= 80:
                            aiMove =3
                        elif your_card.stamina >= 30:
                            aiMove=2
                        elif your_card.stamina >= 20:
                            if your_card.move4enh == "LIFE" or your_card.move4enh in crown_utilities.Damage_Enhancer_Check:
                                aiMove = 4
                            else:
                                aiMove = 1
                        else:
                            aiMove = 1
                    elif self._previous_ai_move == 1:
                        if your_card._barrier_active:
                            if your_card.used_focus and not your_card.used_resolve:
                                aiMove =5
                            else:
                                aiMove = 4
                        else:    
                            if your_card.stamina >=120:
                                aiMove = 0
                            elif your_card.stamina>=100:
                                aiMove = 1
                            elif your_card.stamina>=80:
                                aiMove = 3
                            elif your_card.stamina>=50:
                                aiMove = 0
                            elif your_card.stamina>=30:
                                aiMove = 2
                            else:
                                aiMove = 1   
                    elif self._previous_ai_move == 2:
                        if your_card._barrier_active:
                            if your_card.used_focus and not your_card.used_resolve:
                                aiMove =5
                            else:
                                aiMove = 4
                        else:    
                            if your_card.stamina >=120:
                                aiMove = 4
                            elif your_card.stamina>=100:
                                aiMove = 0
                            elif your_card.stamina>=80:
                                aiMove = 3
                            elif your_card.stamina>=50:
                                aiMove = 2
                            elif your_card.stamina>=30:
                                aiMove = 1
                            else:
                                aiMove = 1   
                    elif self._previous_ai_move == 3:
                        if your_card._barrier_active:
                            if your_card.used_focus and not your_card.used_resolve:
                                aiMove = 5
                            else:
                                aiMove = 4
                        else:    
                            if your_card.stamina >=120:
                                aiMove = 1
                            elif your_card.stamina>=100:
                                aiMove = 2
                            elif your_card.stamina>=80:
                                aiMove = 4
                            elif your_card.stamina>=50:
                                aiMove = 4
                            elif your_card.stamina>=30:
                                aiMove = 0
                            else:
                                aiMove = 1   
                    elif self._previous_ai_move == 4:
                        if your_card._barrier_active:
                            if your_card.used_focus and not your_card.used_resolve:
                                aiMove =5
                            else:
                                aiMove = 4
                        else:    
                            if your_card.stamina >=120:
                                aiMove = 2
                            elif your_card.stamina>=100:
                                aiMove = 1
                            elif your_card.stamina>=80:
                                aiMove = 3
                            elif your_card.stamina>=50:
                                aiMove = 1
                            elif your_card.stamina>=30:
                                aiMove = 0
                            else:
                                aiMove = 1              
                    else:
                        if your_card._barrier_active:
                            if your_card.used_focus and not your_card.used_resolve:
                                aiMove =5
                            else:
                                aiMove = 4
                        else:    
                            if your_card.stamina >=120:
                                aiMove = 4
                            elif your_card.stamina>=100:
                                aiMove = 3
                            elif your_card.stamina>=80:
                                aiMove = 0
                            elif your_card.stamina>=50:
                                aiMove = 2
                            elif your_card.stamina>=30:
                                aiMove = 1
                            else:
                                aiMove = 1   
                        
            self._previous_ai_move = aiMove

        return aiMove


    def add_battle_history_message(self, msg):
        if msg:
            self.previous_moves.append(msg)


    def set_battle_options(self, your_card, opponent_card, companion_card=None):
        b_butts = []
        u_butts = []
        c_butts = []
        if self.is_turn == 3:
            options = ["q", "Q", "0", "1", "2", "3", "4", "7"]
            if your_card.used_focus:
                if your_card.used_resolve:
                    options += [6]
                else:
                    options += [5]
            self.battle_options = options
        else:
            options = ["q", "Q", "0", "1", "2", "3", "4"]
            if self.is_co_op_mode:
                options += ["7", "8", "9", "s", "b"]
            else:
                options += ["s"]
            if your_card.used_focus:
                if your_card.used_resolve:
                    options += ['6']
                else:
                    options += ['5']
            self.battle_options = options

        if your_card.stamina >= 10:
            # if your_card.universe == "Souls" and your_card.used_resolve:
            #     b_butts.append(
            #         manage_components.create_button(
            #             style=ButtonStyle.green,
            #             label=f"{your_card.move2_emoji} 10",
            #             custom_id="1"
            #         )
            #     )
            # else:
            b_butts.append(
                manage_components.create_button(
                    style=ButtonStyle.green,
                    label=f"{your_card.move1_emoji} 10",
                    custom_id="1"
                )
            )

        if your_card.stamina >= 30:
            # if your_card.universe == "Souls" and your_card.used_resolve:
            #     b_butts.append(
            #         manage_components.create_button(
            #             style=ButtonStyle.green,
            #             label=f"{your_card.move3_emoji} 30",
            #             custom_id="2"
            #         )
            #     )
            # else:
            b_butts.append(
                manage_components.create_button(
                    style=ButtonStyle.green,
                    label=f"{your_card.move2_emoji} 30",
                    custom_id="2"
                )
            )

        if your_card.stamina >= 80:
            b_butts.append(
                manage_components.create_button(
                    style=ButtonStyle.green,
                    label=f"{your_card.move3_emoji} 80",
                    custom_id="3"
                )
            )
        
        if your_card.stamina >= 20:
            b_butts.append(
                manage_components.create_button(
                    style=ButtonStyle.blue,
                    label=f"🦠 20",
                    custom_id="4"
                )
            )

            if opponent_card.gravity_hit == False:
                u_butts.append(
                    manage_components.create_button(
                        style=ButtonStyle.blue,
                        label="🛡️ Block 20",
                        custom_id="0"
                    )
                )
                
        if your_card.stamina >= 20 and self.is_co_op_mode and self.mode in crown_utilities.DUO_M:
            if your_card.stamina >= 20:
                c_butts = [
                    manage_components.create_button(
                        style=ButtonStyle.blue,
                        label="🦠 Enhance Ally 20",
                        custom_id="7"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.blue,
                        label="👥 Ally Assist 20",
                        custom_id="8"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.blue,
                        label="🛡️ Ally Block 20",
                        custom_id="9"
                    ),
                ]
            else:
                c_butts = [           
                        manage_components.create_button(
                        style=ButtonStyle.red,
                        label=f"Boost Companion",
                        custom_id="b"
                    )]
        
        elif self.is_co_op_mode and self.mode not in crown_utilities.DUO_M and your_card.stamina >= 20:
            c_butts = [
                manage_components.create_button(
                    style=ButtonStyle.blue,
                    label="Assist Companion 20",
                    custom_id="7"
                )
            ]

        if your_card.used_focus and your_card.used_resolve and not your_card.usedsummon and not self.is_raid_game_mode:
            u_butts.append(
                manage_components.create_button(
                    style=ButtonStyle.green,
                    label="🧬",
                    custom_id="6"
                )
            )

        if your_card.used_focus and not your_card.used_resolve:
            u_butts.append(
                manage_components.create_button(
                    style=ButtonStyle.green,
                    label="⚡Resolve!",
                    custom_id="5"
                )
            )
                
        u_butts.append(
            manage_components.create_button(
                style=ButtonStyle.grey,
                label="Quit",
                custom_id="q"
            ),
        )

        if not self.is_explore_game_mode and not self.is_easy_difficulty and not self.is_abyss_game_mode and not self.is_tutorial_game_mode and not self.is_scenario_game_mode and not self.is_raid_game_mode and not self.is_pvp_game_mode and not self.is_boss_game_mode:
            u_butts.append(
                manage_components.create_button(
                style=ButtonStyle.red,
                label=f"Save",
                custom_id="s"
            )
            )

        self.battle_buttons = b_butts
        self.utility_buttons = u_butts
        self.co_op_buttons = c_butts


    def set_levels_message(self, your_card, opponent_card, companion_card=None):
        level_to_emoji = {
            0: "🔰",
            200: "🔱",
            700: "⚜️",
            999: "🏅"
        }
        def get_player_message(card):
            lvl = int(card.card_lvl)
            emoji = "🔰"
            
            if lvl >= 1000:
                emoji = "🏅"
            elif lvl >= 700:
                emoji = "⚜️"
            elif lvl >=200:
                emoji = "🔱"
            return f"{emoji} *{lvl} {card.name}*"

        p1_msg = get_player_message(your_card)
        p2_msg = get_player_message(opponent_card)
        message = f"{crown_utilities.set_emoji(your_card._talisman)} | {p1_msg}\n🆚\n{crown_utilities.set_emoji(opponent_card._talisman)} | {p2_msg}"

        if self.is_co_op_mode:
            p3_msg = get_player_message(companion_card)
            message = f"{crown_utilities.set_emoji(your_card._talisman)} | {p1_msg}\n{crown_utilities.set_emoji(companion_card._talisman)} | {p3_msg}\n🆚\n{crown_utilities.set_emoji(opponent_card._talisman)} | {p2_msg}"

        return message


    def error_end_match_message(self):
        response = ""
        if not self.is_abyss_game_mode and not self.is_scenario_game_mode:
            if not self.is_tutorial_game_mode:
                if self.is_pvp_game_mode:
                    response = f"Your :vs: timed out. Your channel has been closed"
                elif self.is_boss_game_mode:
                    response = f"Your Boss Fight timed out. Your channel has been closed."
                else:
                    response = f"Your Game timed out. Your channel has been closed but your spot in the tales has been saved where you last left off."
            else:
                response = f"Your Game timed out. Your channel has been closed, restart the tutorial with **/solo**."
        else:
            response = f"Your game timed out. Your channel has been closed and your Abyss Floor was Reset."
        self.match_has_ended = True
        return response

    def get_battle_time(self):
        wintime = time.asctime()
        starttime = time.asctime()
        h_gametime = starttime[11:13]
        m_gametime = starttime[14:16]
        s_gametime = starttime[17:19]
        h_playtime = int(wintime[11:13])
        m_playtime = int(wintime[14:16])
        s_playtime = int(wintime[17:19])
        gameClock = crown_utilities.getTime(int(h_gametime), int(m_gametime), int(s_gametime), h_playtime, m_playtime,
                            s_playtime)
        
        if int(gameClock[0]) == 0 and int(gameClock[1]) == 0:
            return f"Battle Time: {gameClock[2]} Seconds."
        elif int(gameClock[0]) == 0:
            return f"Battle Time: {gameClock[1]} Minutes and {gameClock[2]} Seconds."
        else:
            return f"Battle Time: {gameClock[0]} Hours {gameClock[1]} Minutes and {gameClock[2]} Seconds."
        
        
        
        
    def saved_game_embed(self, player_card, opponent_card, companion_card = None):
        picon = ":crossed_swords:"
        save_message = "Tale"
        if self.is_dungeon_game_mode:
            save_message = "Dungeon"
            picon = ":fire:"

                
        embedVar = discord.Embed(title=f"💾 {opponent_card.universe} {save_message} Saved!", description=textwrap.dedent(f"""
            {self.get_previous_moves_embed()}
            
            """),colour=discord.Color.green())
        embedVar.add_field(name="💽 | Saved Data",
                                value=f"🌍 | **Universe**: {opponent_card.universe}\n{picon} | **Progress**: {self.current_opponent_number + 1}\n:flower_playing_cards: | **Opponent**: {opponent_card.name}")
        embedVar.set_footer(text=f"{self.get_battle_time()}")
        return embedVar
    
    def close_pve_embed(self, player_card, opponent_card, companion_card = None):
        picon = ":crossed_swords:"
        close_message = "Tale"
        f_message = f"💾 | Enable /autosave or use the Save button to maintain progress!"
        db_adjustment = 1
        if self.is_dungeon_game_mode:
            close_message = "Dungeon"
            picon = ":fire:"
        if self.is_boss_game_mode:
            close_message = "Boss"
            picon = ":japanese_ogre:"
            f_message = f"💀 | You fail to claim {opponent_card.name}'s Soul"
        if self.is_abyss_game_mode:
            close_message = "Abyss"
            picon = ":new_moon:"
            f_message = f"💀 | The Abyss Claims Another..."
        if self.is_explore_game_mode:
            close_message = "Explore Battle"
            picon = ":milky_way:"
            f_message = f"💀 | Explore Battle Failed!"
        if self.is_scenario_game_mode:
            close_message = "Scenario Battle"
            picon = "📹"
            f_message = f"💀 | Scenario Battle Ended."
            
            

                
        embedVar = discord.Embed(title=f"{picon} {opponent_card.universe} {close_message} Ended!", description=textwrap.dedent(f"""
            """),colour=discord.Color.red())
        embedVar.add_field(name=f"{picon} | Last Battle : {self.current_opponent_number + db_adjustment}",
                                value=f":flower_playing_cards: | **Opponent**: {opponent_card.name}")
        
        embedVar.set_footer(text=f_message)
        return embedVar
    
    def close_pvp_embed(self, player, opponent):
        picon = ":vs:"
        icon1 = "1️⃣"
        icon2 = "2️⃣"
        close_message = "PVP"
        f_message = f":people_hugging: | Try Co-Op Battle and Conquer The Multiverse Together!"
        if self.is_tutorial_game_mode:
            close_message = "Tutorial"
            icon2 = ":teacher:"
            f_message = f"🧠 | Tutorial will teach you about Game Mechanics and Card Abiltiies!"
        if self.is_raid_game_mode:
            close_message = "Raid"
            icon2 = "🛡️"
            f_message = f"⛩️ | Raid Associations to Claim the Bounty or Claim The Shield Title"
            

                
        embedVar = discord.Embed(title=f"{picon} {close_message} Ended!", description=textwrap.dedent(f"""
            {player.disname} :vs: {opponent.disname}
            """),colour=discord.Color.red())
        embedVar.add_field(name=f"{icon1} | {player.disname}",
                                value=f":flower_playing_cards: | {player.equipped_card}\n:reminder_ribbon: | {player.equipped_title}\n:mechanical_arm: | {player.equipped_arm}\n🧬 | {player.equippedsummon}")
        embedVar.add_field(name=f"{icon2} | {opponent.disname}",
                                value=f":flower_playing_cards: | {opponent.equipped_card}\n:reminder_ribbon: | {opponent.equipped_title}\n:mechanical_arm: | {opponent.equipped_arm}\n🧬 | {opponent.equippedsummon}")
        embedVar.set_footer(text=f_message)
        return embedVar
    
    def next_turn(self):
        if self.is_co_op_mode:
            if self.is_turn == 3:
                self.is_turn = 0
            else:
                self.is_turn += 1
        else:
            self.is_turn = (self.is_turn + 1) % 2


    def repeat_turn(self):
        self.is_turn = self.is_turn


    def previous_turn(self):
        if self.is_co_op_mode:
            if self.is_turn == 3:
                self.is_turn = 2
            elif self.is_turn == 2:
                self.is_turn = 1
            elif self.is_turn == 1:
                self.is_turn = 0
        else:
            self.is_turn = int(not self.is_turn)


    def get_co_op_bonuses(self, player1, player2):
        if self.is_tales_game_mode or self.is_dungeon_game_mode:
            if player1.guild == player2.guild and player1.guild != 'PCG':
                self.are_teammates = True
                self.co_op_stat_bonus = 50
            if player1.family == player2.family and player1.family != 'PCG':
                self.are_family_members=True
                self.co_op_health_bonus=100
            
            if self.are_teammates:
                bonus_message = f":checkered_flag:**{player1.guild}:** 🗡️**+{self.co_op_stat_bonus}** 🛡️**+{self.co_op_stat_bonus}**"
                if self.are_family_members:
                    bonus_message = f":family_mwgb:**{player1.family}:** ❤️**+{self.co_op_health_bonus}**\n:checkered_flag:**{player1.guild}:**🗡️**+{self.co_op_stat_bonus}** 🛡️**+{self.co_op_stat_bonus}**"
            elif self.are_family_members:
                    bonus_message = f":family_mwgb:**{player1.family}:** ❤️**+{self.co_op_health_bonus}**"
            else:
                bonus_message = f"Join a Guild or Create a Family for Coop Bonuses!"

            return bonus_message
    


    async def set_boss_win(self, player1, boss_card, companion=None):
        query = {'DISNAME': player1.disname} 
        fight_query = {'$set' : {'BOSS_FOUGHT' : True}}
        resp = db.updateUserNoFilter(query, fight_query)
        if boss_card.name not in player1.boss_wins:
            if self.is_hard_difficulty:
                await crown_utilities.bless(5000000, player1.did)
            else:
                await crown_utilities.bless(15000000, player1.did)
            if self.is_co_op_mode:
                if self.is_hard_difficulty:
                    await crown_utilities.bless(5000000, companion.did)
                else:
                    await crown_utilities.bless(15000000, companion.did)
            new_query = {'$addToSet': {'BOSS_WINS': boss_card.name}}
            resp = db.updateUserNoFilter(query, new_query)




    async def set_pvp_win_loss(self, your_player_id, opponent_player_id):
        await crown_utilities.bless(10000, your_player_id)

        player1_query = {'DID': your_player_id}
        win_value = {"$inc": {"PVP_WINS" : 1}}
        win_update = db.updateUserNoFilter(player1_query, win_value)

        loss_value = {"$inc": {"PVP_LOSS" : 1}}
        player2_query = {'DID': opponent_player_id}
        loss_update = db.updateUserNoFilter(player2_query, loss_value)


    async def save_boss_win(self, player1, player1_card, player1_title, player1_arm):
        match = await crown_utilities.savematch(player1.did, player1_card.name, player1_card.path, player1_title.name,
                                player1_arm.name, "N/A", "Boss", False)
        db.updateUserNoFilter({'DID': player1.did}, {'$set': {'BOSS_FOUGHT': True}})


    async def save_abyss_win(self, user, player, player1_card):
        bless_amount = 100000 + (10000 * int(self.abyss_floor))
        await crown_utilities.bless(bless_amount, player.did)
        new_level = int(self.abyss_floor) + 1
        response = db.updateUserNoFilter({'DID': player.did}, {'$set': {'LEVEL': new_level}})
        cardlogger = await crown_utilities.cardlevel(user, player1_card.name, player.did, "Purchase", "n/a")


    async def pvp_victory_embed(self, winner, winner_card, winner_arm, winner_title, loser, loser_card):
        wintime = time.asctime()
        starttime = time.asctime()
        h_gametime = starttime[11:13]
        m_gametime = starttime[14:16]
        s_gametime = starttime[17:19]
        h_playtime = int(wintime[11:13])
        m_playtime = int(wintime[14:16])
        s_playtime = int(wintime[17:19])
        gameClock = crown_utilities.getTime(int(h_gametime), int(m_gametime), int(s_gametime), h_playtime, m_playtime,
                            s_playtime)

        
        talisman_response = crown_utilities.inc_talisman(winner.did, winner.equipped_talisman)
        
        self.set_pvp_win_loss(winner.did, loser.did)

        if winner.association != "PCG":
            await crown_utilities.blessguild(250, winner.association)

        if winner.guild != "PCG":
            await crown_utilities.bless(250, winner.did)
            await crown_utilities.blessteam(250, winner.guild)
            await crown_utilities.teamwin(winner.guild)

        if loser.association != "PCG":
            await crown_utilities.curseguild(100, loser.association)

        if loser.guild != "PCG":
            await crown_utilities.curse(25, loser.did)
            await crown_utilities.curseteam(50, loser.guild)
            await crown_utilities.teamloss(loser.guild)

        match = await crown_utilities.savematch(winner.did, winner_card.name, winner_card.path, winner_title.name,
                                winner_arm.name, "N/A", "PVP", False)
        if self.is_raid_game_mode:
            embedVar = discord.Embed(
                title=f"{self._raid_end_message}\n\nYou have defeated the {self._association_name} SHIELD!\nMatch concluded in {self.turn_total} turns",
                description=textwrap.dedent(f"""
                                            {self.get_previous_moves_embed()}
                                            
                                            """), colour=0xe91e63)
        victory_message = f":zap: {winner_card.name} WINS!"
        victory_description = f"Match concluded in {self.turn_total} turns."
        if self.is_tutorial_game_mode:
            victory_message = f":zap: TUTORIAL VICTORY"
            victory_description = f"GG! Try the other **/solo** games modes!\nSelect **🌑 The Abyss** to unlock new features or choose **⚔️ Tales/Scenarios** to grind Universes!\nMatch concluded in {self.turn_total} turns."
        
            embedVar = discord.Embed(title=f"{victory_message}\n{victory_description}", description=textwrap.dedent(f"""
            {self.get_previous_moves_embed()}
            
            """),colour=0xe91e63)
        # embedVar.set_author(name=f"{t_card} says\n{t_lose_description}")
        
        if int(gameClock[0]) == 0 and int(gameClock[1]) == 0:
            embedVar.set_footer(text=f"Battle Time: {gameClock[2]} Seconds.")
        elif int(gameClock[0]) == 0:
            embedVar.set_footer(text=f"Battle Time: {gameClock[1]} Minutes and {gameClock[2]} Seconds.")
        else:
            embedVar.set_footer(
                text=f"Battle Time: {gameClock[0]} Hours {gameClock[1]} Minutes and {gameClock[2]} Seconds.")
            
            
        f_message = self.get_most_focused(winner_card, loser_card)
        embedVar.add_field(name=f"🌀 | Focus Count",
                        value=f"**{loser_card.name}**: {loser_card.focus_count}\n**{winner_card.name}**: {winner_card.focus_count}")
        #Most Damage Dealth
        d_message = self.get_most_damage_dealt(winner_card, loser_card)
        embedVar.add_field(name=f":boom: | Damage Dealt",
                        value=f"**{loser_card.name}**: {loser_card.damage_dealt}\n**{winner_card.name}**: {winner_card.damage_dealt}")
        #Most Healed
        h_message = self.get_most_damage_healed(winner_card, loser_card)
        embedVar.add_field(name=f":mending_heart: | Healing",
                        value=f"**{loser_card.name}**: {loser_card.damage_healed}\n**{winner_card.name}**: {winner_card.damage_healed}")
            
            
            
        if self._is_bounty_match:
            embedVar.add_field(name=":shinto_shrine: Raid Earnings", value=f"**:coin:{self._raid_bounty_plus_bonus}**")
        if self._is_title_match:
            embedVar.add_field(name=":shinto_shrine: Raid Earnings", value=f"**:shield: New Shield** {self.player.disname}")
        return embedVar


    def you_lose_embed(self, player_card, opponent_card, companion_card = None):
        wintime = time.asctime()
        starttime = time.asctime()
        h_gametime = starttime[11:13]
        m_gametime = starttime[14:16]
        s_gametime = starttime[17:19]
        h_playtime = int(wintime[11:13])
        m_playtime = int(wintime[14:16])
        s_playtime = int(wintime[17:19])
        gameClock = crown_utilities.getTime(int(h_gametime), int(m_gametime), int(s_gametime), h_playtime, m_playtime,
                            s_playtime)
        if self.is_raid_game_mode:
            embedVar = discord.Embed(title=f"🛡️ **{opponent_card.name}** defended the {self._association_name}\nMatch concluded in {self.turn_total} turns",
                description=textwrap.dedent(f"""
                                            {self.get_previous_moves_embed()}
                                            """),
                colour=0x1abc9c)
        else:
            embedVar = discord.Embed(title=f":skull: Try Again", description=textwrap.dedent(f"""
            {self.get_previous_moves_embed()}
            
            """),colour=0xe91e63)
            
            clock = self.get_battle_time()
            embedVar.set_footer(text=f"{clock}")
            
        if companion_card:
            f_message = self.get_most_focused(player_card, opponent_card, companion_card)
            embedVar.add_field(name=f"🌀 | Focus Count",
                            value=f"**{opponent_card.name}**: {opponent_card.focus_count}\n**{player_card.name}**: {player_card.focus_count}\n**{companion_card.name}**: {companion_card.focus_count}")
            #Most Damage Dealth
            d_message = self.get_most_damage_dealt(player_card, opponent_card, companion_card)
            embedVar.add_field(name=f":anger_right: | Damage Dealt",
                            value=f"**{opponent_card.name}**: {opponent_card.damage_dealt}\n**{player_card.name}**: {player_card.damage_dealt}\n**{companion_card.name}**: {companion_card.damage_dealt}")
            #Most Healed
            h_message = self.get_most_damage_healed(player_card, opponent_card, companion_card)
            embedVar.add_field(name=f":mending_heart: | Healing",
                            value=f"**{opponent_card.name}**: {opponent_card.damage_healed}\n**{player_card.name}**: {player_card.damage_healed}\n**{companion_card.name}**: {companion_card.damage_healed}")
        else:
            f_message = self.get_most_focused(player_card, opponent_card)
            embedVar.add_field(name=f"🌀 | Focus Count",
                            value=f"**{opponent_card.name}**: {opponent_card.focus_count}\n**{player_card.name}**: {player_card.focus_count}")
            #Most Damage Dealth
            d_message = self.get_most_damage_dealt(player_card, opponent_card)
            embedVar.add_field(name=f":boom: | Damage Dealt",
                            value=f"**{opponent_card.name}**: {opponent_card.damage_dealt}\n**{player_card.name}**: {player_card.damage_dealt}")
            #Most Healed
            h_message = self.get_most_damage_healed(player_card, opponent_card)
            embedVar.add_field(name=f":mending_heart: | Healing",
                            value=f"**{opponent_card.name}**: {opponent_card.damage_healed}\n**{player_card.name}**: {player_card.damage_healed}")
        return embedVar

    def get_most_focused(self, player_card, opponent_card, companion_card=None):
        value = ""
        if companion_card:
            if opponent_card.focus_count >= player_card.focus_count:
                if opponent_card.focus_count >= companion_card.focus_count:
                    value=f"{opponent_card.name}"
                else:
                    value=f"{companion_card.name}"
            elif player_card.focus_count >= companion_card.focus_count:
                value=f"{player_card.name}"
            else:
                value=f"{companion_card.name}"
        else:
            if opponent_card.focus_count >= player_card.focus_count:
                value=f"{opponent_card.name}"
            else:
                value=f"{player_card.name}"
        return value
    
    def get_most_damage_dealt(self, player_card, opponent_card, companion_card=None):
        value = ""
        if companion_card:
            if opponent_card.damage_dealt >= player_card.damage_dealt:
                if opponent_card.damage_dealt >= companion_card.damage_dealt:
                    value=f"{opponent_card.name}"
                else:
                    value=f"{companion_card.name}"
            elif player_card.damage_dealt >= companion_card.damage_dealt:
                value=f"{player_card.name}"
            else:
                value=f"{companion_card.name}"
        else:
            if opponent_card.damage_dealt >= player_card.damage_dealt:
                value=f"{opponent_card.name}"
            else:
                value=f"{player_card.name}"
        return value
    
    def get_most_damage_healed(self, player_card, opponent_card, companion_card=None):
        value = ""
        if companion_card:
            if opponent_card.damage_healed >= player_card.damage_healed:
                if opponent_card.damage_healed >= companion_card.damage_healed:
                    value=f"{opponent_card.name}"
                else:
                    value=f"{companion_card.name}"
            elif player_card.damage_healed >= companion_card.damage_healed:
                value=f"{player_card.name}**"
            else:
                value=f"{companion_card.name}"
        else:
            if opponent_card.damage_healed >= player_card.damage_healed:
                value=f"{opponent_card.name}"
            else:
                value=f"{player_card.name}"
        return value
        
        

    async def explore_embed(self, ctx, winner, winner_card, opponent_card):
        talisman_response = crown_utilities.inc_talisman(winner.did, winner.equipped_talisman)
        
        if self.player1_wins:
            if self.explore_type == "glory":
                await crown_utilities.bless(self.bounty, winner.did)
                drop_response = await crown_utilities.store_drop_card(winner.did, opponent_card.name, self.selected_universe, winner.vault, winner.owned_destinies, 3000, 1000, "Purchase", False, 0, "cards")
            
                message = f"VICTORY\n:coin: {'{:,}'.format(self.bounty)} Bounty Received!\nThe game lasted {self.turn_total} rounds.\n\n{drop_response}"
            if self.explore_type == "gold":
                await crown_utilities.bless(self.bounty, winner.did)
                message = f"VICTORY\n:coin: {'{:,}'.format(self.bounty)} Bounty Received!\nThe game lasted {self.turn_total} rounds."
            
            if winner.association != "PCG":
                await crown_utilities.blessguild(250, winner.association)

            if winner.guild != "PCG":
                await crown_utilities.bless(250, winner.did)
                await crown_utilities.blessteam(250, winner.guild)
                await crown_utilities.teamwin(winner.guild)

        else:
            if self.explore_type == "glory":
                await crown_utilities.curse(1000, winner.did)
            
            message = f"YOU LOSE!\nThe game lasted {self.turn_total} rounds."

        embedVar = discord.Embed(title=f"{message}",description=textwrap.dedent(f"""
        {self.get_previous_moves_embed()}
        
        """),colour=0x1abc9c)
        
        f_message = self.get_most_focused(winner_card, opponent_card)
        embedVar.add_field(name=f"🌀 | Focus Count",
                        value=f"**{opponent_card.name}**: {opponent_card.focus_count}\n**{winner_card.name}**: {winner_card.focus_count}")
        #Most Damage Dealth
        d_message = self.get_most_damage_dealt(winner_card, opponent_card)
        embedVar.add_field(name=f":boom: | Damage Dealt",
                        value=f"**{opponent_card.name}**: {opponent_card.damage_dealt}\n**{winner_card.name}**: {winner_card.damage_dealt}")
        #Most Healed
        h_message = self.get_most_damage_healed(winner_card, opponent_card)
        embedVar.add_field(name=f":mending_heart: | Healing",
                        value=f"**{opponent_card.name}**: {opponent_card.damage_healed}\n**{winner_card.name}**: {winner_card.damage_healed}")
        
        return embedVar


    async def get_win_rewards(self, player):
        reward_data = {}

        if player.rift == 1:
            rift_response = db.updateUserNoFilter({'DID': str(player.did)}, {'$set': {'RIFT': 0}})

        if player.family != "PCG":
            family_bank = await crown_utilities.blessfamily(self.fam_reward_amount, player.family)
            reward_data['FAMILY_BANK'] = family_bank
            
        if player.guild != "PCG":
            team_bank = await crown_utilities.blessteam(self.bank_amount, player.guild)
            reward_data['TEAM_BANK'] = team_bank
            
        random_element = crown_utilities.select_random_element(self.difficulty, self.mode)
        essence = crown_utilities.inc_essence(player.did, random_element["ELEMENT"], random_element["ESSENCE"])
        reward_data['RANDOM_ELEMENT'] = random_element['ESSENCE']
        reward_data['ESSENCE'] = essence

        return reward_data
    

    async def get_corruption_message(self, ctx):
        corruption_message = ""

        if self.is_easy_difficulty or (not self.is_tales_game_mode and not self.is_dungeon_game_mode):
            return corruption_message

        if self.is_corrupted:
            corruption_message = await crown_utilities.corrupted_universe_handler(ctx, self.selected_universe, self.difficulty)
            if not corruption_message:
                corruption_message = "You must dismantle a card from this universe to enable crafting."

        return corruption_message


    async def get_rematch_buttons(self, player):
        try:
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
            
            self.rematch_buff = False
            if player.guild != 'PCG':
                team_info = db.queryTeam({'TEAM_NAME': str(player.guild.lower())})
                guild_buff_info = team_info['ACTIVE_GUILD_BUFF']
                if guild_buff_info == 'Rematch':
                    self.rematch_buff =True
            
            if self.rematch_buff: #rematch update
                play_again_buttons.append(
                    manage_components.create_button(
                        style=ButtonStyle.green,
                        label=f"Guild Rematches Available!",
                        custom_id="grematch"
                    )
                )
            
            elif player.retries >= 1:
                play_again_buttons.append(
                    manage_components.create_button(
                        style=ButtonStyle.green,
                        label=f"{player.retries} Rematches Available!",
                        custom_id="rematch"
                    )
                )

            else:
                self.rematch_buff = False

            return play_again_buttons
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

def ai_enhancer_moves(your_card, opponent_card):
    aiMove = 1
    if your_card.move4enh in crown_utilities.Time_Enhancer_Check:
        if your_card.move4enh == "HASTE":
            if opponent_card.stamina <= your_card.stamina:
                aiMove =4
            else:
                if your_card.stamina >=80 and your_card.used_focus:
                    aiMove = 3
                elif your_card.stamina>=30 and your_card.used_focus:
                    aiMove = 2
                else:
                    aiMove = 1
        elif your_card.move4enh == "SLOW":
            if your_card.stamina <= opponent_card.stamina:
                aiMove =4
            else:
                if your_card.stamina >=80 and your_card.used_focus:
                    aiMove = 3
                elif your_card.stamina>=30 and your_card.used_focus:
                    aiMove = 2
                else:
                    aiMove = 1
        else:
            if your_card.used_focus ==False:
                aiMove=4
            else:
                if your_card.move4enh == "BLINK":
                    aiMove =4
                else:
                    if your_card.stamina >=80 and your_card.used_focus:
                        aiMove = 3
                    elif your_card.stamina>=30 and your_card.used_focus:
                        aiMove = 2
                    else:
                        aiMove = 1
    elif your_card.move4enh in crown_utilities.SWITCH_Enhancer_Check:
        if your_card.move4enh == "CONFUSE":
            if opponent_card.defense >= your_card.defense:
                if opponent_card.attack >= your_card.defense:
                    if opponent_card.attack>=opponent_card.defense:
                        aimove =4
                    else:
                        if your_card.stamina >=80 and your_card.used_focus:
                            aiMove = 3
                        elif your_card.stamina>=30 and your_card.used_focus:
                            aiMove = 2
                        else:
                            aiMove = 1
                else:
                    if your_card.stamina >=80 and your_card.used_focus:
                        aiMove = 3
                    elif your_card.stamina>=30 and your_card.used_focus:
                        aiMove = 2
                    else:
                        aiMove = 1
            else:
                if your_card.stamina >=80 and your_card.used_focus:
                    aiMove = 3
                elif your_card.stamina>=30 and your_card.used_focus:
                    aiMove = 2
                else:
                    aiMove = 1
        else:
            if your_card.attack >= 800 and your_card.defense>= 800:
                aiMove = 1
            else:
                aiMove = 4
    elif your_card.move4enh in crown_utilities.Damage_Enhancer_Check or your_card.move4enh in crown_utilities.Turn_Enhancer_Check: #Ai Damage Check
        aiMove = 4
    elif your_card.move4enh in crown_utilities.Gamble_Enhancer_Check: #Ai Gamble and Soul checks
        aiMove =4
    elif your_card.move4enh in crown_utilities.Stamina_Enhancer_Check: #Ai Stamina Check
        if your_card.stamina >= 240:
            if your_card.stamina >=80 and your_card.used_focus:
                aiMove = 3
            elif your_card.stamina>=30 and your_card.used_focus:
                aiMove = 2
            else:
                aiMove = 3
        else:
            aiMove = 4
    elif your_card.move4enh in crown_utilities.TRADE_Enhancer_Check: #Ai Trade Check
        if your_card.defense >= your_card.attack and your_card.defense <= (your_card.attack * 2):
            aiMove = 4
        elif your_card.attack <= (your_card.defense * 2):
            aiMove =4
        else:
            if your_card.stamina >=90 and your_card.used_focus:
                if your_card.defense >= your_card.attack:
                    if your_card.used_focus and not your_card.used_resolve:
                        aiMove =5
                    else:
                        if your_card.stamina >=80 and your_card.used_focus:
                            aiMove = 3
                        elif your_card.stamina>=30 and your_card.used_focus:
                            aiMove = 2
                        else:
                            aiMove = 1
                else:
                    aiMove = 3
            else:
                if your_card.stamina >=80 and your_card.used_focus:
                    aiMove = 3
                elif your_card.stamina>=30 and your_card.used_focus:
                    aiMove = 2
                else:
                    aiMove = 1
    elif your_card.move4enh in crown_utilities.Healer_Enhancer_Check: #Ai Healer Check
        if your_card.health >= your_card.max_health:
            if your_card.stamina >=80 and your_card.used_focus:
                aiMove = 3
            elif your_card.stamina>=30 and your_card.used_focus:
                aiMove = 2
            else:
                aiMove = 1
        else:
            aiMove = 4
    elif your_card.move4enh in crown_utilities.INC_Enhancer_Check: #Ai Inc Check
        if your_card.attack >= 8000 or your_card.defense >=8000:
            if your_card.stamina >=80 and your_card.used_focus:
                aiMove = 3
            elif your_card.stamina>=30 and your_card.used_focus:
                aiMove = 2
            else:
                aiMove = 1
        else:
            aiMove = 4
    elif your_card.move4enh in crown_utilities.DPS_Enhancer_Check: #Ai Steal Check
        if your_card.attack >= 8000 and opponent_card.attack >=100:
            if your_card.stamina >=80 and your_card.used_focus:
                aiMove = 3
            elif your_card.stamina>=30 and your_card.used_focus:
                aiMove = 2
            else:
                aiMove = 1
        elif your_card.defense >= 8000 and opponent_card.defense >=100:
            if your_card.stamina >=80 and your_card.used_focus:
                aiMove = 3
            elif your_card.stamina>=30 and your_card.used_focus:
                aiMove = 2
            else:
                aiMove = 1
        else:
            aiMove = 4
    elif your_card.move4enh in crown_utilities.FORT_Enhancer_Check: #Ai Fort Check
        if (opponent_card.attack<= 50 or your_card.attack >=5000) or your_card.health <= 1000 or your_card.health <= (.66 * your_card.max_health):
            if your_card.stamina >=80 and your_card.used_focus:
                aiMove = 3
            elif your_card.stamina>=30 and your_card.used_focus:
                aiMove = 2
            else:
                aiMove = 1
        elif (opponent_card.defense <=50 or your_card.defense >= 5000) or your_card.health <= 1000 or your_card.health <= (.66 * your_card.max_health):
            if your_card.stamina >=80 and your_card.used_focus:
                aiMove = 3
            elif your_card.stamina>=30 and your_card.used_focus:
                aiMove = 2
            else:
                aiMove = 1
        else:
            aiMove = 4
    elif your_card.move4enh in crown_utilities.Sacrifice_Enhancer_Check: #Ai Sacrifice Check
        if your_card.attack >= 5000 or your_card.health <= 1000 or your_card.health <= (.75 * your_card.max_health):
            if your_card.used_focus and not your_card.used_resolve:
                aiMove =5
            else:
                if your_card.stamina >=80 and your_card.used_focus:
                    aiMove = 3
                elif your_card.stamina>=30 and your_card.used_focus:
                    aiMove = 2
                else:
                    aiMove = 1
        elif your_card.defense >= 5000 or your_card.health <=1000 or your_card.health <= (.75 * your_card.max_health):
            if your_card.used_focus and not your_card.used_resolve:
                aiMove =5
            else:
                if your_card.stamina >=80 and your_card.used_focus:
                    aiMove = 3
                elif your_card.stamina>=30 and your_card.used_focus:
                    aiMove = 2
                else:
                    aiMove = 1
        else:
            aiMove = 4
    else:
        aiMove = 4 #Block or Enhance
        
    #Killing Blow Checks
    if opponent_card.health <= 200:
        if your_card.stamina >= 80:
            aiMove =3
        elif your_card.stamina >= 30:
            aiMove=2
        elif your_card.stamina >= 20:
            if your_card.move4enh == "LIFE" or your_card.move4enh in crown_utilities.Damage_Enhancer_Check:
                aiMove = 4
            else:
                aiMove = 1
        else:
            aiMove = 1
            
        
    return aiMove





