import numpy as np
import math
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def random_state(N):
    #initialise state randomly
    state = np.random.rand(N,N)
    state[state<0.5] = 0
    state[state>=0.5] = 1

    return state

def rules_of_life(x,y):
    #calculate number of alive neighbours for cell
    num_neighbours = state[(x-1)%N,y] + state[(x+1)%N,y] + state[x,(y-1)%N] + state[x,(y+1)%N] + state[(x+1)%N,(y+1)%N] + state[(x-1)%N,(y+1)%N] + state[(x+1)%N,(y-1)%N] + state[(x-1)%N,(y-1)%N]

    #for live cell
    if state[x,y] == 1:
        if num_neighbours < 2 or num_neighbours > 3:
            new_state[x,y] = 0

    #for dead cell
    elif state[x,y] == 0:
        if num_neighbours == 3:
            new_state[x,y] = 1

def state_update():
    #function to update entire system
    global state

    #iterate over every cell in state
    for i in range(N):
        for j in range(N):
            rules_of_life(i,j)

    state = np.copy(new_state)

    return state

def centre_of_mass(state):
    #calculates position of centre of mass
    x, y = np.where(state==1)
    x_mean = np.mean(x)
    y_mean = np.mean(y)

    return (x_mean, y_mean)

def total_alive(state):
    #function to calculate total number of live cells
    num = np.sum(state)

    return num

#seed for structures
oscillator = [[0,1,0],[0,1,0],[0,1,0]]
beacon = [[1,1,0,0],[1,1,0,0],[0,0,1,1],[0,0,1,1]]
glider = [[0,1,0],[0,0,1],[1,1,1]]

N=50    #dimensions for NxN grid
#User for method
choice = input("Type (1) for random state, (2) for oscillator or (3) for glider.     ")
init=None
if choice == "1":
    init=1
elif choice == "2":
    init=2
elif choice == "3":
    init=3

#initialise state according to input
if init==1:
    state = random_state(N)
elif init==2:
    state = np.zeros((N,N))
    state[24:27,24:27] = oscillator
elif init==3:
    state = np.zeros((N,N))
    state[1:4,1:4] = glider
    f=open('glider.dat', 'w')
    xpos = np.empty(0)
    ypos = np.empty(0)

#initialise animation
fig=plt.figure()
im=plt.imshow(state, cmap='binary')

new_state = np.copy(state)

#time evolution loop
for n in range(3000):
    state = state_update()

    plt.cla()
    im=plt.imshow(state, cmap='binary')
    plt.draw()
    plt.pause(0.0001)
    #print(n)
    if init==3:
        if n%10==0:
            xpos = np.append(xpos, centre_of_mass(state)[0])
            ypos = np.append(ypos, centre_of_mass(state)[1])
            k = len(xpos)
            if xpos[k-1]>xpos[k-2]:     #loops take account of PBC miscalculations
                if ypos[k-1]>ypos[k-2]:
                    xvel = (xpos[k-1] - xpos[k-2])/10
                    yvel = (ypos[k-1] - ypos[k-2])/10
                    speed = math.sqrt(xvel**2 + yvel**2)

                    f.write('%lf %lf %lf %lf %lf\n'%(xpos[-1], ypos[-1], xvel, yvel, speed))

f.close()
