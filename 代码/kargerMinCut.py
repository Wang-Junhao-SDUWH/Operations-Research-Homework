import random
import copy

def ranContract(v, e):
    connect = []
    while len(v)>2:
        [a, b] = e.pop(random.randrange(0, len(e)))
        connect.append([a, b])
        v.remove(a)
        new = []
        for i in range(len(e)):
            if e[i][0] == a:
                e[i][0] = b
            elif e[i][1] == a:
                e[i][1] = b
            if e[i][0] != e[i][1]:
                new.append(e[i])
        e = new
    return(len(e), connect, v)

def findE(V1, e):
    connectToV1 = []
    new = []
    cur = [V1]
    while cur!=[]:
        for i in cur:
            for j in range(len(e)):
                if e[j][0]==i:
                    new.append(e[j][1])
                if e[j][1]==i:
                    new.append(e[j][0])
            e = [g for g in e if g[0] != i and g[1] != i]
        connectToV1+=new
        cur = new
        new = []
    return connectToV1
if __name__ == '__main__':
    file = open('kargerMinCut.txt')
    f = list(file)
    edges = []
    vertices = []
    for i in range(len(f)):
        dat = f[i].split()
        vertices.append(int(dat[0]))
        # 200个点
        for j in range(1, len(dat)):
            if [int(dat[j]), int(dat[0])] not in edges:
                edges.append([int(dat[0]), int(dat[j])])
    # print(len(vertices), len(edges))
    min = 100000
    for i in range(200):
        v = copy.deepcopy(vertices)
        e = copy.deepcopy(edges)
        r, g, b = ranContract(v, e)
        if min>r:
            min=r
            con = findE(b[1], g)
    print("================Karger==============")
    print("the min-cut is ",min)
    print("the min-cut contracted to V1 is \n",con)
