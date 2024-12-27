# Simulating lightly interacting particles using the Ising Model

_An implementation of the Ising Model in Python. This project has been made following several tutorials in Statistical Mechanics and Computational Methods._

## Project overview
The Ising Model is used to model the behaviour of interacting particles. Here it has been used to model the energy of a system consisting of spin-up and sping-down particles. In this model, the energy of a particle in a system is taken to be a function of the spins of the particles in it's neighbourhood. What the simulation below aims to show is that in a temperature bath (T), there is an equilibrium state where the total energy of the system stabilises.

## Explaining The Code

### Defining a random state
We first define a function that returns a random state with the state-size and probabilities pre-defined by the user.

```python3
import numpy as np
```

```python3
#Creates a square matrix of side N with P% up-spins
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

### Defining the energy of a microstate<sup>*</sup>

We define the energy of each particle in our system as the sum of the spins of its nearest neighbours. To start, we define the energy of each particle as the sum of the spins of each of its cardinal neighbours, i.e, up, down, left and right. Therefore, if we generate a 3x3 matrix, the energy of the particle at (1,1) is the the sum of the spins at (0,1), (1,0), (1,2) and (2,1).

![Image : 10X10 random spin matrix](https://github.com/poppitypopper/ising-model/blob/main/state-charts/Frame_4***.png)

To calculate the energy of a state, we simply sum up the energies of the constituent particles. This becomes computationally taxing as our states grow in size, or if our problem grows in dimensions. Instead, we convolve a kernel with our matrix to get an array with the energies of each particle.

```python3
from scipy.ndimage import generate_binary_structure, convolve
```
For our simulation, since we only consider the interactions from the immediate cardinal neighbours, we generate a "binary structure", or a kernel, with dimensionality '2' and directionality '1' with the center 'voided'. Graphically, it can be represented as such : 

![Image : Kernel](https://github.com/poppitypopper/ising-model/blob/main/state-charts/Frame%202.png)

When convolved with our state, we get an array containing the energies of all the particles. It is then trivial to sum up the array to get the energy of the microstate.
> <sup>*</sup> A _microstate_ is a state the system is in during a time-step. If our simulation has 100,000 time steps, the system 'goes through' 100,000 microstates, with each state being 'different' than the other, and the states coming after being in some sense, dependent on the states before.

We define a function to find the energy of a passed array (microstate) 

```python3
def calculate_energy(arr):
    kern = generate_binary_structure(2,1)
    kern[1][1] = False
    energies = convolve(arr, kern, mode='constant', cval=0)
    return energies.sum()
```

### The Metropolis Algorithm

We have the tools to generate a state and find its energy, we begin with the algorithm for the simulation.
1) Generate a random state
2) Flip a random spin
3) Measure the energy of the system before and after the flip
4) If E<sub>after flip</sub> < E<sub>before flip</sub>, commit the spin flip
5) If E<sub>after flip</sub> > E<sub>before flip</sub>, commit to the flip with the probability of e<sup>(E<sub>before</sub> - E<sub>after</sub>)/kT</sup>

```python3
def metropolis(beta, matrix_size, up_spin_percent, max_epochs):
    state = create_random_state(matrix_size, up_spin_percent)
    steps = []  
    energies = []  

    for step in range(max_epochs):
        Ei = calculate_energy(state)  

        # Flip a random spin
        x, y = np.random.randint(0, matrix_size, size=2)
        state[x, y] *= -1  

        
        Ef = calculate_energy(state)

        if Ef > Ei:
            probability = np.exp(-(beta) * (Ef - Ei))
            if np.random.rand() >= probability:
                state[x, y] *= -1  # Revert the spin flip if not accepted

        steps.append(step)
        energies.append(calculate_energy(state))

    final_state = state
    return steps, energies, final_state
```
### Outcome

The test can be run for several combinations of temperature and epochs to arrive at logical conclusions about the system. 

```python3

beta = 0.7
matrix_size = 100
up_spin_percent = 50
max_epochs = 100000

steps, energies, final_state = metropolis(beta, matrix_size, up_spin_percent, max_epochs)

print_array(final_state)
plt.plot(steps, energies, label="Energy")
plt.xlabel("Steps")
plt.ylabel("Energy")
plt.title("Energy vs. Steps")
plt.legend()
plt.show()

```
![Image : metropolis(0.7, 100, 50, 100000)](https://github.com/poppitypopper/ising-model/blob/main/state-charts/100%2C000_epochs.png)


