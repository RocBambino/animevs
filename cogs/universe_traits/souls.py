import crown_utilities

def souls_resolve(player_card, battle_config):
    if player_card.universe == "Souls":
        battle_config.add_to_battle_log(f"(**{battle_config.turn_total}**) **{player_card.name}** 🩸 Phase 2: Enhanced Moveset!")
        combat_phases(player_card)
        return True
    else:
        return False

def combat_phases(player_card):
    if player_card.used_resolve and player_card.universe == "Souls":
        player_card.move1 = player_card.move2
        player_card.move1ap = player_card.move2ap
        player_card.move1_stamina = player_card.move1_stamina
        player_card.move1_element = player_card.move2_element
        player_card.move1_emoji = player_card.move2_emoji
        
        player_card.move2 = player_card.move3
        player_card.move2ap = player_card.move3ap
        player_card.move2_stamina = player_card.move2_stamina
        player_card.move2_element = player_card.move3_element
        player_card.move2_emoji = player_card.move3_emoji


def combo_recognition(player_card, battle_config, opponent_card):
    if opponent_card.universe == "Souls":
        opponent_card.attack = round(opponent_card.attack + (60 + battle_config.turn_total))
        battle_config.add_to_battle_log(f"(**🌀**) 🩸 Combo Recognition! **{opponent_card.name}** Increased Attack by **{60 + battle_config.turn_total}** 🔺")








