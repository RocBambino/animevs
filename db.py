from pymongo import MongoClient
import certifi
import messages as m
from decouple import config
import re

if config('ENV') == "production":
    # PRODUCTION
    use_database = "PCGPROD"
else:
    # TEST
    use_database = "PCGTEST"

# TOKEN = config('MONGOTOKEN_TEST')
MONGO = config('MONGO_LOGIN')
mongo = MongoClient(MONGO, tlsCAFile=certifi.where())

# mongo = pymongo.MongoClient(TOKEN)

db = mongo[use_database]

users_col = db["USERS"]
teams_col = db["TEAMS"]
family_col = db["FAMILY"]
guild_col = db["GUILD"]
sessions_col = db["SESSIONS"]
games_col = db["GAMES"]
matches_col = db["MATCHES"]
tournaments_col = db["TOURNAMENTS"]
gods_col = db["GODS"]
cards_col = db["CARDS"]
titles_col = db["TITLES"]
arm_col = db["ARM"]
universe_col = db['UNIVERSE']
house_col = db["HOUSE"]
hall_col = db["HALL"]
boss_col = db['BOSS']
pet_col = db['PET']
vault_col =db["VAULT"]
menu_col = db['MENU']
abyss_col = db['ABYSS']
trade_col = db['TRADE']
server_col = db['SERVER']
arena_col = db['ARENA']
codes_col = db['CODES']
scenario_col = db['SCENARIO']

acceptable = [1, 2, 3, 4]
arm_exclude_list = ['BASIC', 'SPECIAL', 'ULTIMATE']
arm_moves_only = ['BASIC', 'SPECIAL', 'ULTIMATE']


def viewQuery(search_string):
    collections = {
        "CARDS": "NAME",
        "TITLES": "TITLE",
        "ARM": "ARM",
        "UNIVERSE": "TITLE",
        "HOUSE": "HOUSE",
        "HALL": "HALL",
        "BOSS": "NAME",
        "PET": 'PET'
    }

    results = []
    counter = 0
    for col_name, field in collections.items():
        col = db[col_name]
        result = col.find({field: {"$regex": f"^{str(search_string)}$", "$options": "i"}})
        if result:
            for r in result:
                if counter == 4:
                    break
                results.append({"TYPE": col_name, "DATA": r, "INDEX": counter})
                counter += 1

    # print(results)
    if results:
        return results
    else:
        return False

def viewQuerySearch(search_string):
    collections = {
        "CARDS": "NAME",
        "TITLES": "TITLE",
        "ARM": "ARM",
        "UNIVERSE": "TITLE",
        "HOUSE": "HOUSE",
        "HALL": "HALL",
        "BOSS": "NAME",
        "PET": 'PET'
    }

    results = []
    counter = 0
    for col_name, field in collections.items():
        col = db[col_name]
        result = col.find({field: {"$regex": f"^{str(search_string)}$", "$options": "i"}})
        if result:
            for r in result:
                if counter == 4:
                    break
                results.append({"TYPE": col_name, "DATA": r, "INDEX": counter})
                counter += 1

    if results:
        return results
    else:
        return False



'''Check if Collection Exists'''
def col_exists(col):
    collections = db.list_collection_names()
    if col in collections:
        return True
    else:
        return False




def queryAllAbyss():
    try:
        data = abyss_col.find()
        return data
    except:
        return False


def queryAbyss(query):
    try:
        data = abyss_col.find_one(query)
        return data
    except:
        return False

''' MENU '''
def menu_exists(data):
    collection_exists = col_exists("MENU")
    if collection_exists:
        menuexist = menu_col.find_one(data)
        if menuexist:
            return True
        else:
            return False
    else:
        return False


def queryAllMenu():
    try:
        data = menu_col.find()
        return data
    except:
        print("Find menu failed.")


def createMenu(menu):
    try:
        data = menu_col.insert_one(menu)
    except Exception as e:
        return e


def queryScenario(scenario):
    try:
        data = scenario_col.find_one(scenario)
        if data:
            return data
        else:
            return False
    except Exception as e:
        return e

def queryAllScenariosByUniverse(universe):
    try:
        data = scenario_col.find({'UNIVERSE': universe})
        if data:
            return data
        else:
            return False
    except Exception as e:
        return e
#########################################################################
''' SERVER '''
def createServer(server):
    try:
        data = server_col.insert_one(server)
        return True
    except Exception as e:
        return e

def queryServer(server):
    try:
        data = server_col.find_one(server)
        if data:
            return data
        else:
            return False
    except Exception as e:
        return e

def updateServer(server, new_server):
    try:
        data = server_col.update_one(server, new_server)
        return True
    except Exception as e:
        return e


#########################################################################
''' ARENA '''
def createArena(arena):
    try:
        data = arena_col.insert_one(arena)
        return True
    except Exception as e:
        return e

def queryArena(arena):
    try:
        data = arena_col.find_one(arena)
        if data:
            return data
        else:
            return False
    except Exception as e:
        return e

def updateArenaNoFilter(arena, arena_update):
    try:
        data = arena_col.update_one(arena, arena_update)
        return True
    except Exception as e:
        return e

def updateArena(query, new_value, arrayFilters):
    try:
        update = arena_col.update_one(query, new_value, array_filters=arrayFilters)
        return True
    except Exception as e:
        return e

#########################################################################
''' CODES '''
def queryCodes(query):
    try:
        response = codes_col.find_one(query)
        return response
    except Exception as e:
        return False

def createCode(query):
    try:
        response = codes_col.insert_one(query)
        return response
    except Exception as e:
        return e

def updateCode(query, new_value):
    try:
        response = codes_col.update_one(query, new_value)
        return response
    except Exception as e:
        return e

#########################################################################
''' GUILD '''
def guild_exists(data):
    collection_exists = col_exists("GUILD")
    if collection_exists:
        guild = guild_col.find_one(data)
        if guild:
            return True
        else:
            return False
    else:
        return False

def updateManyGuild(new_value):
    guild_col.update_many({}, new_value)
    return True

def queryGuild(guild):
    try:
        exists = guild_exists({'FDID': guild['FDID']})
        if exists:
            data = guild_col.find_one(guild)
            return data
        else:
           return False
    except:
        print("Find Association failed.")
        
