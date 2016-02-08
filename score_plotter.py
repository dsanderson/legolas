from __future__ import division
import os
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

def import_scores(fname):
    f = open(os.path.join(os.getcwd(),fname),'r')
    data = f.read()
    f.close()
    indicies = []
    scores = []
    for row in data.split():
        if row.strip() != '':
            indicies.append(int(row.split(',')[0].strip()))
            scores.append(float(row.split(',')[1].strip()))
    return indicies, scores

def import_costs(total):
    costs = []
    for i in xrange(total):
        path = os.path.join(os.getcwd(),'data')
        f = open(os.path.join(path,'{}_data.txt'.format(i)),'r')
        data = f.read()
        f.close()
        cost = float(data.split()[0].strip())
        costs.append(cost)
    return costs

def get_paretos(costs, scores):
    paretos = []
    for i in tqdm(xrange(len(costs))):
        c = costs[i]
        s = scores[i]
        pareto = True
        for j in xrange(len(costs)):
            if j != i:
                if costs[j]<c and scores[j]<s:
                    pareto = False
                    break
        if pareto:
            paretos.append(i)
    return paretos

if __name__ == '__main__':
    total = 168
    indicies, scores = import_scores('scoring.csv')
    costs = import_costs(total)
    paretos = get_paretos(costs,scores)
    plt.plot(scores, costs, 'r.', alpha = 0.35)
    plt.hold(True)
    #plot pareto points
    p_costs = [costs[i] for i in paretos]
    p_scores = [scores[i] for i in paretos]
    plt.plot(p_scores,p_costs,'b.')
    plt.xlabel('score')
    plt.ylabel('cost')

    f_path = os.path.join(os.getcwd(),'data')
    failed = 0
    total = 168
    fig = plt.figure()
    plt.hold(True)
    for i in tqdm(range(total)):
        f = open(os.path.join(f_path,str(i)+'_data.txt'),'r')
        data = f.read()
        f.close()
        if not ('True' in data):
            failed += 1
        else:
            f = open(os.path.join(f_path,str(i)+'_path.csv'),'r')
            data = f.read()
            f.close()
            xs = []
            ys = []
            for d in data.split()[1:]:
                if d.strip() != '':
                    xs.append(float(d.split(',')[0].strip()))
                    ys.append(float(d.split(',')[1].strip()))
            plt.plot(xs,ys,'r-',alpha=0.25)
            if i == 9:
                target_path = [tuple(xs),tuple(ys)]
    for i in paretos:
        f = open(os.path.join(f_path,str(i)+'_data.txt'),'r')
        data = f.read()
        f.close()
        if not ('True' in data):
            failed += 1
        else:
            f = open(os.path.join(f_path,str(i)+'_path.csv'),'r')
            data = f.read()
            f.close()
            xs = []
            ys = []
            for d in data.split()[1:]:
                if d.strip() != '':
                    xs.append(float(d.split(',')[0].strip()))
                    ys.append(float(d.split(',')[1].strip()))
            plt.plot(xs,ys,'b-',alpha=0.50)
            if i == 9:
                target_path = [tuple(xs),tuple(ys)]
    plt.plot(target_path[0],target_path[1],'g-',alpha=0.75)
    plt.axis('equal')

    fig = plt.figure()
    plt.hold(True)
    for i in paretos:
        f = open(os.path.join(f_path,str(i)+'_data.txt'),'r')
        data = f.read()
        f.close()
        if not ('True' in data):
            failed += 1
        else:
            f = open(os.path.join(f_path,str(i)+'_path.csv'),'r')
            data = f.read()
            f.close()
            xs = []
            ys = []
            for d in data.split()[1:]:
                if d.strip() != '':
                    xs.append(float(d.split(',')[0].strip()))
                    ys.append(float(d.split(',')[1].strip()))
            alpha = 1-(scores[i]/max(scores))
            plt.plot(xs,ys,'g-',alpha=alpha)
            if i == 9:
                target_path = [tuple(xs),tuple(ys)]
    #plt.plot(target_path[0],target_path[1],'k-',alpha=0.75)
    plt.axis('equal')

    plt.show()
