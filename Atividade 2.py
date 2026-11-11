
# Nome:        [Rodrigo]
# Matrícula:   [2612130046]
# Disciplina:  Matemática Discreta
# Turno:       [matutino]
#Se o teste de primalidade tiver mais divisões que isso, só o começo e o fim são mostrados
LIMITE_LINHAS = 40

#Funções auxiliares

def ler_inteiro(mensagem):
    """Pede um número inteiro ao usuário e repete a pergunta até a entrada ser válida."""
    while True:
        texto = input(mensagem)
        try:
            return int(texto)
        except ValueError:
            print("  Entrada inválida: digite um número inteiro (ex.: 7 ou -3).")


def perguntar_sim_nao(mensagem):
    """Pergunta s/n e repete até receber uma resposta válida. Retorna True para 's'."""
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta == "s":
            return True
        if resposta == "n":
            return False
        print("  Responda com s ou n.")

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


def imprimir(linhas, recuo):
    """Imprime uma lista de textos, um por linha, com `recuo` espaços na frente."""
    for linha in linhas:
        print(" " * recuo + linha)

#Procedimentos matemáticos

def mdc(a, b):

    a = abs(a)
    b = abs(b)
    if a < b:                      #começa dividindo o maior pelo menor
        a, b = b, a
    passos = []
    while b != 0:
        passos.append(f"{a} = {a // b}·{b} + {a % b}")
        a, b = b, a % b
    return a, passos


def inverso_modular(a, n):

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

    #Aqui r_ant é o último resto não nulo (= mdc(a, n)) e t_ant é o coeficiente dele.
    if r_ant != 1:
        passos.append(f"mdc({a}, {n}) = {r_ant} ≠ 1  ->  não existe inverso")
        return None, passos

    y = t_ant % n
    passos.append(f"mdc = 1 e t = {t_ant}  ->  inverso = {t_ant} mod {n} = {y}")
    return y, passos

def teste_primalidade(n):

    testes = []
    d = 2
    while d * d <= n:
        resto = n % d
        testes.append((d, resto))
        if resto == 0:
            return False, d, testes
        d = d + 1
    return True, None, testes


def exp_modular(base, expoente, modulo):

    b = base % modulo            #base já reduzida módulo `modulo`
    resultado = 1 % modulo
    e = expoente

    #expoente em binário (bit mais significativo à esquerda), só para mostrar
    binario = ""
    x = expoente
    while x > 0:
        binario = str(x % 2) + binario
        x = x // 2
    if binario == "":
        binario = "0"

    passos = [f"Calcular {base}^{expoente} mod {modulo} por quadrados sucessivos",
              f"Expoente {expoente} em binário: {binario}  (bits lidos do último para o primeiro)",
              f"Em cada etapa: se o bit é 1, resultado = resultado · base; depois base = base²; tudo mod {modulo}"]
    if b != base:
        passos.append(f"Base reduzida: {base} mod {modulo} = {b}")

    etapa = 0
    while e > 0:
        etapa = etapa + 1
        bit = e % 2
        passos.append(f"Etapa {etapa}: bit {bit} (expoente restante {e})")
        if bit == 1:
            produto = resultado * b
            novo = produto % modulo
            passos.append(f"    resultado: {resultado} · {b} = {produto} ≡ {novo} (mod {modulo})")
            resultado = novo
        else:
            passos.append(f"    resultado: continua {resultado} (bit 0, não multiplica)")
        e = e // 2
        if e > 0:                      # só eleva ao quadrado se ainda restam bits
            quadrado = b * b
            novo_b = quadrado % modulo
            passos.append(f"    base:      {b}² = {quadrado} ≡ {novo_b} (mod {modulo})")
            b = novo_b

    passos.append(f"Resultado: {base}^{expoente} mod {modulo} = {resultado}")
    return resultado, passos


def linha_divisao(n, d, resto):
    """Texto de uma divisão do teste de primalidade."""
    if resto == 0:
        return f"{n} mod {d} = {resto}   <- divide"
    return f"{n} mod {d} = {resto}"


