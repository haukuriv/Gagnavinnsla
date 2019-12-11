# -*- coding: utf-8 -*-
import csv
import numpy as np
import time
# fall til að lesa inn og fá einstök gildi úr hverjum dálk

def import_file(fileread, delimiter):
    f = open(fileread)
    
    dreader = csv.DictReader(f, delimiter=delimiter)
    
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
    
    return data, var_set


start = time.time()

fileread = 'SuperheroDataset.csv'
filewrite = 'insertstatements.txt'

data, var_set = import_file(fileread, ',')
data2, var_set2 = import_file('super_hero_powers.csv', ',') 


del_me = set() # Þær ofurhetjur sem hafa ekki stats

#del_me.update(set(var_set['Name']).symmetric_difference(var_set1['hero_names']))

stat_str = sorted(['Intelligence','Strength','Speed','Durability','Power','Combat'])
join_super = sorted(list(set(var_set['Name']).intersection(var_set2['hero_names'])))
# Upphafsstilla
hero = {}

for thehero in join_super:#var_set['Name']:
    hero[thehero] = {}
    hero[thehero]['powers'] = []
    for thestat in stat_str:
        hero[thehero][thestat] = ''
         
del_me = set()
               
for d in data:
    if d['Name'] in join_super:
        for thekey in d.keys():
            if thekey in stat_str and d[thekey] == '':
                del_me.add(d['Name'])
            elif thekey in stat_str:
                hero[d['Name']][thekey] = d[thekey]

for thehero in del_me:
    del hero[thehero]



Upowers = list(data2[0].keys())
Upowers = sorted(Upowers[1:])

for d in data2:
    if d['hero_names'] in hero.keys():
        for thekey in d.keys():
            if d[thekey] == 'True' and thekey != 'hero_names':
                hero[d['hero_names']]['powers'].append(thekey)


strats = np.zeros( (6, len(hero)) )

j = 0
for thehero in hero:
    i = 0
    for thestrat in hero[thehero]:
        if thestrat != 'powers':
            strats[i, j] = hero[thehero][thestrat]
            i += 1
    j += 1

nr_fights = 10000
rand_mat = []
day = []
for i in range(len(hero)):
    np.random.seed(i)
    rand_mat.append(np.random.uniform(0.5, 1.25, size = (nr_fights, 6)))
    day.append(rand_mat[i] @ strats[:,i])

i = 0
for thehero in hero:
    hero[thehero]['stat/day'] = day[i]
    i += 1

f = open(filewrite,"w")
for thehero1 in hero:
    for thehero2 in hero:
        if thehero1 < thehero2:
            #f.write("%s vs %s: %.2f%% chance of winning\n" % (thehero1, thehero2, np.sum(hero[thehero1]['stat/day'] > hero[thehero2]['stat/day']) / nr_fights * 100))
            f.write("INSERT INTO fights (hero1, hero2, nrwon1, nrwon2, tie) VALUES (%i, %i, %i, %i, %i);\n" % (join_super.index(thehero1)+1, join_super.index(thehero2)+1, np.sum(hero[thehero1]['stat/day'] > hero[thehero2]['stat/day']), np.sum(hero[thehero1]['stat/day'] < hero[thehero2]['stat/day']), np.sum(hero[thehero1]['stat/day'] == hero[thehero2]['stat/day'])))

i = 1
for thepower in Upowers:
    f.write("INSERT INTO powers (id, power) VALUES (%i, '%s');\n" % (i, thepower))
    i += 1

i = 1
for thehero in hero:
    for thepower in hero[thehero]['powers']:
        f.write("INSERT INTO link_power (id, hero_id, power_id) VALUES (%i, %i, %i);\n" % (i, join_super.index(thehero)+1, Upowers.index(thepower)+1))
        i += 1

f.close()





print('\nIt took %.2f seconds to run the code.' % (time.time()-start))


