def queryGuildAlt(guild):
    try:
        exists = guild_exists({'GNAME': guild['GNAME']})
        if exists:
            data = guild_col.find_one(guild)
            return data
        else:
           return False
    except:
        print("Find Association failed.")

def updateGuild(query, new_value):
    try:
        exists = guild_exists({'FDID': query['FDID']})
        if exists:
            data = guild_col.update_one(query, new_value)
            return data
        else:
           return False
    except:
        print("Find Association failed.")
        
def updateGuildAlt(query, new_value):
    try:
        exists = guild_exists({'GNAME': query['GNAME']})
        if exists:
            data = guild_col.update_one(query, new_value)
            return data
        else:
           return False
    except:
        print("Find Association failed.")

def queryAllGuild(guild):
    data = guild_col.find()
    return data

def createGuild(guild, user, name):
    guild_name = name
    
    try:
        find_user = queryUser({'DID': str(user.id)})
        
        if find_user['GUILD'] != 'PCG':
            return "User is already part of a Association. "
        else:
            exists = guild_exists({'FDID': guild['FDID']})
            if exists:
                return "Association already exists."
            else:
                print("Inserting new Association.")
                guild_col.insert_one(guild)

                # Add Guild to User Profile as well
                query = {'DID': str(user.id)}
                new_value = {'$set': {'GUILD': guild_name}}
                users_col.update_one(query, new_value)
                find_user = queryUser({'DID': str(user.id)})
                return f":flags: **{find_user['NAME']}** has founded the Association: **{find_user['GUILD']}** . "
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

def deleteGuild(guild, user):
    try:
        exists = guild_exists({'FDID': guild['FDID']})
        if exists:
            guild = guild_col.find_one(guild)
            if str(user.id) == guild['FDID']:
                users_col.update_many({'GUILD': guild['GNAME']}, {'$set': {'GUILD': 'PCG'}})
                teams_col.update_many({'GUILD': guild['GNAME']}, {'$set': {'GUILD': 'PCG'}})
                universe_col.update_many({'GUILD': guild['GNAME']}, {'$set': {'GUILD': 'PCG'}})
                guild_col.delete_one({'FDID': guild['FDID']})
                return f":flags: Association **{guild['GNAME']}** deleted."
            else:
                return "This user is not a member of the Association."
        else:
            return "Association does not exist."

    except:
        return "Delete Association failed."

def deleteGuildSworn(query, value, user, new_user):
    try:
        exists = guild_exists({'FDID': query['FDID']})
        if exists:
            guild = guild_col.find_one(query)
            if str(user.id) == guild['FDID']:
                update = guild_col.update_one(query, value, upsert=True)
                # Add Guild to User Profile as well
                query = {'DID': str(new_user.id)}
                new_value = {'$set': {'GUILD': 'PCG'}}
                users_col.update_one(query, new_value)
                find_user = queryUser({'DID': str(new_user.id)})
                return f":flags: **{find_user['NAME']}** has been removed from **{guild['GNAME']}**. "
            else:
                return "This user is not a member of the Association."
        else:
            return "Association does not exist."

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

def deleteGuildSwornAlt(query, value, user):
    try:
        exists = guild_exists({'FDID': query['FDID']})
        if exists:
            guild = guild_col.find_one(query)
            if str(user.id) == guild['WDID']:
                update = guild_col.update_one(query, value, upsert=True)
                # Add Guild to User Profile as well
                query = {'DID': str(user.id)}
                new_value = {'$set': {'GUILD': 'PCG'}}
                users_col.update_one(query, new_value)
                find_user = queryUser({'DID': str(user.id)})
                return f":flags: **{find_user['NAME']}** has been removed from **{guild['GNAME']}**."
            else:
                return "This user is not a member of the Association."
        else:
            return "Association does not exist."

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

def addGuildShield(query, add_to_guild_query, user, new_user):
    try:
        exists = guild_exists({'FDID': query['FDID']})
        if exists:
            guild = guild_col.find_one(query)
            if str(user.id) == guild['FDID'] or str(user.id) == guild['WDID']:
                guild_col.update_one(query, add_to_guild_query, upsert=True)

                # Add Guild to User Profile as well
                query = {'DID': str(new_user.id)}
                new_value = {'$set': {'GUILD': guild['GNAME']}}
                users_col.update_one(query, new_value)
                find_user = queryUser({'DID': str(new_user.id)})
                return f":flags: **{find_user['NAME']}** became the **Shield** of **{guild['GNAME']}**. "
            else:
                return "The Owner of the Association can add new members. "
        else:
            return "Cannot add user to the Association."
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

def addGuildSworn(query, add_to_guild_query, user, new_user):
    try:
        exists = guild_exists({'FDID': query['FDID']})
        if exists:
            guild = guild_col.find_one(query)
            if str(user.id) == guild['FDID']:
                guild_col.update_one(query, add_to_guild_query, upsert=True)

                # Add Guild to User Profile as well
                query = {'DID': str(new_user.id)}
                new_value = {'$set': {'GUILD': guild['GNAME']}}
                users_col.update_one(query, new_value)
                find_user = queryUser({'DID': str(new_user.id)})
                return f":flags: **{find_user['NAME']}** became the **Sworn** of **{guild['GNAME']}**. "
            else:
                return "The Owner of the Association can add new members. "
        else:
            return "Cannot add user to the Association."
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
    
def addGuildSword(query, add_to_guild_query, user, new_team):
    try:
        exists = guild_exists({'FDID': query['FDID']})
        if exists:
            guild = guild_col.find_one(query)
            if str(user.id) == guild['FDID'] or  str(user.id) == guild['WDID'] or str(user.id) == guild['SDID']:
                guild_col.update_one(query, add_to_guild_query, upsert=True)

                # Add Guild to Guild Profile as well
                query = {'TEAM_NAME': new_team.lower()}
                new_value = {'$set': {'GUILD': guild['GNAME']}}
                teams_col.update_one(query, new_value) 
                return f":flags: **{new_team}** enlisted as a {guild['GNAME']} **Sword**!. "
            else:
                return "The Leaders of Associations can add new members. "
        else:
            return "Cannot add user to the Association."
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
    