def mostrar_primalidade(nome, n):
    """Mostra o teste de primalidade de n (divisão por tentativas) e devolve True se n é primo."""
    primo, divisor, testes = teste_primalidade(n)
    print(f"  {nome} = {n}: dividir por d = 2, 3, 4, ... enquanto d·d <= {n}")

    if len(testes) <= LIMITE_LINHAS:
        for d, resto in testes:
            print("      " + linha_divisao(n, d, resto))
    else:
        for d, resto in testes[:15]:
            print("      " + linha_divisao(n, d, resto))
        print(f"      ... {len(testes) - 20} divisões omitidas (nenhuma deu resto 0) ...")
        for d, resto in testes[-5:]:
            print("      " + linha_divisao(n, d, resto))

    if primo:
        if len(testes) > 0:
            proximo = testes[-1][0] + 1
        else:
            proximo = 2
        print(f"      próximo d = {proximo}: {proximo}·{proximo} = {proximo * proximo} > {n}  ->  fim dos testes")
        print(f"      nenhum divisor encontrado  ->  {n} é PRIMO")
    else:
        print(f"      {n} é divisível por {divisor}  ->  {n} é COMPOSTO ({n} = {divisor} · {n // divisor})")
    return primo

#Parte A — Primalidade e parâmetros RSA

def verificar_p_q(p, q):
    """
    """
    print("\nPasso 1 — Condições: p e q inteiros maiores que 1 e distintos")
    valido = True
    for nome, valor in (("p", p), ("q", q)):
        if valor > 1:
            print(f"  {nome} = {valor}  ->  maior que 1, OK")
        else:
            print(f"  {nome} = {valor}  ->  NÃO é maior que 1")
            valido = False
    if p != q:
        print(f"  p = {p} e q = {q}  ->  distintos, OK")
    else:
        print(f"  p = q = {p}  ->  NÃO são distintos")
        valido = False

    if not valido:
        print("\nPasso 2 — Primalidade: não realizado (corrija as condições do Passo 1)")
        return False

    print("\nPasso 2 — Primalidade de p e q (divisão por tentativas)")
    p_primo = mostrar_primalidade("p", p)
    q_primo = mostrar_primalidade("q", q)
    return p_primo and q_primo

def parte_a():
    titulo("PARTE A — Primalidade e parâmetros RSA")

    #Passos 1 a 4: p e q válidos, n = p·q e φ(n); repete se algo não servir
    while True:
        p = ler_inteiro("Digite o inteiro p (precisa ser primo): ")
        q = ler_inteiro("Digite o inteiro q (precisa ser primo e diferente de p): ")
        if not verificar_p_q(p, q):
            print("\n  p e q não atendem às condições. Digite novos valores.\n")
            continue

        n = p * q
        phi = (p - 1) * (q - 1)
        print("\nPasso 3 — Módulo n = p · q")
        print(f"  n = {p} · {q} = {n}")
        print("\nPasso 4 — Função totiente de Euler φ(n)")
        print("  p e q são primos distintos: mdc(p, q) = 1, φ(p) = p - 1 e φ(q) = q - 1.")
        print("  Como φ é multiplicativa para números coprimos: φ(n) = φ(p) · φ(q) = (p - 1)(q - 1).")
        print(f"  φ(n) = ({p} - 1) · ({q} - 1) = {p - 1} · {q - 1} = {phi}")
        if phi < 3:
            print(f"  Não existe e com 1 < e < φ(n) = {phi}. Escolha primos maiores.\n")
            continue
        break

    #Passos 5 e 6: expoente público e, com 1 < e < φ(n) e mdc(e, φ(n)) = 1
    print("\nPasso 5 — Expoente público e, com 1 < e < φ(n)")
    print("Passo 6 — Condição: mdc(e, φ(n)) = 1  (e coprimo com φ(n))")
    while True:
        e = ler_inteiro(f"Digite o expoente público e (1 < e < {phi}): ")
        if not (1 < e < phi):
            print(f"  Erro: e = {e} não cumpre 1 < e < {phi}. Digite outro valor.")
            continue
        print(f"  Passo 5: 1 < {e} < {phi}  ->  OK")
        g, passos = mdc(e, phi)
        print(f"  Passo 6: mdc(e, φ(n)) = mdc({e}, {phi}) pelo algoritmo de Euclides:")
        imprimir(passos, 8)
        if g == 1:
            print(f"        mdc({e}, {phi}) = 1  ->  e é coprimo com φ(n), OK")
            break
        print(f"        mdc({e}, {phi}) = {g} ≠ 1  ->  e NÃO serve. Digite outro valor.")

    #Passo 7: resumo
    print("\nPasso 7 — Parâmetros escolhidos")
    print(f"  p = {p}")
    print(f"  q = {q}")
    print(f"  n = p · q = {n}")
    print(f"  φ(n) = {phi}")
    print(f"  expoente público e = {e}")
    return p, q, n, phi, e

#Parte B — Construção das chaves

