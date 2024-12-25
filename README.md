# Simulating lightly interacting particles using the Ising Model

_An implementation of the Ising Model in Python. This project has been made following several tutorials in Statistical Mechanics and Computational Methods._

## Project overview
The Ising Model is used to model the behaviour of interacting particles. In this specific project it has been used to model the energy of a system consisting of spin-up and sping-down particles. In this model, the energy of a particle in a system is taken to be a function of the spins of the particles in it's neighbourhood. What the simulation below aims to show is that in a temperature bath (T), there is an equilibrium state where the total energy of the system stabilises.

## Explaining The Code

### Defining a random state
We first define a function that returns a random state with the state-size and probabilities pre-defined by the user.

```python3
import numpy as np
```

```python3
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

```python3
create_random_state(10,50)
```

![Image : 10X10 random spin matrix](https://github.com/poppitypopper/ising-model/blob/main/state-charts/Figure_*1.png)

### Defining the energy of a microstate

We define the energy of each particle in our system as the sum of the spins of its nearest neighbours. To start, we define the energy of each particle as the sum of the spins of each of its cardinal neighbours, i.e, up, down, left and right. Therefore, if we generate a 3x3 matrix, the energy of the particle at (1,1) is the the sum of the spins at (0,1), (1,0), (1,2) and (2,1).

![Image : 10X10 random spin matrix](https://github.com/poppitypopper/ising-model/blob/main/state-charts/Frame_4***.png)

To calculate the energy of a state, we simply sum up the energies of the constituent particles. This becomes computationally taxing as our states grow in size, or if our problem grows in dimensions. Instead of the naive approach, we utilise the convolve function in the SciPy library.

```python3
from scipy.ndimage import generate_binary_structure, convolve
```
For our simulation, since we only consider the interactions from the immediate cardinal neighbours, we generate a "binary structure" with dimensionality '2' and directionality '1' with the center 'voided'. Graphically, it can be represented as such : 

![Image : Kernel](https://github.com/poppitypopper/ising-model/blob/main/state-charts/Frame%202.png)

When convolved with our state, we get a matrix with the 



