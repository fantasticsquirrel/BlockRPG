metadata = Hash()
data = Hash(default_value=0)
map = Hash(default_value=0)


random.seed()

@construct
def seed():
    metadata['operator'] = ctx.caller

    metadata['terrains'] = ['fields', 'forests', 'hills', 'mountains', 'canyons', 'swamps', 'lakes']

@export
def new_map(grid_size : int = 10):

    caller = ctx.caller
    terrainlist = metadata['terrains']
    grid = []

    g = 0
    while g < grid_size:
        grid.append(g)
        g += 1

    for x in grid:
        y = 0
        while y < grid_size:
            map[ x , y ] = True
            map[ x , y , "terrain"] = terrainlist[random.randint(0,6)]
            y += 1
        x += 1

    map['maxrc'] = grid_size - 1

@export
def adjacent_check(row : int, column : int): #enter row and column of zone you want to attack
    zone = data[conquest_id , 'map' , row , column ]
    assert zone['Owner'] != ctx.caller, 'You own this territory and cannot attack it.'

    zoneup    = data[conquest_id , 'map' , row , column - 1]
    zonedown  = data[conquest_id , 'map' , row , column + 1]
    zoneleft  = data[conquest_id , 'map' , row - 1, column]
    zoneright = data[conquest_id , 'map' , row + 1, column]
    assert zoneup['Owner'] or zonedown['Owner'] or zoneleft['Owner'] or zoneright['Owner'] == ctx.caller, 'You cannot attack this territory since you do not own an adjacent territory.'

    #add check to make sure the zone you're attacking is attackable


def gen_rnd_int(int_sum, n):
    mean = int_sum / n
    variance = int(0.5 * mean)

    min_v = mean - variance
    max_v = mean + variance
    array = [min_v] * n

    diff = int_sum - min_v * n
    while diff > 0:
        a = random.randint(0, n - 1)
        if array[a] >= max_v:
            continue
        array[a] += 1
        diff -= 1
    return array










metadata = Hash()
random.seed()

@construct
def seed():
    metadata['operator'] = ctx.caller
    metadata['test'] = ['a' , 'b' , 'c' , 'd' , 'e' , 'f' , 'g' , 'h' , 'i' , 'j' , 'k' , 'l' , 'm' , 'n' , 'o' , 'p' , 'q' , 'r' , 's' , 't' , 'u' , 'v' , 'w' , 'x' , 'y' , 'z']

@export
def test1():
    testlist = metadata['test']
    return testlist[random.randint(0, 25)]

@export
def test2():
    testlist2 = ['a' , 'b' , 'c' , 'd' , 'e' , 'f' , 'g' , 'h' , 'i' , 'j' , 'k' , 'l' , 'm' , 'n' , 'o' , 'p' , 'q' , 'r' , 's' , 't' , 'u' , 'v' , 'w' , 'x' , 'y' , 'z']
    return testlist2[random.randint(0, 25)]
