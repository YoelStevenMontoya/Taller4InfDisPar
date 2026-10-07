import random
import threading
import time

N = 1000        #tamano de la matriz (N x N)
BLOQUE = 100    #tamano de cada bloque (BLOQUE x BLOQUE)

# Paso 1: crear la matriz con numeros aleatorios (del 1 al 100)
random.seed(1)
matriz = [[random.randint(1, 100) for _ in range(N)] for _ in range(N)]


# Version secuencial: suma todos los elementos con dos bucles
def suma_secuencial(matriz):
    total = 0
    for fila in matriz:
        for valor in fila:
            total += valor
    return total


# Paso 3: funcion que ejecuta cada hilo, suma solo su bloque
def suma_bloque(matriz, fila_ini, col_ini, resultados, indice):
    suma = 0
    for i in range(fila_ini, fila_ini + BLOQUE):
        for j in range(col_ini, col_ini + BLOQUE):
            suma += matriz[i][j]
    resultados[indice] = suma  # cada hilo guarda en su propia posicion


# Paso 2 y 4: dividir en bloques, crear un hilo por bloque y combinar resultados
def suma_paralela(matriz):
    bloques_por_lado = N // BLOQUE                     # 10 bloques por lado
    num_bloques = bloques_por_lado * bloques_por_lado  # 100 bloques
    resultados = [0] * num_bloques
    hilos = []

    indice = 0
    for fila_ini in range(0, N, BLOQUE):
        for col_ini in range(0, N, BLOQUE):
            h = threading.Thread(target=suma_bloque,
                                 args=(matriz, fila_ini, col_ini, resultados, indice))
            hilos.append(h)
            h.start()
            indice += 1

    for h in hilos:
        h.join()          # esperar a que todos terminen

    return sum(resultados)   # combinar los resultados parciales


if __name__ == '__main__':
    print(f"Matriz de {N}x{N}, bloques de {BLOQUE}x{BLOQUE}")

    inicio = time.time()
    total_sec = suma_secuencial(matriz)
    fin = time.time()
    t_sec = fin - inicio
    print(f"Secuencial -> suma: {total_sec} | tiempo: {t_sec:.4f} s")

    inicio = time.time()
    total_par = suma_paralela(matriz)
    fin = time.time()
    t_par = fin - inicio
    print(f"Con hilos  -> suma: {total_par} | tiempo: {t_par:.4f} s")

    print("Las sumas coinciden:", total_sec == total_par)
    print(f"Speedup: {t_sec / t_par:.2f}")