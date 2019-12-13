import csv
import numpy as np
import time

start = time.time()

# fall til að lesa inn og fá einstök gildi úr hverjum dálk

def import_file(fileread, delimiter):
    # Les inn gögnin
    f = open(fileread)
    
    dreader = csv.DictReader(f, delimiter=delimiter)
    
    data = []
    for d in dreader:
        data.append(d)
    
    f.close()
    
    # Finna unique gildi fyrir alla lykla
    var_set = {}
    # Bý til lyklana fyrir dictionary hér
    for keys in data[0].keys():
        var_set[keys] = set()
    # Keyri í gegnum öll gögnin til að taka saman öll gögn og finna einstök gildi fyrir alla lykla
    for d in data:
        for keys in d.keys():
            var_set[keys].add(d[keys])
    # Breyti breytunum innan lyklanna yfir í lista og raða þeim í stafrófsröð svo það sé þægilegra að skoða handvirkt
    for thekey in var_set.keys():
        var_set[thekey] = sorted(list(var_set[thekey]))
    
    return data, var_set

fileread1 = 'SuperheroDataset.csv'
fileread2 = 'super_hero_powers.csv'
filewrite = 'insertstatements.sql'

data, var_set = import_file(fileread1, ',')
data2, var_set2 = import_file(fileread2, ',') 

# Lyklar fyrir bardagastuðlana
stat_str = sorted(['Intelligence','Strength','Speed','Durability','Power','Combat'])

# Finnum sameiginlegar hetjur milli beggja gagnasafnanna
join_super = sorted(list(set(var_set['Name']).intersection(var_set2['hero_names'])))

# Upphafsstilla hetju dictionary-ið með öllum þeim hetjum sem gagnasöfnin eiga sameiginlegt
hero = {}
for thehero in join_super:
    hero[thehero] = {}
    hero[thehero]['powers'] = []
    for thestat in stat_str:
        hero[thehero][thestat] = ''
         
# Bý til þessa breyta til að eyða þeim hetjum seinna meir sem hafa ekki bardagastuðla
del_me = set() # Þær ofurhetjur sem hafa ekki stats

# Keyri í gegnum allt gagnasafnið til að bæta við öllum bardagastuðlum
for d in data:
    if d['Name'] in join_super:
        for thekey in d.keys():
            if thekey in stat_str and d[thekey] == '':
                del_me.add(d['Name'])
            elif thekey in stat_str:
                hero[d['Name']][thekey] = d[thekey]

# Eyði út þeim ofurhetjum sem hafa ekki bardagastuðla
for thehero in del_me:
    del hero[thehero]


# Upphafsstilli bardagastuðla fylkið
strats = np.zeros( (6, len(hero)) )

# Keyri í gegnum bardagastuðlanna hjá hverri hetju og fylli inní "strats" fylkið
j = 0
for thehero in hero:
    i = 0
    for thestrat in hero[thehero]:
        if thestrat != 'powers':
            strats[i, j] = hero[thehero][thestrat]
            i += 1
    j += 1

nr_fights = 10000 # fasti fyrir fjölda bardaga
rand_mat = [] # Upphafsstilla handhófskenndu vægin fyrir bardagastuðlana
day = [] # Upphafsstilla fylkið sem mun innihalda útreikninga frá bardagamódelinu
for i in range(len(hero)):
    np.random.seed(i)
    rand_mat.append(np.random.uniform(0.5, 1.25, size = (nr_fights, 6)))
    day.append(rand_mat[i] @ strats[:,i])

# Bæti inn niðurstöðunum úr bardagamódelinu við dictionary-ið
i = 0
for thehero in hero:
    hero[thehero]['stat/day'] = day[i]
    i += 1


# Einstakur listi yfir alla ofurkrafta úr gagnasafninu - Verður notað seinna til að skrifa in "INSERT" skipanir fyrir SQL
Upowers = list(data2[0].keys())
Upowers = sorted(Upowers[1:])

for d in data2:
    if d['hero_names'] in hero.keys():
        for thekey in d.keys():
            if d[thekey] == 'True' and thekey != 'hero_names':
                hero[d['hero_names']]['powers'].append(thekey)

# Listi yfir allar ofurhetjur sem bæði gagnasöfnin hafa sameiginlegt og hafa bardagastuðla
all_supers = list(hero.keys())

##############################################################################


# Upphafsstilla
ins = []
eye_set = set()  
hair_set = set()
########## Eye og hair setinn voru  notuð til að sjá ef stafsetningar villur voru í gagnasettinu sjálfu.



