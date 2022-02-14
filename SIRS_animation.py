import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

"""
Absorbing state parameters:         N=2500, p1=0.1, p2=0.5, p3=0.5
Dynamic equilibrium parameters:     N=2500, p1=0.5, p2=0.5, p3=0.5
Cylice wave paramteters:            N=10000, p1=0.8, p2=0.1, p3=0.01
"""
###FUNCTIONS###
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

def disease_dynamics(state,x,y):
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

def initial_state():
    #initalise state so equal numbers of S,I,R compartments to start
    state = np.random.randint(0, 3, (l,l))

    return state

###INPUT###
if(len(sys.argv) != 5):
    print("Usage python SIRS_animation.py N P1 P2 P3    ")
    sys.exit()
l=int(sys.argv[1])
p1=float(sys.argv[2])
p2=float(sys.argv[3])
p3=float(sys.argv[4])

N=l**2
nstep = 25000000

###METHOD###
def animation():

    #intialise lxl grid
    state = initial_state()

    #initialise animation
    fig = plt.figure()
    im=plt.imshow(state, animated=True)

    for n in range(nstep):

        irand = np.random.randint(0,l)
        jrand = np.random.randint(0,l)
        state[irand,jrand] = disease_dynamics(state,irand,jrand)

        if n%25000==0:
            #show animation
            plt.cla()
            im=plt.imshow(state, animated=True)
            plt.draw()
            plt.pause(0.001)

animation()
