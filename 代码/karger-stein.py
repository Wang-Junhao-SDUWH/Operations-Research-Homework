import random
import math
import copy
import time
import networkx as nx
import matplotlib.pyplot as plt

def drawNet(v,e):
    G = nx.Graph()
    G.add_nodes_from(v)
    G.add_edges_from(e)
    nx.draw_spectral(G)
    plt.show()

def ranContract(v, e, terminal):
    connect = []
    while len(v)>terminal:
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
    return (e, connect, v)

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

def loaddata(path):
    print("==================="+path+"===================")
    file = open(path)
    f = file.readlines()
    edges = []
    vertices = []
    for i in range(len(f)):
        dat = f[i].split()
        for i in dat:
            if int(i) not in vertices:
                vertices.append(int(i))
        if [int(dat[0]), int(dat[1])] not in edges and [int(dat[1]), int(dat[0])] not in edges:
            edges.append([int(dat[0]), int(dat[1])])
    print("vertices:", len(vertices), "edges:", len(edges))
    return vertices, edges

def karger_stein(v,e):
    if len(v) >= 6:
        t = int(len(v)/math.sqrt(2)) + 1
        e_1, c_1, v_1 = ranContract(v, e, t)
        e_2, c_2, v_2 = ranContract(v, e, t)
        if len(e_1) < len(e_2):
            r,g,b = karger_stein(v_1, e_1)
        else:
            r,g,b = karger_stein(v_2, e_2)
        return r,g,b
    else:
        r,g,b = ranContract(v,e,2)
        return r,g,b

if __name__ == '__main__':
    fileList = ['./data/BenchmarkNetwork.txt','./data/test1.txt','./data/Corruption_Gcc.txt', './data/Crime_Gcc.txt', './data/PPI_gcc.txt', './data/RodeEU_gcc.txt']
    times_for_k = []
    times_for_kg = []
    for fi in fileList:
        vertices, edges = loaddata(fi)
        drawNet(vertices, edges)
        numVer = len(vertices)
        min_ = 100000
        start_time = time.time()
        n = int(math.log(numVer)*math.log(numVer))
        for i in range(n):
            v = copy.deepcopy(vertices)
            e = copy.deepcopy(edges)
            r, g, b = ranContract(v, e, 2)
            if min_>len(r):
                min_=len(r)
                con = findE(b[1], g)
        time_dura = time.time() - start_time
        times_for_k.append(time_dura)
        print("time duration for karge : ",time_dura)
        print("the min-cut is ",min_)
        print("the min-cut contracted to V1 is \n",con)

        min_ = 100000
        start_time = time.time()
        # n*（n-1）/2
        for i in range(n):
            v = copy.deepcopy(vertices)
            e = copy.deepcopy(edges)
            r, g, b = karger_stein(v, e)
            if min_>len(r):
                min_=len(r)
                con = findE(b[1], g)
        time_dura = time.time() - start_time
        times_for_kg.append(time_dura)
        print("time duration for karge-stein : ",time_dura)
        print("the min-cut is ",min_)
        print("the min-cut contracted to V1 is \n",con)