from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import math
from tqdm import tqdm
import copy
import scipy.optimize
import random
import os

def fix(nodes, rels):
    """set nodes with fixed values to the appropriate values, prior to scoring"""
    for r in rels:
        if r[0] == 'fix':
            nodes[r[1]] = r[2]
    return nodes

def get_free(nodes, rels):
    """return a sorted list of nodes which are free to move"""
    node_names = set(nodes.keys())
    for r in rels:
        if r[0] == 'fix':
            node_names.remove(r[1])
    node_names = list(node_names)
    node_names.sort()
    return node_names

def score(nodes,rels):
    score = 0.0
    for r in rels:
        if r[0] == 'dist':
            err = (math.sqrt((nodes[r[1]][0]-nodes[r[2]][0])**2 + (nodes[r[1]][1]-nodes[r[2]][1])**2) - r[3])**2
            score += err
    return score

def score_func(vec):
    """uses a closure to create copy of the node and relationship list, which is then modified as nessecary"""
    nodes2 = copy.deepcopy(nodes)
    for i, n in enumerate(free_nodes):
        nodes2[n] = [vec[2*i],vec[2*i+1]]
    s = score(nodes2,rels)
    return s

def solve_e(nodes, e_length, e_shift):
    mid = [((1+e_shift)*nodes['d'][0]+(1-e_shift)*nodes['c'][0])/2,((1+e_shift)*nodes['d'][1]+(1-e_shift)*nodes['c'][1])/2]
    xl = -nodes['c'][1]+mid[1]
    yl = nodes['c'][0]-mid[0]
    scale = (e_length/math.sqrt(xl**2+yl**2))
    xl = xl*scale
    yl = yl*scale
    e = [mid[0]+xl,mid[1]+yl]
    return e

def plot_linkage(nodes, rels, axis_limits = False):
    fig = plt.figure()
    plt.hold(True)
    for n in nodes:
        plt.plot(nodes[n][0],nodes[n][1],'.')
    for r in rels:
        if r[0] == 'dist':
            plt.plot([nodes[r[1]][0],nodes[r[2]][0]],[nodes[r[1]][1],nodes[r[2]][1]],'r-')
        elif r[0] == 'draw':
            plt.plot([nodes[r[1]][0],nodes[r[2]][0]],[nodes[r[1]][1],nodes[r[2]][1]],'k-')
    plt.hold(False)
    plt.axis([-2,2,-2,2])
    plt.axis('equal')

def plot_path(path, out):
    fig = plt.figure()
    plt.hold(True)
    plt.axis([-2,2,-2,2])
    #convert list of node states to vectors for plotting
    node_paths = {}
    for n in path[0].keys():
        node_paths[n] = []
    for p in path:
        for n in p.keys():
            node_paths[n].append(tuple(p[n]))
    #plot the paths
    for n in node_paths.keys():
        if n == out:
            clr = 'r-'
        else:
            clr = 'k-'
        plt.plot([x[0] for x in node_paths[n]], [x[1] for x in node_paths[n]], clr)
    plt.hold(False)
    plt.axis('equal')

def make_path(b_x=1.0,b_y=0.0,a_l=1.0,c_l=0.5,d_l=1.0,length=0.5, e_shift=0.0):
    path = []
    nodes = {'a':[0,0],'b':[b_x,b_y],'c':[b_x,b_y+c_l],'d':[0,d_l],'e':[0,0]}
    out = 'e'
    #t = 1.0#0.0
    quality = True
    for t in np.linspace(0.0,1.0,60):
        rels = [('fix','a',[0,0]),
            ('fix','b',[b_x,b_y]),
            ('fix','c',[nodes['b'][0]+c_l*math.cos(2*math.pi*t+math.pi/2),nodes['b'][1]+c_l*math.sin(2*math.pi*t+math.pi/2)]),
            ('dist','a','d',a_l),
            ('dist','c','d',d_l),
            ('fix','e',[0,0]),
            ('draw','a','b'),
            ('draw','c','b'),
            ('draw','e','c'),
            ('draw','e','d')
           ]
        nodes = fix(nodes,rels)
        free_nodes = get_free(nodes,rels)

        def score_func(vec):
            """uses a closure to create copy of the node and relationship list, which is then modified as nessecary"""
            nodes2 = copy.deepcopy(nodes)
            for i, n in enumerate(free_nodes):
                nodes2[n] = [vec[2*i],vec[2*i+1]]
            s = score(nodes2,rels)
            return s

        #optimize the location
        vec0 = []
        for n in free_nodes:
            vec0.append(nodes[n][0])
            vec0.append(nodes[n][1])
        res = scipy.optimize.minimize(score_func, vec0, method = 'CG', options = {'disp':False})
        if not res.success or res.fun > 0.0001:
            quality = False
            break
        nodes['d'] = res.x
        nodes['e'] = solve_e(nodes,length,e_shift)
        path.append(copy.deepcopy(nodes))
    #plot_linkage(path[0],rels)
    #plot_path(path,'e')
    #plt.show()
    return path, quality

if __name__ == '__main__':
    random.seed(888)
    out = 'e'
    f_path = os.path.join(os.getcwd(),'data')
    successes = 0
    for i in tqdm(range(10000)):
        b_x = random.uniform(0.5,1.5)
        b_y = random.uniform(-0.5,0.5)
        c_l = random.uniform(0.15,1.0)
        a_l = random.uniform(c_l,1.5)
        d_l = random.uniform(math.sqrt(b_x**2+b_y**2),2.0)
        length = random.uniform(-0.5,0.5)
        e_shift = random.uniform(-0.75,0.75)
        linkage = [b_x,b_y,a_l,c_l,d_l,length,e_shift]
        path, quality = make_path(*linkage)
        #pull out the x and y values for the output node
        if quality:
            out_path = []
            for p in path:
                out_path.append(tuple(p[out]))
            cost = math.sqrt(b_x**2+b_y**2)+a_l+c_l+d_l+length
            #write the score to a file
            f = open(os.path.join(f_path,str(successes)+'_data.txt'),'w')
            f.write('{}\n{}\n{}'.format(cost,linkage,quality))
            f.close()
            #write the path out
            f = open(os.path.join(f_path,str(successes)+'_path.csv'),'w')
            f.write('x,y\n')
            for p in out_path:
                f.write('{},{}\n'.format(p[0],p[1]))
            f.close()
            successes += 1
    #print cost, out_path
