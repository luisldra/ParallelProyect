import numpy as np

def fill_dotplot_secuencial(Secuencia1, Secuencia2, dotplot):
    for i in range(len(Secuencia1)):
        for j in range(len(Secuencia2)):
            dotplot[i, j] = 1 if Secuencia1[i] == Secuencia2[j] else 0
