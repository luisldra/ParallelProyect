import threading
import numpy as np

def fill_dotplot_hilos(Secuencia1, Secuencia2, dotplot):
    def worker(start, end):
        for i in range(start, end):
            for j in range(len(Secuencia2)):
                dotplot[i, j] = 1 if Secuencia1[i] == Secuencia2[j] else 0

    n_threads = 4
    chunk_size = len(Secuencia1) // n_threads
    threads = []
    
    for n in range(n_threads):
        start = n * chunk_size
        end = (n + 1) * chunk_size if n != n_threads - 1 else len(Secuencia1)
        thread = threading.Thread(target=worker, args=(start, end))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
