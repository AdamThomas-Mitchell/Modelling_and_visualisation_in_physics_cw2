import numpy as np
import sys
import matplotlib.pyplot as plt

def random_state(N):
    #initialise state randomly
    state = np.random.rand(N,N)
    state[state<0.5] = 0
    state[state>=0.5] = 1

    return state

def rules_of_life(x,y):
    #calculate number of alive neighbours for cell
    #num_neighbours = np.sum(state[x-1:(x+2)%N,y-1:(y+2)%N]) - state[x,y]
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
    global state        #why needed?

    #iterate over every cell in state
    for i in range(N):
        for j in range(N):
            rules_of_life(i,j)

    state = np.copy(new_state)

    return state

def total_alive(state):
    #function to calculate total number of live cells
    num = np.sum(state)

    return int(num)

N=50
num_sim=500
#steps_to_equib = np.zeros(500)
steps_to_equib =np.empty(0)
for i in range(num_sim):
    print("[completion:" + str(round(100*i/num_sim)) + '%]', end='\r')

    state = random_state(N)     #initialise random state
    new_state = np.copy(state)

    #time evolution loop
    numcells_array = np.zeros(2500)     #number of cells alive at each time pt
    for n in range(2500):
        state = state_update()
        numcells_array[n] = total_alive(state)  #record number of cells alive


        #loop to check if system has equilibrated
        if np.all(numcells_array[n-10:n] == numcells_array[n]) and n>10:
            #steps_to_equib[i] = n
            steps_to_equib = np.append(steps_to_equib, n)
            break

hist, bins, p = plt.hist(steps_to_equib, bins=50)
plt.title('Histogram for the time until system reaches equilibrium')
plt.xlabel('Steps until equilibrium')
plt.ylabel('Frequency')
plt.show()
