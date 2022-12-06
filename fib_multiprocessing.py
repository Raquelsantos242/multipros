""" 
fib_multiprocessing

programa que retorna fibonacci de 1.000.000 de números
usando multiprocessing -> divide o conjunto de dados em 4 partes
                         para executar o cálculo em paralelo, usando 4 processos

ESSE É UM EXEMPLO DE PARALELISMO!!!!

PARALELISMO (PARALLELISM) -> "Uma tarefa complexa é dividida em subtarefas,
que representam partes de um mesmo problema. Cada subtarefa será executada
ao mesmo tempo. Tipicamente, será necessário combinar os resultados das 
subtarefas para produzir o resultado geral. As subtarefas normalmente são 
muito similares ou exatamente iguais.

Ou seja: no paralelismo é comum que múltiplas cópias da mesma funcionalidade 
sejam executadas ao mesmo tempo, porém sobre dados diferentes"
"""

import multiprocessing
import random
import time

#-----------------------------------------
# PASSO 1: criar a função que eu quero
#            executar em paralelo
#-----------------------------------------
def fibonacci(n):
  if n in (1,2): return 1
  else:
    a1 = 1
    a2 = 1
    for x in range(3,n+1):
        a1, a2 = a2, (a1 + a2)
    
    return a2

# *** ATENÇÃO !!!
#-----------------------------------------
# PASSO 2: criar a função de paralelização
#          (processa um pedaço da lista)
#-----------------------------------------
def calcFibonacci(q1, q2):
    lista = q1.get()
    
    for x in range(len(lista)):
        lista[x] = (lista[x], fibonacci(lista[x]))
    
    q2.put(lista)

#-----------------------------------------
# PASSO 3: calcular os resultados usando
#          4 processos
#-----------------------------------------
if __name__ == "__main__":
    
    # 3.1.1 define o tamanho da lista
    N = 1_000_000
    
    # 3.1.2 criar a lista de entrada (a)
    a = [] # ENTRADA -> lista com os números originais

    for i in range(N):
        a.append(random.randint(1,20))
    
    # 3.2 aqui começaremos a parte que irá disparar 4 processos 
    # e obter fib de cada elemento da lista "a". Cada processo cuidará
    # de processar 1/4 da lista. E vou medir o tempo
    
    t_inicio = float(time.time()) # 3.1 captura o tempo de início
    
    # 3.2.1 Número de processos a serem criados
    NProcs = 4 # 
    
    # *** 3.2.2 Define as filas de entrada e saída dos processos
    q_entrada = multiprocessing.Queue()
    q_saida = multiprocessing.Queue()
    
    # 3.2.3 criar uma lista de processos e vou disparar cada processo
    lista_procs = []
    for i in range(NProcs):
        ini = i * int(N/NProcs)       # início do intervalo da lista
        fim = (i + 1) * int(N/NProcs) # fim do intervalo da lista
        q_entrada.put(a[ini:fim]) # *** novidade!
        p = multiprocessing.Process(target=calcFibonacci, args=(q_entrada, q_saida)) # *** novidade
        p.start()
        lista_procs.append(p)

    # *** 3.2.4 faz o programa principal esperar todos os processos terminarem
    #for p in lista_procs: p.join()
        
    # *** 3.2.5 reunir os resultados de cada processo no programa principal
    b = []
    for i in range(NProcs):
        b = b + q_saida.get()
    
    # *** 3.2.6 agora sim termino de exibir o tempo de execução
    t_fim = float(time.time())
    
    print('tempo processos = ', t_fim - t_inicio)
    
    
    #aux = input()
    
    print('tamanho das listas, primeiro registro, último registro')
    print(len(a), len(b))
    print(b[0][0], '--->', b[0][1])
    print(b[N-1][0], '--->', b[N-1][1])
    #aux = input()
    
    
    