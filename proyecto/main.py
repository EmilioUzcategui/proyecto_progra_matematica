from asignacion_hungaro import cli_asignacion_hungaro
from transporte import cli_problema_transporte
from asignacion_servidores import cli_asignacion_servidores

def main():
    while True:
        print("\n--- Menú Principal ---")
        print("1. Asignación con Método Húngaro")
        print("2. Asignación con Restricciones de Transporte")
        print("3. Asignación de Solicitudes a Servidores")
        print("0. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            cli_asignacion_hungaro()
        elif opcion == "2":
            cli_problema_transporte()
        elif opcion == "3":
            cli_asignacion_servidores()
        elif opcion == "0":
            break
        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()
