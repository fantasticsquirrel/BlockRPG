metadata = Hash()
mobdata = Hash()
moblocations = Hash()
moblocationcounts = Hash()
random.seed()

@construct
def seed():
    metadata['operator'] = ctx.caller
    metadata['map_contract'] = 'con_rpg_map'
    metadata['c_list'] = ["con_battles"]

@export
def change_metadata(key: str, new_value: str):
    assert ctx.caller == metadata['operator'], "Only the operator can set metadata."
    metadata[key] = new_value

@export
def new_mob_type(type : str, MS : int, MD : int, RS : int, RD : int, HP : int):

    mobdata[type]={
        "MS": MS,
        "MD": MD,
        "RS": RS,
        "RD": RD,
        "HP": HP
    }

    mobdata[type,"count"] = 0


def new_mob_apply_stats(type):

    count = mobdata[type,"count"]
    count += 1

    stats = mobdata[type]

    mobdata[type, count, "stats", "MS"] = stats["MS"]
    mobdata[type, count, "stats", "MD"] = stats["MD"]
    mobdata[type, count, "stats", "RS"] = stats["RS"]
    mobdata[type, count, "stats", "RD"] = stats["RD"]
    mobdata[type, count, "stats", "HP"] = stats["HP"]

    mobdata[type, count, "alive"] = True
    mobdata[type,"count"] = count

    ct = [count, type]
    return ct

@export
def new_mob_random(type : str):

    ct = new_mob_apply_stats(type)
    map_contract = metadata['map_contract']
    map = ForeignHash(foreign_contract=map_contract, foreign_name='map')
    row = random.randint(0, map['maxrc'])
    column = random.randint(0, map['maxrc'])

    moblocations[ct[0] , ct[1]] = [row , column]

    if moblocationcounts[row , column] == None:
        moblocationcounts[row , column] =1
    else:
        moblocationcounts[row , column] +=1

@export
def lotsa_mobs(type : str , num : int):
    m = 0
    while m <= num:
        new_mob_random (type)
        m+=1

@export
def change_stats(type : str, count : int, stat : str, amount : int): #this is a simple function to change the stats of a mob. the conditions to change the stat will come from the functions or contracts calling it
    assert ctx.caller in metadata['c_list'], "You can't change stats."
    mobstat = mobdata[type, count, "stats", stat] += amount
    mobstat += amount
    if stat == "HP" and mobstat <= 0:
        amount = 0
        mobdata[type, count, "alive"] = False
        loc = moblocations[type , count]
        moblocations[type , count] = False
        moblocationcounts[loc[0] , loc[1]] -=1

    mobdata[type, count, "stats", stat] = amount
