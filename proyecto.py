import argparse
import numpy as np
import time
import matplotlib.pyplot as plt
from mpi4py import MPI
import json
from utils import merge_sequences_from_fasta
from secuencial import fill_dotplot_secuencial
from hilos import fill_dotplot_hilos
from multiprocessing_fill import fill_dotplot_multiprocessing
from mpi_fill import fill_dotplot_mpi

def parse_args():
    parser = argparse.ArgumentParser(description="Dotplot Generator")
    parser.add_argument("--file1", type=str, required=True, help="Path to the first FASTA file")
    parser.add_argument("--file2", type=str, required=True, help="Path to the second FASTA file")
    parser.add_argument("--estrategia", type=str, choices=["secuencial", "hilos", "multiprocessing", "mpi"], required=True, help="Paralelización a utilizar")
    parser.add_argument("--filter", type=int, default=128, help="Filter size")
    return parser.parse_args()

def visualize_dotplot(dotplot, estrategia):
    try:
        output_file = f"dotplot_{estrategia}.png"
        plt.imshow(dotplot, cmap='gray_r', interpolation='none')
        plt.title(f"Dotplot {estrategia}")
        plt.xlabel('Sequence 2')
        plt.ylabel('Sequence 1')
        plt.savefig(output_file)
        plt.close()
        print(f"Dotplot saved as {output_file}")
    except Exception as e:
        print(f"Error visualizing dotplot: {e}")

def save_times(data, estrategia, tiempos, num_processes):
    if estrategia not in data:
        data[estrategia] = {}
    if estrategia == 'mpi':
        if num_processes not in data[estrategia]:
            data[estrategia][num_processes] = []
        data[estrategia][num_processes] = {
            "carga_datos": tiempos["carga_datos"],
            "ejecucion": tiempos["ejecucion"],
            "visualizacion": tiempos["visualizacion"],
            "total": tiempos["total"],
            "num_processes": num_processes
        }
    else:
        data[estrategia] = {
            "carga_datos": tiempos["carga_datos"],
            "ejecucion": tiempos["ejecucion"],
            "visualizacion": tiempos["visualizacion"],
            "total": tiempos["total"],
            "num_processes": num_processes
        }
    with open('pruebas.json', 'w') as f:
        json.dump(data, f, indent=4)

def load_times():
    try:
        with open('pruebas.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def main():
    args = parse_args()

    # Inicializa la comunicación MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Medición de tiempos
    tiempos = {}

    if rank == 0:
        # Leer y combinar las secuencias
        start_time = time.time()
        try:
            Secuencia1 = merge_sequences_from_fasta(args.file1)
            Secuencia2 = merge_sequences_from_fasta(args.file2)
        except Exception as e:
            print(f"Error reading sequences: {e}")
            return
        tiempos['carga_datos'] = time.time() - start_time

        if not Secuencia1 or not Secuencia2:
            print("Error: One of the sequences is empty.")
            return

        # Usar solo las primeras bases según el filtro
        Secuencia1 = Secuencia1[:args.filter]
        Secuencia2 = Secuencia2[:args.filter]

        # Inicializa la matriz de dotplot (solo en el proceso maestro)
        dotplot = np.zeros((len(Secuencia1), len(Secuencia2)), dtype=np.uint8)
        print("La matriz de resultado tiene tamaño:", dotplot.shape)
    else:
        Secuencia1 = None
        Secuencia2 = None
        dotplot = None

    # Difundir las secuencias a todos los procesos
    Secuencia1 = comm.bcast(Secuencia1, root=0)
    Secuencia2 = comm.bcast(Secuencia2, root=0)

    # Llenar la matriz de dotplot según la estrategia seleccionada
    start_time = time.time()
    if args.estrategia == "secuencial":
        fill_dotplot_secuencial(Secuencia1, Secuencia2, dotplot)
    elif args.estrategia == "hilos":
        fill_dotplot_hilos(Secuencia1, Secuencia2, dotplot)
    elif args.estrategia == "multiprocessing":
        fill_dotplot_multiprocessing(Secuencia1, Secuencia2, dotplot)
    elif args.estrategia == "mpi":
        dotplot = fill_dotplot_mpi(Secuencia1, Secuencia2)
    tiempos['ejecucion'] = time.time() - start_time

    if rank == 0:
        print(f"Tiempo de ejecución ({args.estrategia}): {tiempos['ejecucion']:.4f} segundos")

        # Visualizar el dotplot
        start_time = time.time()
        if dotplot is not None:
            visualize_dotplot(dotplot, args.estrategia)
        tiempos['visualizacion'] = time.time() - start_time

        # Calcular tiempos totales y tiempos muertos
        tiempos['total'] = tiempos['carga_datos'] + tiempos['ejecucion'] + tiempos['visualizacion']
        tiempos['tiempo_muerto'] = tiempos['total'] - tiempos['ejecucion']
        print(f"Tiempos: {tiempos}")

        # Cargar tiempos anteriores
        data = load_times()

        # Guardar los nuevos tiempos
        save_times(data, args.estrategia, tiempos, size if args.estrategia == 'mpi' else 1)

if __name__ == "__main__":
    main()
