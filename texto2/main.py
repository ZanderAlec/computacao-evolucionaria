import random
import ler_textos as lt
import matplotlib.pyplot as plt
import time
import sys

# Verificar se o caminho do arquivo foi fornecido como argumento
if len(sys.argv) != 2:
    print("Uso: python main.py caminho/para/arquivo.txt")
    sys.exit(1)

# Usar o argumento da linha de comando
caminho_arquivo = sys.argv[1]
texto1, texto2 = lt.carregar_arquivos(caminho_arquivo)

from sentence_transformers import SentenceTransformer, util

# Carregar o modelo SBERT
modelo_sbert = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def gerar_texto_com_cromossomo(cromossomo, palavras):
    # Gerar o texto baseado no cromossomo
    palavras_selecionadas = [palavras[i] for i in range(len(cromossomo)) if cromossomo[i] == 1]
    texto_gerado = " ".join(palavras_selecionadas)
    return texto_gerado

def calcular_similaridade_com_cromossomo(cromossomo, palavras, texto1):
    # Gerar o texto do cromossomo
    texto2_gerado = gerar_texto_com_cromossomo(cromossomo, palavras)
    
    # Calcular a similaridade usando SBERT
    similaridade = calcular_similaridade(texto1, texto2_gerado)
    return similaridade

def calcular_similaridade(texto1, texto2):
    # Gerar embeddings para cada texto
    embedding1 = modelo_sbert.encode(texto1, convert_to_tensor=True)
    embedding2 = modelo_sbert.encode(texto2, convert_to_tensor=True)
    
    # Calcular a similaridade de cosseno entre os embeddings
    similaridade = util.cos_sim(embedding1, embedding2).item()
    
    return similaridade

def gerar_populacao_inicial(texto, tamanho_populacao):
    # Dividir o texto em palavras
    palavras = texto.split()
    tamanho_texto = len(palavras)
    
    # Gerar população inicial
    populacao = []
    for _ in range(tamanho_populacao):
        # Cada cromossomo é um vetor binário com o mesmo tamanho do texto
        cromossomo = [random.choice([0, 1]) for _ in range(tamanho_texto)]
        populacao.append(cromossomo)
    
    return populacao, palavras

def ajustar_fitness(similaridades_cromossomos, tendencia):

    fitness = []

    for i in similaridades_cromossomos:
        if tendencia == 'MAX':
            fitness.append(i)
        elif tendencia == 'MIN':
            fitness.append(1 - i)

    return fitness

def selecao_torneio_com_tendencia(populacao, fitness_geracao, tamanho_torneio, num_selecionados):
    selecionados = []
    indices_disponiveis = list(range(len(populacao)))
    
    for _ in range(num_selecionados):
        torneio = random.sample(indices_disponiveis, tamanho_torneio)
        
        fitness_torneio = [fitness_geracao[i] for i in torneio]
        
        melhor_indice = torneio[fitness_torneio.index(max(fitness_torneio))]
        
        selecionados.append(populacao[melhor_indice])
        
        indices_disponiveis.remove(melhor_indice)
    
    return selecionados

def cruzamento(populacao_selecionada):
    filhos = []
    
    if len(populacao_selecionada) % 2 == 1:
        indice_aleatorio = random.randint(0, len(populacao_selecionada) - 2)
        populacao_selecionada.append(populacao_selecionada[indice_aleatorio])
    
    # Cruzamento de ponto único para cada par de indivíduos
    for i in range(0, len(populacao_selecionada), 2):
        cromossomo1 = populacao_selecionada[i]
        cromossomo2 = populacao_selecionada[i + 1]
        
        # Escolher um ponto de corte aleatório
        ponto_corte = random.randint(1, len(cromossomo1) - 1)
        
        # Criar os filhos trocando as partes após o ponto de corte
        filho1 = cromossomo1[:ponto_corte] + cromossomo2[ponto_corte:]
        filho2 = cromossomo2[:ponto_corte] + cromossomo1[ponto_corte:]

        # print("PAI", cromossomo1)
        # print("FILHO", filho1)
        # print("MÃE", cromossomo2)
        # print("FILHA", filho2)
        # print("PAI", cromossomo1)
        
        filhos.append(filho1)
        filhos.append(filho2)
    
    return filhos