def deleteGuildSword(query, value, user, new_team):
    try:
        exists = guild_exists({'FDID': query['FDID']})
        if exists:
            guild = guild_col.find_one(query)
            if str(user.id) == guild['FDID'] or str(user.id) == guild['WDID'] or str(user.id) == guild['SDID']:
                update = guild_col.update_one(query, value, upsert=True)
                # Add Guild to User Profile as well
                query = {'TEAM_NAME': new_team}
                new_value = {'$set': {'GUILD': 'PCG'}}
                teams_col.update_one(query, new_value) 
                return f":flags: **{new_team}** renounced their oath to **{guild['GNAME']}**!."
            else:
                return "This user is not a member of the Association."
        else:
            return "Association does not exist."

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
        
def deleteGuildSwordAlt(query, value, new_team):
    try:
        exists = guild_exists({'GNAME': query['GNAME']})
        if exists:
            guild = guild_col.find_one(query)
            update = guild_col.update_one(query, value, upsert=True)
            # Add Guild to User Profile as well
            query = {'TEAM_NAME': new_team}
            new_value = {'$set': {'GUILD': 'PCG'}}
            teams_col.update_one(query, new_value) 
            return f":flags: **{new_team}** renounced their oath to **{guild['GNAME']}**!."
        else:
            return "Association does not exist."

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

########################################################################      
''' FAMILY '''
def family_exists(data):
    collection_exists = col_exists("FAMILY")
    if collection_exists:
        familyexists = family_col.find_one(data)
        if familyexists:
            return True
        else:
            return False
    else:
        return False

def updateManyFamily(new_value):
    family_col.update_many({}, new_value)
    return True

def queryFamily(family):
    try:
        exists = family_exists({'HEAD': family['HEAD']})
        if exists:
            data = family_col.find_one(family)
            return data
        else:
           return False
    except:
        print("Find family failed.")
        
def queryFamilyAlt(family):
    try:
        exists = family_exists({'PARTNER': family['PARTNER']})
        if exists:
            data = family_col.find_one(family)
            return data
        else:
           return False
    except:
        print("Find family failed.")

def updateFamily(query, new_value):
    try:
        exists = family_exists({'HEAD': query['HEAD']})
        if exists:
            data = family_col.update_one(query, new_value)
            return data
        else:
           return False
    except:
        print("Find family failed.")

def queryAllFamily(family):
    data = family_col.find()
    return data

def createFamily(family, user):
    try:
        find_user = queryUser({'DISNAME': user})
        exists = family_exists({'HEAD': family['HEAD']})
        if exists:
            return queryFamily({'HEAD': user})
        else:
            print("Inserting new Family.")
            family_col.insert_one(family)

            # Add Guild to User Profile as well
            query = {'DISNAME': user}
            new_value = {'$set': {'FAMILY': family['HEAD']}}
            users_col.update_one(query, new_value)
            return "Family has been created. "
    except:
        return "Cannot create Family."

def deleteFamily(family, user):
    try:
        exists = family_exists({'HEAD': family['HEAD']})
        if exists:
            family = family_col.find_one(family)
            if user == family['HEAD']:
                users_col.update_many({'FAMILY': family['HEAD']}, {'$set': {'FAMILY': 'PCG'}})
                family_col.delete_one({'HEAD': family['HEAD']})
                return "Family deleted."
            else:
                return "This user is not a member of the Family."
        else:
            return "Family does not exist."

    except:
        return "Delete Family failed."

def deleteFamilyMember(query, value, user, new_user):
    try:
        exists = family_exists({'HEAD': query['HEAD']})
        if exists:
            family = family_col.find_one(query)
            if user == family['HEAD']:
                update = family_col.update_one(query, value, upsert=True)
                # Add Guild to User Profile as well
                query = {'DISNAME': str(new_user)}
                new_value = {'$set': {'FAMILY': 'PCG'}}
                users_col.update_one(query, new_value)
                return "User has been removed from family. "
            else:
                return "This user is not a member of the family."
        else:
            return "Family does not exist."

    except:
        print("Delete Guild Member failed.")

def deleteFamilyMemberAlt(query, value, user):
    try:
        exists = family_exists({'HEAD': query['HEAD']})
        if exists:
            family = family_col.find_one(query)
            if user in family['KIDS']:
                update = family_col.update_one(query, value, upsert=True)
                # Add Guild to User Profile as well
                query = {'DISNAME': str(user)}
                new_value = {'$set': {'FAMILY': 'PCG'}}
                users_col.update_one(query, new_value)
                return "User has been removed from family. "
            else:
                return "This user is not a member of the family."
        else:
            return "Family does not exist."

    except:
        print("Delete Guild Member failed.")


def addFamilyMember(query, add_to_family_query, user, new_user):
    exists = family_exists({'HEAD': query['HEAD']})
    if exists:
        family = family_col.find_one(query)
        if user == family['HEAD']:
            family_col.update_one(query, add_to_family_query, upsert=True)

             # Add Guild to User Profile as well
            query = {'DISNAME': new_user}
            new_value = {'$set': {'FAMILY': family['HEAD']}}
            users_col.update_one(query, new_value)
            return "User added to the Family. "
        else:
            return "The Family Head & Partner can add new members. "
    else:
        return "Cannot add user to the Family."

def addFamilyMemberAlt(query, add_to_family_query, user, new_user):
    exists = family_exists({'PARTNER': query['PARTNER']})
    if exists:
        family = family_col.find_one(query)
        if user == family['PARTNER']:
            family_col.update_one(query, add_to_family_query, upsert=True)

             # Add Guild to User Profile as well
            query = {'DISNAME': new_user}
            new_value = {'$set': {'FAMILY': family['HEAD']}}
            users_col.update_one(query, new_value)
            return "User added to the Family. "
        else:
            return "The Family Head & Partner can add new members. "
    else:
        return "Cannot add user to the Family."
#########################################################################
''' MATCHES '''
def matches_exists(data):
    collection_exists = col_exists("MATCHES")
    if collection_exists:
        matchexists = matches_col.find_one(data)
        if matchexists:
            return True
        else:
            return False
    else:
        return False

def updateManyMatches(new_value):
    matches_col.update_many({}, new_value)
    return True

def queryMatch(matches):
    try:
        exists = matches_exists({'CARD': matches['CARD']})
        if exists:
            data = matches_col.find_one(matches)
            return data
        else:
           return False
    except:
        print("Find matches failed.")

