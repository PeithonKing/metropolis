#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int get_energy(int *lattice, int N, int J) {
    int energy = 0;
    for (int x = 0; x < N; x++) {
        for (int y = 0; y < N; y++) {
            int spin = lattice[x * N + y];
            energy += J * spin * (
                lattice[((x - 1 + N) % N) * N + y] + // up
                lattice[((x + 1) % N) * N + y] + // down
                lattice[x * N + ((y - 1 + N) % N)] + // left
                lattice[x * N + ((y + 1) % N)]  // right
            );
        }
    }
    return energy;
}


int **metropolis(
    int *lattice,  // Now a flattened 1D array
    int N,
    int times,
    double B,
    int J,
    int seed,
    int net_energy,
    int net_spins
){
    srand(seed);

    // Allocate memory for energies and magnetization
    int **energies_magnetization = (int **)malloc(2 * sizeof(int *));
    energies_magnetization[0] = (int *)malloc(times * sizeof(int));
    energies_magnetization[1] = (int *)malloc(times * sizeof(int));

    for (int i = 0; i < times; i++) {
        int x = rand() % N;
        int y = rand() % N;

        // Calculate the indices of the neighbors in the flattened array
        int neighbour_sum = 0;
        neighbour_sum += lattice[((x - 1 + N) % N) * N + y]; // up neighbour
        neighbour_sum += lattice[((x + 1 + N) % N) * N + y]; // down neighbour
        neighbour_sum += lattice[x * N + (y - 1 + N) % N]; // left neighbour
        neighbour_sum += lattice[x * N + (y + 1 + N) % N]; // right neighbour

        int delta_E = -4 * J * lattice[x * N + y] * neighbour_sum;

        // printf("[%d, %d], delta_E: %d", x, y, delta_E);
        // Apply the Metropolis criterion
        if (delta_E <= 0 || (delta_E > 0 && exp(-B * delta_E) > (double)rand() / RAND_MAX)){
            lattice[x * N + y] *= -1;  // Flip the spin
            net_energy += delta_E;
            net_spins += 2 * lattice[x * N + y];  // Update net spins
            // printf("[%d, %d, 1], delta_E: %d\n", x, y, delta_E);
            // printf("    [%d, %d, 1],\n", x, y);
        }
        else{
            // printf("[%d, %d, 0], delta_E: %d\n", x, y, delta_E);
            // printf("    [%d, %d, 0],\n", x, y);
        }

        // Store energy and magnetization
        energies_magnetization[0][i] = net_energy;
        energies_magnetization[1][i] = net_spins;

        // printf("\n");
    }

    return energies_magnetization;
}


int **metropolis_seq(
    int *lattice,  // Now a flattened 1D array
    int N,
    int times,
    double B,
    int J,
    int seed,
    int net_energy,
    int net_spins
){
    srand(seed);

    // Allocate memory for energies and magnetization
    int **energies_magnetization = (int **)malloc(2 * sizeof(int *));
    energies_magnetization[0] = (int *)malloc(times * N * N * sizeof(int));
    energies_magnetization[1] = (int *)malloc(times * N * N * sizeof(int));

    for (int i = 0; i < times; i++) {
        // Iterate over all lattice sites
        for (int x = 0; x < N; x++) {
            for (int y = 0; y < N; y++) {

                // Calculate the indices of the neighbors in the flattened array
                int neighbour_sum = 0;
                neighbour_sum += lattice[((x - 1 + N) % N) * N + y]; // up neighbour
                neighbour_sum += lattice[((x + 1 + N) % N) * N + y]; // down neighbour
                neighbour_sum += lattice[x * N + (y - 1 + N) % N]; // left neighbour
                neighbour_sum += lattice[x * N + (y + 1 + N) % N]; // right neighbour

                int delta_E = -4 * J * lattice[x * N + y] * neighbour_sum;

                // Apply the Metropolis criterion
                if (delta_E <= 0 || (delta_E > 0 && exp(-B * delta_E) > (double)rand() / RAND_MAX)){
                    // printf("    [%d, %d, %d]  # ,\n", x, y, lattice[x * N + y]);
                    lattice[x * N + y] *= -1;  // Flip the spin
                    net_energy += delta_E;
                    net_spins += 2 * lattice[x * N + y];  // Update net spins
                    // printf("[%d, %d, 1], delta_E: %d\n", x, y, delta_E);
                }
                else{
                    // printf("[%d, %d, 0], delta_E: %d\n", x, y, delta_E);
                    // printf("    [%d, %d, ]  # ,\n", x, y);
                }

            }
        }

        // Store energy and magnetization after each iteration over all sites
        energies_magnetization[0][i] = net_energy;
        energies_magnetization[1][i] = net_spins;
    }

    return energies_magnetization;
}

