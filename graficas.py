import json
import matplotlib.pyplot as plt

def plot_speedup_and_efficiency(data):
    if "secuencial" not in data:
        print("Datos de ejecución secuencial no encontrados. Ejecute el programa con la estrategia 'secuencial' primero.")
        return

    sequential_time = data["secuencial"]["total"]
    strategies = []
    speedups = []
    efficiencies = []

    for strategy, values in data.items():
        if strategy != "secuencial":
            for num_proc, val in values.items():
                strategies.append(f"{strategy}_{num_proc}")
                parallel_time = val["total"]
                num_processes = val["num_processes"]
                speedup = sequential_time / parallel_time
                efficiency = speedup / num_processes
                speedups.append(speedup)
                efficiencies.append(efficiency)

    plt.figure()
    plt.subplot(1, 2, 1)
    plt.bar(strategies, speedups)
    plt.xlabel('Estrategia')
    plt.ylabel('Aceleración')
    plt.title('Aceleración')

    plt.subplot(1, 2, 2)
    plt.bar(strategies, efficiencies)
    plt.xlabel('Estrategia')
    plt.ylabel('Eficiencia')
    plt.title('Eficiencia')

    plt.savefig('speedup_and_efficiency.png')
    plt.close()

def plot_execution_times(data):
    strategies = []
    times = []

    for strategy, values in data.items():
        if strategy == "secuencial":
            strategies.append(strategy)
            times.append(values["total"])
        else:
            for num_proc, val in values.items():
                strategies.append(f"{strategy}_{num_proc}")
                times.append(val["total"])

    plt.figure()
    plt.bar(strategies, times)
    plt.xlabel('Estrategia')
    plt.ylabel('Tiempo (s)')
    plt.title('Tiempos de Ejecución')
    plt.savefig('execution_times.png')
    plt.close()

# Cargar datos desde el archivo pruebas.json
def load_times():
    try:
        with open('pruebas.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("No se encontró el archivo 'pruebas.json'.")
        return {}

# Función principal para cargar datos y generar las gráficas
def main():
    data = load_times()
    if data:
        plot_execution_times(data)
        plot_speedup_and_efficiency(data)

if __name__ == "__main__":
    main()
