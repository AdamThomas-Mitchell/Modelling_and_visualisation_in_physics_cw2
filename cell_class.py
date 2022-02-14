import numpy as np

class cell(object):
    def __init__(self,label,comp,im):
        self.label = label
        self.comp = int(comp)
        self.im = im

    def disease_dynamics(self,inf_nn,p1,p2,p3):
        #function to apply rules to given cell
        if self.im == False:
            #susceptible compartment
            if self.comp == 0:
                if inf_nn >= 1:
                    if np.random.rand() < p1:
                        self.comp = 1

            #infected compartment
            elif self.comp == 1:
                if np.random.rand() < p2:
                    self.comp = 2

            #recovered compartment
            elif self.comp == 2:
                if np.random.rand() < p3:
                    self.comp = 0

        if self.im == True:
            self.comp = 2   #permanently in recovered compartment if immune