def parte_b(e, phi, n):
    titulo("PARTE B — Construção das chaves")

    #Passo 1: valores da Parte A
    print("Passo 1 — Valores usados (calculados na Parte A)")
    print(f"  e = {e}")
    print(f"  φ(n) = {phi}")

    #Passo 2: d = inverso de e módulo φ(n), por Euclides estendido
    print("\nPasso 2 — Inverso multiplicativo: achar d tal que e · d ≡ 1 (mod φ(n))")
    print("  Euclides estendido: a cada divisão r_ant = q·r + r_novo, calcula-se t_novo = t_ant - q·t.")
    print("  Se o mdc for 1, o t do último resto não nulo é o inverso (reduzido módulo φ(n)).")
    d, passos = inverso_modular(e, phi)
    print(f"  Procurando d com {e} · d ≡ 1 (mod {phi}):")
    imprimir(passos, 6)
    print(f"  d = {d}")

    #Passo 3: verificação e·d ≡ 1 (mod φ(n))
    print("\nPasso 3 — Verificação de e · d ≡ 1 (mod φ(n))")
    produto = e * d
    k = produto // phi
    resto = produto % phi
    print(f"  e · d = {e} · {d} = {produto}")
    print(f"  {produto} = {phi} · {k} + {resto}   (resto {resto})")
    if resto == 1:
        print(f"  Resto 1  ->  e · d ≡ 1 (mod {phi})  ->  OK")
    else:
        print("  O resto não é 1  ->  ERRO no cálculo de d")

    #Passo 4: chaves
    print("\nPasso 4 — Chaves")
    print(f"  Chave pública:  (e, n) = ({e}, {n})")
    print(f"  Chave privada:  (d, n) = ({d}, {n})")
    if d == e:
        print("  Observação: d = e, então a chave privada coincide com a pública.")
        print("  Isso é válido matematicamente, mas inseguro na prática.")
    return d

#Parte C — Cifragem e decifragem

def parte_c(n, e, d):
    titulo("PARTE C — Cifragem e decifragem")

    # Passo 1: ler M com 0 <= M < n
    print("Passo 1 — Número M a ser cifrado, com 0 <= M < n")
    while True:
        M = ler_inteiro(f"Digite o número M (0 <= M < {n}): ")
        if 0 <= M < n:
            print(f"  Condição 0 <= M < n:  0 <= {M} < {n}  ->  OK")
            break
        print(f"  Erro: M = {M} não cumpre 0 <= M < {n}. Digite outro valor.")

    # Passo 2: cifragem C ≡ M^e (mod n)
    print(f"\nPasso 2 — Cifragem: C ≡ M^e (mod n), ou seja, C = {M}^{e} mod {n}")
    C, passos = exp_modular(M, e, n)
    imprimir(passos, 2)
    print(f"  C = {C}")

    # Passo 3: decifragem M' ≡ C^d (mod n) com a chave privada
    print(f"\nPasso 3 — Decifragem com a chave privada: M' ≡ C^d (mod n), ou seja, M' = {C}^{d} mod {n}")
    M2, passos = exp_modular(C, d, n)
    imprimir(passos, 2)
    print(f"  M' = {M2}")

    # Passo 4: resumo
    print("\nPasso 4 — Resumo")
    print(f"  Número original:          M  = {M}")
    print(f"  Número cifrado:           C  = {C}")
    print(f"  Resultado da decifragem:  M' = {M2}")

    # Passo 5: M' = M ?
    print("\nPasso 5 — Verificação: M' = M ?")
    if M2 == M:
        print(f"  {M2} = {M}  ->  SIM")
        print("  Conclusão: a decifragem recuperou o número original; as chaves funcionam.")
    else:
        print(f"  {M2} ≠ {M}  ->  NÃO")
        print("  Conclusão: ERRO, a decifragem não recuperou M (revisar os parâmetros).")
    return M, C, M2

# Parte D — Teoremas de Fermat e de Euler na exponenciação modular

