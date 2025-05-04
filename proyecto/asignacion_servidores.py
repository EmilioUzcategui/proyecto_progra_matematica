import numpy as np
from scipy.optimize import linear_sum_assignment
from collections import defaultdict

class AsignadorSolicitudes:
    def __init__(self, costos, prioridades, capacidades):
        self.costos_original = np.array(costos)
        self.prioridades = np.array(prioridades)
        self.capacidades = capacidades
        self.servidores = len(costos)
        self.solicitudes = len(costos[0])
        self.resultado = []
        self.servidor_expandido = []

        self.costos_expandido = self._expandir_matriz()

    def _expandir_matriz(self):
        filas_expandida = []
        servidor_map = []

        penalizacion = self.prioridades * 10  # mayor prioridad = menor penalización

        for s, capacidad in enumerate(self.capacidades):
            for _ in range(capacidad):
                fila = self.costos_original[s] + penalizacion
                filas_expandida.append(fila)
                servidor_map.append(s)

        self.servidor_expandido = servidor_map
        return np.array(filas_expandida)

    def resolver(self):
        if self.costos_expandido.shape[0] < self.solicitudes:
            raise ValueError("No hay suficiente capacidad total para atender todas las solicitudes.")

        matriz_cuadrada = self._hacer_cuadrada(self.costos_expandido)
        fila, col = linear_sum_assignment(matriz_cuadrada)

        self.resultado = []
        for f, c in zip(fila, col):
            if c < self.solicitudes:  # Ignorar asignaciones ficticias
                self.resultado.append((self.servidor_expandido[f], c))

    def _hacer_cuadrada(self, matriz):
        filas, columnas = matriz.shape
        if filas > columnas:
            padding = np.full((filas, filas - columnas), 9999)
            return np.hstack((matriz, padding))
        elif columnas > filas:
            padding = np.full((columnas - filas, columnas), 9999)
            return np.vstack((matriz, padding))
        return matriz

    def imprimir_resultado(self):
        print("\nAsignaciones óptimas de solicitudes a servidores:")
        tiempo_total = 0
        cargas = defaultdict(list)

        for servidor, solicitud in self.resultado:
            tiempo = self.costos_original[servidor][solicitud]
            cargas[servidor].append((solicitud, tiempo))
            tiempo_total += tiempo
            print(f"  Servidor {servidor} -> Solicitud {solicitud} (tiempo: {tiempo})")

        print(f"\nTiempo total de procesamiento: {tiempo_total}")
        print("\nCarga distribuida entre servidores:")
        for servidor in range(self.servidores):
            solicitudes = cargas.get(servidor, [])
            print(f"  Servidor {servidor}: {len(solicitudes)} solicitud(es)")

def cli_asignacion_servidores():
    print("\n== Asignación de Solicitudes a Servidores ==")

    S = int(input("Número de servidores: "))
    R = int(input("Número de solicitudes: "))

    print("\nIntroduce la matriz de costos (tiempo estimado de procesamiento):")
    costos = []
    for i in range(S):
        fila = list(map(int, input(f"  Servidor {i + 1}: ").split()))
        if len(fila) != R:
            raise ValueError("Número incorrecto de columnas.")
        costos.append(fila)

    print("\nIntroduce el vector de prioridades (0=alta, mayor=nivel más bajo):")
    prioridades = list(map(int, input("  Prioridades: ").split()))
    if len(prioridades) != R:
        raise ValueError("Longitud incorrecta del vector de prioridades.")

    print("\nIntroduce la capacidad de cada servidor (cuántas solicitudes puede atender):")
    capacidades = list(map(int, input("  Capacidades: ").split()))
    if len(capacidades) != S:
        raise ValueError("Cantidad incorrecta de capacidades.")

    asignador = AsignadorSolicitudes(costos, prioridades, capacidades)
    asignador.resolver()
    asignador.imprimir_resultado()
