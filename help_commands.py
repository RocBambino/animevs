import textwrap


CROWN_UNLIMITED_GAMES = textwrap.dedent(f"""\
**🆕How to Register, Delete, Lookup your account**
**/register**: 🆕 Register your account
**/deleteaccount**: Delete your account
**/player**: Lookup your account, or a friends
**/build**: View your current build, cards, titles, arms, talismans, summons and more
                                        
**PVE**
**/play** - Battle through a variety of PVE modes                                      

                                        
**PVE Game Modes**
**🆘 The Tutorial** - Learn Anime VS+ battle system
**⚡ Randomize** - Select and start a Random Game Mode Below
**⚔️ Tales** - Normal battle mode to earn cards, accessories and more
**👺 Dungeon** - Hard battle mode to earn dungeon cards, dungeon accessories, and more
**📽️ Scenario Battle** - Battle through unique scenarios to earn Cards and Moves
**💀 Raid Battle** - Battle through High Level scenarios to earn Mythical Cards and Moves
**🌌 Explore Battle** - Random Encounter battles to earn rare cards and major rewards
                                        
**PVP**
**/pvp** - Battle a rival in PVP mode
                                        
[Join the Anime VS+ Support Server](https://discord.gg/2JkCqcN3hB)
""")


UNIVERSE_STUFF = textwrap.dedent(f"""\
**View Universes!**
**/universes** - View all available universe info including all available cards, accessories, and destinies

**/view** - Lookup/View all available game items.
[Join the Anime VS+ Support Server](https://discord.gg/2JkCqcN3hB)
""")


LEGEND = textwrap.dedent(f"""\
**Card Basics**
🀄 - **Card Tier** *1-10*
🔱 - **Card Level**
🥋 - **Card Class**
❤️ - **Card Health** (HLT)
🌀 / ⚡ - **Card Stamina** (ST)
🗡️ - **Attack (ATK)** Blue Crystal 🟦
🛡️ - **Defense (DEF)** Red Crystal 🟥
🏃 - **Speed**

**Accessories & Summons**
⚠️ - Your title or arm does not match your universe
🎗️ - **Title accessory**  *Title enhancers are applied each turn, passively.*
🦾 - **Arm accessory** *Arm enhancers are applied passively throughout the duration of battle.*
📿 - **Talisman** *Equip Elemntal  Talismans to bypass opponent affinities*
🧬 - **Summon!** *Summons use Active Enhancers that are available during battle after you Resolve*

**Currency**
💰 - **Coins** *Buy items in the shop and blacksmith*
💎 - **Gems** *Craft universe hearts, souls, cards, and destiny lines!*
🪔 - **Essence** *Craft Elemental Talismans*

[Join the Anime VS+ Support Server](https://discord.gg/2JkCqcN3hB)
""")


