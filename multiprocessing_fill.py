import numpy as np
from multiprocessing import Pool

# Función para comparar fragmentos de secuencias
def compare_sequences(args):
    seq1_chunk, seq2 = args  # Desempaqueta los argumentos
    chunk_size = len(seq1_chunk)  # Obtiene el tamaño del fragmento de la secuencia 1
    dotplot_chunk = np.zeros((chunk_size, len(seq2)), dtype=np.uint8)  # Inicializa un arreglo de ceros para almacenar el dotplot
    for i in range(chunk_size):  # Itera sobre cada elemento del fragmento de la secuencia 1
        for j in range(len(seq2)):  # Itera sobre cada elemento de la secuencia 2
            dotplot_chunk[i, j] = 1 if seq1_chunk[i] == seq2[j] else 0  # Llena el dotplot_chunk con 1 si los elementos coinciden, de lo contrario con 0
    return dotplot_chunk  # Retorna el fragmento del dotplot

# Función para llenar el dotplot usando multiprocessing
def fill_dotplot_multiprocessing(seq1, seq2, dotplot, num_cores):
    chunk_size = len(seq1) // num_cores  # Calcula el tamaño de cada fragmento basado en el número de núcleos

    # Crear fragmentos de la secuencia 1 para distribuir entre los procesos
    seq1_chunks = [seq1[i * chunk_size: (i + 1) * chunk_size] for i in range(num_cores)]
    
    # Si hay restos, añadirlos al último fragmento
    if len(seq1) % num_cores != 0:
        seq1_chunks[-1].extend(seq1[num_cores * chunk_size:])

    with Pool(num_cores) as pool:  # Crea un grupo de procesos
        results = pool.map(compare_sequences, [(chunk, seq2) for chunk in seq1_chunks])  # Mapea la función compare_sequences a los fragmentos de seq1

    # Combina los resultados en el dotplot original
    start_row = 0
    for result in results:  # Itera sobre los resultados de los procesos
        dotplot[start_row:start_row + result.shape[0], :] = result  # Copia el resultado en la posición correspondiente del dotplot
        start_row += result.shape[0]  # Actualiza la fila de inicio para el siguiente fragmento

