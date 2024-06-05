import argparse
import numpy as np
import time
import matplotlib.pyplot as plt
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
    output_file = f"dotplot_{estrategia}.png"
    plt.imshow(dotplot, cmap='gray_r', interpolation='none')
    plt.title(f"Dotplot {estrategia}")
    plt.xlabel('Sequence 2')
    plt.ylabel('Sequence 1')
    plt.savefig(output_file)
    plt.close()
    print(f"Dotplot saved as {output_file}")

def main():
    args = parse_args()

    # Leer y combinar las secuencias
    Secuencia1 = merge_sequences_from_fasta(args.file1)
    Secuencia2 = merge_sequences_from_fasta(args.file2)

    # Usar solo las primeras bases según el filtro
    Secuencia1 = Secuencia1[:args.filter]
    Secuencia2 = Secuencia2[:args.filter]

    # Crear la matriz de dotplot
    dotplot = np.zeros((len(Secuencia1), len(Secuencia2)), dtype=np.uint8)
    print("La matriz de resultado tiene tamaño:", dotplot.shape)

    # Llenar la matriz de dotplot según la estrategia seleccionada
    begin = time.time()
    if args.estrategia == "secuencial":
        fill_dotplot_secuencial(Secuencia1, Secuencia2, dotplot)
    elif args.estrategia == "hilos":
        fill_dotplot_hilos(Secuencia1, Secuencia2, dotplot)
    elif args.estrategia == "multiprocessing":
        fill_dotplot_multiprocessing(Secuencia1, Secuencia2, dotplot)
    elif args.estrategia == "mpi":
        dotplot = fill_dotplot_mpi(Secuencia1, Secuencia2)
    end = time.time()
    print(f"Tiempo de ejecución ({args.estrategia}): {end - begin} segundos")

    # Visualizar el dotplot
    if dotplot is not None:
        visualize_dotplot(dotplot, args.estrategia)
        # np.savetxt(f"dotplot_{args.estrategia}.txt", dotplot, fmt="%d")

if __name__ == "__main__":
    main()