ELEMENTS_LIST = [
    "👊 Physical - If ST(stamina) greater than 80, Deals Bonus Damage. After 3 Strike gain a Parry\n",
    "⚔️ Sword - Every 3rd attack will result in a Critical Strike that also increases Atack by 40% of damage dealt.\n",
    "🏹 Ranged - If ST(stamina) greater than 30, Deals 1.7x Damage. Every 3 Ranged Attacks Increase Hit Chance by 10%\n",
    "🔫 Gun - Goes through shields. Has a 40% chance to strike twice. Double striking lowers opponents defense by 35% of the current value.\n",
    "♻️ Reckless - Deals Incredible Bonus Damage, take 40% as reckless at the cost of a turn to recover. If Reckless would kill you reduce HP to 1. Reckless is buffed when resolved, but you take more damage as well.\n",
    "🔥 Fire - Does 50% damage of previous attack over the next opponent turns, burn effect bypasses shields and stacks.\n",
    "💧 Water - Each strike increases all water move AP by 100. Every 200 AP, gain a shield. Every 400 AP send a Tsunami Strike for True Damage.\n",
    "⛰️ Earth - Penetrates Parry. Increases Def by 25% AP. Grants Shield - Increase by 50% DMG.\n",
    "🌩️ Electric- Add 35% DMG Dealt to Shock damage, Shock damage amplifies all Move AP.\n",
    "🌪️ Wind - On Miss or Crit, boosts all wind damage by 75% of damage dealt.\n",
    "🌿 Nature - Saps Opponent ATK and DEF for 35% of Damage & heals Health and Max Health for that amount as well.\n",
    "❄️ Ice - Every 3rd attack, opponent freezes and loses 1 turn, and loses attack and defense equal to 50% of damage dealt.\n",
    "🅱️ Bleed - Penetrates Parry. Every 2 Attacks deal (10x turn count + 5% Health) damage to opponent.\n",
    "🧿 Energy - Has higher 35% higher chance of Crit. This crit hit goes through all protections\n",
    "🔮 Psychic - Penetrates Barriers. Reduce opponent ATK & DEF by 35% DMG. After 3 Hits Gain a Barrier\n",
    "💤 Sleep - Every 2nd attack adds a stack of Rest. Before Opponent focuses they must Rest, skipping their turn, for each stack of Rest. Opponent only takes sleep damage while Resting.\n",
    "☠️ Death - Deals 40% DMG to opponent max health. Gain Attack equal to that amount. Executes opponent if their health equals 10% of their base max health.\n",
    "❤️‍🔥 Life - Create Max Health and Heal for 40% DMG.\n",
    "🌕 Light - Increases ATK by 40% of DMG. 40% of DMG is stored and attacks the opponent when they focus\n",
    "🌑 Dark- Penetrates all Protections & decreases opponent ST(Stamina) by 15.\n",
    "🧪 Poison - Penetrates Shields and Parry. Stacks Poison damage equal to 35% of damage done. Stacking up to 30% of opponent max health. The Opponent takes damage when they attack.\n",
    "🩻 Rot - Penetrates Shields and Parry. Stacks Rot damage equal to 15% of damage done stacking up to 20% of max health. The Opponent takes damage when they attack.\n",
    "⌛ Time - Strong Block and Increase Turn Count by 3, If ST(Stamina) is < 50, Focus for 1 Turn and goes through and lowers opponent barriers and parry and AP is increased by damage dealt * turn total / 100.\n",
    "🪐 Gravity - Disables Opponent Block, Reduce opponent DEF by 40% DMG, Decrease Turn Count By 3, goes through barrier and parry.\n",
    "🐲 Draconic - Draconic attacks can only be ULTIMATE or Summoned. Pentrates all protections. Combines the AP and Elemental Effects of your BASIC and SPECIAL attack into one powerful blow!.",

]


ELEMENTS = textwrap.dedent(f"""\
**🔅 Elements**    
👊 Physical - If ST(stamina) greater than 80, Deals Bonus Damage. After 3 Strike gain a Parry
                           
⚔️ Sword - Every 3rd attack will result in a Critical Strike that also increases Atack by 40% of damage dealt.
                           
🏹 Ranged - If ST(stamina) greater than 30, Deals 1.7x Damage. Every 3 Ranged Attacks Increase Hit Chance by 10%
                           
🔫 Gun - Penetrates Shield. Has a 40% chance to deal a double hit. Double striking lowers opponents defense by 35% of the current value.
                           
♻️ Reckless - Deals Incredible Bonus Damage, take 60% as reckless. If Reckless would kill you reduce HP to 1. After striking you enter a resting state, skipping your turn.

🔥 Fire - Does 50% damage of previous attack over the next opponent turns, burn effect bypasses shields and stacks.

❄️ Ice - Every 3 attacks, opponent freezes and loses 1 turn, and loses attack and defense equal to 50% of damage dealt.

💧 Water - Each strike increases all water move AP by 100. Every 200 AP, gain a shield. Every 400 AP send a Tsunami Strike for True Damage

⛰️ Earth - Cannot be Parried. Grants Shield and Increases Def by 30% AP.
                           
🌿 Nature - Saps Opponent ATK and DEF for 35% of Damage & heals Health and Max Health for that amount as well.

🌩️ Electric- Add 10% DMG Dealt to Shock damage, added to all Move AP.

🌪️ Wind - On Miss or Crit boosts all wind damage by 60% of damage dealt.

🔮 Psychic - Penetrates Barriers. Reduce opponent ATK & DEF by 15% DMG. After 3 Hits Gain a Barrier
                           
💤 Sleep - Every 2nd attack adds a stack of Rest. Before Opponent focuses they must Rest, skipping their turn, for each stack of Rest. Opponent only takes sleep damage while Resting.

☠️ Death - Deals 30% DMG to opponent max health. Gain Attack equal to that amount.

❤️‍🔥 Life - Steals 30% damage done health and max health from opponent.

🌕 Light - Increases ATK by 40% of DMG. 40% of DMG is stored and attacks the opponent when they focus.

🌑 Dark- Penetrates Shields, Barriers and Parries & decreases opponent ST(Stamina) by 15.

🧪 Poison - Penetrates shields, stacks poison damage equal to 35% of damage done stacking up to 30% of max health. This damage hits the opponent when the opponent attacks.

🩻 Rot - Penetrates shields, stacks rot damage equal to 15% of damage done stacking up to 20% of max health. This damage hits the opponents max health when the opponent attacks.

🧿 Energy - Has higher 35% higher chance of Crit.

⌛ Time - Strong Block and Increase Turn Count by 3, If ST(Stamina) is < 50, Focus for 1 Turn and lower opponent protections and goes through parry.

🅱️ Bleed - Every 2 Attacks deal (10x turn count + 5% Health) damage to opponent.

🪐 Gravity - Disables Opponent Block, Reduce opponent DEF by 50% DMG, Decrease Turn Count By 3, goes through barrier and parry.
                           
🐲 Draconic - Draconic attacks can only be ULTIMATE or Summoned, combines the AP and Elemental Effects of your BASIC and SPECIAL attack into one powerful blow!.

[Join the Anime VS+ Support Server](https://discord.gg/2JkCqcN3hB)
""")


