"""
CP2 SIRS component part 2 and 3
"""
import numpy as np
import math
import random

def num_inf_neighbours(state,x,y):
    inf_nn = 0
    if state[(x+1)%l,y] == 1:
        inf_nn += 1
    if state[x-1,y] == 1:
        inf_nn += 1
    if state[x,(y+1)%l] == 1:
        inf_nn += 1
    if state[x,y-1] ==1:
        inf_nn += 1

    return inf_nn

def disease_dynamics(state,x,y,p1,p2,p3):
    #function to apply rules to given cell
    #susceptible compartment
    if state[x,y] == 0:     #corresponds to susceptible cell
        if num_inf_neighbours(state,x,y) >= 1:
            if np.random.rand() < p1:
                state[x,y] = 1

    #infected compartment
    elif state[x,y] == 1:       #corresponds to infected cell
        if np.random.rand() < p2:
            state[x,y] = 2

    #recovered compartment
    elif state[x,y] == 2:       #corresponds to recovered cell
        if np.random.rand() < p3:
            state[x,y] = 0

    return state[x,y]

def initial_state(l):
    #initalise state so equal numbers of S,I,R compartments to start
    state = np.random.randint(0, 3, (l,l))
    return state

def total_infected(state):
    #calculates number of infected cells in state
    total_inf = np.sum(np.where(state==1, state, 0))
    return total_inf

def inf_variance(num_inf_array,N):
    #calculates variance in mean infected proportion
    var = (np.mean(np.square(num_inf_array)) - np.mean(num_inf_array)**2.0)/N
    return var  #try np.var

def var_bootstrap(total_inf_vals,N):
    #calculates error in variance using bootstrap method
    var_samples = np.zeros(1000)
    for k in range(1000):
        inf_vals_resample = np.zeros_like(total_inf_vals)
        for m in range(len(total_inf_vals)):
            inf_vals_resample[m] = random.choice(total_inf_vals)
        new_variance = inf_variance(inf_vals_resample, N)
        var_samples[k] = new_variance
    var_error = math.sqrt(np.mean(var_samples**2.0) - np.mean(var_samples)**2.0)

    return var_error


l=50
N=l**2
nstep=2750000  #number of steps simulation runs for
nequib=250000   #number of steps to wait for equilibration
nsweep=N     #number of steps on average for one sweep for lxl system
p2=0.5
p1_vals = np.arange(0.0, 1.05, 0.05)
#p1_vals = np.arange(0.2, 0.51, 0.01)
p3_vals = np.arange(0.0, 1.05, 0.05)
#p3_vals = np.array([0.5])

f=open('sirs_data_part4test.dat','w')
for i in range(len(p1_vals)):
    for j in range(len(p3_vals)):
        print("[completion:" + str(round(100*(i*len(p3_vals) + j)/(len(p1_vals)*len(p3_vals)),5)) + '%]', end='\r')    #progress bar

        p1=p1_vals[i]
        p3=p3_vals[j]
        total_inf_vals = np.empty(0)

        state = initial_state(l)
        for n in range(nstep):
            irand = np.random.randint(0,l)
            jrand = np.random.randint(0,l)
            state[irand,jrand] = disease_dynamics(state, irand, jrand, p1, p2, p3)

            if n>nequib and n%nsweep==0:    #record data every sweep after 100 sweeps for equilibration
                total_inf = total_infected(state)
                if total_inf == 0:
                    total_inf_vals = np.zeros(1)
                    break
                else:
                    total_inf_vals = np.append(total_inf_vals, total_inf)

        ave_inf_frac = np.mean(total_inf_vals/N)
        inf_var = np.var(total_inf_vals)/N
        var_error = var_bootstrap(total_inf_vals, N)

        f.write('%lf %lf %lf %lf %lf\n'%(p1, p3, ave_inf_frac, inf_var, var_error))
    f.write('\n')
f.close()
