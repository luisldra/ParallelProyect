from mpi4py import MPI
import numpy as np

def fill_dotplot_mpi(Secuencia1, Secuencia2):
    # Inicializa la comunicación MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()  # Obtiene el rango (identificador) del proceso actual
    size = comm.Get_size()  # Obtiene el número total de procesos
    
    n1 = len(Secuencia1)
    n2 = len(Secuencia2)
    
    # Calcula el tamaño de los fragmentos para cada proceso
    chunk_size = n1 // size
    remainder = n1 % size
    
    # Determina el rango de índices que cada proceso manejará para Secuencia1
    if rank < remainder:
        start = rank * (chunk_size + 1)
        end = start + chunk_size + 1
    else:
        start = rank * chunk_size + remainder
        end = start + chunk_size
    
    # Cada proceso obtiene su fragmento de Secuencia1
    local_Secuencia1 = Secuencia1[start:end]
    
    # Cada proceso calcula su porción del dotplot comparando su fragmento de Secuencia1 con toda Secuencia2
    local_dotplot = np.zeros((len(local_Secuencia1), n2), dtype=np.uint8)
    for i in range(len(local_Secuencia1)):
        for j in range(len(Secuencia2)):
            local_dotplot[i, j] = 1 if local_Secuencia1[i] == Secuencia2[j] else 0
    
    # Recolecta todos los dotplots locales en el proceso maestro
    all_dotplots = comm.gather(local_dotplot, root=0)
    
    if rank == 0:
        # El proceso maestro combina todas las porciones del dotplot
        dotplot = np.zeros((n1, n2), dtype=np.uint8)
        for i in range(size):
            if i < remainder:
                start_i = i * (chunk_size + 1)
                end_i = start_i + chunk_size + 1
            else:
                start_i = i * chunk_size + remainder
                end_i = start_i + chunk_size
            
            dotplot[start_i:end_i, :] = all_dotplots[i]
        return dotplot