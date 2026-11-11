Continuação portifolio matematica discreta.


ATIVIDADE 2 — Criptografia RSA simplificada

Parte A: primalidade de p e q, n = p·q, φ(n) = (p-1)(q-1) e expoente público e.
Parte B: expoente privado d (inverso de e módulo φ(n)) e chaves pública e privada.
Parte C: cifragem C ≡ M^e (mod n) e decifragem M' ≡ C^d (mod n) de um número inteiro M.
Parte D: Teoremas de Euler e de Fermat na exponenciação modular.

O programa trabalha com um número inteiro M (e não com textos) e imprime na tela os passos
essenciais de cada resolução: valores usados, cálculos intermediários, verificação das
condições, aplicação dos teoremas e conclusões. Nos procedimentos feitos por repetição
(teste de primalidade, algoritmo de Euclides, Euclides estendido e exponenciação modular),
cada etapa relevante é mostrada.

Os procedimentos matemáticos centrais estão implementados neste próprio arquivo. Não são
usadas funções prontas como math.gcd, pow(a, b, n) ou pow(a, -1, n), nem bibliotecas como
sympy: apenas os operadores + - * // %.

Para executar:  python atividade2.py
