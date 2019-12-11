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
attr = []
ins = []
#######################
f3 = open('SuperHeroDataset.csv')
dreader = csv.DictReader(f3,delimiter = ',' )
 

 
for i in dreader:
    attr.append(i)
     
f3.close()
eye_set = set()  
hair_set = set()
#insert_heros = "insert into heroes (name,race,eye_color,skin_color,Height,Weight) values ('{}','{}',{},'{}','{}',{},{},{},{},{},{},{},{});\n"
insert_heros = "insert into heroes (name,race,Gender,eye_color,skin_color,Height,Weight,Intellect,Strength,Speed,Durability,Power,Combat) values ('{}','{}','{}',{},'{}','{}',{},{},{},{},{},{},{});\n"

for i in attr:
    inte = i['Intelligence']
    stre = i['Strength']
    speed = i['Speed']
    power = i['Power']
    combat = i['Combat']
    dura = i['Durability']
    name = i['Name']
      
        
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
        race = i['Race'].lower()
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

    ins.append(insert_heros.format(name,race.lower(),Gender.lower(),eye_color.lower(),skin_color.lower(),height,weight,inte,stre,speed,dura,power,combat))
    
f = open(filewrite,"w")
for x in ins:
    f.write(x)

f.close()
#######################

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
    rand_mat.append(np.random.uniform(0.75, 1.25, size = (200, 6)))
    day.append(rand_mat[i] @ strats[:,i])

i = 0
for thehero in hero:
    hero[thehero]['stat/day'] = day[i]
    i += 1

f = open(filewrite,"a")
for thehero1 in hero:
    for thehero2 in hero:
        if thehero1 < thehero2:
            #f.write("%s vs %s: %.2f%% chance of winning\n" % (thehero1, thehero2, np.sum(hero[thehero1]['stat/day'] > hero[thehero2]['stat/day']) / 30 * 100))
            f.write("INSERT INTO fights (hero1, hero2, wins1, wins2, tie) VALUES ('%s', '%s', %i, %i, %i);\n" % (thehero1, thehero2, np.sum(hero[thehero1]['stat/day'] > hero[thehero2]['stat/day']), np.sum(hero[thehero1]['stat/day'] < hero[thehero2]['stat/day']), np.sum(hero[thehero1]['stat/day'] == hero[thehero2]['stat/day'])))
f.close()









