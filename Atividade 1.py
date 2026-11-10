
# Nome:        [Rodrigo Otavio]
# Matrícula:   [2612130046]
# Disciplina:  Matemática Discreta
# Turno:       [Matutino]

"""
ATIVIDADE 1 — Congruência Modular e Teorema Chinês do Resto

Parte A: verifica se a ≡ b (mod n).
Parte B: resolve sistemas de 3 ou 4 congruências pelo Teorema Chinês do Resto (TCR).




"""



# Funções auxiliares


def ler_inteiro(mensagem):
    """Pede um número inteiro ao usuário e repete a pergunta até a entrada ser válida."""
    while True:
        texto = input(mensagem)
        try:
            return int(texto)
        except ValueError:
            print("  Entrada inválida: digite um número inteiro (ex.: 7 ou -3).")


def com_par(x):
    """Coloca números negativos entre parênteses (só para as contas ficarem legíveis)."""
    if x < 0:
        return "(" + str(x) + ")"
    return str(x)


def titulo(texto):
    """Imprime um título destacado."""
    print("\n" + "=" * 64)
    print(texto)
    print("=" * 64)



# Procedimentos matemáticos


def mdc(a, b):
    """
    Máximo divisor comum pelo algoritmo de Euclides:
        mdc(a, b) = mdc(b, a mod b)
    Repete até o resto ser 0; o último valor não nulo é o MDC.
    """
    a = abs(a)
    b = abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def verificar_congruencia(a, b, n):
    """
    Lógica da Parte A (n > 0):
        a ≡ b (mod n)  <=>  n divide (a - b)  <=>  o resto de (a - b) por n é 0.
    Como n > 0, o resto de % em Python fica sempre entre 0 e n-1, igual à definição
    matemática (mesmo com números negativos).
    Retorna (diferenca, quociente, resto, congruentes).
    """
    diferenca = a - b
    quociente = diferenca // n      # diferenca = n · quociente + resto
    resto = diferenca % n
    return diferenca, quociente, resto, resto == 0


def inverso_modular(a, n):
    """
    Inverso multiplicativo de a módulo n (n > 0) pelo algoritmo de Euclides ESTENDIDO.

    Ideia: a cada divisão do algoritmo de Euclides, todo resto r pode ser escrito como
    r = s·n + t·a (identidade de Bézout). Como s·n ≡ 0 (mod n), basta acompanhar o
    coeficiente t, que cumpre  r ≡ t·a (mod n).  Ele é atualizado com a mesma conta
    dos restos:  t_novo = t_ant - q·t.
    Quando o resto chega a 0, o último resto não nulo é o mdc(a, n). Se ele for 1,
    o t correspondente é o inverso de a (reduzido módulo n).

    Retorna (y, passos):
        y      -> número entre 0 e n-1 tal que a·y ≡ 1 (mod n); None se mdc(a, n) != 1
        passos -> lista de textos com as contas feitas (para mostrar ao usuário)
    """
    r_ant, r = n, a % n        # restos:        n  e  (a mod n)
    t_ant, t = 0, 1            # coeficientes:  n ≡ 0·a  e  (a mod n) ≡ 1·a  (mod n)
    passos = [f"{a} mod {n} = {r}"]

    while r != 0:
        q = r_ant // r                 # quociente da divisão
        r_novo = r_ant - q * r         # novo resto
        t_novo = t_ant - q * t         # novo coeficiente
        if r_novo != 0:
            passos.append(f"{r_ant} = {q}·{r} + {r_novo}      t = {t_ant} - {q}·{com_par(t)} = {t_novo}")
        else:
            passos.append(f"{r_ant} = {q}·{r} + 0      (resto 0: fim)")
        r_ant, r = r, r_novo
        t_ant, t = t, t_novo

    # Aqui r_ant é o último resto não nulo (= mdc(a, n)) e t_ant é o coeficiente dele.
    if r_ant != 1:
        passos.append(f"mdc({a}, {n}) = {r_ant} ≠ 1  ->  não existe inverso")
        return None, passos

    y = t_ant % n
    passos.append(f"mdc = 1 e t = {t_ant}  ->  inverso = {t_ant} mod {n} = {y}")
    return y, passos


