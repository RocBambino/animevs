import textwrap

# PLAYER_COMMANDS="`/d` - Delete `USER` Account" + "\n\n" + "`/vs` `GAME` @`PLAYER` - How many times you defeated opponent" + "\n\n" + "`/r` - Register `USER` Account\n\n"
# PROFILE_COMMANDS="`/lkg` - Lookup available `GAMES`" + "\n\n" + "`/ag` `GAME` - Add `GAME` to `USER` account" + "\n\n" + "`/uign` `GAME` `IGN` - Update In Game Name for `GAME`"  + "\n\n" + "`/lk` @`player` - Lookup a `PLAYERS` profile" + "\n\n" +  "`/lkt` `TEAM Name` - Lookup `TEAM PROFILE`\n\n"
# SENPAI_COMMANDS="`/senpai` - Learn Basic Of Party Chat Gaming Bot" + "\n\n" + "`/bootcamp` - Learn `LOBBY` commands" + "\n\n" + "`/franchise` - Learn `TEAM` commands" + "\n\n" + "`/legend` - Learn `TOURNAMENT` commands\n\n"
# LOBBY_COMMANDS="`/lobby` - Check if `USER` is hosting a lobby" + "\n\n" + "`/check` - Check if `PLAYER` is in a `LOBBY`" + "\n\n" + "`/createlobby` lobbysize `GAME` - Create `LOBBY` up to size 5" + "\n\n" + "`/end` - End `LOBBY` and Record `SCORE`" + "\n\n" + "`/deletelobby` - Delete `LOBBY`" + "\n\n" + "`/joinlobby`  @`PLAYER`- Join  `PLAYER` `LOBBY`" + "\n\n" + "`/score` @`PLAYER` - Score (`PLAYER` / `TEAM`) in `LOBBY`" + "\n\n" + "`/add` (LOCKED) -  Add `PLAYERS` into `LOBBY`\n\n" 
# SHOP_COMMANDS= "`/shop` - Open Pop Up `SHOP`" + "\n\n" + "`/viewcard` - Preview `CARD` in `SHOP`" + "\n\n" + "`/buycard` - Buy `CARD` from `SHOP`" + "\n\n" + "`/viewtitle` - preview `TITLE` in `SHOP`" + "\n\n" + "`/buytitle` - Buy `TITLE` from `SHOP`" + "\n\n" + "`/viewarm` - preview `ARM` in `SHOP`" + "\n\n" + "`/buyarm` - Buy `ARM` from `SHOP`\n\n" + "\n\n" + "`/viewpet` - preview `PET` in `VAULT`"
# TEAM_COMMANDS="`/createteam` `GAME` `TEAM name` - Create `TEAM`" + "\n\n" +   "`/addteamgame` `GAME` - Add `GAME` to `TEAM`" + "\n\n" + "`/deleteteam` `TEAM` - Delete `TEAM` (`OWNER` Only)" + "\n\n" + "`/addtoteam` @`PLAYER` - Add `PLAYER` to `TEAM` (`OWNER` Only)" + "\n\n" + "`/deletemember` @`PLAYER` - Delete `MEMBER` (`OWNER` Only)" + "\n\n" + "`/apply` @`PLAYER` - Applys for `TEAM` (`PLAYER` must be `OWNER`)" + "\n\n" + "`/leaveteam` `TEAM` - Leave `TEAM`\n\n"
# CROWN_UNLIMITED_PLAYER_COMMANDS="`/vault` - Open `VAULT` *Use :fast_forward:*\n\n`/equipcard` `CARD Name` - Equip new `CARD`\n\n`/equiptitle` - Equip new `TITLE`\n\n`/equiparm` - Equip new `ARM`\n\n`/viewpet` - View `PET` Stats\n\n`/equippet` - Equip new `PET`\n\n`/trade` @`PLAYER` `ITEM` - trade `CARDS`, `TITLES`, `ARMS` or `PETS`\n\n`/sell` @`PLAYER` `ITEM` - sell `CARDS`, `TITLES`, `ARMS` or `PETS`\n\n`/build` - view current Build\n\n`/savedeck` - save current Build\n\n`/viewdeck` - view/load Saved Builds\n\n`/shop` - Open Pop Up `SHOP` *Use :fast_forward:*\n\n"

CROWN_UNLIMITED_GAMES = textwrap.dedent(f"""\
**🆕How to Register, Delete, Lookup your account**
**/register**: 🆕 Register your account
**/deleteaccount**: Delete your account
**/player**: Lookup your account, or a friends
**/family**: Lookup your family, or a friends


**PVE Game Modes**
**🆘 The Tutorial** - Learn Anime VS+ battle system
**🌑 The Abyss** - Climb the ladder for rewards and unlockables
**⚔️ Tales** - Normal battle mode to earn cards, accessories and more
**🔥 Dungeon** - Hard battle mode to earn dungeon cards, dungeon accessories, and more
**👹 Boss Encounter** - Extreme Boss battles to earn Boss cards, boss accessories and more
**:projector: Scenario Battle** - Battle through unique scenarios to earn Cards and Moves

**Solo Player!**
**/solo** - Play through all pve game modes solo to earn solo rewards

**Co-op Players!**
**/coop** - Play through all pve game modes with a friend to earn co-op rewards

**Duo with AI**
**/duo** - Play through all pve game modes with one of your build **/presets** as an AI companion

**PVP**
**/pvp** - Battle a rival in PVP mode

[Join the Anime VS+ Support Server](https://discord.gg/2JkCqcN3hB)
""")


UNIVERSE_STUFF = textwrap.dedent(f"""\
**View Universes!**
**/universes** - View all available universe info including all available cards, accessories, and destinies

[Join the Anime VS+ Support Server](https://discord.gg/2JkCqcN3hB)
""")


