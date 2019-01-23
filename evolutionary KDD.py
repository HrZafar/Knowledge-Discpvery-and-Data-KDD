import random
import csv

relation = ['<', '>', '=']
total_attr = int(input('Total Attributes = '))
attr = list(range(total_attr))
type = list(range(total_attr))
upper_bound = list(range(total_attr))
lower_bound = list(range(total_attr))
values = {}
print('Enter Attributes Name, Type and bounds')
for i in range(total_attr):
    print(i + 1, ':')
    attr[i] = input('Name: ')
    type[i] = input('Type: ')
    if type[i] == 'int' or type[i] == 'float':
        lower_bound[i] = int(input('Lower bound: '))
        upper_bound[i] = int(input('Upper bound: '))
    elif type[i] == 'binary':
        lower_bound[i] = 0
        upper_bound[i] = 1
    elif type[i] == 'nominal':
        no = int(input('No. of values: '))
        val = []
        lower_bound[i] = 0
        upper_bound[i] = no - 1
        print('enter values for ', attr[i], ':')
        for j in range(no):
            val.append(input())
        values[attr[i]] = val

print('')
print('Attributes:')
for i in range(len(attr)):
    if type[i] == 'int' or type[i] == 'float' or type[i] == 'binary':
        print(i + 1, 'Name:', attr[i], ' Type:', type[i], ' Bounds: (', lower_bound[i], ',', upper_bound[i], ')')
    elif type[i] == 'nominal':
        print(i + 1, 'Name:', attr[i], ' Type:', type[i], ' Values:', values[attr[i]])
print('')


def binary_tournament(list):
    p1_1 = random.randint(0, len(list) - 1)
    p1_2 = random.randint(0, len(list) - 1)
    while p1_1 == p1_2:
        p1_2 = random.randint(0, len(list) - 1)
    if list[p1_1]['fitness'] > list[p1_2]['fitness']:
        p1 = p1_1
    else:
        p1 = p1_2
    p2_1 = random.randint(0, len(list) - 1)
    p2_2 = random.randint(0, len(list) - 1)
    while p2_1 == p2_2:
        p2_2 = random.randint(0, len(list) - 1)
    if list[p2_1]['fitness'] > list[p2_2]['fitness']:
        p2 = p2_1
    else:
        p2 = p2_2
    while p1 == p2:
        p1, p2 = binary_tournament(list)
    return p1, p2


