
# Dotplot Generator

## Descripción

Este proyecto es una herramienta para generar dotplots a partir de secuencias de ADN. Un dotplot es una representación visual que compara dos secuencias y muestra similitudes entre ellas. Este programa permite elegir entre varias estrategias de paralelización para llenar la matriz de dotplot.

## Requisitos

- Python 3.x
- mpi4py
- numpy
- matplotlib

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/tu_usuario/dotplot-generator.git
    cd dotplot-generator
    ```

2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

### Ejecución del programa

Para ejecutar el programa, utiliza el siguiente comando:
```bash
python dotplot_generator.py --file1 <path_to_first_fasta_file> --file2 <path_to_second_fasta_file> --estrategia <estrategia> --filter <filter_size>
```

#### Argumentos

- `--file1`: Ruta al primer archivo FASTA.
- `--file2`: Ruta al segundo archivo FASTA.
- `--estrategia`: Estrategia de paralelización a utilizar (`secuencial`, `hilos`, `multiprocessing`, `mpi`).
- `--filter`: Tamaño del filtro (opcional, por defecto es 128).

### Ejemplo de uso

```bash
python dotplot_generator.py --file1 secuencia1.fasta --file2 secuencia2.fasta --estrategia secuencial --filter 128
```

### Estrategias de paralelización

El programa soporta las siguientes estrategias de paralelización:

1. `secuencial`: Llenado del dotplot de manera secuencial.
2. `hilos`: Uso de múltiples hilos para el llenado del dotplot.
3. `multiprocessing`: Uso de múltiples procesos para el llenado del dotplot.
4. `mpi`: Uso de MPI (Message Passing Interface) para distribuir la carga de trabajo entre múltiples nodos.

## Estructura del código

- `dotplot_generator.py`: Archivo principal que ejecuta el programa.
- `utils.py`: Contiene funciones utilitarias, como la función `merge_sequences_from_fasta` para leer y combinar secuencias de archivos FASTA.
- `secuencial.py`: Implementa la función `fill_dotplot_secuencial` para llenar el dotplot de manera secuencial.
- `hilos.py`: Implementa la función `fill_dotplot_hilos` para llenar el dotplot utilizando hilos.
- `multiprocessing_fill.py`: Implementa la función `fill_dotplot_multiprocessing` para llenar el dotplot utilizando múltiples procesos.
- `mpi_fill.py`: Implementa la función `fill_dotplot_mpi` para llenar el dotplot utilizando MPI.

## Manejo de errores

El programa incluye manejo de errores para:

1. Lectura de archivos FASTA: Captura y maneja excepciones en caso de errores al leer los archivos de secuencia.
2. Inicialización de MPI: Verifica que la inicialización de MPI se realice correctamente.
3. Generación del dotplot: Maneja posibles errores internos en las funciones de generación del dotplot.
4. Visualización del dotplot: Captura y maneja excepciones al guardar la visualización del dotplot.

## Salida

El programa genera un archivo PNG con el dotplot generado. El archivo se guarda con el nombre `dotplot_<estrategia>.png` en el directorio actual.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, por favor sigue los siguientes pasos:

1. Haz un fork de este repositorio.
2. Crea una rama con tu nueva característica (`git checkout -b feature/nueva-caracteristica`).
3. Haz commit de tus cambios (`git commit -am 'Añadir nueva característica'`).
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`).
5. Abre un Pull Request.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
