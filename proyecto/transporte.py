import numpy as np

class ProblemaTransporte:
    def __init__(self, costos, suministro, demanda):
        self.costos = np.array(costos)
        self.suministro = suministro.copy()
        self.demanda = demanda.copy()
        self.resultado = np.zeros_like(self.costos)
        self.filas, self.columnas = self.costos.shape

    def resolver(self):
        s = self.suministro.copy()
        d = self.demanda.copy()

        while True:
            # Encontrar la celda con el menor costo
            min_val = np.inf
            for i in range(self.filas):
                for j in range(self.columnas):
                    if s[i] > 0 and d[j] > 0 and self.costos[i][j] < min_val:
                        min_val = self.costos[i][j]
                        x, y = i, j

            if min_val == np.inf:
                break  # No hay más asignaciones posibles

            cantidad = min(s[x], d[y])
            self.resultado[x][y] = cantidad
            s[x] -= cantidad
            d[y] -= cantidad

    def imprimir_resultado(self):
        total = 0
        print("\nAsignaciones:")
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.resultado[i][j] > 0:
                    cantidad = self.resultado[i][j]
                    costo_individual = self.costos[i][j]
                    subtotal = cantidad * costo_individual
                    total += subtotal
                    print(f"  Programador {i} -> Tarea {j} x {cantidad} (costo: {costo_individual})")

        print(f"\nCosto total mínimo: {total}")

        # Reporte detallado
        print("\n--- Reporte detallado de optimización ---")
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.resultado[i][j] > 0:
                    cantidad = self.resultado[i][j]
                    costo = self.costos[i][j]
                    subtotal = cantidad * costo
                    print(f"  Asignación: Programador {i} -> Tarea {j}")
                    print(f"    Cantidad asignada: {cantidad}")
                    print(f"    Costo individual: {costo}")
                    print(f"    Subtotal: {subtotal}")
        print(f"\nCosto total combinado: {total}")

def cli_problema_transporte():
    print("\n== Asignación con restricciones de transporte ==")

    N = int(input("Número de programadores: "))
    M = int(input("Número de tareas: "))

    print("Introduce la matriz de costos (costo combinado desempeño + transporte):")
    costos = []
    for i in range(N):
        fila = list(map(int, input(f"  Fila {i+1}: ").split()))
        if len(fila) != M:
            raise ValueError("Número de columnas incorrecto.")
        costos.append(fila)

    print("Introduce el vector de suministro (máximo de tareas por programador):")
    suministro = list(map(int, input("  Suministro: ").split()))
    if len(suministro) != N:
        raise ValueError("Longitud de suministro incorrecta.")

    print("Introduce el vector de demanda (número de programadores requeridos por tarea):")
    demanda = list(map(int, input("  Demanda: ").split()))
    if len(demanda) != M:
        raise ValueError("Longitud de demanda incorrecta.")

    problema = ProblemaTransporte(costos, suministro, demanda)
    problema.resolver()
    problema.imprimir_resultado()
