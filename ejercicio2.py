import numpy as np
import random
import time

N = 1000

#Paso 1: crear dos matrices de N x N con numeros aleatorios
#(se crean con numpy y luego se pasan a listas para el bucle de Python)
np.random.seed(1)
A = np.random.rand(N, N)
B = np.random.rand(N, N)
A_lista = A.tolist()
B_lista = B.tolist()


#Paso 2: multiplicacion con NumPy (usa instrucciones SIMD por debajo)
def multiplicar_numpy(A, B):
    return np.dot(A, B)


#paso 3: multiplicacion con bucle tradicional de Python (3 bucles)
def multiplicar_bucles(A, B):
    n = len(A)
    C = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            suma = 0.0
            for k in range(n):
                suma += A[i][k] * B[k][j]
            C[i][j] = suma
    return C


if __name__ == '__main__':
    print(f"Matrices de {N}x{N}")

    #Paso 4: medir tiempos
    inicio = time.time()
    C_numpy = multiplicar_numpy(A, B)
    fin = time.time()
    t_numpy = fin - inicio
    print(f"NumPy: {t_numpy:.4f} segundos")

    inicio = time.time()
    C_bucles = multiplicar_bucles(A_lista, B_lista)
    fin = time.time()
    t_bucles = fin - inicio
    print(f"Bucles de Python: {t_bucles:.2f} segundos")

    #verificar que los dos resultados sean iguales
    print("Resultados iguales:", np.allclose(C_numpy, np.array(C_bucles)))
    print(f"NumPy fue {t_bucles / t_numpy:.0f} veces mas rapido")