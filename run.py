import os
import numpy as np
import argparse
from wrapper import metropolis
from tqdm import tqdm, trange

# Set up argument parser
parser = argparse.ArgumentParser(description="Run the Metropolis algorithm.")
parser.add_argument('--seed', type=int, default=23, help="Random seed (default: 23)")
parser.add_argument('--times', type=int, default=10_00_000, help="Number of iterations (default: 10,00,000)")
parser.add_argument('--N', type=int, default=100, help="Lattice size N (default: 100)")
parser.add_argument('--J', type=int, default=-1, help="Interaction strength J (default: -1)")
parser.add_argument('--n_images', type=int, default=1000, help="Number of images to generate (default: 1000)")
parser.add_argument('--temp', type=float, default=7, help="Temperature (default: 7)")

args = parser.parse_args()

# Extract values from args
seed = args.seed
times = args.times
N = args.N
J = args.J
n_images = args.n_images
temp = args.temp

beta = 1 / temp
    
# Prepare file path
dir_path = f"generated_data/{N}_{J}/{temp}/"

# Create directories if they don't exist
os.makedirs(dir_path, exist_ok=True)

# Main loop
for i in trange(n_images):
    np.random.seed(seed)
    lattice = np.ones((N, N))
    lattice[np.random.rand(N, N) < 0.25] = -1

    energies, magnetization, lattice = metropolis(lattice, times, beta, J, seed, sequential=False)
    np.save(
        f"{dir_path}{i}.npy",
        {
            'energies': energies,
            'magnetization': magnetization,
            'lattice': lattice
        }
    )

    seed += 1
