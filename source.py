import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve, generate_binary_structure

# Creates a random square matrix of side N with P% of spots as 1 and the others as -1
def create_random_state(N, P):
    random_array = np.random.random((N, N))
    random_array = np.where(random_array > (P / 100), -1, 1)
    return random_array

# Prints an array representation
def print_array(arr):
    plt.imshow(arr, cmap="coolwarm")
    plt.colorbar()
    plt.title("Final State of the System")
    plt.show()

# Calculation of energy of a passed array
def calculate_energy(arr):
    kernel = generate_binary_structure(2, 1).astype(int)
    kernel[1, 1] = 0  # Center is excluded
    interaction = convolve(arr, kernel, mode='constant', cval=0)
    total_energy = -(arr * interaction).sum() / 2  # Avoid double-counting
    return total_energy

# Plotting the results
def get_plots(epochs, energies, average_spins):
    # Plot energy vs. epochs
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(epochs, energies, label="Energy", color="blue")
    plt.xlabel("Steps")
    plt.ylabel("Energy")
    plt.title("Energy vs. Steps")
    plt.legend()

    # Plot average spin vs. epochs
    plt.subplot(1, 2, 2)
    plt.plot(epochs, average_spins, label="Average Spin", color="red")
    plt.xlabel("Steps")
    plt.ylabel("Average Spin")
    plt.title("Average Spin vs. Steps")
    plt.legend()

    plt.tight_layout()
    plt.show()

# Metropolis algorithm (naive)
def metropolis(beta, matrix_size, up_spin_percent, max_epochs):
    state = create_random_state(matrix_size, up_spin_percent)
    epochs = []
    energies = []
    average_spins = []

    for epoch in range(max_epochs):
        # Compute current energy
        Ei = calculate_energy(state)

        # Flip a random spin
        x, y = np.random.randint(0, matrix_size, size=2)
        state[x, y] *= -1  # Trial flip

        # Compute new energy
        Ef = calculate_energy(state)

        # Metropolis acceptance criterion
        if Ef > Ei:
            probability = np.exp(-beta * (Ef - Ei))
            if np.random.uniform(0, 1) >= probability:
                state[x, y] *= -1  # Revert the spin flip if not accepted

        # Record data for plotting
        epochs.append(epoch)
        energies.append(calculate_energy(state))
        average_spins.append(state.mean())  # Compute average spin at this step

    final_state = state
    return epochs, energies, average_spins, final_state
