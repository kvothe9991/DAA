'''
Generador de casos del problema [521D] Shop.
https://codeforces.com/problemset/problem/521/D
'''
import random
import argparse
import operator
import itertools
from random import randint
from functools import reduce

from shop import solve_shop_greedy

ASSIGN_T, ADD_T, MULT_T = 0,1,2


def _check_answer(a: list, b: list, answer: list):
    '''
    Devuelve el resultado de la multiplicatoria de `a` luego de aplicar las `b`
    transformaciones.

    `b`: es de la forma `(t,j,v)`: t, el tipo; j, el a[j] que modifica; v, el valor.
    '''
    a,b = a.copy(), [b[i] for i in answer]
    
    # Ordena por tuplas, así quedan agrupados por a[j] en el orden de tipos deseado.
    b.sort()

    # Realiza las transformaciones.
    for (j,t,v) in b:
        if t == ASSIGN_T:
            a[j] = v
        elif t == ADD_T:
            a[j] += v
        elif t == MULT_T:
            a[j] *= v
    
    # Halla el producto final.
    return reduce(operator.mul, a, 1)


def _get_combinations(L, m):
    ''' Devuelve todas las combinaciones, indizadas, de `L` de longitud `m`. '''
    # Genera todos los subconjuntos de ``L` de longitud `m`.
    combos_with_index = itertools.combinations(enumerate(L), m)
    
    # Convierte a listas y las devuelve emparejadas para facilitar la sintaxis al usarlo.
    for comb in combos_with_index:
        ks, elems = map(list, zip(*comb))
        yield ks, elems


def solve_shop_with_brute_force(a: list, b: list, m: int):
    '''
    Resuelve el problema de shop asumiendo la correctitud de la ordenación planteada
    en el informe: (=,+,*). En lugar de utilizar un enfoque greedy prueba a tomar todo
    posible subconjunto de `b` y retorna una multiplicatoria de `a` óptima.
    '''
    answer = []
    answer_result = 0

    # Genera todos los subconjuntos de `b` de longitud m. Cada elemento del subconjunto
    # contiene el índice original y el valor. Nótese que se generan subconjuntos,
    # no permutaciones.
    for mj in range(m+1):
        for ks, b_subset in _get_combinations(b, mj):
            # Halla la multiplicatoria de `a` luego de aplicar las `b` transformaciones.
            b_subset = list(b_subset)
            result = _check_answer(a, b, ks)
            if result > answer_result:
                answer = ks
                answer_result = result
    
    return answer, answer_result


def assess_greedy(*case):
    '''
    Evalúa la correctitud del algoritmo greedy.
    '''
    a, b, m = case

    # Obtiene la respuesta por fuerza bruta.
    bf_answer, bf_result = solve_shop_with_brute_force(a, b, m)

    # Obtiene la respuesta del greedy.
    g_answer = solve_shop_greedy(a, b, m)
    g_result = _check_answer(a, b, g_answer)

    # Compara y declara los resultados.
    print('For:')
    print('\ta =', a)
    print('\tb =', b)
    print('\tm =', m)
    print('results were:')
    print('\t     Greedy:', g_answer)
    print('\tBrute Force:', bf_answer)
    if g_result == bf_result:
        print('\033[92m' + 'OK.' + '\033[0m')
    else:
        print('\033[91m' + 'ERROR!' + '\033[0m')
        print('Greedy:', g_result)
        print('Brute force:', bf_result)


def generate_cases_and_evaluate(case_count = 10, max_k = 10):
    ''' Genera casos de prueba y evalúa el greedy. '''
    for i in range(case_count):
        print('\n\n\033[93m' + 'Caso #%d:' % (i+1) + '\033[0m')

        k = randint(1,max_k)
        n = randint(1,2*k)
        m = randint(1,n)
        
        a = [randint(1,100) for _ in range(k)]
        
        b = []
        for _ in range(n):
            t = randint(0,2)
            j = randint(0,k-1)
            v = (randint(1,200) if t in (ASSIGN_T, ADD_T) else randint(1,10))
            b.append((j,t,v))
        
        assess_greedy(a, b, m)
        
        print('='*100)



if __name__ == '__main__':
    # Parser para leer datos pasados al llamar este script
    parser = argparse.ArgumentParser(description='Tester de casos para el problema Shop.')
    parser.add_argument('case_count', type=int, help='Cantidad de casos a generar.')
    args = parser.parse_args()

    generate_cases_and_evaluate(args.case_count)