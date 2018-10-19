from itertools import permutations

def go1(xs):
    accum = xs.copy()
    while len(accum):
        xs = accum.pop()
        while len(xs):
            x = xs.pop()
            for y in xs:
                rest = xs[:y]
                rest.append((x, y))
                xs.append(rest)

    return xs




def go(xs):
    accum = xs.copy()
    while len(accum):
        xs = accum.pop()
        for x in xs:
            k = xs.index(x)
            xs.remove(x)
            for y in xs:
                another = xs.copy()
                another.remove(y)
                another.insert(0, (x,y))
                xs.append(another)
            xs.insert(k, x)
        xs.remove(xs)

    return xs

def permute(xs):
    various = []
    for i in range(len(xs)):
        for j in range(i + 1, len(xs)):
            various.append((xs[i], xs[j]))
    
    return various


def generate(xs):
    various = permute(xs)
    xs_to = []
    for var in various:
        temp = list(xs)
        temp.remove(var[0])
        temp.remove(var[1])
        temp.insert(0, var)
        xs_to.append(tuple(temp))
    
    return xs_to





#print(go([[0, 1, 2, 3]]))
#print(type((1,2)))
#print([p for p in permutations([1, 2, 3, 4]) if p[0] < p[1]])
mydict = {(1,2,3,4):(1,2)}
# dictionary = mydict.copy()
# def rec(mydict):
#     if len(next(iter(mydict.keys()))) == 1:
#         return mydict
#     for key in mydict.keys():
#         mydict[key] = generate(key)

#     myvalues = list(mydict.values())
#     mydict.clear()
#     for value in myvalues:
#         for val in value:
#             mydict[val] = (1,2)
    
#     return rec(mydict)


def rec(xs):
    if len(xs[0]) == 2:
        return xs
    ls = []
    for x in xs:
        gen = generate(x)
        for g in gen:
            ls.append(g)

    # lss = ls.copy()
    # for i in range(len(lss)):
    #     if len(lss[i]) == 2:
    #         for j in range(i + 1, len(lss)):
    #             tt = list(lss[j])
    #             if tt.count(lss[i][0]):
    #                 ls[j] = 0
    


    return rec(ls)


#print(rec(mydict))

xs = rec([(1,2,3)])
#xs = generate([(1,2),3,4])
# xs_r = []
# for x in xs:
#     if type(x[-1]) is int:
#         xs_r.append(x)
#     else:
#         x = list(x)
#         x.reverse()
#         xs_r.append(tuple(x))
i = 0
for i in range(xs.count(0)):
    xs.remove(0)
for x in xs:
    print(i, x)
    i = i + 1

# print(generate(((1,2),3,4)))