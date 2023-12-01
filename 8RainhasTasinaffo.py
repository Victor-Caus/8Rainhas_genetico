import random
import matplotlib.pyplot as plt

# Cada estado/individuo sera uma cadeia onde rainhas[i] representa em qual coluna está a rainha da linha i

def gerar_populacao(tamanho_cromossomo: int, tamanho_populacao: int):
    """
    Função para gerar uma população inicial de indivíduos para um algoritmo genético.

    Args:
        tamanho_cromossomo (int): Número máximo de valores que cada gene do cromossomo pode ter.
        tamanho_populacao (int): Tamanho da população a ser gerada.

    Returns:
        list: Lista de indivíduos, onde cada indivíduo é uma lista de genes (cromossomo).
    """
    populacao = []
    for _ in range(tamanho_populacao):
        cromossomo = []
        for _ in range(tamanho_cromossomo):
            cromossomo.append(random.randint(0, tamanho_cromossomo - 1))
        populacao.append(cromossomo)
    return populacao
def aptidao(cromossomo: list):
    """
    Função de fitness (aptidão): Retorna o número de pares de rainhas não atacantes (Quanto mais aptidão melhor é o estado)

    Args:
        cromossomo (list): Lista representando o cromossomo (indivíduo/estado).

    Returns:
        int: Número de pares de rainhas não atacantes.
    """
    colisoes = 0
    comprimento = len(cromossomo)

    # Varrer todos os pares distintos e ver se há colisao ou nao entre eles
    for i in range(0, comprimento - 1):
        for j in range(i + 1, comprimento-1):
            #Ataque vertical da rainha
            if cromossomo[i] == cromossomo[j]:
                colisoes += 1

            #Ataque diagonal da rainha
            if abs(cromossomo[i] - cromossomo[j]) == abs(i - j):
                colisoes += 1
    # Total de pares (pela formula da PA) - pares colidindo:
    return (comprimento * (comprimento - 1))/2 - colisoes

