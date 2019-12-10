import csv
import numpy as np

# Lesa inn gögnin
fileread = 'super_hero_powers.csv'
fileread = 'heroes_information.csv'
fileread = 'SuperheroDataset.csv'
filewrite = 'insertstatements.txt'
f = open(fileread)

dreader = csv.DictReader(f, delimiter=',')

data = []
for d in dreader:
    data.append(d)

f.close()

# Finna unique gildi fyrir alla lykla
var_set = {}

for keys in data[0].keys():
    var_set[keys] = set()

for d in data:
    for keys in d.keys():
        var_set[keys].add(d[keys])


for thekey in var_set.keys():
    var_set[thekey] = sorted(list(var_set[thekey]))


del_me = set() # Þær ofurhetjur sem hafa ekki stats

stat_str = sorted(['Intelligence','Strength','Speed','Durability','Power','Combat'])

# Upphafsstilla
hero = {}

for thehero in var_set['Name']:
    hero[thehero] = {}
    for thestat in stat_str:
        hero[thehero][thestat] = ''

for d in data:
    for thekey in d.keys():
        if thekey in stat_str:
            if d[thekey] == '':
                del_me.add(d['Name'])
            hero[d['Name']][thekey] = d[thekey]

for thehero in del_me:
    del hero[thehero]
    del var_set['Name'][var_set['Name'].index(thehero)]

strats = np.zeros( (6, len(hero)) )
#for thehero in var_set['Name']:

j = 0
for thehero in hero:
    i = 0
    for thestrat in hero[thehero]:
        strats[i, j] = hero[thehero][thestrat]
        i += 1
    j += 1


rand_mat = []
day = []
for i in range(len(hero)):
    np.random.seed(i)
    rand_mat.append(np.random.uniform(0.5, 1.25, size = (30, 6)))
    day.append(rand_mat[i] @ strats[:,i])

i = 0
for thehero in hero:
    hero[thehero]['stat/day'] = day[i]
    i += 1

f = open(filewrite,"w")
for thehero1 in hero:
    for thehero2 in hero:
        if thehero1 < thehero2:
            #f.write("%s vs %s: %.2f%% chance of winning\n" % (thehero1, thehero2, np.sum(hero[thehero1]['stat/day'] > hero[thehero2]['stat/day']) / 30 * 100))
            f.write("INSERT INTO fights (hero1, hero2, nrwon1, nrwon2, tie) VALUES ('%s', '%s', %i, %i, %i);\n" % (thehero1, thehero2, np.sum(hero[thehero1]['stat/day'] > hero[thehero2]['stat/day']), np.sum(hero[thehero1]['stat/day'] < hero[thehero2]['stat/day']), np.sum(hero[thehero1]['stat/day'] == hero[thehero2]['stat/day'])))
f.close()