def verificar_condicoes(modulos):
    """
    Passo 2 do roteiro da Parte B: confere se os módulos são positivos e dois a dois coprimos.
    Mostra cada verificação e devolve True (tudo certo) ou False (fora das condições).
    """
    valido = True

    # (a) todos os módulos positivos?
    for i in range(len(modulos)):
        if modulos[i] > 0:
            print(f"  n{i + 1} = {modulos[i]}  ->  positivo, OK")
        else:
            print(f"  n{i + 1} = {modulos[i]}  ->  NÃO é positivo")
            valido = False

    if not valido:
        return False       # com módulo não positivo não faz sentido continuar

    # (b) dois a dois coprimos?  mdc(n_i, n_j) = 1 para todo par i < j
    for i in range(len(modulos)):
        for j in range(i + 1, len(modulos)):
            d = mdc(modulos[i], modulos[j])
            if d == 1:
                print(f"  mdc(n{i + 1}, n{j + 1}) = mdc({modulos[i]}, {modulos[j]}) = 1  ->  coprimos, OK")
            else:
                print(f"  mdc(n{i + 1}, n{j + 1}) = mdc({modulos[i]}, {modulos[j]}) = {d}  ->  NÃO são coprimos")
                valido = False

    return valido



# Parte A — Verificação de congruência modular


def parte_a():
    titulo("PARTE A — Verificação de congruência modular")

    # Passo 1: ler a, b e n, exigindo n > 0
    a = ler_inteiro("Digite o inteiro a: ")
    b = ler_inteiro("Digite o inteiro b: ")
    n = ler_inteiro("Digite o módulo n (n > 0): ")
    while n <= 0:
        print("  Erro: o módulo n precisa ser maior que 0.")
        n = ler_inteiro("Digite o módulo n (n > 0): ")

    # Passos 2, 3 e 4: diferença, divisão por n e teste do resto
    diferenca, quociente, resto, congruentes = verificar_congruencia(a, b, n)

    print("\nCálculos")
    print(f"  a - b = {a} - {com_par(b)} = {diferenca}")
    print(f"  Dividindo {diferenca} por {n}:  {diferenca} = {n} · {com_par(quociente)} + {resto}"
          f"   (quociente {quociente}, resto {resto})")
    print(f"  O resto é zero? {'SIM' if congruentes else 'NÃO'}")

    # Conferência extra: dois números são congruentes quando têm o mesmo resto na divisão por n
    print("\nConferência pelos restos individuais")
    print(f"  {a} mod {n} = {a % n}")
    print(f"  {b} mod {n} = {b % n}")
    print(f"  Restos {'iguais' if a % n == b % n else 'diferentes'}.")

    # Passo 5: conclusão
    print("\nConclusão")
    if congruentes:
        print(f"  Como {diferenca} é divisível por {n} (resto 0), {n} divide (a - b).")
        print(f"  Logo {a} ≡ {b} (mod {n}): {a} e {b} SÃO congruentes módulo {n}.")
    else:
        print(f"  Como {diferenca} NÃO é divisível por {n} (resto {resto} ≠ 0), {n} não divide (a - b).")
        print(f"  Logo {a} e {b} NÃO são congruentes módulo {n}.")


# ----------------------------------------------------------------------
# Parte B — Teorema Chinês do Resto
# ----------------------------------------------------------------------