def fermat_em_primo(a, nome, r, d):
    """Verifica o Pequeno Teorema de Fermat para a base a e o primo r (r = p ou r = q)."""
    print(f"\n  --- módulo {nome} = {r} (primo) ---")
    print(f"  Condições: {r} é primo (verificado na Parte A) e {r} não divide a = {a}")
    resto = a % r
    print(f"      a mod {r} = {a} mod {r} = {resto}")
    if resto == 0:
        print(f"      {r} divide {a}  ->  condição NÃO satisfeita: Fermat NÃO se aplica")
        teste = exp_modular(a, r - 1, r)[0]
        print(f"  Conferência: {a}^{r - 1} mod {r} = {teste}  ->  diferente de 1, como esperado")
        print("  Sem o teorema não se reduz o expoente: vale a exponenciação modular por reduções sucessivas.")
        return

    print(f"      {resto} ≠ 0  ->  {r} não divide a, condição satisfeita")
    print(f"  Aplicação: a^(r-1) ≡ 1 (mod r), com r - 1 = {r - 1}")
    valor, passos = exp_modular(a, r - 1, r)
    imprimir(passos, 6)
    if valor == 1:
        print(f"  {a}^{r - 1} mod {r} = 1  ->  Fermat verificado")
    else:
        print(f"  {a}^{r - 1} mod {r} = {valor}  ->  ERRO (deveria ser 1)")

    #Redução de expoente pelo teorema: a^E ≡ a^(E mod (r-1)) (mod r), aqui com E = d
    k = d // (r - 1)
    resto_exp = d % (r - 1)
    print(f"  Redução de expoente: a^E ≡ a^(E mod (r-1)) (mod r). Com E = d = {d}:")
    print(f"      {d} = {r - 1} · {k} + {resto_exp}   ->  E mod (r-1) = {resto_exp}")
    reduzido = exp_modular(a, resto_exp, r)[0]
    direto = exp_modular(a, d, r)[0]
    print(f"      {a}^{resto_exp} mod {r} = {reduzido}   (com o expoente reduzido)")
    print(f"      {a}^{d} mod {r} = {direto}   (exponenciação modular direta)")
    if reduzido == direto:
        print("      Resultados iguais  ->  a redução de expoente está correta, OK")
    else:
        print("      Resultados diferentes  ->  ERRO")


def fermat_em_composto(a, n):
    """Mostra que o Pequeno Teorema de Fermat não vale para o módulo composto n = p·q."""
    print(f"\n  --- módulo RSA n = {n} (composto) ---")
    print("  Fermat NÃO se aplica ao módulo n: n não é primo, então a condição do teorema falha.")
    valor = exp_modular(a, n - 1, n)[0]
    print(f"  Contraexemplo (só para ilustrar, o teorema não é usado): {a}^{n - 1} mod {n} = {valor}")
    if valor != 1:
        print("      diferente de 1  ->  a conclusão do teorema não vale em módulo composto.")
    else:
        print("      deu 1 por coincidência (n é pseudoprimo de Fermat nessa base);")
        print("      o teorema não garante isso para n composto.")


