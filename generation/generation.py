import random

width, height = 64, 64
level = ['0'] * height

for i in range(height):
    level[i] = ['□'] * width

start = random.randint(0, height - 1)
level[start][0] = '*'
ind1 = 0
ind2 = start
sp = ['U'] * 5 + ['D'] * 5 + ['R'] * 6
sp1 = [['U'] * 20 + ['D'] * 4 + ['R'] * 4 + ['L'] * 4,
       ['U'] * 20 + ['D'] * 4 + ['R'] * 4 + ['L'] * 4,
       ['U'] * 4 + ['D'] * 20 + ['R'] * 6 + ['L'] * 4,
       ['U'] * 4 + ['D'] * 20 + ['R'] * 4 + ['L'] * 6]

last = ''
path = []
while ind1 != width - 1:
    r = random.choice(sp)
    if r == 'R':
        ind1 += 1
        level[ind2][ind1] = '■'
        path.append((ind2, ind1))
        last = ''
    elif r == 'D' and ind2 != height - 1 and last != 'U':
        ind2 += 1
        level[ind2][ind1] = '■'
        path.append((ind2, ind1))
        last = 'D'
    elif r == 'U' and ind2 != 0 and last != 'D':
        ind2 -= 1
        level[ind2][ind1] = '■'
        path.append((ind2, ind1))
        last = 'U'

del path[-1]
sub_paths = []

level[ind2][ind1] = '*'

for i in range(64):
    if i > 5:
        start = random.choice([random.choice(path),
                               random.choice(sub_paths),
                               random.choice(sub_paths),
                               random.choice(sub_paths),
                               random.choice(sub_paths),
                               random.choice(sub_paths),
                               random.choice(sub_paths),
                               random.choice(sub_paths),
                               random.choice(sub_paths),
                               random.choice(sub_paths)])
    else:
        start = random.choice(path)

    ind2, ind1 = start

    cur_sp = random.choice(sp1)

    for j in range(random.randint(32, 64)):
        r = random.choice(cur_sp)
        if r == 'R' and last != 'L' and ind1 <= width - 2:
            ind1 += 1
            level[ind2][ind1] = '■'
            sub_paths.append((ind2, ind1))
            last = 'R'
        elif r == 'L' and last != 'R' and ind1 >= 1:
            ind1 -= 1
            level[ind2][ind1] = '■'
            sub_paths.append((ind2, ind1))
            last = 'L'
        elif r == 'D' and ind2 <= height - 2 and last != 'U':
            ind2 += 1
            level[ind2][ind1] = '■'
            sub_paths.append((ind2, ind1))
            last = 'D'
        elif r == 'U' and ind2 >= 1 and last != 'D':
            ind2 -= 1
            level[ind2][ind1] = '■'
            sub_paths.append((ind2, ind1))
            last = 'U'


# multiplication
large_level = []
for i in level:
 string = ''
 for j in i:
  string += j * 2
 large_level.append(string)
 large_level.append(string)

print(*large_level, sep='\n')
'''

# print(path)
for i in level:
    print(''.join(i))
print(len(level))
'''