def parte_b():
    titulo("PARTE B — Teorema Chinês do Resto")

    # Passo 1: quantidade de congruências (3 ou 4) e valores de a_i e n_i
    k = ler_inteiro("Quantas congruências tem o sistema? (3 ou 4): ")
    while k != 3 and k != 4:
        print("  Opção inválida: escolha 3 ou 4.")
        k = ler_inteiro("Quantas congruências tem o sistema? (3 ou 4): ")

    restos = []       # a_1, ..., a_k
    modulos = []      # n_1, ..., n_k
    for i in range(1, k + 1):
        print(f"\nEquação {i}:  x ≡ a{i} (mod n{i})")
        restos.append(ler_inteiro(f"  a{i} (resto)  = "))
        modulos.append(ler_inteiro(f"  n{i} (módulo) = "))

    print("\nSistema informado")
    for i in range(k):
        print(f"  x ≡ {restos[i]} (mod {modulos[i]})")

    # Passo 2: módulos positivos e dois a dois coprimos?
    print("\nPasso 2 — Verificação dos módulos")
    if not verificar_condicoes(modulos):
        print("\nResultado: o sistema está FORA DAS CONDIÇÕES PREVISTAS para esta atividade")
        print("(os módulos precisam ser positivos e dois a dois coprimos). Nada foi calculado.")
        return
    print("  Módulos válidos: todos positivos e dois a dois coprimos.")

    # Passo 3: N = n_1 · n_2 · ... · n_k
    N = 1
    for n_i in modulos:
        N = N * n_i
    print("\nPasso 3 — Produto dos módulos")
    print(f"  N = {' · '.join(str(n_i) for n_i in modulos)} = {N}")

    # Passos 4 e 5: para cada equação, N_i = N / n_i e o inverso y_i de N_i módulo n_i
    print("\nPassos 4 e 5 — Para cada equação: N_i = N / n_i e o inverso y_i de N_i módulo n_i")
    termos = []
    for i in range(k):
        a_i = restos[i]
        n_i = modulos[i]

        N_i = N // n_i                            # divisão exata, pois n_i divide N
        y_i, passos = inverso_modular(N_i, n_i)   # y_i existe: mdc(N_i, n_i) = 1
        produto = N_i * y_i
        termo = a_i * N_i * y_i
        termos.append(termo)

        print(f"\nEquação {i + 1}:  x ≡ {a_i} (mod {n_i})")
        print(f"  N{i + 1} = N / n{i + 1} = {N} / {n_i} = {N_i}")
        print(f"  Inverso de N{i + 1} = {N_i} módulo {n_i} (Euclides estendido):")
        for linha in passos:
            print("      " + linha)
        confere = (produto % n_i == 1 % n_i)
        print(f"  y{i + 1} = {y_i}   conferência: {N_i} · {y_i} = {produto}  e  "
              f"{produto} mod {n_i} = {produto % n_i}  ->  {'OK' if confere else 'ERRO'}")
        print(f"  Termo {i + 1}: a{i + 1} · N{i + 1} · y{i + 1} = {com_par(a_i)} · {N_i} · {y_i} = {termo}")

    # Passo 6: soma dos termos, reduzida módulo N
    soma = 0
    for termo in termos:
        soma = soma + termo
    x0 = soma % N
    quociente = soma // N
    print("\nPasso 6 — Soma dos termos e redução módulo N")
    print(f"  S = {' + '.join(com_par(t) for t in termos)} = {soma}")
    print(f"  x0 = S mod N = {soma} mod {N} = {x0}   ({soma} = {N} · {com_par(quociente)} + {x0})")

    # Passo 7: solução geral e verificação de x0 em cada congruência
    print("\nPasso 7 — Solução geral e verificação")
    print(f"  Solução geral: x = {x0} + {N}·t, com t inteiro")
    print(f"  (exemplos: t = -1 -> x = {x0 - N};  t = 0 -> x = {x0};  t = 1 -> x = {x0 + N})")
    print(f"\n  Verificando x0 = {x0} em cada congruência (mesma conta da Parte A):")
    todas_ok = True
    for i in range(k):
        dif, q, r, ok = verificar_congruencia(x0, restos[i], modulos[i])
        print(f"    x ≡ {restos[i]} (mod {modulos[i]}):  {x0} - {com_par(restos[i])} = {dif}"
              f" = {modulos[i]} · {com_par(q)} + {r}  ->  {'OK' if ok else 'FALHOU'}")
        if not ok:
            todas_ok = False

    if todas_ok:
        print(f"\nConclusão: x0 = {x0} satisfaz as {k} congruências.")
        print(f"O conjunto solução é formado por todos os inteiros x ≡ {x0} (mod {N}).")
    else:
        print("\nAtenção: x0 não satisfez todas as congruências (há erro no cálculo).")


#menu

def main():
    titulo("ATIVIDADE 1 — Congruência Modular e Teorema Chinês do Resto")
    while True:
        print("\nMenu")
        print("  1 - Parte A: verificar se a ≡ b (mod n)")
        print("  2 - Parte B: resolver sistema de congruências (TCR)")
        print("  0 - Sair")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            parte_a()
        elif opcao == "2":
            parte_b()
        elif opcao == "0":
            print("Programa encerrado.")
            break
        else:
            print("  Opção inválida.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nPrograma encerrado.")