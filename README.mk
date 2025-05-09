# Interpretador Python para máquina Norma.

## Normas de código:

1) Toda linha deve possuir um rótulo qualquer: Ex.: '1', '1a', 'f2'.

2) Existem duas operações principais: 'if' and 'do', seguidas do comando.
	2.1) 'if' são seguidos de 'zero REG' para verificar se o registrador REG, está zerado.
	2.2) 'do' são seguidos de 'add REG' ou 'dec REG', respectivamente, aumentando 1 no registrado REG ou subtraindo 1
	     do registrador REG.

3) A instrução 'if' tem formato: 'if zero REG then goto TAG1 else goto TAG2'. Se REG for zero, então vai para a linha TAG1, caso REG não estive zerado, vai para a linha TAG2.

4) A instrução 'do' tem formado 'do add REG then goto TAG' ou 'do dec REG then goto TAG'.

5) Ir para uma linha não existente, encerra o programa. Por padrão, comece o programa a partir de 1 e use 'goto 0' para acabar.


### Exemplo de programas:

#### Transferir o valor que está no registrador B para A.
1: if zero B then goto 0 else goto 2
2: do dec B then goto 3
3: do add A then goto 1
