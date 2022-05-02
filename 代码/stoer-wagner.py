import time
import copy


def loaddata(path):
    print("==================="+path+"===================")
    file = open(path)
    f = file.readlines()
    edges = []
    vertices = []
    for i in range(len(f)):
        dat = f[i].split()
        if [int(dat[0]), int(dat[1])] not in edges and [int(dat[1]), int(dat[0])] not in edges:
            edges.append([int(dat[0]), int(dat[1])])
    for edge in edges:
        vertices.append(edge[0])
        vertices.append(edge[1])
    vertices = list(set(vertices))
    return vertices, edges


def stMinCut(vs,es,num_v):
    ves = copy.deepcopy(vs)
    eds = copy.deepcopy(es)
    Anode = 1
    A = [Anode]
    A_ajac = [0 for v in range(num_v)]
    A_ajac.append(0)    #转换为1起点

    # init A_ajac
    for e in es:
        if e[0] == Anode:
            A_ajac[e[1]] += 1
        if e[1] == Anode:
            A_ajac[e[0]] += 1

    s = A[0]
    t = None
    while len(vs) > 1:
        maxi = -float('inf')
        nxt = None
        for a in range(1,len(A_ajac)):
            if A_ajac[a] > maxi and a not in A:
                nxt = a
                maxi = A_ajac[a]
        #print('next vertice : ',nxt)
        #print('connection : ',maxi)
        t = s
        s = nxt
        # 把s合进A中
        A.append(s)
        # 删除s点
        vs.remove(s)
        # 删除边、继承边
        new_eds = []
        for e in es:
            # 删除边
            if e == [Anode,s] or e == [s,Anode]:
                continue
            elif e[0] == s:
                new_eds.append([Anode,e[1]])
                A_ajac[e[1]] += 1
            elif e[1] == s:
                new_eds.append([e[0],Anode])
                A_ajac[e[0]] += 1
            else:
                new_eds.append(e)
        es = new_eds
        #print('edges: ',es)
        #print('vertices : ',vs)

    return [[s],A],A_ajac[s],t

def contract(vs,es,t,s):
    # 删除s点
    vs.remove(s)
    # 删除边、继承边
    new_eds = []
    for e in es:
        # 删除边
        if e == [t,s] or e == [s,t]:
            continue
        elif e[0] == s:
            new_eds.append([t,e[1]])
        elif e[1] == s:
            new_eds.append([e[0],t])
        else:
            new_eds.append(e)
    es = new_eds

    return vs,es

def globalMinCut(vs,es,num_v):
    ves = copy.deepcopy(vs)
    eds = copy.deepcopy(es)

    if len(vs) == 2:
        cut = 0
        for e in es:
            if e == [vs[0],vs[1]] or e == [vs[1],vs[0]]:
                cut += 1
        return [[vs[0]],[vs[1]]], cut
    else:
        cut1, c1, t = stMinCut(ves,eds,num_v)
        s = cut1[0][0]
        vs,es = contract(vs,es,t,s)
        cut2, c2 = globalMinCut(vs,es,num_v)
        for cut in cut2:
            if t in cut:
                cut.append(s)
        if c1 <= c2:
            return cut1, c1
        else:
            return cut2, c2


if __name__=='__main__':
    fileList = ['./data/BenchmarkNetwork.txt','./data/test1.txt','./data/Corruption_Gcc.txt', './data/Crime_Gcc.txt', './data/PPI_gcc.txt', './data/RodeEU_gcc.txt']
    for path in fileList:
        start_time = time.time()
        vertices, edges = loaddata(path)
        print('vertices: ',len(vertices),'edges: ',len(edges))
        minCutSet, minCut = globalMinCut(vertices,edges,len(vertices))
        print("the min-cut is ",minCut)
        minCutSet[0].sort()
        print("the nodes linked to V1 is ",minCutSet[0])
        time_dura = time.time() - start_time
        print("time duration : ",time_dura)