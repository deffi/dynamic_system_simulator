import numpy as np
from matplotlib import pyplot as plt

class System:
    pass

class P(System):
    def __init__(self, K=1):
        self._K=K
        self._y=0
        
    def update(self, dt, u):
        self._y=u

    def output(self):
        # Return state
        return self._y
    

class PT1(System):
    def __init__(self, T, K=1):
        # Initialize parameters
        self._T = T
        self._K = K
        
        # Initialize state
        self._y = 0
    
    def update(self, dt, u):
        # Fetch parameters
        K = self._K
        T = self._T
        
        #Update state
        y = self._y
        y = 1 / (T / dt + 1) * (K * u + T / dt * y)
        self._y = y

    def output(self):
        # Return state
        return self._y

if __name__ == '__main__':
    system=PT1(1, 1)
    #system=P(1)

    time = 5
    dt = 1/50

    def u(t):
        if t>=1:
            return 1
        else:
            return 0

    T=np.arange(0, time+dt, dt)
    
    Y=np.zeros(np.size(T))
     
    Y[0]=system.output()
    previous_t=T[0]
    for i, t in enumerate(T[1:]):
        system.update(dt, u(t))
        Y[i+1]=system.output()

    plt.plot(T, Y, '.-')
    plt.show()
