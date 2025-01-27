import ctypes
import numpy as np
from tqdm import tqdm, trange

# Load the shared library
metropolis_lib = ctypes.CDLL('./metropolis.so')


# Define the argument and return types for the `metropolis` function
input_types = [
    ctypes.POINTER(ctypes.c_int),  # int *lattice
    ctypes.c_int,                  # int N
    ctypes.c_int,                  # int times
    ctypes.c_double,               # double B
    ctypes.c_int,                  # int J
    ctypes.c_int,                  # int seed
    ctypes.c_int,                  # int net_energy
    ctypes.c_int                   # int net_spins
]

metropolis_lib.metropolis.argtypes = input_types
# Set the return type to a pointer to an array of `int`
metropolis_lib.metropolis.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_int))

# Define the argument and return types for the `metropolis` function
metropolis_lib.metropolis_seq.argtypes = input_types
# Set the return type to a pointer to an array of `int`
metropolis_lib.metropolis_seq.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_int))

metropolis_lib.get_energy.argtypes = [
    ctypes.POINTER(ctypes.c_int),  # int *lattice
    ctypes.c_int,                  # int N
    ctypes.c_int                   # int J
]
metropolis_lib.get_energy.restype = ctypes.c_int








def get_energy(lattice, J = -1):
    N = len(lattice)
    lattice = lattice.astype(np.int32).ravel()
    lattice_ptr = lattice.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
    return metropolis_lib.get_energy(lattice_ptr, N, J)



def metropolis(lattice, times, B, J, seed, sequential=True):
    if sequential and times > 1e5:
        raise ValueError("times is too large for sequential")
    
    N = len(lattice)

    lattice = lattice.astype(np.int32).ravel()
    lattice_ptr = lattice.ctypes.data_as(ctypes.POINTER(ctypes.c_int))

    net_energy = metropolis_lib.get_energy(lattice_ptr, N, J)
    net_spins = np.sum(lattice)
    
    metropolis_func = metropolis_lib.metropolis_seq if sequential else metropolis_lib.metropolis

    # Call the C function
    result_ptr = metropolis_func(
        lattice_ptr,
        ctypes.c_int(N),
        ctypes.c_int(times),
        ctypes.c_double(B),
        ctypes.c_int(J),
        ctypes.c_int(seed),
        ctypes.c_int(net_energy),
        ctypes.c_int(net_spins)
    )

    # bring lattice_ptr and results back to numpy array
    energies = np.ctypeslib.as_array(result_ptr[0], shape=(times,))
    magnetization = np.ctypeslib.as_array(result_ptr[1], shape=(times,))
    lattice = np.ctypeslib.as_array(lattice_ptr, shape=(N*N,)).reshape((N, N))
    return energies, magnetization, lattice


def abs(lattice, times, Bs, J, seed, sequential=True):
    N = len(lattice)
    
    # Convert lattice to C type
    lattice = lattice.astype(np.int32).ravel()
    lattice_ptr = lattice.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
    
    # Initialize arrays to store energies and magnetization for each B
    all_energies = np.zeros((len(Bs), times))
    all_magnetizations = np.zeros((len(Bs), times))
    
    # Do Metropolis simulation for each B
    for i, B in enumerate(tqdm(Bs)):
        net_energy = metropolis_lib.get_energy(lattice_ptr, N, J)
        net_spins = np.sum(lattice)
        
        metropolis_func = metropolis_lib.metropolis_seq if sequential else metropolis_lib.metropolis
        
        # Call the C function
        result_ptr = metropolis_func(
            lattice_ptr,
            ctypes.c_int(N),
            ctypes.c_int(times),
            ctypes.c_double(B),
            ctypes.c_int(J),
            ctypes.c_int(seed),
            ctypes.c_int(net_energy),
            ctypes.c_int(net_spins)
        )
        
        # Get energies and magnetization from result
        energies = np.ctypeslib.as_array(result_ptr[0], shape=(times,))
        magnetization = np.ctypeslib.as_array(result_ptr[1], shape=(times,))
        
        # Store in all_energies and all_magnetizations arrays
        all_energies[i] = energies
        all_magnetizations[i] = magnetization
    
    # Convert lattice back to numpy array
    lattice = np.ctypeslib.as_array(lattice_ptr, shape=(N*N,)).reshape((N, N))
    
    return all_energies, all_magnetizations, lattice



# Example usage
if __name__ == '__main__':
    N = 100  # or 50
    times = 10
    B = 1.0
    J = 1
    seed = 42

    # Create a random 100x100 matrix with entries -1 or 1
    lattice = np.random.choice([-1, 1], size=(N, N))

    # Call the `metropolis` function
    energies, magnetization = metropolis(lattice, times, B, J, seed)
    # result = metropolis(lattice, times, B, J, seed)

    # Print the result
    print("Energies and magnetization matrix:")
    # print(result)
    print(energies)
    print(magnetization)