insert_heros = "INSERT INTO supers (id, name, race, gender, eye_color, hair_color, skin_color, publisher, alignment, height, weight, intelligence, strength, speed, durability, power, combat)\nVALUES ({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {}, {});\n"


dup = ''    # Nota þennan til að tjekka á duplicates í nafna listanum 
            # Sumir voru með mismunandi attributes og stundum voru þeir tómir, þanning að ákveðið var að 
            # taka fyrsta með stats og dumpa rest af duplicates.

for i in data:

    if i['Name'] in hero.keys():                                                #  Ef nafnið á hetjunni finnst inni þessum lista þá má halda áfram, hann var skilgreindur 
                                                                                # með það í huga að innihalda bara nöfn á þeim sem INNIHALDA statsa.        
        the_id = all_supers.index(i['Name'])+1
        name = i['Name'].replace("'",'')                                        # Sér tilvik, fengum  "Ra's Al Ghul"  og ' var að valda usla og eyddum kommunni.
        
        if dup == i['Name']:                                                    #Ef duplicate er true þá er bara haldið áfram
            continue
        
        inte = i['Intelligence']
        stre = i['Strength']
        speed = i['Speed']
        power = i['Power']
        combat = i['Combat']
        dura = i['Durability']                                                  # Pumpa statsa inn 
        
    
    ###########################################################
        if i['Weight'] !='-':
            if ' kg' in i['Weight'].split('//')[1]:                             # Splitta  á //, þar sem við fáum þetta sem t.d.  "XX lbs // YY kg"  
                weight = i['Weight'].split('//')[1].strip(' kg')                # Strippa kg
                if ',' in weight:
                    weight=weight.replace(',','')                               # ef komma, dump it, þar sem það verður vesen með að hafa breyta yfir i float
    
                weight = float(weight)
            if ' tons' in i['Weight'].split('//')[1]:                           # Splitta  á //, þar sem við fáum þetta sem t.d.  "XX lbs // YY tons" 
                weight = i['Weight'].split('//')[1].strip(' tons')              # Strippa kg
                if ',' in weight:
                    weight=weight.replace(',','')                               # ef komma, dump it, þar sem það verður vesen með að hafa breyta yfir i float
    
                weight = float(weight)*1000                                     # Viljum hafa þetta í kg en ekki tonnum
        else: 
            weight = 'N/A'
   ###########################################################
        if i['Height'] !='-':
            if ' cm' in i['Height'].split('//')[1]:                             # Sama pæling herna og fyrir ofan
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
            height = 'N/A'
   ###########################################################                  
    
        if i['Skin color'] != '-':
            skin_color = i['Skin color'].lower()
        else:
            skin_color = 'N/A'
    
        if i['Race'] != '-':
            race = i['Race'].replace("'",'').lower()                            # Sér tilvik, fengum  "yoda's species"  og ' var að valda usla.
                                                                                # Lögum það með að eyða kommunni út. 
                                                                                # Mætti segja að við værum kommunistar

        else:
            race = 'N/A'
    
        if i['Eye color'] != '-':    
            if i['Eye color'] == 'Bown' or i['Eye color'] == 'bown':            # Bown er ekki litur, laga það með if setningu á þeim stöðum sem það á við.
                eye_color = 'brown'
            else:
                eye_color = i['Eye color'].lower()
        else:
            eye_color = 'N/A'
    
        if i['Gender'] != '-':
            Gender = i['Gender'].lower()
        else:
            Gender = 'N/A'
            
        if i['Hair color'] !='-':
            if i['Hair color'] == 'brownn' or i['Hair color'] == 'Brownn':      # bara eitt n í brown, laga það með if setningu á þeim stöðum sem það á við.
                hair = 'brown'
            else:
                hair = i['Hair color'].lower()
        else:
            hair = 'N/A'

        dup = i['Name']                                                         # Dup breytan assignuð uppá duplicates eins og nefnt var áðan
        if i['Creator'] != '':
            publisher = i['Creator'].lower()
        else:
            publisher = 'N/A'
            
        if i['Alignment'] != '-':
            alignment = i['Alignment'].lower()
        else:
            alignment = 'N/A'                                                   # N/A var alltaf assignað ef ekkert gildi fannst. 
    
        ins.append(insert_heros.format(the_id, name,race,Gender,eye_color,hair,skin_color,publisher,alignment,height,weight,inte,stre,speed,dura,power,combat))

print('\nÞað tók %.2f sek að keyra kóðann.' % (time.time()-start))
###############################################################################

start = time.time()

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


print("\nÞað tók %.2f sek að skrifa inn í 'insertstatements.sql'." % (time.time()-start))