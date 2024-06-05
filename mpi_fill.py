from mpi4py import MPI
import numpy as np

def fill_dotplot_mpi(Secuencia1, Secuencia2):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    n = len(Secuencia1)
    chunk_size = n // size
    remainder = n % size
    
    if rank < remainder:
        start = rank * (chunk_size + 1)
        end = start + chunk_size + 1
    else:
        start = rank * chunk_size + remainder
        end = start + chunk_size
    
    if rank == 0:
        # Master process: send portions of Secuencia1 and Secuencia2 to worker processes
        for i in range(1, size):
            if i < remainder:
                start_i = i * (chunk_size + 1)
                end_i = start_i + chunk_size + 1
            else:
                start_i = i * chunk_size + remainder
                end_i = start_i + chunk_size
            comm.send(Secuencia1[start_i:end_i], dest=i, tag=i)
            comm.send(Secuencia2, dest=i, tag=i+size)
        
        local_Secuencia1 = Secuencia1[start:end]
        local_Secuencia2 = Secuencia2
    else:
        # Worker processes: receive portions of Secuencia1 and Secuencia2
        local_Secuencia1 = comm.recv(source=0, tag=rank)
        local_Secuencia2 = comm.recv(source=0, tag=rank+size)
    
    # Each process calculates its portion of the dotplot
    local_dotplot = np.zeros((len(local_Secuencia1), len(local_Secuencia2)), dtype=np.uint8)
    for i in range(len(local_Secuencia1)):
        for j in range(len(local_Secuencia2)):
            local_dotplot[i, j] = 1 if local_Secuencia1[i] == local_Secuencia2[j] else 0
    
    # Gather all local dotplots at the master process
    all_dotplots = comm.gather(local_dotplot, root=0)
    
    if rank == 0:
        # Master process: combine all portions of the dotplot
        dotplot = np.vstack(all_dotplots)
        return dotplot
