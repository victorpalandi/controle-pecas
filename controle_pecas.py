"""
Controle de produção e qualidade de peças.

Cadastra peças, aprova ou reprova cada uma conforme os critérios de qualidade,
guarda as aprovadas em caixas de 10 unidades e gera um relatório final.
"""

import math

PESO_MIN = 95.0
PESO_MAX = 105.0
COMPRIMENTO_MIN = 10.0
COMPRIMENTO_MAX = 20.0
CORES_ACEITAS = ("azul", "verde")
CAPACIDADE_CAIXA = 10

# Categorias de reprovação: aparecem na mensagem de cada peça e na contagem do relatório.
MOTIVO_PESO = "peso fora do intervalo"
MOTIVO_COR = "cor não aceita"
MOTIVO_COMPRIMENTO = "comprimento fora do intervalo"
CATEGORIAS_MOTIVO = (MOTIVO_PESO, MOTIVO_COR, MOTIVO_COMPRIMENTO)


# ---------------------------------------------------------------- entrada

def ler_texto(mensagem):
    """Lê um texto que não pode ficar vazio."""
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("  Valor vazio. Tente novamente.")


def ler_numero(mensagem):
    """Lê um número positivo. Aceita vírgula ou ponto como separador decimal."""
    while True:
        texto = input(mensagem).strip().replace(",", ".")
        try:
            numero = float(texto)
        except ValueError:
            numero = math.nan
        # float() aceita "nan" e "inf"; math.isfinite() barra os dois e também o texto inválido.
        if not math.isfinite(numero):
            print("  Digite um número válido, por exemplo 100 ou 99,5.")
            continue
        if numero <= 0:
            print("  O valor precisa ser maior que zero.")
            continue
        return numero


# ------------------------------------------------------------------ regras

def avaliar_peca(peso, cor, comprimento):
    """
    Confere a peça contra os três critérios de qualidade.
    Devolve uma lista de (categoria, descrição), uma para cada critério violado.
    Lista vazia significa peça aprovada.
    """
    motivos = []
    if not PESO_MIN <= peso <= PESO_MAX:
        motivos.append((MOTIVO_PESO, f"{MOTIVO_PESO} ({peso:g}g)"))
    if cor not in CORES_ACEITAS:
        motivos.append((MOTIVO_COR, f"{MOTIVO_COR} ({cor})"))
    if not COMPRIMENTO_MIN <= comprimento <= COMPRIMENTO_MAX:
        motivos.append((MOTIVO_COMPRIMENTO, f"{MOTIVO_COMPRIMENTO} ({comprimento:g}cm)"))
    return motivos


def texto_motivos(motivos):
    """Junta as descrições dos motivos em uma única frase."""
    return "; ".join(descricao for _, descricao in motivos)


def buscar_peca(pecas, id_peca):
    """Procura uma peça pelo identificador, sem diferenciar maiúsculas de minúsculas."""
    for peca in pecas:
        if peca["id"].lower() == id_peca.lower():
            return peca
    return None


def montar_caixas(pecas):
    """
    Distribui as peças aprovadas em caixas de 10, na ordem de cadastro.
    Devolve (caixas_fechadas, caixa_aberta).
    As caixas são recalculadas a cada consulta, então remover uma peça
    nunca deixa o estoque inconsistente.
    """
    aprovadas = [p for p in pecas if p["aprovada"]]
    total_fechadas = len(aprovadas) // CAPACIDADE_CAIXA
    caixas_fechadas = []
    for numero in range(total_fechadas):
        inicio = numero * CAPACIDADE_CAIXA
        caixas_fechadas.append(aprovadas[inicio:inicio + CAPACIDADE_CAIXA])
    caixa_aberta = aprovadas[total_fechadas * CAPACIDADE_CAIXA:]
    return caixas_fechadas, caixa_aberta


# ------------------------------------------------------------------ opções

def cadastrar_peca(pecas):
    print("\n--- Cadastrar nova peça ---")
    id_peca = ler_texto("ID da peça: ")
    if buscar_peca(pecas, id_peca):
        print("  Já existe uma peça com esse ID. Cadastro cancelado.")
        return
    peso = ler_numero("Peso (g): ")
    cor = ler_texto("Cor: ").lower()
    comprimento = ler_numero("Comprimento (cm): ")

    motivos = avaliar_peca(peso, cor, comprimento)
    peca = {
        "id": id_peca,
        "peso": peso,
        "cor": cor,
        "comprimento": comprimento,
        "aprovada": not motivos,
        "motivos": motivos,
    }
    pecas.append(peca)

    if peca["aprovada"]:
        caixas_fechadas, caixa_aberta = montar_caixas(pecas)
        print("  Peça APROVADA.")
        # Sem caixa aberta logo após aprovar uma peça: a décima acabou de entrar.
        if not caixa_aberta:
            print(f"  Caixa {len(caixas_fechadas)} completou {CAPACIDADE_CAIXA} peças e foi fechada.")
    else:
        print("  Peça REPROVADA: " + texto_motivos(motivos) + ".")


