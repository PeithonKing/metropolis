import os
import numpy as np
import argparse
import wrapper
from tqdm import tqdm, trange

# Set up argument parser
parser = argparse.ArgumentParser(description="Run the Metropolis algorithm.")
parser.add_argument('--seed', type=int, default=23, help="Random seed (default: 23)")
parser.add_argument('--times', type=int, default=1000_000, help="Number of iterations (default: 10,00,000)")
parser.add_argument('--N', type=int, default=64, help="Lattice size N (default: 100)")
parser.add_argument('--J', type=int, default=-1, help="Interaction strength J (default: -1)")
parser.add_argument('--n_images', type=int, default=1000, help="Number of images to generate (default: 1000)")
parser.add_argument('--temp', type=float, default=0., help="Temperature (default: 7)")

args = parser.parse_args()

# Extract values from args
seed = args.seed
times = args.times
N = args.N
J = args.J
n_images = args.n_images
temp = args.temp
dir_path = f"final_data/{n_images}_{seed}_{N}_{J}/"

beta = 1 / temp

store = []
for i in trange(n_images):
    np.random.seed(seed)
    lattice = np.ones((N, N))
    if J < 0: threshold = 0.5
    else: threshold = np.random.choice([0.1, 0.9])
    lattice[np.random.rand(N, N) < threshold] = -1

    lattice = wrapper.metropolis_lowmem(lattice, times, beta, J, seed)
    
    # typecast lattice to boolean, -1 s to 0 and 1s to 1s
    lattice[lattice == -1] = 0
    lattice = lattice.astype(bool)
    
    store.append(lattice)

    seed += 1

os.makedirs(dir_path, exist_ok=True)
np.save(f"{dir_path}{temp}.npy", np.array(store))
