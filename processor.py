from __future__ import division
import os
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

if __name__ == '__main__':
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
    plt.plot(target_path[0],target_path[1],'b-',alpha=0.75)
    print 'Of {}, {} failed ({}%)'.format(total,failed,failed/total*100)
    plt.show()
