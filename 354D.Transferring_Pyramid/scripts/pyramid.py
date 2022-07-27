'''
Solución sin optimizaciones del problema [354D] Transferring Pyramid.
https://codeforces.com/problemset/problem/354/D
'''

from math import inf, sqrt


def insert_cost(n):
    ''' Halla el costo de una subpirámide tamaño `n`. '''
    return 2 + ((n * (n+1)) // 2)

def cost_prefix_sums(column, size):
    ''' Halla el costo acumulado de los elementos de una columna. '''
    n = size
    sums = [0] * (n+1)
    for k in column:
        sums[k-1] += 3
    for i in reversed(range(0,n-1)):
        sums[i] += sums[i+1]
    return sums

def solve_pyramid(n, changes):
    '''
    Utiliza dp para resolver el problema de una pirámide de altura
    `n` con cambios `changes` agrupados por columna.
    '''
    # dp[i] tiene la misma cantidad de elementos que la `i`-ésima columna
    dp = [[inf]*(i+1) for i in [1, *range(1,n+1)]]
    dp[0][0] = 0

    # Iterar por cada columna, computar dp. 
    for i in range(1, n+1):

        # Hallar cost_from[h] el costo de reemplazar los cambios de altura > h.
        cost_from = cost_prefix_sums(changes[i-1], i)

        # Computar dp.
        # 1) Valor trivial que puede tomar dp, el costo mínimo hasta la columna
        #    anterior mas reemplazar los cambios de esta columna uno a uno.
        dp[i][0] = dp[i-1][0] + cost_from[0]

        # 2) Computar el mejor costo de ubicar una subpirámide en esta columna.
        for h in range(1,i+1):
            dp[i][0] = min( dp[i][0], dp[i-1][h-1] + insert_cost(h) + cost_from[h] )
        
        # 3) Computar dp[i][h] para h>0, acarreo de los menores costos de arreglar
        #    la diagonal que pasa por (i,h).
        for h in range(1,i+1):
            dp[i][h] = min( dp[i][h-1], dp[i-1][h-1] + cost_from[h] )
    
    return dp, dp[n][0]



if __name__ == '__main__':
    
    # Datos de entrada.
    n,k = map(int, input().split())

    # Se agrupan los cambios por columna.
    changes_by_col = [[] for _ in range(n)]
    for _ in range(k):
        r,c = map(int, input().split())
        
        # Invertimos las posiciones para indizar por altura y columna ascendientes.
        r,c = n-r+1, n-c+1
        changes_by_col[c-1].append(r)
    
    # Resolver el problema e imprimir respuesta.
    dp, ans = solve_pyramid(n, changes_by_col)
    print(ans)
