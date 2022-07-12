'''
Solución del problema [1117C] Magic Ship.
https://codeforces.com/problemset/problem/1117/C
'''

DIRECTION_MAP = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}


def manhattan(x1, y1, x2, y2):
    ''' Distancia Manhattan entre dos puntos. '''
    return abs(x1 - x2) + abs(y1 - y2)


def binary_search(predicate, low=0, high=10**5):
    ''' Realiza una búsqueda binaria basada en predicado sobre el intervalo discreto [low, high].
    Encuentra la primera posición x en que `predicate(x) = True`. '''
    sol = -1
    
    while low <= high:
        mid = (low + high) // 2
        if predicate(mid):
            # mid puede ser el primer valor que satisface el predicado.
            sol = mid
            high = mid - 1
        else:
            # Se puede descartar el valor mid porque no satisface el predicado.
            low = mid + 1
    
    return sol


def solve_magic_ship(x1, y1, x2, y2, D):
    ''' Resuelve el problema de Magic Ship utilizando búsqueda binaria. '''
    d = manhattan(x1, y1, x2, y2)
    n = len(D)

    # Hallar las sumas parciales de [0,i] para todo i de 0 hasta n.
    # sums[k] contiene el desplazamiento total en k días.
    sums = [(0,0)]
    for dxi, dyi in D:
        sxi, syi = sums[-1]
        sums.append((dxi + sxi, dyi + syi))
    
    # Definir el predicado para la búsqueda binaria.
    def predicate(k):
        xk = x1 + (k//n) * sums[n][0] + sums[k%n][0]
        yk = y1 + (k//n) * sums[n][1] + sums[k%n][1]
        return manhattan(xk, yk, x2, y2) <= k
    
    # Si no hay solución en el máximo posible límite, entonces no puede haber solución.
    if not predicate(n*d):
        return -1

    # Buscar el valor mínimo k que satisfaga el predicado.
    return binary_search(predicate, low=d//2, high=n*d)
    


if __name__ == '__main__':
    # Datos de entrada.
    x1,y1 = map(int, input().split())
    x2,y2 = map(int, input().split())
    n = int(input())
    D = [DIRECTION_MAP.get(d) for d in input()]

    # Obtenemos y mostramos el mínimo.
    k = solve_magic_ship(x1, y1, x2, y2, D)
    print(k)