def queryManyMatches(matches):
    try:
        exists = matches_exists({'CARD': matches['CARD']})
        if exists:
            data = matches_col.find(matches)
            return data
        else:
           return False
    except:
        print("Find matches failed.")

def queryManyMatchesPerPlayer(matches):
    try:
        exists = matches_exists({'PLAYER': matches['PLAYER']})
        if exists:
            data = matches_col.find(matches)
            return data
        else:
           return False
    except:
        print("Find matches failed.")

def queryAllMatches(matches):
    data = matches_col.find()
    return data

def createMatch(match):
    resp = matches_col.insert_one(match)
    if resp:
        return True
    else:
        return False

#########################################################################
'''Check If User Exists'''
def user_exists(data):
    collection_exists = col_exists("USERS")
    if collection_exists:
        user_does_exist = users_col.find_one(data)
        if user_does_exist:
            return True
        else:
            return False
    else:
        return False

'''Check If Vault exist'''
def vault_exist(data):
    collection_exists = col_exists("VAULT")
    if collection_exists:
        vault_does_exist = vault_col.find_one(data)
        if vault_does_exist:
            return True
        else:
            return False
    else:
        return False

def updateManyVaults(new_value):
    vault_col.update_many({}, new_value)
    return True

'''New Vault'''
def createVault(vault):
    try:
        vault_col.insert_one(vault)
    except:
        return "Cannot create vault."

def queryAllVault():
    data = vault_col.find()
    return data

def queryVault(query):
    data = vault_col.find_one(query)
    return data


def altQueryVault(query):
    data = vault_col.find_one(query)
    return data

'''Delete Vault'''
def deleteVault(query):
    try:
        vault_col.delete_one(query)
        return True
    except:
        return False

def updateVault(query, new_value, arrayFilters):
    try:
        update = vault_col.update_one(query, new_value, array_filters=arrayFilters)
        return True
    except Exception as e:
        return False

'''Update Vault With No Array Filters'''
def updateVaultNoFilter(query, new_value):
    try:
        update = vault_col.update_one(query, new_value)
        return True
    except Exception as e:
        return False


def gods_exists(data):
    collection_exists = col_exists("GODS")
    if collection_exists:
        gods_does_exist = gods_col.find_one(data)
        if gods_does_exist:
            return True
        else:
            return False
    else:
        return False

def createGods(query):
    try:
        response = gods_col.insert_one(query)
        return "Gods Created. "
    except:
        return False

def queryGods(query):
    response = gods_col.find_one(query)
    return response

def deleteGods(query):
    response = gods_col.delete_one(query)
    return response

def updateGods(query, new_value):
    exists = gods_exists(query)
    if exists:
        data = gods_col.update_one(query, new_value)
    else:
        return m.TOURNEY_DOES_NOT_EXIST

def addTeamMember(query, add_to_team_query, user, new_user):
    exists = team_exists({'TEAM_NAME': query['TEAM_NAME']})
    if exists:
        team = teams_col.find_one(query)
        teams_col.update_one(query, add_to_team_query, upsert=True)

            # Add Guild to User Profile as well
        query = {'DISNAME': new_user}
        new_value = {'$set': {'TEAM': team['TEAM_NAME']}}
        users_col.update_one(query, new_value)
        return "User added to the Guild. "
    else:
        return "Cannot add user to the Guild."


'''Check If Card Exists'''
def card_exists(data):
    collection_exists = col_exists("CARDS")
    if collection_exists:
        card_does_exist = cards_col.find_one(data)
        if card_does_exist:
            return True
        else:
            return False
    else:
        return False

'''New Card'''
def createCard(card):
    try:
        cardexists = card_exists({'PATH': card['PATH']})
        if cardexists:
            return "Card already exists."
        else:
            cards_col.insert_one(card)
            return "New Card created."
    except:
        return "Cannot create card."

def queryAllCards():
    data = cards_col.find()
    return data

def queryAllCardsBasedOnUniverse(query):
    data = cards_col.find(query)
    return data

def queryTournamentCards():
    data = cards_col.find({'TOURNAMENT_REQUIREMENTS': {'$gt': 0}, 'AVAILABLE': True})
    return data

def queryShopCards():
    data = cards_col.find({'EXCLUSIVE': False, 'AVAILABLE': True, 'HAS_COLLECTION': False})
    return data 

def altQueryShopCards(args):
    data = cards_col.find({'EXCLUSIVE': False, 'AVAILABLE': True, 'HAS_COLLECTION': False})
    return data 

def querySkins(args):
    data = cards_col.find({'SKIN_FOR': args, 'HAS_COLLECTION': False, 'AVAILABLE': True, 'IS_SKIN': True})
    return data 

def queryDungeonCards():
    data = cards_col.find({'AVAILABLE': True, 'HAS_COLLECTION': False, 'EXCLUSIVE': True})
    return data 

def queryDestinyCards():
    data = cards_col.find({'HAS_COLLECTION': True})
    return data 

def queryDropCards(args):
    data = cards_col.find({'UNIVERSE': args, 'EXCLUSIVE': False, 'AVAILABLE': True, 'HAS_COLLECTION': False, 'IS_SKIN': False,'TIER': {'$in': acceptable}})
    return data 

def querySpecificCards(args):
    try:
        data = cards_col.find({'NAME': {'$in': args}})
        return data 
    except Exception as e:
        return False

def querySpecificTitles(args):
    try:
        data = titles_col.find({'TITLE': {'$in': args}})
        return data 
    except Exception as e:
        return False
    
def querySpecificArms(args):
    try:
        data = arm_col.find({'ARM': {'$in': args}})
        return data 
    except Exception as e:
        return False
   

def querySpecificDropCards(args):
    data = cards_col.find({'UNIVERSE': args, 'AVAILABLE': True, 'HAS_COLLECTION': False, 'VUL': False})
    return data 

def queryExclusiveDropCards(args):
    data = cards_col.find({'UNIVERSE': args, 'EXCLUSIVE': True, 'AVAILABLE': True, 'HAS_COLLECTION': False, 'IS_SKIN': False, 'TIER': {'$in': acceptable}})
    return data 

def queryCard(query):
    data = cards_col.find_one(query)
    return data