LEGEND = textwrap.dedent(f"""\
**Card Basics**
🀄 - **Card Tier** *1-7*
🔱 - **Card Level** *1-999*
🥋 - **Card Class**
❤️ - **Card Health** (HLT)
🌀 / ⚡ - **Card Stamina** (ST)
🗡️ - **Attack (ATK)** Blue Crystal 🟦
🛡️ - **Defense (DEF)** Red Crystal 🟥
🏃 - **Speed**
🩸 - Card Passive *Card Passive enhancers are applied each turn, passively.*

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
    "🔥 Fire - Does 50% damage of previous attack over the next opponent turns, stacks.\n",
    "❄️ Ice - Every 2 attacks, opponent freezes and loses 1 turn.\n",
    "💧 Water - Increases all water move AP by 100 Flat.\n",
    "⛰️ Earth - Cannot be Parried. Grants Shield and Increases Def by 30% AP.\n",
    "🌩️ Electric- Add 10% DMG Dealt to Shock damage, added to all Move AP.\n",
    "🌪️ Wind - On Miss, Use Wind Attack, boosts all wind damage by 35% of damage dealt.\n",
    "🔮 Psychic - Penetrates Barriers. Reduce opponent ATK & DEF by 15% DMG. After 3 Hits Gain a Barrier\n",
    "☠️ Death - Deals 30% DMG to opponent max health. Gain Attack equal to that amount.\n",
    "❤️‍🔥 Life - Create Max Health and Heal for 35% DMG.\n",
    "🌕 Light - Regain 50% ST(Stamina) Cost, Illumination Increases ATK by 30% of DMG.\n",
    "🌑 Dark- Penetrates Shields, Barriers and Parries & decreases opponent ST(Stamina) by 15.\n",
    "🧪 Poison - Penetrates shields, Poison 30 damage stacking up to (150 * Card Tier).\n",
    "🏹 Ranged - If ST(stamina) greater than 30, Deals 1.7x Damage. Every 4 Ranged Attacks Increase Hit Chance by 5%\n",
    "🧿 Energy - Has higher 35% higher chance of Crit.\n",
    "♻️ Reckless - Deals Incredible Bonus Damage, take 40% as reckless. If Reckless would kill you reduce HP to 1\n",
    "⌛ Time - Strong Block and Increase Turn Count by 3, If ST(Stamina) is < 50, Focus for 1 Turn and lower opponent protections and goes through parry.\n",
    "🅱️ Bleed - Every 2 Attacks deal (10x turn count + 5% Health) damage to opponent.\n",
    "🪐 Gravity - Disables Opponent Block, Reduce opponent DEF by 30% DMG, Decrease Turn Count By 3, goes through barrier and parry.\n"
]


ELEMENTS = textwrap.dedent(f"""\
**🔅 Elements**    
👊 Physical - If ST(stamina) greater than 80, Deals Bonus Damage. After 3 Strike gain a Parry

🔥 Fire - Does 50% damage of previous attack over the next opponent turns, stacks.

❄️ Ice - Every 2 attacks, opponent freezes and loses 1 turn.

💧 Water - Increases all water move AP by 100 Flat.

⛰️ Earth - Cannot be Parried. Grants Shield and Increases Def by 30% AP.

🌩️ Electric- Add 10% DMG Dealt to Shock damage, added to all Move AP.

🌪️ Wind - On Miss, Use Wind Attack, boosts all wind damage by 35% of damage dealt.

🔮 Psychic - Penetrates Barriers. Reduce opponent ATK & DEF by 15% DMG. After 3 Hits Gain a Barrier

☠️ Death - Deals 30% DMG to opponent max health. Gain Attack equal to that amount.

❤️‍🔥 Life - Create Max Health and Heal for 35% DMG.

🌕 Light - Regain 50% ST(Stamina) Cost, Illumination Increases ATK by 30% of DMG.

🌑 Dark- Penetrates Shields, Barriers and Parries & decreases opponent ST(Stamina) by 15.

🧪 Poison - Penetrates shields, Poison 30 damage stacking up to (150 * Card Tier).

🏹 Ranged - If ST(stamina) greater than 30, Deals 1.7x Damage. Every 4 Ranged Attacks Increase Hit Chance by 5%

🧿 Energy - Has higher 35% higher chance of Crit.

♻️ Reckless - Deals Incredible Bonus Damage, take 40% as reckless. If Reckless would kill you reduce HP to 1

⌛ Time - Strong Block and Increase Turn Count by 3, If ST(Stamina) is < 50, Focus for 1 Turn and lower opponent protections and goes through parry.

🅱️ Bleed - Every 2 Attacks deal (10x turn count + 5% Health) damage to opponent.

🪐 Gravity - Disables Opponent Block, Reduce opponent DEF by 30% DMG, Decrease Turn Count By 3, goes through barrier and parry.

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
**Main Menu!⚒️**
**/menu** - Access your current build, cards, titles, arms, quests, and destinies. You can also open the shop and visit the blacksmith here!

**Reward Codes! ⌨️**
**/code** - Enter in codes to earn in-game rewards!

**Trade! 🎴 🎗️ 🦾**
**/trade** - Start a trade with a friend!
**/tradecoins** - Add 🪙 to your trade!

**Gift! 🪙**
**/gift** - Gift a friend some 🪙!

**Card Analysis! 🎴**
**/analysis** - View specific card statistics and optimal builds for that card

**Do you already know the card or accessories name?**
*If you already know what you want to equip / view, use the fast equip commands below to equip your item...*
*/equipcard*
*/equiparm*
*/equiptitle*
*/equipsummon*
------------------
*/view*

[Join the Anime VS+ Support Server](https://discord.gg/2JkCqcN3hB)
""")