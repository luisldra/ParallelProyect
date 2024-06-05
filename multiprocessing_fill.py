from multiprocessing import Process, Array
import numpy as np

def fill_dotplot_multiprocessing(Secuencia1, Secuencia2, dotplot):
    def worker(start, end, dotplot, Secuencia1, Secuencia2):
        for i in range(start, end):
            for j in range(len(Secuencia2)):
                dotplot[i * len(Secuencia2) + j] = 1 if Secuencia1[i] == Secuencia2[j] else 0

    n_processes = 4
    chunk_size = len(Secuencia1) // n_processes
    dotplot = Array('B', len(Secuencia1) * len(Secuencia2), lock=False)
    processes = []

    for n in range(n_processes):
        start = n * chunk_size
        end = (n + 1) * chunk_size if n != n_processes - 1 else len(Secuencia1)
        process = Process(target=worker, args=(start, end, dotplot, Secuencia1, Secuencia2))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
    
    dotplot = np.frombuffer(dotplot.get_obj(), dtype=np.uint8).reshape((len(Secuencia1), len(Secuencia2)))
