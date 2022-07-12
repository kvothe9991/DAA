'''
Generador de casos del problema [1117C] Magic Ship.
https://codeforces.com/problemset/problem/1117/C
'''
import random
import argparse
from random import randint

from magic_ship import manhattan, solve_magic_ship

DIRS = [(-1,0), (1,0), (0,-1), (0,1)]


def solve_magic_ship_with_brute_force(x1, y1, x2, y2, D):
    ''' Resuelve el problema de Magic Ship utilizando búsqueda binaria. '''
    d = manhattan(x1, y1, x2, y2)
    n = len(D)

    # Hallar las sumas parciales de [0,i] para todo i de 0 hasta n.
    # sums[k] contiene el desplazamiento total en k días.
    sums = [(0,0)]
    for dxi, dyi in D:
        sxi, syi = sums[-1]
        sums.append((dxi + sxi, dyi + syi))

    # Definir el predicado para la búsqueda naive.
    def predicate(k):
        xk = x1 + (k//n) * sums[n][0] + sums[k%n][0]
        yk = y1 + (k//n) * sums[n][1] + sums[k%n][1]
        return manhattan(xk, yk, x2, y2) <= k
    
    # Búsqueda naive de 0 hasta n*d.
    for i in range(n*d):
        if predicate(i):
            return i
    else:
        return -1


def assess_binary(x1, y1, x2, y2, D):
    '''
    Evalúa el rendimiento de la búsqueda binaria.
    '''
    # Obtiene la respuesta por fuerza bruta.
    naive_answer = solve_magic_ship_with_brute_force(x1, y1, x2, y2, D)
    # Obtiene la respuesta por búsqueda binaria.
    bs_answer = solve_magic_ship(x1, y1, x2, y2, D)

    # Compara las respuestas.
    print('For:')
    print('\t(x1,y1) =', (x1,y1))
    print('\t(x2,y2) =', (x2,y2))
    print('\tDIRS =', D)
    print('results were:')
    print('\t     Binary:', bs_answer)
    print('\tBrute Force:', naive_answer)
    if bs_answer == naive_answer:
        print('\033[92m' + 'OK.' + '\033[0m')
    else:
        print('\033[91m' + 'ERROR!' + '\033[0m')
    
def generate_cases(case_count = 10):
    ''' Genera casos de prueba. '''
    for i in range(case_count):
        print('\n\n\033[93m' + 'Caso #%d:' % (i+1) + '\033[0m')

        # Genera los datos.
        x1 = randint(0,100)
        y1 = randint(0,100)
        x2 = randint(0,100)
        y2 = randint(0,100)

        # Genera las direcciones.
        D = [random.choice(DIRS) for _ in range(randint(1,25))]

        # Evalúa la búsqueda binaria.
        assess_binary(x1, y1, x2, y2, D)

        print('='*100)



if __name__ == '__main__':
    # Parser para leer datos pasados al llamar este script
    parser = argparse.ArgumentParser(description='Tester de casos para el problema Shop.')
    parser.add_argument('case_count', type=int, help='Cantidad de casos a generar.')
    args = parser.parse_args()

    generate_cases(args.case_count)