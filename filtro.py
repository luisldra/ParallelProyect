import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

def apply_filter_and_detect_lines(dotplot_path, output_path, filter_size=3):
    try:
        # Cargar el dotplot desde el archivo
        dotplot = plt.imread(dotplot_path)
        
        sigma = 1.0
        
        # Aplicar el filtro de mediana
        filtered_dotplot = gaussian_filter(dotplot, sigma=sigma)
        
        # Guardar la imagen filtrada
        plt.imshow(filtered_dotplot, cmap='gray', interpolation='none')
        plt.title('Dotplot con Filtro de Mediana')
        plt.savefig(output_path)
        plt.close()
        print(f"Filtered dotplot saved as {output_path}")
    except Exception as e:
        print(f"Error applying filter: {e}")
