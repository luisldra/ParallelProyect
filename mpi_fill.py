from mpi4py import MPI  # Importa la librería mpi4py para utilizar MPI
import numpy as np  # Importa la librería numpy para manipulación de arreglos

def fill_dotplot_mpi(Secuencia1, Secuencia2):
    # Inicializa la comunicación MPI
    comm = MPI.COMM_WORLD  # Obtiene el comunicador global
    rank = comm.Get_rank()  # Obtiene el rango (identificador) del proceso actual
    size = comm.Get_size()  # Obtiene el número total de procesos
    
    n1 = len(Secuencia1)  # Longitud de la Secuencia1
    n2 = len(Secuencia2)  # Longitud de la Secuencia2
    
    # Calcula el tamaño de los fragmentos para cada proceso
    chunk_size = n1 // size  # Tamaño base de cada fragmento
    remainder = n1 % size  # Resto de la división para distribuirlo entre los primeros procesos
    
    # Determina el rango de índices que cada proceso manejará para Secuencia1
    if rank < remainder:
        start = rank * (chunk_size + 1)  # Índice inicial del fragmento para procesos con resto
        end = start + chunk_size + 1  # Índice final del fragmento para procesos con resto
    else:
        start = rank * chunk_size + remainder  # Índice inicial del fragmento para procesos sin resto
        end = start + chunk_size  # Índice final del fragmento para procesos sin resto
    
    # Cada proceso obtiene su fragmento de Secuencia1
    local_Secuencia1 = Secuencia1[start:end]  # Fragmento de Secuencia1 asignado a cada proceso
    
    # Cada proceso calcula su porción del dotplot comparando su fragmento de Secuencia1 con toda Secuencia2
    local_dotplot = np.zeros((len(local_Secuencia1), n2), dtype=np.uint8)  # Inicializa la matriz local del dotplot con ceros
    for i in range(len(local_Secuencia1)):  # Itera sobre cada elemento del fragmento de Secuencia1
        for j in range(len(Secuencia2)):  # Itera sobre cada elemento de Secuencia2
            local_dotplot[i, j] = 1 if local_Secuencia1[i] == Secuencia2[j] else 0  # Llena el local_dotplot con 1 si los elementos coinciden, de lo contrario con 0
    
    # Recolecta todos los dotplots locales en el proceso maestro
    all_dotplots = comm.gather(local_dotplot, root=0)  # Envía los dotplots locales al proceso maestro
    
    if rank == 0:
        # El proceso maestro combina todas las porciones del dotplot
        dotplot = np.zeros((n1, n2), dtype=np.uint8)  # Inicializa la matriz completa del dotplot con ceros
        for i in range(size):  # Itera sobre cada proceso
            if i < remainder:
                start_i = i * (chunk_size + 1)  # Índice inicial del fragmento para procesos con resto
                end_i = start_i + chunk_size + 1  # Índice final del fragmento para procesos con resto
            else:
                start_i = i * chunk_size + remainder  # Índice inicial del fragmento para procesos sin resto
                end_i = start_i + chunk_size  # Índice final del fragmento para procesos sin resto
            
            dotplot[start_i:end_i, :] = all_dotplots[i]  # Copia el dotplot local en la posición correspondiente del dotplot completo
        return dotplot  # Retorna el dotplot completo desde el proceso maestro