def parte_d(M, M2, n, phi, p, q, e, d):
    titulo("PARTE D — Teoremas de Euler e de Fermat na exponenciação modular")

    print("Teoremas e condições")
    print("  Euler:  se mdc(a, m) = 1, então a^φ(m) ≡ 1 (mod m).")
    print("          Consequência: com mdc(a, m) = 1, o expoente pode ser reduzido módulo φ(m).")
    print("  Fermat: se r é primo e r não divide a, então a^(r-1) ≡ 1 (mod r).")
    print("          (é o caso de Euler com módulo primo, pois φ(r) = r - 1)")
    print(f"  Atenção: n = p · q = {n} é composto, então Fermat NÃO se aplica ao módulo n.")
    print("  Quando as condições falham, o expoente não pode ser reduzido por esses teoremas:")
    print("  usa-se a exponenciação modular por reduções sucessivas, que vale sempre.")

    #Passo 1: o procedimento de exponenciação modular
    print("\nPasso 1 — Exponenciação modular com reduções sucessivas")
    print("  O procedimento exp_modular (quadrados sucessivos) reduz o resultado módulo m a cada")
    print("  multiplicação: os números intermediários ficam menores que m² e a potência inteira")
    print("  nunca é construída. Ele já foi usado na Parte C e é usado em todos os cálculos abaixo.")

    #Passo 2: Teorema de Euler com a base M e o módulo n
    print(f"\nPasso 2 — Teorema de Euler com base M = {M} e módulo n = {n}")
    print("  Condição: mdc(M, n) = 1")
    g, passos = mdc(M, n)
    imprimir(passos, 6)
    ed = e * d
    if g == 1:
        print(f"      mdc({M}, {n}) = 1  ->  condição satisfeita: Euler pode ser aplicado")
        print(f"  Verificação de M^φ(n) ≡ 1 (mod n), com φ(n) = {phi}:")
        valor, passos = exp_modular(M, phi, n)
        imprimir(passos, 6)
        if valor == 1:
            print(f"  {M}^{phi} mod {n} = 1  ->  Euler verificado")
        else:
            print(f"  {M}^{phi} mod {n} = {valor}  ->  ERRO (deveria ser 1)")

        k = ed // phi
        resto_exp = ed % phi
        print("  Redução de expoente: como M^φ(n) ≡ 1, vale M^E ≡ M^(E mod φ(n)) (mod n).")
        print(f"  Com E = e · d = {e} · {d} = {ed}:")
        print(f"      {ed} = {phi} · {k} + {resto_exp}   ->  E mod φ(n) = {resto_exp}")
        reduzido = exp_modular(M, resto_exp, n)[0]
        direto = exp_modular(M, ed, n)[0]
        print(f"      M^E ≡ M^{resto_exp} ≡ {reduzido} (mod {n})   (com o expoente reduzido)")
        if reduzido == direto:
            print(f"      Conferência direta: {M}^{ed} mod {n} = {direto}  ->  iguais, OK")
        else:
            print(f"      Conferência direta: {M}^{ed} mod {n} = {direto}  ->  DIFERENTES, ERRO")
        if resto_exp == 1:
            print(f"      Como E = 1 + {k}·φ(n): M^E = M · (M^φ(n))^{k} ≡ M · 1^{k} = M (mod {n}).")
            print("      É por isso que a decifragem devolve o número original.")
    else:
        print(f"      mdc({M}, {n}) = {g} ≠ 1  ->  condição NÃO satisfeita: Euler NÃO se aplica")
        print(f"  M e n têm o fator comum {g}; não é permitido reduzir o expoente módulo φ(n).")
        valor = exp_modular(M, phi, n)[0]
        print(f"  Conferência: {M}^{phi} mod {n} = {valor}  ->  diferente de 1, como esperado")
        print("  Nesse caso vale a exponenciação modular por reduções sucessivas (Passo 1), que não")
        print(f"  exige essa condição: foi ela que deu C e M' na Parte C (M' = {M2}, M = {M}).")
        print("  Por que M' = M mesmo assim? Verificação em cada primo r, com E = e · d:")
        for nome, r in (("p", p), ("q", q)):
            lado_esq = exp_modular(M, ed, r)[0]
            lado_dir = M % r
            if lado_esq == lado_dir:
                situacao = "iguais"
            else:
                situacao = "DIFERENTES"
            print(f"      módulo {nome} = {r}: M^E mod {r} = {lado_esq} e M mod {r} = {lado_dir}  ->  {situacao}")
            if M % r == 0:
                print(f"          ({r} divide M: os dois lados são ≡ 0 módulo {r})")
            else:
                print(f"          ({r} não divide M: por Fermat M^({r}-1) ≡ 1 e, como {r}-1 divide E - 1,")
                print(f"           M^E ≡ M módulo {r})")
        print(f"  Como p e q são coprimos, o Teorema Chinês do Resto junta os dois resultados: M^E ≡ M (mod {n}).")

    #Passo 3: Pequeno Teorema de Fermat nos primos p e q (e por que não vale em n)
    print("\nPasso 3 — Pequeno Teorema de Fermat (módulo primo r, base a que r não divide)")
    while True:
        a = ler_inteiro("Digite uma base a para o teste de Fermat: ")
        fermat_em_primo(a, "p", p, d)
        fermat_em_primo(a, "q", q, d)
        fermat_em_composto(a, n)
        print()
        if not perguntar_sim_nao("Testar outra base a? (s/n): "):
            break

    #Passo 4: resumo das condições
    print("\nPasso 4 — Condições de cada teorema (resumo)")
    print("  Euler:  exige mdc(base, módulo) = 1.")
    if g == 1:
        print(f"          Aqui: mdc(M, n) = mdc({M}, {n}) = 1  ->  aplicável a M.")
    else:
        print(f"          Aqui: mdc(M, n) = mdc({M}, {n}) = {g}  ->  NÃO aplicável a M.")
    print("  Fermat: exige módulo primo e base não divisível por ele.")
    print(f"          Vale em p = {p} e em q = {q} (quando não dividem a base); nunca em n = {n}.")
    print("  Se as condições falham: exponenciação modular por reduções sucessivas.")

#menu

def menu_final():
    """Pergunta o que fazer depois da Parte D e devolve '1', '2' ou '0'."""
    while True:
        print("\nO que deseja fazer agora?")
        print("  1 - Testar outro número M com as mesmas chaves")
        print("  2 - Criar novas chaves (voltar à Parte A)")
        print("  0 - Sair")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0" or opcao == "1" or opcao == "2":
            return opcao
        print("  Opção inválida.")


def main():
    titulo("ATIVIDADE 2 — Criptografia RSA simplificada")
    sair = False
    while not sair:
        p, q, n, phi, e = parte_a()
        d = parte_b(e, phi, n)
        while True:
            M, C, M2 = parte_c(n, e, d)
            parte_d(M, M2, n, phi, p, q, e, d)
            opcao = menu_final()
            if opcao != "1":
                sair = (opcao == "0")
                break
    print("Programa encerrado.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nPrograma encerrado.")