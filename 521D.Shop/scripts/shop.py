'''
Solución del problema [521D] Shop.
https://codeforces.com/problemset/problem/521/D
'''

ASSIGN_T, ADD_T, MULT_T = 0,1,2


def solve_shop_greedy(a: list, b: list, m: int):
    '''
    Modifica los valores de las transformaciones de tipos no multiplicativos a 
    expresiones multiplicativas, conservando las referencias a tipos originales
    y cual valor `a_i` modifican.

    `a`: los valores de la lista a optimizar.
    `b`: las transformaciones de entrada.
    '''
    k,n = len(a), len(b)

    # Agrupamos por tipo y por correspondencia a cada elemento de `a`.
    # De forma que para la i-ésima transformación que modifica a `a[j]`` se almacena el valor y el índice j.
    by_type = tuple([[] for _ in range(k)]  # una lista por cada a[i].
                        for _ in range(3))  # k listas por cada tipo.
    for i,(j,t,v) in enumerate(b):
        by_type[t][j].append((v,i))

    # Se tratan las transformaciones (+,=) por cada a[j], se llevan a forma (*).
    # Se juntan todas las transformaciones en b_mult.
    b_mult = []
    for j in range(k):
        # Tomamos la máxima asignación de a[j] y decidimos si utilizarla.
        max_v, i = max(by_type[ASSIGN_T][j], default=(0,0))
        if max_v > a[j]:
            by_type[ADD_T][j].append((max_v - a[j], i))

        # Tomamos las adiciones y las llevamos a multiplicaciones. Por la
        # ordenación inicial de `b`, los valores son ordenados en orden descendiente.
        by_type[ADD_T][j].sort(reverse=True)
        acc = a[j]
        for v,i in by_type[ADD_T][j][:m]:
            b_mult.append(((acc+v)/acc, i))
            acc += v
        
        # Añadimos las transformaciones de multiplicación.
        b_mult.extend(by_type[MULT_T][j])
    
    # Ordenamos por mayor valor de transformación.
    b_mult.sort(reverse=True)
    selected = set(i for _,i in b_mult[:m])

    # Ordenamos `b` aprovechando la ordenación por defecto de las tuplas (j,t,v) para
    # recorrer transformaciones en orden del a[j] asociado, que a su vez están ordenadas
    # por tipo (asignación, luego adición, luego multiplicación). Las transformaciones
    # de tipo y a[j] comunes estarán entonces ordenadas por valores (notar que estos
    # últimos quedarán de forma ascendente, pero esto no afecta la respuesta final).
    #
    # La forma de b_sort es los índices que tomarían los valores b[i] de estar ordenados.
    b_sort = sorted(range(n), key=lambda i: b[i])

    # Devolvemos la lista de transformaciones aplicadas en el orden establecido.
    answer = []
    for i in b_sort:
        if i in selected:
            answer.append(i)
    
    return answer



if __name__ == '__main__':

    # De los datos de entrada, se obtienen A, lista de tamaño k de los valores a
    # optimizar y B la lista de transformaciones disponibles, tamaño n.
    k,n,m = map(int, input().split())
    A = [int(a) for a in input().split()]
    B = []
    for _ in range(n):
        t,j,v = map(int, input().split())

        # Invertimos las tuplas a j,t,v para garantizar el orden deseado.
        B.append((j-1,t-1,v))
    
    answer = solve_shop_greedy(A, B, m)
    
    # Imprimimos la respuesta.
    print(len(answer))
    for i in answer:
        print(i+1)
    