def updateCardWithFilter(query, new_value, arrayFilters):
    try:
        update = cards_col.update_one(query, new_value, array_filters=arrayFilters)
        return True
    except:
        return False

def updateCard(query, new_value):
    try:
        cards_col.update_one(query, new_value)
        return True
    except:
        return False

def updateManyCards(new_value):
    cards_col.update_many({}, new_value)
    return True


def deleteCard(card):
    try:
        cardexists = card_exists({'PATH': card['PATH']})
        if cardexists:
            cards_col.delete_one(card)
            return True
        else:
            return False
    except:
        return False


''' TITLES '''
def title_exists(data):
    collection_exists = col_exists("TITLES")
    if collection_exists:
        title_does_exist = titles_col.find_one(data)
        if title_does_exist:
            return True
        else:
            return False
    else:
        return False

def createTitle(title):
    try:
        titleexists = title_exists({'TITLE': title['TITLE']})
        if titleexists:
            return "Title already exists."
        else:
            titles_col.insert_one(title)
            return "New Title created."
    except:
        return "Cannot create Title."

def updateTitle(query, new_value):
    try:
        titleexists = title_exists({'TITLE': query['TITLE']})
        if titleexists:
            titles_col.update_one(query, new_value)
            return True
        else:
            return False
    except:
        return False

def updateTitleWithFilter(query, new_value, arrayFilters):
    try:
        update = titles_col.update_one(query, new_value, array_filters=arrayFilters)
        return True
    except:
        return False

def updateManyTitles(new_value):
    titles_col.update_many({}, new_value)
    return True

def deleteTitle(title):
    try:
        titleexists = title_exists({'TITLE': title['TITLE']})
        if titleexists:
            titles_col.delete_one(title)
            return True
        else:
            return False
    except:
        return False

def deleteAllTitles(user_query):
    exists = user_exists({'DISNAME': user_query['DISNAME']})
    if exists:
        titles_col.delete_many({})
        return 'All Titles Deleted'
    else:
        return 'Unable to Delete All Titles'

def queryAllTitles():
    data = titles_col.find()
    return data

def queryAllTitlesBasedOnUniverses(query):
    data = titles_col.find(query)
    return data

def queryTitle(query):
    data = titles_col.find_one(query)
    return data

def queryDropTitles(args):
    data = titles_col.find({'UNIVERSE': args, 'EXCLUSIVE': False, 'AVAILABLE': True})
    return data 

def queryExclusiveDropTitles(args):
    data = titles_col.find({'UNIVERSE': args, 'EXCLUSIVE': True, 'AVAILABLE': True})
    return data 

def queryTournamentTitles():
    data = titles_col.find({'TOURNAMENT_REQUIREMENTS': {'$gt': 0}, 'AVAILABLE': True})
    return data

def queryShopTitles():
    data = titles_col.find({'EXCLUSIVE': False, 'AVAILABLE': True})
    return data 



''' ARM '''
def arm_exists(data):
    collection_exists = col_exists("ARM")
    if collection_exists:
        arm_does_exist = arm_col.find_one(data)
        if arm_does_exist:
            return True
        else:
            return False
    else:
        return False

def createArm(arm):
    try:
        armexists = arm_exists({'ARM': arm['ARM']})
        if armexists:
            return "ARM already exists."
        else:
            arm_col.insert_one(arm)
            return "New ARM created."
    except:
        return "Cannot create ARM."

def updateArm(query, new_value):
    try:
        armexists = arm_exists({'ARM': query['ARM']})
        if armexists:
            arm_col.update_one(query, new_value)
            return True
        else:
            return False
    except:
        return False

def updateArmWithFilter(query, new_value, arrayFilters):
    try:
        update = arm_col.update_one(query, new_value, array_filters=arrayFilters)
        return True
    except:
        return False

def updateManyArms(new_value):
    arm_col.update_many({}, new_value)
    return True

def deleteArm(query):
    try:
        armexists = arm_exists({'ARM': query['ARM']})
        if armexists:
            arm_col.delete_one(query)
            return True
        else:
            return False
    except:
        return False

def queryAllArms():
    data = arm_col.find()
    return data

def queryAllArmsBasedOnUniverses(query):
    data = arm_col.find(query)
    return data

def queryArm(query):
    data = arm_col.find_one(query)
    if data is None:
        return False
    else:
        return data



def queryDropArms(args):
    data = arm_col.find({'UNIVERSE': args, 'EXCLUSIVE': False, 'AVAILABLE': True})
    return data 

def queryExclusiveDropArms(args):
    data = arm_col.find({'UNIVERSE': args, 'EXCLUSIVE': True, 'AVAILABLE': True})
    return data 

def queryTournamentArms():
    data = arm_col.find({'TOURNAMENT_REQUIREMENTS': {'$gt': 0}, 'AVAILABLE': True})
    return data

def queryShopArms():
    data = arm_col.find({'EXCLUSIVE': False, 'AVAILABLE': True})
    return data 

''' HALL '''
def hall_exist(data):
    collection_exists = col_exists("HALL")
    if collection_exists:
        hall_does_exist = hall_col.col.find_one(data)
        if hall_does_exist:
            return True
        else:
            return False
    else:
        return False

def createHall(hall):
    try:
        hallexists = hall_exist({'HALL': hall['HALL']})
        if hallexists:
            return "HALL already exists."
        else:
            hall_col.insert_one(hall)
            return "New HALL created."
    except:
        return "Cannot create HALL."

def updateHall(query, new_value):
    try:
        hallexists = hall_exist({'HALL': query['HALL']})
        if hallexists:
            hall_col.update_one(query, new_value)
            return True
        else:
            return False
    except:
        return False

def updateManyHalls(new_value):
    hall_col.update_many({}, new_value)
    return True

def deleteHall(query):
    try:
        hallexists = hall_exist({'HALL': query['HALL']})
        if hallexists:
            hall_col.delete_one(query)
            return True
        else:
            return False
    except:
        return False

def queryAllHalls():
    data = hall_col.find()
    return data


def queryHall(query):
    data = hall_col.find_one(query)
    return data


''' HOUSE '''
def house_exist(data):
    collection_exists = col_exists("HOUSE")
    if collection_exists:
        house_does_exist = house_col.col.find_one(data)
        if house_does_exist:
            return True
        else:
            return False
    else:
        return False

