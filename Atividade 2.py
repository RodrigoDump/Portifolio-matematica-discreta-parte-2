"""
ATIVIDADE 2 - CRIPTOGRAFIA RSA
==============================
Programa que implementa um sistema simplificado de criptografia RSA,
demonstrando a aplicacao de numeros primos, da funcao totiente de Euler,
do inverso multiplicativo e da exponenciacao modular.

Conforme exigido no enunciado, todas as etapas relevantes dos calculos
(valores utilizados, calculos intermediarios, verificacoes das condicoes
matematicas, aplicacao dos teoremas e conclusoes obtidas) sao exibidas na
tela durante a execucao, e nao apenas o resultado final.

Partes implementadas:
    A - Primalidade e parametros RSA
    B - Construcao das chaves
    C - Cifragem e decifragem
    D - Teoremas de Fermat e Euler na exponenciacao modular
"""

import math


# ---------------------------------------------------------------------------
# FUNCOES AUXILIARES DE ENTRADA E FORMATACAO
# ---------------------------------------------------------------------------

def ler_inteiro(mensagem):
    """Le um numero inteiro do usuario, repetindo a pergunta ate obter
    uma entrada valida (trata o caso de o usuario digitar algo que nao
    seja um numero inteiro)."""
    while True:
        entrada = input(mensagem).strip()
        try:
            return int(entrada)
        except ValueError:
            print(f"  >> Entrada invalida ('{entrada}'). Digite um numero inteiro.\n")


def titulo(texto):
    print()
    print("=" * 74)
    print(texto)
    print("=" * 74)


def subtitulo(texto):
    print()
    print(f"--- {texto} ---")


# ---------------------------------------------------------------------------
# PROCEDIMENTOS MATEMATICOS CENTRAIS (implementados pelo aluno, sem usar
# bibliotecas prontas de numeros primos ou de criptografia)
# ---------------------------------------------------------------------------

def eh_primo(numero):
    """
    Verifica se 'numero' e primo por tentativa de divisao (trial division):
    testa a divisibilidade por 2 e, em seguida, pelos impares de 3 ate a
    raiz quadrada de 'numero'. Se nenhum divisor for encontrado, o numero
    e primo.

    Retorna uma tupla (e_primo: bool, divisor_encontrado: int ou None).
    """
    if numero < 2:
        return False, None
    if numero == 2:
        return True, None
    if numero % 2 == 0:
        return False, 2

    limite = math.isqrt(numero)
    divisor = 3
    while divisor <= limite:
        if numero % divisor == 0:
            return False, divisor
        divisor += 2
    return True, None


def mdc_euclides(a, b, mostrar_passos=False):
    """
    Calcula o Maximo Divisor Comum entre a e b por meio do Algoritmo de
    Euclides (divisoes sucessivas: mdc(a,b) = mdc(b, a mod b)).
    Se mostrar_passos=True, exibe cada divisao realizada.
    """
    a, b = abs(a), abs(b)
    if mostrar_passos:
        print(f"      Calculando mdc({a}, {b}) pelo Algoritmo de Euclides:")
    r0, r1 = a, b
    while r1 != 0:
        q = r0 // r1
        r2 = r0 % r1
        if mostrar_passos:
            print(f"        {r0} = {r1} x {q} + {r2}")
        r0, r1 = r1, r2
    if mostrar_passos:
        print(f"      mdc({a}, {b}) = {r0}")
    return r0


