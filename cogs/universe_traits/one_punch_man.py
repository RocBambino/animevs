import crown_utilities
import random


def rank_hero(player_card, battle_config, opponent_card):
    if player_card.universe == "One Punch Man":
        low_tier_cards = [1,2]
        mid_tier_cards = [3,4]
        high_tier_cards = [5,6]
        rank = "F"
        ap_boost = 15 * player_card.tier
        if player_card.tier == 7:
            ap_boost = 110
            rank = ":regional_indicator_s:"
        if player_card.tier in low_tier_cards:
            rank = ":regional_indicator_c:"
        if player_card.tier in mid_tier_cards:
            rank = ":regional_indicator_b:"
        if player_card.tier in high_tier_cards:
            rank = ":regional_indicator_a:"
        player_card.card_lvl_ap_buff = player_card.card_lvl_ap_buff + ap_boost
        
        battle_config.add_to_battle_log(f"(**🌀**)  🩸{rank} Rank Hero : **{player_card.name}** increased AP by **{ap_boost}** :sunny:!")


def hero_reinforcements(player_card, battle_config, opponent_card):
    if opponent_card.universe == "One Punch Man":
        opponent_card.health = round(opponent_card.health + 100)
        opponent_card.max_health = round(opponent_card.max_health + 100)
        battle_config.add_to_battle_log(f"(**🌀**) 🩸 Hero Reinforcements! **{opponent_card.name}**  Increased Health & Max Health ❤️")





