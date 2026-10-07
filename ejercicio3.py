import numpy as np
import threading
import time

N = 10000        #tamano de la matriz
BLOQUE = 1000    #tamano de cada bloque

#Paso 1: crear la matriz de 10000x10000 con numeros aleatorios (enteros 1 a 100)
np.random.seed(1)
matriz = np.random.randint(1, 101, size=(N, N), dtype=np.int32)


#version secuencial: recorre los bloques uno por uno (con numpy dentro)
def suma_secuencial(matriz):
    total = 0
    for i in range(0, N, BLOQUE):
        for j in range(0, N, BLOQUE):
            bloque = matriz[i:i + BLOQUE, j:j + BLOQUE]
            total += int(bloque.sum())
    return total


#Paso 3: lo que hace cada hilo, suma de su bloque con numpy (SIMD)
def suma_bloque(matriz, i, j, resultados, indice):
    bloque = matriz[i:i + BLOQUE, j:j + BLOQUE]
    resultados[indice] = int(bloque.sum())   # suma vectorizada de numpy


#Pasos 2 y 4: un hilo por bloque (SMP) y combinar resultados
def suma_hibrida(matriz):
    num_bloques = (N // BLOQUE) ** 2   #100 bloques
    resultados = [0] * num_bloques
    hilos = []
    indice = 0
    for i in range(0, N, BLOQUE):
        for j in range(0, N, BLOQUE):
            h = threading.Thread(target=suma_bloque,
                                 args=(matriz, i, j, resultados, indice))
            hilos.append(h)
            h.start()
            indice += 1
    for h in hilos:
        h.join()
    return sum(resultados)


if __name__ == '__main__':
    print(f"Matriz de {N}x{N}, bloques de {BLOQUE}x{BLOQUE}")

    #Paso 5: medir tiempos
    inicio = time.time()
    total_sec = suma_secuencial(matriz)
    fin = time.time()
    t_sec = fin - inicio
    print(f"Secuencial -> suma: {total_sec} | tiempo: {t_sec:.4f} s")

    inicio = time.time()
    total_hib = suma_hibrida(matriz)
    fin = time.time()
    t_hib = fin - inicio
    print(f"Hibrido SMP+SIMD -> suma: {total_hib} | tiempo: {t_hib:.4f} s")

    print("Las sumas coinciden:", total_sec == total_hib)
    print(f"Speedup: {t_sec / t_hib:.2f}")