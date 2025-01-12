import random
# weight, hight = map(int, input().split())
weight, hight = 64, 64
a = 3
lst = ['0'] * hight
for i in range(hight):
    lst[i] = [' '] * weight
k = random.randint(0, hight - 1)
k1 = random.randint(0, hight - 1)
lst[k][0] = '*'
lst[k1][-1] = '*'
ind1 = 0
ind2 = k
sp = ['d', 'd', 'u', 'u', 'd', 'u', 'r', 'r', 'r', 'r']
sp1 = ['d', 'd', 'd', 'l', 'l', 'l', 'r', 'r', 'r', 'r']
sp2 = ['d', 'd', 'd', 'r', 'l', 'l', 'l', 'l', 'r', 'r']
last  = ''

while ind1 != weight -1:
    r = random.choice(sp)
    if r == 'r':
        ind1 += 1
        lst[ind2][ind1] = '+'
        last = ''
    elif r == 'd' and ind2 != hight - 1 and last != 'u':
        ind2 += 1
        lst[ind2][ind1] = '+'
        last = 'd'
    elif r == 'u' and ind2 != 0 and last != 'd':
        ind2 -= 1
        lst[ind2][ind1] = '+'
        last = 'u'

if ind2 < k1:
    for i in range(ind2 + 1, k1):
        lst[i][-1] = '+'
elif ind2 > k1:
    for i in range(k1 + 1, ind2 + 1):
        lst[i][-1] = '+'


i1 = random.randint(0 , weight // 2)
i2 = random.randint(weight // 2 + 1, weight - 1)

ind1 = i1
ind2 = 0
while ind2 != hight -1:
    r = random.choice(sp1)
    if r == 'r' and ind1 != weight - 2 and last != 'l':
        ind1 += 1
        lst[ind2][ind1] = '+'
        last = 'r'
    elif r == 'd':
        ind2 += 1
        lst[ind2][ind1] = '+'
        last = ''
    elif r == 'l' and ind1 != 1 and last != 'r':
        ind1 -= 1
        lst[ind2][ind1] = '+'
        last = 'l'


ind1 = i2
ind2 = 0
while ind2 != hight -1:
    r = random.choice(sp2)
    if r == 'r' and ind1 != weight - 2 and last != 'l':
        ind1 += 1
        lst[ind2][ind1] = '+'
        last = 'r'
    elif r == 'd':
        ind2 += 1
        lst[ind2][ind1] = '+'
        last = ''
    elif r == 'l' and ind1 != 1 and last != 'r':
        ind1 -= 1
        lst[ind2][ind1] = '+'
        last = 'l'


for i in range(len(lst)):
    print(lst[i])