def selecao(populacao: list) -> list:
    """
    Função para selecionar os indivíduos mais aptos da população.

    Args:
        populacao (list): Lista de indivíduos.

    Returns:
        list: Lista contendo os pares selecionados para reproduzir (posição par reproduzirá com posição impar seguinte)
    """
    # Avaliação de cada indivíduo pela função de fitness
    pontuacoes = [aptidao(individuo) for individuo in populacao]

    # Cálculo das probabilidades de seleção proporcional à pontuação de fitness
    total_pontuacao = sum(pontuacoes)
    probabilidades = [pontuacao / total_pontuacao for pontuacao in pontuacoes]

    # Seleção de pares para reprodução com base nas probabilidades
    pares_selecionados = []
    for _ in range(len(populacao) // 2):
        # Escolha de dois indivíduos aleatórios, considerando as probabilidades
        par = random.choices(populacao, weights=probabilidades, k=2)
        pares_selecionados.append(par)

    return pares_selecionados
    # Note que o enunciado do LAB possibilita que um individuo seja escolhido duas vezes, isso será
    # a reprodução assexuada

def crossover(pai1: list, pai2: list) -> list:
    """
    Função para realizar o crossover entre dois pais e gerar dois filhos

    Args:
        pai1 (list): Lista representando o primeiro pai (cromossomo).
        pai2 (list): Lista representando o segundo pai (cromossomo).

    Returns:
        list: Lista contendo um ou mais filhos gerados pelo crossover.
    """
    descendentes = []

    ponto_crossover = random.randint(0, len(pai1) - 1)
    filho1 = pai1[:ponto_crossover] + pai2[ponto_crossover:]
    filho2 = pai1[ponto_crossover:] + pai2[:ponto_crossover]
    descendentes.append(filho1)
    descendentes.append(filho2)

    return descendentes

def mutacao(cromossomo: list, probabilidade_mutacao: float = 0.01):
    """
    Função para realizar mutações aleatórias em um cromossomo.

    Args:
        cromossomo (list): Lista representando o cromossomo a ser mutado.
        probabilidade_mutacao (float): Probabilidade de mutação para cada gene (padrão: 0.001).

    Returns:
        list: Cromossomo mutado.
    """
    for i in range(len(cromossomo)):
        if random.random() < probabilidade_mutacao:
            cromossomo[i] = random.randint(0, len(cromossomo) - 1)
    return cromossomo

def algoritmo_genetico_n_rainhas(dimensoes=8, tamanho_populacao=4, geracoes=100, taxa_mutacao=0.01):
    """
    Função que implementa um algoritmo genético para otimização de problemas de maximização.

    Args:
        dimensoes (int): Número de dimensões do espaço de busca.
        tamanho_populacao (int): Tamanho da população a ser gerada.
        geracoes (int): Número de gerações que serão executadas.
        taxa_mutacao (float): Taxa de mutação que será aplicada aos indivíduos selecionados para reprodução.

    Returns:
        list: Lista de resultados contendo a geração atual, o melhor indivíduo da geração atual e o melhor
        indivíduo encontrado até o momento.
    """
    populacao = gerar_populacao(dimensoes, tamanho_populacao)
    melhor_cromossomo = populacao[0] # Só para não ficar vazio inicialmente

    resultados = [] # Lista que armazenará os resultados

    for geracao in range(geracoes):
        nova_populacao = []
        # Escolha aleatória dos pares de pais, tendo como peso o fitness:
        pares = selecao(populacao)
        for par in pares:
            # Gerar 2 filhos para cada par a partir do crossover:
            filhos = crossover(par[0], par[1])
            # Aplicar mutação em cada filho e colocar na nova população:
            for filho in filhos:
                nova_populacao.append(mutacao(filho))

        # Avaliar qual é o melhor cromossomo, para isso usar a função anônima para selecionar o com mais aptidão:
        melhor_cromossomo_atual = max(nova_populacao, key=lambda x: aptidao(x))

        # Atualizar o melhor cromossomo
        if aptidao(melhor_cromossomo_atual) > aptidao(melhor_cromossomo):
            melhor_cromossomo = melhor_cromossomo_atual

        # Salvar os resultados:
        resultados.append([geracao,
                        [melhor_cromossomo_atual, aptidao(melhor_cromossomo_atual)],
                        [melhor_cromossomo, aptidao(melhor_cromossomo)]])

        # População é atualizada:
        populacao = nova_populacao

    return resultados

def plotar_geracoes(results):
    """
    Plota um gráfico com os resultados de cada geração, destacando a evolução do melhor fitness.

    Args:
        results (list): Lista de resultados gerados pelo algoritmo genético.

    Returns:
        None
    """
    geracao = [result[0] for result in results]
    melhor_fitness_geracao = [result[1][1] for result in results]
    melhor_fitness_geral = [result[2][1] for result in results]

    # Cria a figura com subplots
    fig, ax1 = plt.subplots(figsize=(10, 7))

    # Plota o gráfico de linha para o melhor fitness da geração
    ax1.plot(geracao, melhor_fitness_geracao, label='Melhor Fitness da Geração', color='blue', marker='s')
    ax1.set_xlabel('Geração')
    ax1.set_ylabel('Melhor Fitness da Geração', color='blue', fontsize=12)  # Aumenta o tamanho da fonte
    ax1.tick_params('y', colors='blue')

    # Adiciona uma segunda escala para o melhor fitness geral
    ax2 = ax1.twinx()
    ax2.plot(geracao, melhor_fitness_geral, label='Melhor Fitness Geral', color='green', marker='s')
    ax2.set_ylabel('Melhor Fitness Geral', color='green', fontsize=12)  # Aumenta o tamanho da fonte
    ax2.tick_params('y', colors='green')

    # Ajusta as escalas para serem iguais com uma pequena margem superior e inferior
    min_y = min(min(melhor_fitness_geracao), min(melhor_fitness_geral)) - 0.5
    max_y = max(max(melhor_fitness_geracao), max(melhor_fitness_geral)) + 0.5
    ax1.set_ylim(min_y, max_y)
    ax2.set_ylim(min_y, max_y)

    # Adiciona legenda
    fig.legend(loc='upper right', bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes, fontsize=10)  # Reduz o tamanho da fonte

    # Ajusta o layout para garantir que o título e os números estejam visíveis
    fig.tight_layout(rect=[0, 0.05, 0.85, 0.95])  # Reduz o espaço lateral em branco

    plt.title('Evolução do Melhor Fitness ao Longo das Gerações', pad=20, fontsize=14)  # Aumenta o tamanho da fonte do título
    plt.show()

def desenhar_tabuleiro(rainhas: list):
    """
    Função para desenhar um tabuleiro de xadrez com as posições das rainhas, numeração e linhas horizontais.

    Args:
        rainhas (list): Lista representando as posições das rainhas no tabuleiro.

    Returns:
        None
    """
    tamanho = len(rainhas)

    # Desenha a numeração superior
    print("   ", end="")
    for i in range(tamanho):
        print(f"  {i} ", end="")
    print("\n   +" + "---+" * tamanho)

    for i in range(tamanho):
        # Desenha a numeração lateral
        print(f" {i} |", end="")

        for j in range(tamanho):
            if (i + j) % 2 == 0:
                # Quadrado branco
                if rainhas[i] == j:
                    print(" ♛ |", end="")
                else:
                    print("   |", end="")
            else:
                # Quadrado preto
                if rainhas[i] == j:
                    print(" ♛ |", end="")
                else:
                    print("   |", end="")

        print("\n   +" + "---+" * tamanho)

resultados = algoritmo_genetico_n_rainhas(dimensoes=8, tamanho_populacao=64, geracoes=100,taxa_mutacao=0.001)

# Exibir informações sobre cada geração
for resultado in resultados:
    print(f"Geração: {resultado[0]} | Melhor da geração: {resultado[1][1]} | Melhor global: {resultado[2][1]}")

# Exibir o melhor resultado encontrado
melhor_resultado = resultados[-1]
print("\nUm dos melhores resultados:")
print(
    f"Geração: {melhor_resultado[0]} | Genótipo: {melhor_resultado[2][0]} | Aptidão: {melhor_resultado[2][1]}")

# Mostrar o tabuleiro do melhor resultado
desenhar_tabuleiro(melhor_resultado[2][0])

# Plotar a evolução do fitness ao longo das gerações
plotar_geracoes(resultados)
