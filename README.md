# Metropolis Algorithm Implementation

This repository provides an implementation of the **Metropolis algorithm** in **C**, with a Python wrapper to interface with the C code. The algorithm is typically used for simulating systems in statistical mechanics and is applied here for a simple lattice-based model (e.g., Ising model).

## Installation

To use this code, you need to first compile the C implementation into a shared library. You can do this with the following command:

```bash
gcc -shared -fPIC -std=c99 -o metropolis.so metropolis.c -lm
```

This will generate a `metropolis.so` shared library, which you can then use in Python.

## Usage

Once the shared library is compiled, you can use it from Python via the wrapper. Below is an example script that demonstrates how to use the wrapper to run the Metropolis algorithm on a 100x100 lattice.

```python
import numpy as np
import wrapper

# Set parameters
seed = 23
times = 1000_000  # Number of Metropolis steps
N = 100  # Lattice size (100x100)
J = -1  # Interaction strength (negative for ferromagnetic)
temp = 2  # Temperature (T=4.5 is the critical temperature for the Ising model)

beta = 1 / temp

# Initialize the lattice with random spins (75% up, 25% down)
np.random.seed(seed)
lattice = np.ones((N, N))
lattice[np.random.rand(N, N) < 0.25] = -1

# Run the Metropolis algorithm
energies, magnetization, updated_lattice = wrapper.metropolis(lattice, times, beta, J, seed)

# Plot energies, magnetization, and the updated lattice
```
