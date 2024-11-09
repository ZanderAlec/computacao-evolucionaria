import random
import ler_textos as lt

texto1, texto2, texto3 = lt.carregar_arquivos("textos.txt")

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

def monitorar_tendencia(similaridades_geracoes, janela=5, limite_tendencia=0.01):
    
    if len(similaridades_geracoes) < janela + 1:
        return None  # Não há gerações suficientes para calcular a média móvel

    # Calcular a média das últimas `janela` gerações
    media_atual = sum(similaridades_geracoes[-janela:]) / janela
    media_anterior = sum(similaridades_geracoes[-(janela + 1):-1]) / janela
    
    # Verificar tendência com base na diferença das médias móveis
    diferenca = media_atual - media_anterior

    if diferenca > limite_tendencia:
        return 'aumentar'
    elif diferenca < -limite_tendencia:
        return 'diminuir'
    else:
        return 'estavel'

def ajustar_fitness(similaridades_cromossomos, tendencia):

    fitness = []

    for i in similaridades_cromossomos:
        if tendencia == 'diminuir':
            fitness.append(1 - i)
        else:
            fitness.append(i)

    return fitness

def selecao_torneio_com_tendencia(populacao, fitness_geracao, tamanho_torneio, num_selecionados, tendencia):
    selecionados = []
    indices_disponiveis = list(range(len(populacao)))
    
    for _ in range(num_selecionados):
        torneio = random.sample(indices_disponiveis, tamanho_torneio)
        
        fitness_torneio = [fitness_geracao[i] for i in torneio]
        
        if tendencia == 'diminuir':
            melhor_indice = torneio[fitness_torneio.index(min(fitness_torneio))]
        else:
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

    max_geracoes = 100
    geracao = 0
    tam_pop = 10
    best_sim = 0
    worst_sim = 100

    similaridades_geracoes = []
    populacao, palavras = gerar_populacao_inicial(texto3, tam_pop)


    while max_geracoes > geracao and best_sim < 100 and worst_sim > 0:

        similaridades_cromossomos = [calcular_similaridade_com_cromossomo(cromossomo, palavras, texto1) for cromossomo in populacao]
        similaridade_media = sum(similaridades_cromossomos) / len(similaridades_cromossomos)

        similaridades_geracoes.append(similaridade_media)
        tendencia = monitorar_tendencia(similaridades_geracoes, 5, 0.01)
        fitness_geracao = ajustar_fitness(similaridades_cromossomos, tendencia)

        print(f"Geração {geracao} - Similaridade média: {similaridade_media*100:.2f}% - Tendência: {tendencia} - Fitness: {max(fitness_geracao):.4f}")

        selecionados = selecao_torneio_com_tendencia(populacao, fitness_geracao, tamanho_torneio=3, num_selecionados=4, tendencia=tendencia)

        filhos = cruzamento(selecionados)
        mutantes = mutacao(selecionados)

        filhos_similaridades = [calcular_similaridade_com_cromossomo(cromossomo, palavras, texto1) for cromossomo in filhos]
        mutantes_similaridades = [calcular_similaridade_com_cromossomo(cromossomo, palavras, texto1) for cromossomo in mutantes]

        descends = []
        descends_similaridades = []

        descends.extend(filhos)
        descends.extend(mutantes)

        descends_similaridades.extend(filhos_similaridades)
        descends_similaridades.extend(mutantes_similaridades)

        descends_fitness = ajustar_fitness(descends_similaridades, tendencia)

        populacao.extend(descends)
        fitness_geracao.extend(descends_fitness)

        populacao = substituicao(populacao, fitness_geracao, len(descends))

        geracao += 1
        if best_sim < similaridade_media:
            best_sim = similaridade_media
        if worst_sim > similaridade_media:
            worst_sim = similaridade_media
    
    print(f"Geração {geracao} - Similaridade média: {similaridade_media*100:.2f}% - Tendência: {tendencia} - Fitness: {max(fitness_geracao):.4f}")
    