def inverso_multiplicativo(e, modulo, mostrar_passos=False):
    """
    Encontra d tal que (e * d) = 1 (mod modulo), por meio do Algoritmo de
    Euclides Estendido. A cada iteracao, mantem-se o resto da divisao (r)
    e o coeficiente associado a 'e' (s), ate o resto chegar a zero.

    Retorna None se mdc(e, modulo) != 1 (o inverso nao existe nesse caso).
    """
    r0, r1 = modulo, e
    s0, s1 = 0, 1  # coeficientes de 'e' em cada etapa (r_i = s_i*e + t_i*modulo)

    if mostrar_passos:
        print(f"      Algoritmo de Euclides Estendido para o inverso de {e} "
              f"modulo {modulo}:")
        print(f"      {'r':>8}  {'s (coef. de e)':>16}  {'quociente':>10}")
        print(f"      {r0:>8}  {s0:>16}  {'-':>10}")
        print(f"      {r1:>8}  {s1:>16}  {'-':>10}")

    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
        if mostrar_passos:
            print(f"      {r1:>8}  {s1:>16}  {q:>10}")

    mdc_final = r0
    if mostrar_passos:
        print(f"      mdc({e}, {modulo}) = {mdc_final}")

    if mdc_final != 1:
        return None

    d = s0 % modulo
    if mostrar_passos:
        print(f"      Inverso multiplicativo (ajustado para 0 <= d < modulo): "
              f"d = {d}")
    return d


def exp_modular(base, expoente, modulo, mostrar_passos=False):
    """
    Calcula (base ** expoente) mod modulo pelo metodo de "quadrado e
    multiplicacao" (exponenciacao modular rapida / por reducoes
    sucessivas): a cada etapa o resultado parcial e reduzido modulo
    'modulo', de modo que nunca e necessario construir potencias
    inteiras muito grandes.
    """
    if modulo == 1:
        return 0

    resultado = 1
    base_atual = base % modulo
    expoente_restante = expoente

    if mostrar_passos:
        print(f"      Calculando {base}^{expoente} mod {modulo}  "
              f"(expoente em binario: {bin(expoente)[2:]})")
        print(f"      inicio: resultado = 1, base = {base_atual} (mod {modulo})")

    passo = 0
    while expoente_restante > 0:
        passo += 1
        bit = expoente_restante % 2
        if bit == 1:
            novo_resultado = (resultado * base_atual) % modulo
            if mostrar_passos:
                print(f"      passo {passo}: expoente restante = "
                      f"{expoente_restante} (impar) -> resultado = "
                      f"({resultado} x {base_atual}) mod {modulo} = {novo_resultado}")
            resultado = novo_resultado
        else:
            if mostrar_passos:
                print(f"      passo {passo}: expoente restante = "
                      f"{expoente_restante} (par) -> resultado inalterado "
                      f"({resultado})")

        expoente_restante //= 2
        if expoente_restante > 0:
            novo_base = (base_atual * base_atual) % modulo
            if mostrar_passos:
                print(f"               base = (base^2) mod {modulo} = {novo_base}"
                      f"  (novo expoente restante = {expoente_restante})")
            base_atual = novo_base

    if mostrar_passos:
        print(f"      resultado final: {base}^{expoente} mod {modulo} = {resultado}")
    return resultado


# ---------------------------------------------------------------------------
# PARTE A - PRIMALIDADE E PARAMETROS RSA
# ---------------------------------------------------------------------------

