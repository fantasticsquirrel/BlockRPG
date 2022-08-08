metadata = Hash()
mobdata = Hash()
moblocations = Hash()
random.seed()

@construct
def seed():
    metadata['operator'] = ctx.caller
    metadata['map_contract'] = 'con_rpg_map'

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

    mobdata[type, count, "stats"]={
        "MS": stats["MS"],
        "MD": stats["MD"],
        "RS": stats["RS"],
        "RD": stats["RD"],
        "HP": stats["HP"]
    }

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

    moblocations[row , column , ct[0] , ct[1]] = True
    if moblocations[row , column , "count"] == None:
        moblocations[row , column , "count"] =1
    else:
        moblocations[row , column , "count"] +=1

@export
def lotsa_mobs(type : str , num : int):
    m = 0
    while m <= num:
        new_mob_random (type)
        m+=1
