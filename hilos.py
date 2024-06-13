import threading  # Importa el módulo de threading para crear y manejar hilos.
import numpy as np  # Importa el módulo numpy para manejar matrices de manera eficiente.

# Define la función fill_dotplot_hilos que toma las secuencias Secuencia1 y Secuencia2,
# una matriz dotplot para llenar, y el número de hilos a usar (por defecto 4).
def fill_dotplot_hilos(Secuencia1, Secuencia2, dotplot, n_threads=4):
    
    # Define una función interna worker que será ejecutada por cada hilo.
    # Esta función toma un rango de índices (start, end) y compara las secuencias dentro de ese rango.
    def worker(start, end):
        for i in range(start, end):  # Itera sobre el rango de índices asignado al hilo.
            for j in range(len(Secuencia2)):  # Itera sobre todos los índices de Secuencia2.
                # Llena el dotplot con 1 si los caracteres en Secuencia1 y Secuencia2 son iguales, de lo contrario con 0.
                dotplot[i, j] = 1 if Secuencia1[i] == Secuencia2[j] else 0

    # Calcula el tamaño de cada segmento que cada hilo procesará.
    chunk_size = len(Secuencia1) // n_threads
    threads = []  # Lista para mantener referencia a los hilos creados.
    
    # Crea y lanza los hilos.
    for n in range(n_threads):
        start = n * chunk_size  # Calcula el índice de inicio del segmento para este hilo.
        # Calcula el índice de fin del segmento para este hilo.
        # El último hilo se asegura de procesar hasta el final de Secuencia1.
        end = (n + 1) * chunk_size if n != n_threads - 1 else len(Secuencia1)
        # Crea un nuevo hilo para ejecutar la función worker con los argumentos start y end.
        thread = threading.Thread(target=worker, args=(start, end))
        threads.append(thread)  # Añade el hilo a la lista de hilos.
        thread.start()  # Inicia el hilo.
    
    # Espera a que todos los hilos terminen su ejecución.
    for thread in threads:
        thread.join()  # Espera a que el hilo termine.