def parte_a():
    titulo("PARTE A - PRIMALIDADE E PARAMETROS RSA")

    while True:
        print("\nInforme dois numeros primos p e q (inteiros, maiores que 1 e "
              "distintos entre si).")
        p = ler_inteiro("  p = ")
        q = ler_inteiro("  q = ")

        if p <= 1 or q <= 1:
            print("  >> p e q devem ser inteiros maiores que 1. Tente novamente.")
            continue
        if p == q:
            print("  >> p e q devem ser distintos. Tente novamente.")
            continue

        primo_p, divisor_p = eh_primo(p)
        primo_q, divisor_q = eh_primo(q)

        print(f"\n  Verificando se p = {p} e primo (divisao por 2 e pelos "
              f"impares ate {math.isqrt(p)}):")
        if primo_p:
            print(f"    Nenhum divisor encontrado -> p = {p} e primo.")
        else:
            print(f"    {p} e divisivel por {divisor_p} -> p = {p} NAO e primo.")

        print(f"\n  Verificando se q = {q} e primo (divisao por 2 e pelos "
              f"impares ate {math.isqrt(q)}):")
        if primo_q:
            print(f"    Nenhum divisor encontrado -> q = {q} e primo.")
        else:
            print(f"    {q} e divisivel por {divisor_q} -> q = {q} NAO e primo.")

        if primo_p and primo_q:
            break
        print("\n  >> p e q precisam ser ambos primos. Vamos tentar novamente.")

    n = p * q
    print(f"\n  n = p x q = {p} x {q} = {n}")

    phi_n = (p - 1) * (q - 1)
    print("  Como p e q sao primos distintos, vale a propriedade "
          "phi(n) = (p-1)(q-1):")
    print(f"  phi(n) = ({p}-1) x ({q}-1) = {p - 1} x {q - 1} = {phi_n}")

    while True:
        print(f"\nInforme o expoente publico e, com 1 < e < phi(n) = {phi_n}.")
        e = ler_inteiro("  e = ")

        if not (1 < e < phi_n):
            print(f"  >> e deve satisfazer 1 < e < {phi_n}. Tente novamente.")
            continue

        print("\n  Verificando se mdc(e, phi(n)) = 1:")
        resultado_mdc = mdc_euclides(e, phi_n, mostrar_passos=True)

        if resultado_mdc == 1:
            print(f"  mdc({e}, {phi_n}) = 1 -> e e valido (coprimo com phi(n)).")
            break
        print(f"  mdc({e}, {phi_n}) = {resultado_mdc} (diferente de 1) -> e nao "
              f"e valido. Tente novamente.")

    subtitulo("Parametros obtidos na Parte A")
    print(f"  p       = {p}")
    print(f"  q       = {q}")
    print(f"  n       = {n}")
    print(f"  phi(n)  = {phi_n}")
    print(f"  e       = {e}")

    return p, q, n, phi_n, e


# ---------------------------------------------------------------------------
# PARTE B - CONSTRUCAO DAS CHAVES
# ---------------------------------------------------------------------------

def parte_b(e, n, phi_n):
    titulo("PARTE B - CONSTRUCAO DAS CHAVES")

    print(f"\nDeterminando d tal que (e x d) = 1 (mod phi(n)), com e = {e} e "
          f"phi(n) = {phi_n}.")
    d = inverso_multiplicativo(e, phi_n, mostrar_passos=True)

    verificacao = (e * d) % phi_n
    print(f"\n  Verificacao: (e x d) mod phi(n) = ({e} x {d}) mod {phi_n} = "
          f"{verificacao}")
    if verificacao == 1:
        print("  A condicao e x d = 1 (mod phi(n)) foi satisfeita.")
    else:
        print("  ATENCAO: a condicao nao foi satisfeita (erro inesperado).")

    subtitulo("Chaves RSA")
    print(f"  Chave publica:  (e, n) = ({e}, {n})")
    print(f"  Chave privada:  (d, n) = ({d}, {n})")

    return d


# ---------------------------------------------------------------------------
# PARTE C - CIFRAGEM E DECIFRAGEM
# ---------------------------------------------------------------------------

def parte_c(e, d, n):
    titulo("PARTE C - CIFRAGEM E DECIFRAGEM")

    while True:
        print(f"\nInforme o numero inteiro M a ser cifrado, com 0 <= M < n = {n}.")
        M = ler_inteiro("  M = ")
        if 0 <= M < n:
            break
        print(f"  >> M deve satisfazer 0 <= M < {n}. Tente novamente.")

    subtitulo("Cifragem: C = M^e mod n")
    C = exp_modular(M, e, n, mostrar_passos=True)

    subtitulo("Decifragem: M' = C^d mod n")
    M_linha = exp_modular(C, d, n, mostrar_passos=True)

    subtitulo("Resultado da cifragem/decifragem")
    print(f"  Numero original  (M)  = {M}")
    print(f"  Numero cifrado   (C)  = {C}")
    print(f"  Numero decifrado (M') = {M_linha}")

    if M_linha == M:
        print("\n  M' = M -> a decifragem recuperou corretamente o numero "
              "original.")
    else:
        print("\n  ATENCAO: M' != M -> ha um erro no processo.")

    return M, C