def createHouse(house):
    try:
        houseexists = house_exist({'HOUSE': house['HOUSE']})
        if houseexists:
            return "HOUSE already exists."
        else:
            house_col.insert_one(house)
            return "New HOUSE created."
    except:
        return "Cannot create HOUSE."

def updateHouse(query, new_value):
    try:
        houseexists = house_exist({'HOUSE': query['HOUSE']})
        if houseexists:
            house_col.update_one(query, new_value)
            return True
        else:
            return False
    except:
        return False

def updateManyHouses(new_value):
    house_col.update_many({}, new_value)
    return True

def deleteHouse(query):
    try:
        houseexists = house_exist({'HOUSE': query['HOUSE']})
        if houseexists:
            house_col.delete_one(query)
            return True
        else:
            return False
    except:
        return False

def queryAllHouses():
    data = house_col.find()
    return data


def queryHouse(query):
    data = house_col.find_one(query)
    return data


''' PETS '''
def pet_exists(data):
    collection_exists = col_exists("PET")
    if collection_exists:
        pet_does_exist = pet_col.find_one(data)
        if pet_does_exist:
            return True
        else:
            return False
    else:
        return False

def createPet(pet):
    try:
        petexists = pet_exists({'PET': pet['PET']})
        if petexists:
            return "Pet already exists."
        else:
            pet_col.insert_one(pet)
            return "New Pet created."
    except:
        return "Cannot create Pet."

def updatePet(query, new_value):
    try:
        petexists = pet_exists({'PET': query['PET']})
        if petexists:
            pet_col.update_one(query, new_value)
            return True
        else:
            return False
    except:
        return False

def updateManyPets(new_value):
    pet_col.update_many({}, new_value)
    return True

def deletePet(pet):
    try:
        petexists = pet_exists({'PET': pet['PET']})
        if petexists:
            pet_col.delete_one(pet)
            return True
        else:
            return False
    except:
        return False

def deleteAllPet(pet_query):
    exists = pet_exists({'PET': pet_query['PET']})
    if exists:
        pet_col.delete_many({})
        return 'All Pets Deleted'
    else:
        return 'Unable to Delete All Pets'

def queryAllPets():
    data = pet_col.find()
    return data

def queryPet(query):
    data = pet_col.find_one(query)
    return data

def queryDropPets(args):
    data = pet_col.find({'UNIVERSE': args,  'EXCLUSIVE': False,  'AVAILABLE': True})
    return data 

def queryExclusiveDropPets(args):
    data = pet_col.find({'UNIVERSE': args, 'EXCLUSIVE': True, 'AVAILABLE': True})
    return data 

def queryAllPetsBasedOnUniverses(query):
    data = pet_col.find(query)
    return data


''' UNIVERSE '''
def universe_exists(data):
    collection_exists = col_exists("UNIVERSE")
    if collection_exists:
        universe_does_exist = universe_col.find_one(data)
        if universe_does_exist:
            return True
        else:
            return False
    else:
        return False

def updateManyUniverses(new_value):
    universe_col.update_many({}, new_value)
    return True

def createUniverse(universe):
    try:
        universeexists = universe_exists({'TITLE': universe['TITLE']})
        if universeexists:
            return "Universe already exists."
        else:
            universe_col.insert_one(universe)
            return "New Universe created."
    except:
        return "Cannot create Universe."

def updateUniverse(query, new_value):
    try:
        universe_col.update_one(query, new_value)
        return True
    except:
        return False

def deleteUniverse(query):
    try:
        universeexists = universe_exists({'TITLE': query['TITLE']})
        if universeexists:
            universe_col.delete_one(query)
            return True
        else:
            return False
    except:
        return False

def queryCorruptedUniverse():
    try:
        data = universe_col.find_one({"CORRUPTED": True})
        if data:
            return data
        else:
            return False
    except Exception as e:
        return False

def queryAllUniverse():
    data = universe_col.find({"HAS_CROWN_TALES": True})
    return data


def queryTaleAllUniverse():
    data = universe_col.find({"HAS_CROWN_TALES": True})
    return data


def queryTaleUniversesNotRift():
    data = universe_col.find({"HAS_CROWN_TALES": True, "TIER": {"$nin": [9]}})

    return data


def queryDungeonAllUniverse():
    data = universe_col.find({"HAS_DUNGEON": True})
    return data


def queryDungeonUniversesNotRift():
    data = universe_col.find({"HAS_DUNGEON": True, "TIER": {"$nin": [9]}})

    return data


def queryAvailableUniverse():
    data = universe_col.find({"AVAILABLE": True})
    return data

def queryExploreUniverses():
    data = universe_col.find({"HAS_CROWN_TALES": True, "HAS_DUNGEON": True})
    return data

def queryUniverse(query):
    try:
        data = universe_col.find_one(query)
        return data
    except:
        return False


''' BOSS '''
def boss_exists(data):
    collection_exists = col_exists("BOSS")
    if collection_exists:
        boss_does_exist = boss_col.find_one(data)
        if boss_does_exist:
            return True
        else:
            return False
    else:
        return False

def updateManyBosses(new_value):
    boss_col.update_many({}, new_value)
    return True

def createBoss(boss):
    try:
        bossexists = boss_exists({'NAME': boss['NAME']})
        if bossexists:
            return "Boss already exists."
        else:
            boss_col.insert_one(boss)
            return "New Boss created."
    except:
        return "Cannot create Boss."

def updateBoss(query, new_value):
    try:
        bossexists = boss_exists({'NAME': query['NAME']})
        if bossexists:
            boss_col.update_one(query, new_value)
            return True
        else:
            return False
    except:
        return False

def deleteBoss(query):
    try:
        bossexists = boss_exists({'NAME': query['NAME']})
        if bossexists:
            boss_col.delete_one(query)
            return True
        else:
            return False
    except:
        return False

def queryAllBosses():
    data = boss_col.find()
    return data

def queryBoss(query):
    data = boss_col.find_one(query)
    return data



'''Query User'''
def queryUser(user):
    try:
        data = users_col.find_one(user)
        if data:
            return data
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
        return False

def queryAllUsers():
    data = users_col.find()
    return data

def createUsers(users):
    exists = user_exists({'DID': users['DID']})
    if exists:
        return False
    else:
        data = users_col.insert_one(users)
        return True
    
