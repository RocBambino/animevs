import crown_utilities

def shinigami_eyes(player_card, battle_config):
    if player_card.universe == "Death Note":
        value = 6
        battle_config.add_to_battle_log(f"({battle_config.turn_total}) {player_card.name} used shinigami eyes to sacrifice {round((.15 * player_card.max_health))} max health to increase turn count by {value + player_card.tier}")
        player_card.max_health = round(player_card.max_health - (.15 * player_card.max_health))
        if player_card.health >= player_card.max_health:
            player_card.health = player_card.max_health
        battle_config.turn_total = battle_config.turn_total + player_card.tier + value

def scheduled_death(player_card, battle_config, opponent_card):
    if player_card.universe == "Death Note":
        if battle_config.turn_total >= (150):
            battle_config.add_to_battle_log(f"({battle_config.turn_total}) 🩸 {opponent_card.name} had a heart attack and died, as was written")
            opponent_card.health = -1000


def set_deathnote_message(player_card, battle_config):
    if not player_card.scheduled_death_message:
        if player_card.universe == "Death Note":
            player_card.scheduled_death_message = True
            battle_config.add_to_battle_log(f"({battle_config.turn_total}) 🩸 {player_card.name} scheduled death 📓 turn 150")