# ---------------------------------------------------------------------------
# PARTE D - TEOREMAS DE FERMAT E EULER NA EXPONENCIACAO MODULAR
# ---------------------------------------------------------------------------

def parte_d(p, q, n, phi_n, M):
    titulo("PARTE D - TEOREMAS DE FERMAT E EULER NA EXPONENCIACAO MODULAR")

    subtitulo("Teorema de Euler")
    print("  Enunciado: se mdc(a, n) = 1, entao a^phi(n) = 1 (mod n).")
    print(f"  Verificando se mdc(M, n) = 1, com M = {M} e n = {n}:")
    mdc_M_n = mdc_euclides(M, n, mostrar_passos=True)

    if mdc_M_n == 1:
        print("\n  Como mdc(M, n) = 1, a condicao do Teorema de Euler e "
              "satisfeita.")
        resultado_euler = exp_modular(M, phi_n, n, mostrar_passos=True)
        if resultado_euler == 1:
            print(f"\n  M^phi(n) mod n = {resultado_euler} -> confirma o "
                  f"Teorema de Euler.")
        else:
            print(f"\n  M^phi(n) mod n = {resultado_euler} -> resultado "
                  f"inesperado (revise os calculos).")
    else:
        print(f"\n  Como mdc(M, n) = {mdc_M_n} (diferente de 1), a condicao do "
              "Teorema de Euler NAO e satisfeita. Nesse caso, o teorema nao "
              "garante que M^phi(n) = 1 (mod n).")

    subtitulo("Pequeno Teorema de Fermat")
    print("  Enunciado: se p e primo e a nao e divisivel por p, entao "
          "a^(p-1) = 1 (mod p).")
    print(f"  Vamos aplica-lo usando o modulo primo p = {p} (um dos primos "
          f"usados na construcao de n).")

    while True:
        print(f"\nInforme um valor inteiro 'a' que NAO seja divisivel por "
              f"p = {p}.")
        a = ler_inteiro("  a = ")
        if a % p != 0:
            break
        print(f"  >> a nao pode ser divisivel por p = {p} (o teorema exige "
              "mdc(a, p) = 1). Tente novamente.")

    resultado_fermat = exp_modular(a, p - 1, p, mostrar_passos=True)
    if resultado_fermat == 1:
        print(f"\n  a^(p-1) mod p = {a}^{p - 1} mod {p} = {resultado_fermat} "
              "-> confirma o Pequeno Teorema de Fermat.")
    else:
        print(f"\n  a^(p-1) mod p = {a}^{p - 1} mod {p} = {resultado_fermat} "
              "-> resultado inesperado (revise os calculos).")

    subtitulo("Por que os teoremas nao se aplicam diretamente a n?")
    print(f"  n = {n} = {p} x {q} e um numero composto (produto de dois "
          "primos distintos), e nao primo.")
    print("  O Pequeno Teorema de Fermat exige um modulo PRIMO; por isso, "
          "nao pode ser aplicado diretamente a n (modulo RSA).")
    print("  Para reduzir expoentes modulo n (como nas Partes B e C), "
          "utilizamos:")
    print("    - o Teorema de Euler, quando mdc(base, n) = 1 (pois phi(n) e "
          "conhecido); ou")
    print("    - a exponenciacao modular por reducoes sucessivas (quadrado "
          "e multiplicacao), valida em qualquer caso, inclusive quando as "
          "condicoes dos teoremas de Euler e de Fermat nao sao satisfeitas.")


# ---------------------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------------

def main():
    print("PROGRAMA - CRIPTOGRAFIA RSA SIMPLIFICADA (ATIVIDADE 2)")
    print("Partes A, B, C e D executadas em sequencia, com os passos dos "
          "calculos exibidos na tela.")

    p, q, n, phi_n, e = parte_a()
    d = parte_b(e, n, phi_n)
    M, C = parte_c(e, d, n)
    parte_d(p, q, n, phi_n, M)

    titulo("FIM DO PROGRAMA")


if __name__ == "__main__":
    main()