# Simulating lightly interacting particles using the Ising Model

_An implementation of the Ising Model in Python. This project has been made following several tutorials in Statistical Mechanics and Computational Methods._

## Project overview
The Ising Model is used to model the behaviour of interacting particles. In this specific project it has been used to model the energy of a system consisting of spin-up and sping-down particles. We first define a function that returns a random state with the state-size and probabilities pre-defined by the user.

```
import numpy as np
```

```
#Creates a square matrix of side N wirh P% up-spins
def create_random_state(N,P):
    random_array = np.random.random((N,N))
    for i in range(N):
        for j in range(N):
            if (random_array[i][j] > (P/100)) :
                random_array[i][j] = (-1)
            else :
                random_array[i][j] = 1
    return random_array
```

```
create_random_state(10,50)
```

![Image : 10X10 random spin matrix](https://github.com/poppitypopper/ising-model/blob/main/state-charts/Figure_*1.png)

We define the "energy" of a particle in this system by summing up the spin values of its cardinal neighbours. 

$ \sigma $



