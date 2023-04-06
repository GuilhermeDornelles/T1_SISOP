# T1_SISOP

---

Projeto de Execução Dinâmica de Processos

###TO-DO List

- Implementar lógica pra ler as infos de entrada (info dos processos a serem executados)
- Implementar parser para ler entrada e converter em comandos
  - DONE
- Implementar classe Processo e PCB
  - Feito o esqueleto, vai sendo modificada com o tempo
- Implementar algoritmo de filas bloqueados, prontos e finalizados
- Implementar algoritmo RR
- Implementar algoritmo SJF

###Anotacoes de aula

- SYSCALL 1 ou 2 pode bloquear (mover P pra lista de bloqueados) o P antes ou depois de fazer o I/O

- Uma Unidade de tempo é uma iteração no 'while(True)' mais de fora do programa

  - Esse loop só vai finalizar quando todos os Ps estiverem finalizados

- Tempo de chegada (instante de carga) dos Ps é definido nas configs de entrada e podem ser diferentes pra cada P

- Waiting time: é o tempo que o P ficou na fila de prontos
- Running time: é o tempo que o P ficou com o processador
- Turnaroung time: é a diferença do instante que o P foi finalizado para o instante de carga dele

- Output da interface:

  - Ideal é salvar o Output em um txt, todos os logs da execução

- Informar as versões de linguagem usadas no manual PDF