BOT_COMMANDS = textwrap.dedent(f"""\
**Guild Commands**
**/guild** - Guild lookup, configurations, and apply for
**/guildoperations** - Guild operations
**/createguild** - Create guild 
**/disbandguild** - Delete guild
**/recruit** - Recruit player to your guild
**/leaveguild guild** - Leave Guild
**/pay** - Send Guild Members coin
**/donate** - Donate coin to Guild Bank


**Association Commands**
**/association** - Association lookup
**/oath** - Create Association/Reswear Association
**/disband** - Delete Association (Founder Only)
**/betray** - Leave Association (Sworn Only)
**/knight** - Set Association Shield to Player (Association Owners Only)
**/ally** - Add Guild To Association (Association Owners Only)
**/exile** - Kick Guild from Association (Association Owners Only)
**/renounce** - Leave Association (Guild Owner Only)
**/sponsor** - Send Guild coin (Association Owners Onlu)
**/fund** - Donate coin to Association Bank
**/bounty** - Set Association Bounty (Association Owners Only)
**/viewhall** - View Hall Information


**Family Commands**
**/family** - Family Menu
**/marry** - Invite User to join Family
**/divorce** - Ask for divorce from partner
**/adopt** - Adopt kid into family
**/disown** - Remove Kid From Family
**/leavefamily** - Leave from family (Kid Only)
**/allowance** - Send Family Members coin (Head/Partner Only)
**/invest** - Invest coin into family Bank
**/houses** - Show list of available houses
**/viewhouse** - View House Information

[Join the Anime VS+ Support Server](https://discord.gg/2JkCqcN3hB)
""")


CTAP_COMMANDS = textwrap.dedent(f"""\
                                
**Inventory Commands**
**/cards** - View your available cards
**/titles** - View your available titles
**/arms** - View your available arms
**/summons** - View your available summons
**/talismans** - View your available talismans
**/attune** - Attune elemental talismans from essence
                                
**Shop Commands**
**/marketplace** - View the online marketplace
**/blacksmith** - View the blacksmith

**Reward Codes! ⌨️**
**/code** - Enter in codes to earn in-game rewards!

**Trade! 🎴 🎗️ 🦾**
**/trade** - Start a trade with a friend!
**/tradecoins** - Add 🪙 to your trade!

**Gift! 🪙**
**/gift** - Gift a friend some 🪙!
[Join the Anime VS+ Support Server](https://discord.gg/2JkCqcN3hB)
""")

OPTION_COMMANDS = textwrap.dedent(f"""\

**Options**
**/help** - View all heklp commands and manual
**/explore**  - Toggle Explore mode
**/difficulty** - Change the difficulty of the game
**/autosave** - Toggle autosave on or off
**/battlehistory** - Update battle history length

[Join the Anime VS+ Support Server](https://discord.gg/2JkCqcN3hB)
""")