def deleteUser(user):
    try:
        users_col.delete_one({'DISNAME': user})
        return "User removed from the system. "
    except:
        print("Delete User failed.")

def updateUser(query, new_value, arrayFilters):
    try:
        update = users_col.update_one(query, new_value, array_filters=arrayFilters)
        return "Update completed. "
    except:
        return False

def updateUserNoFilter(query, new_value):
    try:
        update = users_col.update_one(query, new_value)
        return "Update completed. "
    except:
        return False

    
def updateUserNoFilterAlt(query, new_value):
    try:
        update = users_col.update_one(query, new_value)
        return "Update completed. "
    except:
        return False

def updateManyUsers(new_value):
    users_col.update_many({}, new_value)
    return True



''' TEAMS '''
def team_exists(data):
    collection_exists = col_exists("TEAMS")
    if collection_exists:
        teamexists = teams_col.find_one(data)
        if teamexists:
            return True
        else:
            return False
    else:
        return False

def updateManyTeams(new_value):
    teams_col.update_many({}, new_value)
    return True

def queryTeam(team):
    try:
        exists = team_exists({'TEAM_NAME': team['TEAM_NAME'].lower()})
        if exists:
            data = teams_col.find_one(team)
            return data
        else:
            return False
    except:
        return False

def updateTeam(query, new_value):
    try:
        data = teams_col.update_one(query, new_value)
        if data:
            return data
        else:
           return False
    except:
        print("Find Guild failed.")

def updateTeamWithFilter(query, new_value, arrayFilter):
    try:
        data = teams_col.update_one(query, new_value, array_filters=arrayFilter)
        if data:
            print("hi")
            return data
        else:
           return False
    except:
        print("Find Guild failed.")

def queryAllTeams(team):
    data = teams_col.find()
    return data

def createTeam(team, user):
    try:
        find_user = queryUser({'DID': user})
        if find_user['TEAM'].lower and find_user['TEAM'] != 'PCG':
            return "You're already in a Guild"
        else:
            exists = team_exists({'TEAM_NAME': team['TEAM_NAME']})
            if exists:
                return False
            else:
                teams_col.insert_one(team)

                # Add Guild to User Profile as well
                query = {'DID': user}
                new_value = {
                    '$set': {'TEAM': team['TEAM_DISPLAY_NAME']},
                    '$inc': {'MEMBER_COUNT': 1}
                    }
                users_col.update_one(query, new_value)
                return "Guild has been successfully created. "
    except:
        return "Cannot create Guild."

def deleteTeam(team, user):
    try:
        exists = team_exists({'TEAM_NAME': team['TEAM_NAME']})
        if exists:
            team = teams_col.find_one(team)
            users_col.update_many({'TEAM': team['TEAM_DISPLAY_NAME']}, {'$set': {'TEAM': "PCG"}})
            teams_col.delete_one({'TEAM_NAME': team['TEAM_NAME']})
            return f"**{team['TEAM_DISPLAY_NAME']}** has been deleted."

        else:
            return "Guild does not exist."

    except:
        return "Delete Guild failed."

def deleteTeamMember(query, value, user):
    try:
        exists = team_exists({'TEAM_NAME': query['TEAM_NAME']})
        if exists:
            team = teams_col.find_one(query)
            update = teams_col.update_one(query, value, upsert=True)
            
            
            # Remove user guild and make it PCG
            user_query = {'DID': str(user)}
            new_value = {'$set': {'TEAM': 'PCG'}}
            users_col.update_one(user_query, new_value)
            return f"You've successfully left **{team['TEAM_DISPLAY_NAME']}**"
        else:
            return "Guild does not exist."

    except:
        print("Delete Guild Member failed.")

def addTeamMember(query, add_to_team_query, user, new_user):
    exists = team_exists({'TEAM_NAME': query['TEAM_NAME']})
    if exists:
        team = teams_col.find_one(query)

        teams_col.update_one(query, add_to_team_query, upsert=True)

        # Add Guild to User Profile as well
        query = {'DISNAME': new_user}
        new_value = {'$set': {'TEAM': team['TEAM_DISPLAY_NAME']}}
        users_col.update_one(query, new_value)
        return "User added to the Guild. "

    else:
        return "Cannot add user to the Guild."

def game_exists(game):
    collection_exists = col_exists("GAMES")
    if collection_exists:
        gamesexist = games_col.find_one(game)
        if gamesexist:
            return True
        else:
            return False
    else:
        return False

def updateManyGames(new_value):
    games_col.update_many({}, new_value)
    return True



''' GAMES '''
def queryGame(game):
    try:
        exists = game_exists({'ALIASES': game['ALIASES']})
        if exists:
            data = games_col.find_one(game)
            return data
        else:
            return False
    except:
        return False

def deleteGame(game):
    try:
        exists = game_exists({'GAME': game['GAME']})
        if exists:
            data = games_col.delete_one(game)
            return True
        else:
            return False
    except:
        print("Find Game failed.")

def query_all_games():
    games = games_col.find()
    if games:
        return games
    else:
        return False

def addGame(game):
    exists = game_exists({'GAME': game['GAME']})
    if exists:
        print("Game Already Exists.")
    else:
       added = games_col.insert_one(game)
       return("Game has been added")

def updateGame(query, new_value):
    exists = game_exists({'GAME': query['GAME']})
    if exists:
       added = games_col.update_one(query, new_value)
       return("Game has been added")
    else:
        return False


''' SESSIONS '''
def session_exist(data):
    collection_exists = col_exists("SESSIONS")
    if collection_exists:
        sessionexists = sessions_col.find_one(data)
        if sessionexists:
            return True
        else:
            return False
    else:
        return False

def querySession(session):
    try:
        exists = session_exist({'OWNER': session['OWNER'], 'AVAILABLE': True})
        if exists:
            data = sessions_col.find_one(session)
            return data
        else:
            return False
           
    except:
        return "Find Session failed."

def querySessionForUser(query):
    data = sessions_col.find(query)
    return data
   
def querySessionMembers(session):
    data = sessions_col.find_one(session)
    return data

