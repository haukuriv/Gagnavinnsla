#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 10:23:03 2019

@author: gunnarhak
"""

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
#        tmp = ''
        
        for keys in d.keys():
#            if d[keys] == tmp:
#                num = '1'
#                d[keys] = d[keys] + num
            var_set[keys].add(d[keys])
            #tmp = d[keys]
    
    
    for thekey in var_set.keys():
        var_set[thekey] = sorted(list(var_set[thekey]))
    
    return data, var_set


start = time.time()

fileread = 'SuperheroDataset.csv'
filewrite = 'insertstatements.sql'

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


all_supers = list(hero.keys())
##############################################################################


# Upphafsstilla
attr = []
ins = []
#######################
##attr, var_set3 = import_file('SuperHeroDataset.csv', ',') 
#f3 = open('SuperHeroDataset.csv')
#dreader = csv.DictReader(f3,delimiter = ',' )
#
#
#
#for i in dreader:
#    attr.append(i)
#
#f3.close()
eye_set = set()  
hair_set = set()
#insert_heros = "insert into heroes (name,race,eye_color,skin_color,Height,Weight) values ('{}','{}',{},'{}','{}',{},{},{},{},{},{},{},{});\n"
insert_heros = "INSERT INTO supers (id, name, race, gender, eye_color, hair_color, skin_color, publisher, alignment, height, weight, intelligence, strength, speed, durability, power, combat)\nVALUES ({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {}, {});\n"


dup = ''

for i in data:

    
    if i['Name'] in hero.keys():
        the_id = all_supers.index(i['Name'])+1
        name = i['Name'].replace("'",'')
        if dup == i['Name']:
            continue
        
        inte = i['Intelligence']
        stre = i['Strength']
        speed = i['Speed']
        power = i['Power']
        combat = i['Combat']
        dura = i['Durability']
        
    
    
        if i['Weight'] !='-':
            if ' kg' in i['Weight'].split('//')[1]:
                weight = i['Weight'].split('//')[1].strip(' kg')
                if ',' in weight:
                    weight=weight.replace(',','')
    
                weight = float(weight)
            if ' tons' in i['Weight'].split('//')[1]:
                weight = i['Weight'].split('//')[1].strip(' tons')
                if ',' in weight:
                    weight=weight.replace(',','')
    
                weight = float(weight)*1000
        else: 
            weight = 'None'
    
        if i['Height'] !='-':
            if ' cm' in i['Height'].split('//')[1]:
                height = i['Height'].split('//')[1].strip(' cm')
                if ',' in height:
                    height=height.replace(',','')
                height = float(height)
    
            if ' meters' in i['Height'].split('//')[1]:
                height = i['Height'].split('//')[1].strip(' meters')
                if ',' in height:
                    height=height.replace(',','')
                height = float(height)*100
        else:
            height = 'None'
    
            ###### 
    
        if i['Skin color'] != '-':
            skin_color = i['Skin color'].lower()
        else:
            skin_color = 'none'
    
        if i['Race'] != '-':
            race = i['Race'].replace("'",'').lower()

        else:
            race = 'none'
    
        if i['Eye color'] != '-':    
            if i['Eye color'] == 'Bown' or i['Eye color'] == 'bown':
                eye_color = 'brown'
            else:
                eye_color = i['Eye color'].lower()
        else:
            eye_color = 'none'
    
        if i['Gender'] != '-':
            Gender = i['Gender'].lower()
        else:
            Gender = 'none'
        if i['Hair color'] !='-':
            if i['Hair color'] == 'brownn' or i['Hair color'] == 'Brownn':
                hair = 'brown'
            else:
                hair = i['Hair color'].lower()
        else:
            hair = 'none'
    
        eye_set.add(eye_color)
        hair_set.add(hair)
        dup = i['Name']
        if i['Creator'] != '':
            publisher = i['Creator']
        else:
            publisher = 'None'
            
        if i['Alignment'] != '-':
            alignment = i['Alignment']
        else:
            alignment = 'None'
    
        ins.append(insert_heros.format(the_id, name,race.lower(),Gender.lower(),eye_color.lower(),hair.lower(),skin_color.lower(),publisher.lower(),alignment.lower(),height,weight,inte,stre,speed,dura,power,combat))


###############################################################################
    
f = open(filewrite,"w")

for x in ins:
    f.write(x)
    

bla = []
for thehero1 in hero:
    for thehero2 in hero:
        if thehero1 < thehero2:
            #f.write("%s vs %s: %.2f%% chance of winning\n" % (thehero1, thehero2, np.sum(hero[thehero1]['stat/day'] > hero[thehero2]['stat/day']) / nr_fights * 100))
            f.write("INSERT INTO fights (super1_id, super2_id, wins1, wins2, tie) VALUES (%i, %i, %i, %i, %i);\n" % (all_supers.index(thehero1)+1, all_supers.index(thehero2)+1, np.sum(hero[thehero1]['stat/day'] > hero[thehero2]['stat/day']), np.sum(hero[thehero1]['stat/day'] < hero[thehero2]['stat/day']), np.sum(hero[thehero1]['stat/day'] == hero[thehero2]['stat/day'])))

for thepower in Upowers:
    f.write("INSERT INTO powers (power) VALUES ('%s');\n" % thepower)

i = 1
for thehero in hero:
    for thepower in hero[thehero]['powers']:
        f.write("INSERT INTO link_power (id, super_id, power_id) VALUES (%i, %i, %i);\n" % (i, all_supers.index(thehero)+1, Upowers.index(thepower)+1))
        i += 1

f.close()


print('\nIt took %.2f seconds to run the code.' % (time.time()-start))