def mutacao(cromossomos, taxa_mutacao=0.05):
    for cromossomo in cromossomos:
        # print("antes", cromossomo)
        for i in range(len(cromossomo)):
            # Realiza a mutação com a taxa de mutação
            if random.random() < taxa_mutacao:
                cromossomo[i] = 1 - cromossomo[i]  # Alterna entre 0 e 1
        # print("depois", cromossomo)
    return cromossomos

def substituicao(pop, fitness, tam_eliminate):
    # Ordena a população com base no fitness em ordem decrescente
    indices_ordenados = sorted(range(len(fitness)), key=lambda k: fitness[k], reverse=True)
    pop_ordenada = [pop[i] for i in indices_ordenados]
    
    # Remove os últimos elementos (piores) de acordo com tam_eliminate
    pop_final = pop_ordenada[:-tam_eliminate]
    
    return pop_final


if __name__ == "__main__":

    inicio = time.time()

    max_geracoes = 100
    geracao = 0
    tam_pop = 10

    melhora_fit_historica = 0
    piora_fit_historica = 0
    
    cont_max = 0
    cont_min = 0

    similaridades_geracoes_MAX = []
    similaridades_geracoes_MIN = []

    populacao_MAX, palavras = gerar_populacao_inicial(texto2, tam_pop)
    populacao_MIN, palavras = gerar_populacao_inicial(texto2, tam_pop)

    # Criar listas para armazenar os valores de fitness ao longo das gerações
    fitness_historico_MAX = []
    fitness_historico_MIN = []

    #DEBUG: SIMILARIDADE COM OS TEXTOS COMPLETOS
    # print(calcular_similaridade(texto1, texto2))

    while max_geracoes > geracao and cont_max < 8 or cont_min < 8:

        similaridades_cromossomos_MAX = [calcular_similaridade_com_cromossomo(cromossomo, palavras, texto1) for cromossomo in populacao_MAX]
        similaridades_cromossomos_MIN = [calcular_similaridade_com_cromossomo(cromossomo, palavras, texto1) for cromossomo in populacao_MIN]

        # similaridade_media_MAX = sum(similaridades_cromossomos_MAX) / len(similaridades_cromossomos_MAX)
        # similaridade_media_MIN = sum(similaridades_cromossomos_MIN) / len(similaridades_cromossomos_MIN)

        similaridade_MAX = max(similaridades_cromossomos_MAX)
        similaridade_MIN = max(similaridades_cromossomos_MIN)

        fitness_geracao_MAX = ajustar_fitness(similaridades_cromossomos_MAX, tendencia="MAX")
        fitness_geracao_MIN = ajustar_fitness(similaridades_cromossomos_MIN, tendencia="MIN")

        print("GERAÇÃO: ", geracao)
        print(f"MAX: Similaridade Max: {similaridade_MAX*100:.2f}% - Fitness: {max(fitness_geracao_MAX*100):.2f}")
        print(f"MIN: Similaridade Min: {similaridade_MIN*100:.2f}% - Fitness: {max(fitness_geracao_MIN*100):.2f}")

        selecionados_MAX = selecao_torneio_com_tendencia(populacao_MAX, fitness_geracao_MAX, tamanho_torneio=3, num_selecionados=4)
        selecionados_MIN = selecao_torneio_com_tendencia(populacao_MIN, fitness_geracao_MIN, tamanho_torneio=3, num_selecionados=4)

        # MAXIMIZANDO SIMILARIDADE
        filhos_MAX = cruzamento(selecionados_MAX)
        mutantes_MAX = mutacao(selecionados_MAX)

        filhos_similaridades_MAX = [calcular_similaridade_com_cromossomo(cromossomo, palavras, texto1) for cromossomo in filhos_MAX]
        mutantes_similaridades_MAX = [calcular_similaridade_com_cromossomo(cromossomo, palavras, texto1) for cromossomo in mutantes_MAX]

        descends_MAX = []
        descends_similaridades_MAX = []

        descends_MAX.extend(filhos_MAX)
        descends_MAX.extend(mutantes_MAX)

        descends_similaridades_MAX.extend(filhos_similaridades_MAX)
        descends_similaridades_MAX.extend(mutantes_similaridades_MAX)

        descends_fitness_MAX = ajustar_fitness(descends_similaridades_MAX, tendencia="MAX")

        populacao_MAX.extend(descends_MAX)
        fitness_geracao_MAX.extend(descends_fitness_MAX)

        populacao_MAX = substituicao(populacao_MAX, fitness_geracao_MAX, len(descends_MAX))

        # MINIMIZANDO SIMILARIDADE
        filhos_MIN = cruzamento(selecionados_MIN)
        mutantes_MIN = mutacao(selecionados_MIN)

        filhos_similaridades_MIN = [calcular_similaridade_com_cromossomo(cromossomo, palavras, texto1) for cromossomo in filhos_MIN]
        mutantes_similaridades_MIN = [calcular_similaridade_com_cromossomo(cromossomo, palavras, texto1) for cromossomo in mutantes_MIN]

        descends_MIN = []
        descends_similaridades_MIN = []

        descends_MIN.extend(filhos_MIN)
        descends_MIN.extend(mutantes_MIN)

        descends_similaridades_MIN.extend(filhos_similaridades_MIN)
        descends_similaridades_MIN.extend(mutantes_similaridades_MIN)

        descends_fitness_MIN = ajustar_fitness(descends_similaridades_MIN, tendencia="MIN")

        populacao_MIN.extend(descends_MIN)
        fitness_geracao_MIN.extend(descends_fitness_MIN)

        populacao_MIN = substituicao(populacao_MIN, fitness_geracao_MIN, len(descends_MIN))

        geracao += 1

        if melhora_fit_historica + 0.01 >= max(fitness_geracao_MAX):
            cont_max += 1
        else:
            melhora_fit_historica = max(fitness_geracao_MAX)
            cont_max = 0
        if piora_fit_historica + 0.01 >= max(fitness_geracao_MIN):
            cont_min += 1
        else:
            piora_fit_historica = max(fitness_geracao_MIN)
            cont_min = 0        
        
        print("CONT_MAX:", cont_max)
        print("CONT_MIN:", cont_min)

        # Dentro do while, após calcular fitness_geracao_MAX e fitness_geracao_MIN, adicione:
        fitness_historico_MAX.append(max(fitness_geracao_MAX) * 100)  # Multiplicando por 100 para escala percentual
        fitness_historico_MIN.append(max(fitness_geracao_MIN) * 100)

    if max(fitness_geracao_MAX) > max(fitness_geracao_MIN):
        print("TEXTOS SIMILARES: ", similaridade_MAX)
    else:
        print("TEXTOS NãO SIMILARES: ", similaridade_MIN)
    
    final = time.time()
    tempo_total = (final - inicio) / 60
    print(f"Tempo de execução: {tempo_total:.2f} minutos")

    # Após o while, criar o gráfico:
    # Preparar os dados para o gráfico
    geracoes = list(range(len(fitness_historico_MAX)))

    # Criar o gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(geracoes, fitness_historico_MAX, 'b-', label='Fitness Maximização', linewidth=2)
    plt.plot(geracoes, fitness_historico_MIN, 'r-', label='Fitness Minimização', linewidth=2)

    # Configurar o gráfico
    plt.title('Evolução do Fitness ao Longo das Gerações')
    plt.xlabel('Gerações')
    plt.ylabel('Fitness (%)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.ylim(0, 100)

    # Mostrar o gráfico
    plt.show()

    