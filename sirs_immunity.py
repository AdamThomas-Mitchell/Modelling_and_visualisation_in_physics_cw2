import numpy as np
import math
import random
from cell_class import cell

l=100
N=l**2
p1=0.5
p2=0.5
p3=0.5
num_im = 10
nstep=2750000
nequib=250000
nsweep=N
npoint = int((nstep - nequib)/nsweep)

def init_system(l,num_im):

    N=l**2
    init_comp = np.random.randint(0,3,N)
    init_im = np.full(N, False)
    init_im[:num_im] = True
    system = np.empty(N, dtype=object)
    for i in range(N):
        system[i] = cell(i, init_comp[i], init_im[i])
    np.random.shuffle(system)
    system = np.reshape(system, (l,l))

    return system

def num_inf_neighbours(state,x,y):

    inf_nn = 0
    if state[(x+1)%l,y].comp == 1:
        inf_nn += 1
    if state[x-1,y].comp == 1:
        inf_nn += 1
    if state[x,(y+1)%l].comp == 1:
        inf_nn += 1
    if state[x,y-1].comp ==1:
        inf_nn += 1

    return inf_nn

def total_infected(state):
    
    tot_inf = 0
    for x in range(l):
        for y in range(l):
            if system[x,y].comp == 1:
                tot_inf += 1

    return tot_inf


f=open('sirs_immunity_.dat','w')
im_vals = np.arange(0, N, 100)

for i in range(len(im_vals)):
    print("[completion:" + str(round(100*(i/len(im_vals)),5)) + '%]', end='\r')
    num_im = im_vals[i]
    tot_inf_vals = np.zeros(npoint)
    system = init_system(l,num_im)
    for n in range(nstep):
        irand = np.random.randint(0,l)
        jrand = np.random.randint(0,l)
        inf_nn = num_inf_neighbours(system,irand,jrand)
        system[irand,jrand].disease_dynamics(inf_nn, p1, p2, p3)
        if n>nequib and n%nsweep==0:
            data_point = int((n-nequib)/nsweep)
            total_inf = total_infected(system)
            if total_inf == 0:
                break
            else:
                tot_inf_vals[data_point] = total_inf
    im_frac = num_im/N
    ave_inf_frac = np.mean(tot_inf_vals)/N
    f.write('%lf %lf\n'%(im_frac, ave_inf_frac))

f.close()
