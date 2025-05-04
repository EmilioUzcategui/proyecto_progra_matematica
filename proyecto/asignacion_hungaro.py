import numpy as np
from scipy.optimize import linear_sum_assignment

# Definición de la función para leer la matriz desde un archivo

def leer_matriz_desde_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()
        matriz = [list(map(int, linea.strip().split())) for linea in lineas]

    longitud_columnas = len(matriz[0])
    for i, fila in enumerate(matriz):
        if len(fila) != longitud_columnas:
            raise ValueError(f"La fila {i + 1} no tiene la misma cantidad de columnas que las demás.")

    return np.array(matriz)

# Definición de la función para leer la matriz desde consola
def leer_matriz_por_consola():

    filas = int(input("Número de programadores: "))
    columnas = int(input("Número de tareas: "))
    matriz = []
    for i in range(filas):
        fila = list(map(int, input(f"  Fila {i + 1} (separada por espacios): ").split()))
        if len(fila) != columnas:
            raise ValueError(f"La fila {i + 1} no tiene {columnas} columnas.")
        matriz.append(fila)
    return np.array(matriz), filas, columnas

# Definición de la función para hacer la matriz cuadrada
def hacer_matriz_cuadrada(matriz, maximizar):
    filas, columnas = matriz.shape
    if filas == columnas:
        return matriz, filas, columnas

    dimension = max(filas, columnas)
    relleno = 0 if maximizar else np.max(matriz) + 1000
    matriz_cuadrada = np.full((dimension, dimension), relleno)
    matriz_cuadrada[:filas, :columnas] = matriz
    return matriz_cuadrada, filas, columnas
# Definición de la función principal para la asignación de programadores a tareas
def cli_asignacion_hungaro():
    print("\n== Asignación de Programadores a Tareas ==")
    metodo = input("¿Deseas ingresar los datos desde archivo o consola? (archivo/consola): ").strip().lower()

    if metodo == "archivo":
        archivo = input("Ruta del archivo de costos: ")
        matriz_original = leer_matriz_desde_archivo(archivo)
        filas_original, columnas_original = matriz_original.shape
    elif metodo == "consola":
        matriz_original, filas_original, columnas_original = leer_matriz_por_consola()
    else:
        print("Método no válido. Intenta de nuevo.")
        return

    maximizar = input("¿Deseas maximizar eficiencia? (s/n): ").lower() == 's'
    if maximizar:
        max_valor = np.max(matriz_original)
        matriz_original = max_valor - matriz_original

    matriz_cuadrada, filas_reales, columnas_reales = hacer_matriz_cuadrada(matriz_original, maximizar)

    fila_ind, col_ind = linear_sum_assignment(matriz_cuadrada)
    asignaciones = list(zip(fila_ind, col_ind))
    costo_total = matriz_cuadrada[fila_ind, col_ind].sum()

    print("\nMatriz de costos usada (posiblemente cuadrada):")
    print(matriz_cuadrada)

    print("\nAsignaciones óptimas (Programador -> Tarea):")
    for p, t in asignaciones:
        if p < filas_original and t < columnas_original:
            print(f"  Programador {p} -> Tarea {t}")

    if maximizar:
        eficiencia_total = np.max(matriz_cuadrada) * len(asignaciones) - costo_total
        print(f"\nEficiencia total: {eficiencia_total}")
    else:
        print(f"\nCosto total: {costo_total}")