def createSession(session):
    exists = session_exist({'OWNER': session['OWNER'], 'AVAILABLE': True})
    if exists:
        return m.ALREADY_IN_SESSION
    else:
        if session['GAME'] == "Crown Unlimited":
            response = sessions_col.insert_one(session)
            return response
        else:
            if len(session['TEAMS']) == 0:
                sessions_col.insert_one(session)
                return "New Lobby has been created"
            elif session['TOURNAMENT']:
                sessions_col.insert_one(session)
                return "New Tournament Session has been created"
            else:       
                players_per_team_count = [x for x in session['TEAMS'][0]['TEAM']]
                print(players_per_team_count)
                print(session['TYPE'])
                if session['TYPE'] != len(players_per_team_count):

                    return "Guild and Session Type do not match. "
                else:
                    sessions_col.insert_one(session)
                    return "New Session started. "

def joinSession(session, query):
    sessionquery = querySession(session)
    matchtype = sessionquery['TYPE']
    if not sessionquery['IS_FULL']:
        if sessionquery['GODS'] and query['POSITION'] == 0:
            teaminsert = sessions_col.update_one(session, {'$addToSet': {'TEAMS': query}})
            return m.SESSION_JOINED
        elif query['POSITION'] == 0:
            teaminsert = sessions_col.update_one(session, {'$addToSet': {'TEAMS': query}})
            return m.SESSION_JOINED
        else:
            if matchtype == len(query['TEAM']):
                # List of current teams in session
                p = [x for x in sessionquery['TEAMS']]
                
                # Check if Guild trying to join is part of a Guild already
                list_matching = [x for x in p[0]['TEAM'] if x in query['TEAM']]

                if len(list_matching) == 0:
                    teaminsert = sessions_col.update_one(session, {'$addToSet': {'TEAMS': query}, '$set': {'IS_FULL': True}})

                    return m.SESSION_JOINED
                else: 
                    return 'Lobby full.'
            elif matchtype < len(query['TEAM']):
                return 'Too many players in Guild'
            elif matchtype > len(query['TEAM']):
                return 'Not enough players in Guild'
    else:
        return "Lobby is full. "

def joinExhibition(session, query):
    sessionquery = querySession(session)
    matchtype = sessionquery['TYPE']
    if len(query['TEAM']) != 3:
        if len(query['TEAM']) != 1:       
            # List of current teams in session
            p = [x for x in sessionquery['TEAMS']]
            
            # Check if Guild trying to join is part of a Guild already
            list_matching = [x for x in p[0]['TEAM'] if x in query['TEAM']]

            if len(list_matching) == 0:
                teaminsert = sessions_col.update_one(session, {'$addToSet': {'TEAMS': query}, '$set': {'IS_FULL': True}})

                return m.SESSION_JOINED
            else: 
                return 'Session full.'
        else:
            teaminsert = sessions_col.update_one(session, {'$addToSet': {'TEAMS': query}})
            return m.SESSION_JOINED

def joinKingsGambit(session, query):
    sessionquery = querySession(session)
    matchtype = sessionquery['TYPE']
    if len(query['TEAM']) != 3:
        if len(query['TEAM']) != 1:       
            # List of current teams in session
            p = [x for x in sessionquery['TEAMS']]
            
            # Check if Guild trying to join is part of a Guild already
            list_matching = [x for x in p[0]['TEAM'] if x in query['TEAM']]

            if len(list_matching) == 0:
                teaminsert = sessions_col.update_one(session, {'$addToSet': {'TEAMS': query}})

                return m.SESSION_JOINED
            else: 
                return m.LOBBY_IS_FULL
        else:
            teaminsert = sessions_col.update_one(session, {'$addToSet': {'TEAMS': query}})
            return m.SESSION_JOINED

def endSession(session):
    exists = session_exist({'OWNER': session['OWNER'], 'AVAILABLE': True})
    if exists:
        sessions_col.update_one(session, {'$set': {'AVAILABLE': False}})
        return m.SESSION_HAS_ENDED
    else:
        return m.SESSION_DOES_NOT_EXIST

def deleteSession(session):
    exists = session_exist({'OWNER': session['OWNER'], 'AVAILABLE': True})
    if exists:
        sessions_col.delete_one({'OWNER': session['OWNER'], 'AVAILABLE': True})
        return m.SESSION_HAS_ENDED
    else:
        return m.SESSION_DOES_NOT_EXIST

def deleteAllSessions(user_query):
    exists = user_exists({'DISNAME': user_query['DISNAME']})
    if exists:
        sessions_col.delete_many({})
        return 'All Sessions Deleted'
    else:
        return 'Unable to Delete All Sessions'

def updateSession(session, query, update_query):
    exists = session_exist({'OWNER': session['OWNER'], 'AVAILABLE': True})
    if exists:
        sessions_col.update_one(query, update_query)
        return True
    else:
        return False




''' KINGS GAMBIT '''
def updatekg(session, query, update_query, arrayFilter):
    exists = session_exist({'OWNER': session['OWNER'], 'AVAILABLE': True, "KINGSGAMBIT": True})
    if exists:
        sessions_col.update_one(query, update_query,  array_filters=arrayFilter)
        return True
    else:
        return False
    
    
''' TRADES '''
def trade_exists(data):
    collection_exists = col_exists("TRADE")
    print(collection_exists)
    if collection_exists:
        trade_does_exist = trade_col.find_one(data)
        if trade_does_exist:
            return True
        else:
            return False
    else:
        return False

def updateManyTrade(new_value):
    trade_col.update_many({}, new_value)
    return True

def createTrade(trade):
    try:
        tradeexists = trade_exists({'MDID': trade['MDID'], 'BDID': trade['BDID'], 'OPEN': trade['OPEN']})
        if tradeexists:
            return "Trade already exists."
        else:
            trade_col.insert_one(trade)
            return trade
    except:
        return "Cannot create Trade."

def updateTrade(trade_query, new_value):
    try:
        trade_col.update_one(trade_query, new_value)
        return True
    except:
        return False

def deleteTrade(query):
    try:
        tradeexists = trade_exists({'MDID': query['MDID'], 'BDID': query['BDID'], 'OPEN': query['OPEN']})
        if tradeexists:
            trade_col.delete_one(query)
            return True
        else:
            return False
    except:
        return False

def queryAllTrade():
    data = trade_col.find()
    return data

def queryTrade(query):
    try:
        data = trade_col.find_one(query)
        return data
    except:
        return False