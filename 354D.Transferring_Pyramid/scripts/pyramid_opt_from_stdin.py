'''
Solución optimizada del problema [354D] Transferring Pyramid.
https://codeforces.com/problemset/problem/354/D
'''

from math import inf, sqrt
import sys


def insert_cost(n):
    ''' Halla el costo de una subpirámide tamaño `n`. '''
    return 2 + ((n * (n+1)) // 2)

def cost_prefix_sums(costs, column, ceil):
    ''' Halla el costo acumulado de los elementos de una columna. '''
    n = ceil
    high = ceil
    
    # Limpia los valores de la lista.
    for i in range(ceil+1):
        costs[i] = 0

    # Cuenta los costos de los cambios marcados por columna.
    for h in column:
        high = max(high, h)
        if h > n:
            costs[n] += 3
        else:
            costs[h-1] += 3
    
    # Acumula las sumas por altura >= i.
    for i in reversed(range(0,high)):
        costs[i] += costs[i+1]
    
    return costs

def solve_pyramid(n, changes):
    '''
    Utiliza dp para resolver el problema de una pirámide de altura
    `n` con cambios `changes` agrupados por columna.
    '''
    # Hallar techo de los costos de inserción. (Optimización de tiempo).
    k = sum(len(col) for col in changes)
    ceil = int(sqrt(6*k))

    # dp[i] tiene la misma cantidad de elementos que la `i`-ésima columna
    cost_from = [0]*(n+1)
    dp = [[inf]*(n+1) for _ in range(2)]
    curr, prev = 0, 1
    dp[curr][0] = 0

    # Iterar por cada columna, computar dp. 
    for i in range(1, n+1):

        # Limpiar los datos viejos de dp. Cambiar referencias del actual.
        m = min(i, ceil)
        curr, prev = prev, curr
        for j in range(i+1):
            dp[curr][j] = inf

        # Hallar cost_from[h] el costo de reemplazar los cambios de altura > h.
        cost_from = cost_prefix_sums(cost_from, changes[i-1], m)

        # Computar dp.
        # 1) Valor trivial que puede tomar dp, el costo mínimo hasta la columna
        #    anterior mas reemplazar los cambios de esta columna uno a uno.
        dp[curr][0] = dp[prev][0] + cost_from[0]

        # 2) Computar el mejor costo de ubicar una subpirámide en esta columna.
        for h in range(1,m+1):
            dp[curr][0] = min( dp[curr][0], dp[prev][h-1] + insert_cost(h) + cost_from[h] )
        
        # 3) Computar dp[i][h] para h>0, acarreo de los menores costos de arreglar
        #    la diagonal que pasa por (i,h).
        for h in range(1,m+1):
            dp[curr][h] = min( dp[curr][h-1], dp[prev][h-1] + cost_from[h] )

    return dp, dp[curr][0]



if __name__ == '__main__':
    
    # Lectura mejorada para entradas muy grandes.
    with sys.stdin as input:

        n,k = map(int, input.readline().split())

        # Se agrupan los cambios por columna.
        changes_by_col = [[] for _ in range(n)]
        for line in input.readlines():
            r,c = map(int, line.split())
            
            # Invertimos las posiciones para indizar por altura y columna ascendientes.
            r,c = n-r+1, n-c+1
            changes_by_col[c-1].append(r)
    
    # Resolver el problema e imprimir respuesta.
    dp, ans = solve_pyramid(n, changes_by_col)
    print(ans)