def descrever(peca):
    return (f"ID {peca['id']} | {peca['peso']:g}g | {peca['cor']} | "
            f"{peca['comprimento']:g}cm")


def listar_pecas(pecas):
    print("\n--- Peças aprovadas e reprovadas ---")
    if not pecas:
        print("  Nenhuma peça cadastrada.")
        return
    aprovadas = [p for p in pecas if p["aprovada"]]
    reprovadas = [p for p in pecas if not p["aprovada"]]

    print(f"\nAprovadas ({len(aprovadas)}):")
    for p in aprovadas:
        print("  " + descrever(p))
    if not aprovadas:
        print("  Nenhuma.")

    print(f"\nReprovadas ({len(reprovadas)}):")
    for p in reprovadas:
        print("  " + descrever(p) + " -> " + texto_motivos(p["motivos"]))
    if not reprovadas:
        print("  Nenhuma.")


def remover_peca(pecas):
    print("\n--- Remover peça cadastrada ---")
    if not pecas:
        print("  Nenhuma peça cadastrada.")
        return
    id_peca = ler_texto("ID da peça a remover: ")
    peca = buscar_peca(pecas, id_peca)
    if not peca:
        print("  Peça não encontrada.")
        return
    pecas.remove(peca)
    if peca["aprovada"]:
        print("  Peça removida. As caixas foram reagrupadas com as aprovadas restantes.")
    else:
        print("  Peça reprovada removida. As caixas não mudam.")


def listar_caixas_fechadas(pecas):
    print("\n--- Caixas fechadas ---")
    caixas_fechadas, caixa_aberta = montar_caixas(pecas)
    if not caixas_fechadas:
        print("  Nenhuma caixa fechada ainda.")
    for numero, caixa in enumerate(caixas_fechadas, start=1):
        ids = ", ".join(p["id"] for p in caixa)
        print(f"  Caixa {numero} ({len(caixa)}/{CAPACIDADE_CAIXA}): {ids}")
    if caixa_aberta:
        print(f"  (Caixa {len(caixas_fechadas) + 1} em andamento: "
              f"{len(caixa_aberta)}/{CAPACIDADE_CAIXA} peças)")


def gerar_relatorio(pecas):
    print("\n=========== RELATÓRIO FINAL ===========")
    aprovadas = [p for p in pecas if p["aprovada"]]
    reprovadas = [p for p in pecas if not p["aprovada"]]
    caixas_fechadas, caixa_aberta = montar_caixas(pecas)
    caixas_usadas = len(caixas_fechadas) + (1 if caixa_aberta else 0)

    print(f"Total de peças cadastradas: {len(pecas)}")
    print(f"Total de peças aprovadas:   {len(aprovadas)}")
    print(f"Total de peças reprovadas:  {len(reprovadas)}")

    if reprovadas:
        contagem = {categoria: 0 for categoria in CATEGORIAS_MOTIVO}
        for p in reprovadas:
            for categoria, _ in p["motivos"]:
                contagem[categoria] += 1
        print("\nMotivos de reprovação (uma peça pode ter mais de um):")
        for categoria, quantidade in contagem.items():
            if quantidade:
                print(f"  {categoria}: {quantidade}")

    print(f"\nCaixas utilizadas: {caixas_usadas}")
    print(f"  Fechadas: {len(caixas_fechadas)}")
    if caixa_aberta:
        print(f"  Aberta: 1, com {len(caixa_aberta)} de {CAPACIDADE_CAIXA} peças")
    print("=======================================")


# -------------------------------------------------------------------- menu

def mostrar_menu():
    print("\n===== CONTROLE DE PEÇAS =====")
    print("1 - Cadastrar nova peça")
    print("2 - Listar peças aprovadas/reprovadas")
    print("3 - Remover peça cadastrada")
    print("4 - Listar caixas fechadas")
    print("5 - Gerar relatório final")
    print("0 - Sair")


def main():
    pecas = []
    acoes = {
        "1": cadastrar_peca,
        "2": listar_pecas,
        "3": remover_peca,
        "4": listar_caixas_fechadas,
        "5": gerar_relatorio,
    }
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            print("Encerrando o programa.")
            break
        acao = acoes.get(opcao)
        if acao:
            acao(pecas)
        else:
            print("Opção inválida. Digite um número de 0 a 5.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C ou fim da entrada: sai sem mostrar o erro técnico do Python.
        print("\nPrograma encerrado.")