def fitness(rule):
    fit = 0
    with open('heart_disease data.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        firstline = True
        for row in readCSV:
            cond = True
            i = 0
            if firstline == True:
                firstline = False
            else:
                while cond == True and i < len(rule['attr']):
                    x = (row[rule['attr'][i]])
                    if x == '?':
                        x = 0
                    if type[rule['attr'][i]] == 'int' or type[rule['attr'][i]] == 'binary':
                        x = int(x)
                    elif type[rule['attr'][i]] == 'float':
                        x = float(x)
                    if relation[rule['rel'][i]] == '<':
                        if rule['func'][i] == 0:
                            if not (x < rule['val'][i]):
                                cond = False
                        else:
                            if x < rule['val'][i]:
                                cond = False
                    elif relation[rule['rel'][i]] == '>':
                        if rule['func'][i] == 0:
                            if not (x > rule['val'][i]):
                                cond = False
                        else:
                            if x > rule['val'][i]:
                                cond = False
                    elif relation[rule['rel'][i]] == '=':
                        if type[rule['attr'][i]] != 'nominal':
                            if rule['func'][i] == 0:
                                if not (x == rule['val'][i]):
                                    cond = False
                            else:
                                if x == rule['val'][i]:
                                    cond = False
                        else:
                            if rule['func'][i] == 0:
                                if not (x == values[attr[rule['attr'][i]]][rule['val'][i]]):
                                    cond = False
                            else:
                                if x == values[attr[rule['attr'][i]]][rule['val'][i]]:
                                    cond = False
                    i += 1
                if cond == True:
                    if int(row[-1]) == rule['goal']:
                        fit += 1
                elif cond == False:
                    if int(row[-1]) != rule['goal']:
                        fit += 1
    return fit


def mutation(child):
    probability = random.randint(1, 100)
    if probability > 25:
        rel = random.randint(0, len(child['rel']) - 1)
        if type[child['attr'][rel]] == 'nominal':
            child['rel'][rel] = 2
        else:
            child['rel'][rel] = random.randint(0, len(relation) - 1)
        val = random.randint(0, len(child['val']) - 1)
        if type[child['attr'][val]] == 'int' or type[child['attr'][val]] == 'nominal' or type[
            child['attr'][val]] == 'binary':
            child['val'][val] = random.randint(lower_bound[child['attr'][val]], upper_bound[child['attr'][val]])
        else:
            child['val'][val] = random.uniform(lower_bound[child['attr'][val]], upper_bound[child['attr'][val]])
        func = random.randint(0, len(child['func']) - 1)
        fun = random.randint(0, 100)
        if fun > 75:
            fun = 1
        else:
            fun = 0
        child['func'][func] = fun
    return child


def crossover(p1, p2):
    ch = {}
    attr = []
    rel = []
    val = []
    func = []
    if len(p1['attr']) < 2 or len(p1['attr']) < 2:
        return p2, p1
    point = int((min(len(p1['attr']), len(p2['attr'])) + 1) / 2)
    i = 0
    while len(attr) < len(p2['attr']):
        check = 0
        if i < point:
            attr.append(p1['attr'][i])
            rel.append(p1['rel'][i])
            val.append((p1['val'][i]))
            func.append(p1['func'][i])
        else:
            for j in range(len(attr)):
                if attr[j] == p2['attr'][i]:
                    check = 1
            if check == 0:
                attr.append(p2['attr'][i])
                rel.append(p2['rel'][i])
                val.append((p2['val'][i]))
                func.append(p2['func'][i])
        i += 1
        if i == len(p2['attr']) and len(attr) < len(p2['attr']):
            i = 0
            point = 0
    ch['attr'] = attr
    ch['rel'] = rel
    ch['val'] = val
    ch['func'] = func
    ch['goal'] = p1['goal']
    ch = mutation(ch)
    ch['fitness'] = fitness(ch)
    return ch


def gen_childs(generation, n):
    list = []
    l = len(generation[0])
    for i in range(int(n / 2)):
        p1, p2 = binary_tournament(generation)
        a = crossover(generation[p1], generation[p2])
        if len(a) != l:
            a = a[0]
        list.append(a)
        b = crossover(generation[p2], generation[p1])
        if len(b) != l:
            b = b[0]
        list.append(b)
    return list


def gen_individuals(n):
    list = []
    for i in range(n):
        dict = {}
        rel = []
        val = []
        func = []
        size = random.randint(4, total_attr)
        dict['attr'] = random.sample(range(0, total_attr), size)
        for j in range(size):
            if type[dict['attr'][j]] == 'nominal':
                r = 2
            else:
                r = random.randint(0, len(relation) - 1)
            rel.append(r)
        dict['rel'] = rel
        for j in range(size):
            if type[dict['attr'][j]] == 'int' or type[dict['attr'][j]] == 'nominal' or type[
                dict['attr'][j]] == 'binary':
                v = random.randint(lower_bound[dict['attr'][j]], upper_bound[dict['attr'][j]])
            else:
                v = random.uniform(lower_bound[dict['attr'][j]], upper_bound[dict['attr'][j]])
            val.append(v)
        dict['val'] = val
        for j in range(size):
            fun = random.randint(0, 100)
            if fun > 75:
                fun = 1
            else:
                fun = 0
            func.append(fun)
        dict['func'] = func
        dict['goal'] = random.randint(0, 1)
        dict['fitness'] = fitness(dict)
        list.append(dict)
    return list


def g_best(gen):
    best = {'fitness': 0}
    for i in range(len(gen)):
        if best['fitness'] < gen[i]['fitness']:
            best = gen[i]
    return best


pop_size = 30
gen_size = 50
g_bests = []
generation = gen_individuals(pop_size)
print(generation)
g_bests.append(g_best(generation))
for i in range(gen_size - 1):
    childs = gen_childs(generation, pop_size)
    generation_1 = generation + childs
    generation = []
    for k in range(int(pop_size / 2)):
        p1, p2 = binary_tournament(generation_1)
        generation.append(generation_1[p1])
        generation.append(generation_1[p2])
    g_bests.append(g_best(generation))
for i in range(len(g_bests)):
    print(i, g_bests[i]['fitness'], g_bests[i])
show = g_bests[-1]
function = ['AND', 'AND NOT']
print('')
for i in range(len(show['attr'])):
    if type[show['attr'][i]] != 'nominal':
        if show['func'][i] == 1:
            if i == 0:
                print('IF NOT (', attr[show['attr'][i]], relation[show['rel'][i]], show['val'][i], ')')
            else:
                print(function[1], '(', attr[show['attr'][i]], relation[show['rel'][i]], show['val'][i], ')')
        else:
            if i == 0:
                print('IF (', attr[show['attr'][i]], relation[show['rel'][i]], show['val'][i], ')')
            else:
                print(function[0], '(', attr[show['attr'][i]], relation[show['rel'][i]], show['val'][i], ')')
    else:
        if show['func'][i] == 1:
            if i == 0:
                print('IF NOT (', attr[show['attr'][i]], relation[show['rel'][i]],
                      values[attr[show['attr'][i]]][show['val'][i]], ')')
            else:
                print(function[1], '(', attr[show['attr'][i]], relation[show['rel'][i]],
                      values[attr[show['attr'][i]]][show['val'][i]], ')')
        else:
            if i == 0:
                print('IF (', attr[show['attr'][i]], relation[show['rel'][i]],
                      values[attr[show['attr'][i]]][show['val'][i]], ')')
            else:
                print(function[0], '(', attr[show['attr'][i]], relation[show['rel'][i]],
                      values[attr[show['attr'][i]]][show['val'][i]], ')')
print('THEN ( goal =', show['goal'], ')')
