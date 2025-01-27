import ctypes
from time import time
import numpy as np
import numpy.ctypeslib as npct

# Load the shared library
metropolis_lib = ctypes.CDLL('./metropolis.so')

# Define the argument and return types for the `metropolis` function
metropolis_lib.metropolis.argtypes = [
    ctypes.POINTER(ctypes.POINTER(ctypes.c_int)),  # int **lattice
    ctypes.c_int,                                 # int N
    ctypes.c_int,                                 # int times
    ctypes.c_double,                              # double B
    ctypes.c_int,                                 # int J
    ctypes.c_int,                                 # int seed
    ctypes.c_int,                                 # int net_energy
    ctypes.c_int                                  # int net_spins
]
# Set the return type to a pointer to an array of `int`
metropolis_lib.metropolis.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_int))

# Wrapper function to convert numpy arrays and call the C function
def metropolis(lattice, times, B, J, seed):
    
    total_time = 0
    t0 = time()

    N = len(lattice)
    net_energy = 0
    net_spins = np.sum(lattice)

    # Convert the numpy array `lattice` to a ctypes-compatible pointer
    # lattice = lattice.astype(np.int32)
    # lattice_ptr = (ctypes.POINTER(ctypes.c_int) * N)()
    # for i in range(N):
    #     lattice_ptr[i] = lattice[i].ctypes.data_as(ctypes.POINTER(ctypes.c_int))
    
    
    lattice_ptr = np.ascontiguousarray(lattice, dtype=np.int32)
    print(f"{type(lattice_ptr)}")
    
    
    total_time += time() - t0
    
    
    # lattice_ptr = np.ctypeslib.as_ctypes(lattice)

    # Call the C function
    result_ptr = metropolis_lib.metropolis(
        lattice_ptr,
        ctypes.c_int(N),
        ctypes.c_int(times),
        ctypes.c_double(B),
        ctypes.c_int(J),
        ctypes.c_int(seed),
        ctypes.c_int(net_energy),
        ctypes.c_int(net_spins)
    )

    t0 = time()
    
    # Convert the result back into a numpy array (shape: 2 x times)
    result = np.zeros((2, times), dtype=np.int32)
    for i in range(2):
        result[i] = np.ctypeslib.as_array(result_ptr[i], shape=(times,))

    
    total_time += time() - t0
    print("Total time wasted: ", total_time)
    
    return np.array(result)
    # return np.ctypeslib.as_array(result_ptr, shape=(2, times))  # result_ptr  # result

# Example usage
if __name__ == '__main__':
    N = 100  # or 50
    times = 10
    B = 1.0
    J = 1
    seed = 42
    net_energy = 0
    net_spins = 0

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
