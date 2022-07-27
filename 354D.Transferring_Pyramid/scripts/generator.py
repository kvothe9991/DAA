'''
Generador de casos del problema [354D] Transferring Pyramid.
https://codeforces.com/problemset/problem/354/D
'''
import random
import argparse
from time import time
from random import randint
import resource

import pyramid, pyramid_opt


def assess_solutions(n, changes):
    '''
    Compara los algoritmos de solución.
    '''
    # Obtiene respuesta y tiempo de ejecución del algoritmo no optimizado.
    start = time()
    _, norm_answer = pyramid.solve_pyramid(n, changes)
    norm_time = (time() - start)

    # Obtiene respuesta y tiempo de ejecución del optimizado.
    start = time()
    _, opt_answer = pyramid_opt.solve_pyramid(n, changes)
    opt_time = (time() - start)

    # Mejor muestra de los datos de entrada.
    legacy_changes = []
    for i in range(n):
        for r in changes[i]:
            legacy_changes.append((i+1,r))

    # Compara las respuestas.
    print('For:')
    print('\tn =', n)
    print('\tchanges (col,row) =', legacy_changes)
    print('results were:')
    print('\t          Normal:', norm_answer, 'achieved in', '%fms.' % norm_time)
    print('\t       Optimized:', opt_answer, 'achieved in', '%fms.' % opt_time)
    if norm_answer == opt_answer:
        print('\033[92m' + 'OK.' + '\033[0m')
    else:
        print('\033[91m' + 'ERROR!' + '\033[0m')


def generate_cases(case_count = 10):
    ''' Genera casos de prueba. '''

    for i in range(case_count):
        print('\n\n\033[93m' + 'Caso #%d:' % (i+1) + '\033[0m')

        # Datos.
        # 1) Altura de la pirámide.
        n = randint(2, 1000)

        # 2) Cambios de entrada.
        changes = [[] for _ in range(n)]
        change_count = randint(0, 50)
        for _ in range(change_count):
            c = randint(1,n)
            r = randint(1,c)
            changes[c-1].append(r)
        
        # Evalúa el caso.
        assess_solutions(n, changes)

        print('='*100)


if __name__ == '__main__':
    # Parser para leer datos pasados al llamar este script
    parser = argparse.ArgumentParser(description='Tester de casos para el problema Transferring Pyramid.')
    parser.add_argument('case_count', type=int, help='Cantidad de casos a generar.')
    args = parser.parse_args()

    generate_cases(args.case_count)