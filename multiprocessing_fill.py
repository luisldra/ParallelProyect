import numpy as np
from multiprocessing import Pool

def compare_sequences(args):
    seq1_chunk, seq2 = args
    chunk_size = len(seq1_chunk)
    dotplot_chunk = np.zeros((chunk_size, len(seq2)), dtype=np.uint8)
    for i in range(chunk_size):
        for j in range(len(seq2)):
            dotplot_chunk[i, j] = 1 if seq1_chunk[i] == seq2[j] else 0
    return dotplot_chunk

def fill_dotplot_multiprocessing(seq1, seq2, dotplot, num_cores):
    chunk_size = len(seq1) // num_cores

    # Crear fragmentos de la secuencia 1 para distribuir entre los procesos
    seq1_chunks = [seq1[i * chunk_size: (i + 1) * chunk_size] for i in range(num_cores)]
    
    # Si hay restos, añadirlos al último fragmento
    if len(seq1) % num_cores != 0:
        seq1_chunks[-1].extend(seq1[num_cores * chunk_size:])

    with Pool(num_cores) as pool:
        results = pool.map(compare_sequences, [(chunk, seq2) for chunk in seq1_chunks])

    # Combina los resultados en el dotplot original
    start_row = 0
    for result in results:
        dotplot[start_row:start_row + result.shape[0], :] = result
        start_row += result.shape[0]
