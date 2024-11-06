from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import imprimir as imp


def vetorizar_textos(textos):
    vetorizer = TfidfVectorizer()
    matriz_tfidf = vetorizer.fit_transform(textos)
    # Obtém os nomes das palavras (vocabulário) e transforma a matriz em uma lista de vetores
    vocabulário = vetorizer.get_feature_names_out()
    vetores = matriz_tfidf.toarray()
    
    return vetores, vocabulário

def gerar_populacao_inicial(vetor1, vetor2, vocab, tamanho_populacao=10, amplitude_mutacao=0.1):
    populacao = []
    
    # Convertendo os vetores para palavras
    palavras_texto1 = set([vocab[i] for i in range(len(vetor1)) if vetor1[i] > 0])
    palavras_texto2 = set([vocab[i] for i in range(len(vetor2)) if vetor2[i] > 0])
    
    # Garantir que não tentemos selecionar um número de palavras maior do que o número disponível
    num_palavras_texto1_max = max(1, len(palavras_texto1) // 2)
    num_palavras_texto2_max = max(1, len(palavras_texto2) // 2)
    
    # Gerar cromossomos com maior diversidade
    for _ in range(tamanho_populacao):
        cromossomo = []
        
        # Selecionar palavras aleatórias de ambos os textos
        num_palavras_texto1 = np.random.randint(1, num_palavras_texto1_max + 1)  # Garantir que a seleção seja válida
        num_palavras_texto2 = np.random.randint(1, num_palavras_texto2_max + 1)  # Garantir que a seleção seja válida
        
        cromossomo.extend(np.random.choice(list(palavras_texto1), size=num_palavras_texto1, replace=False))
        cromossomo.extend(np.random.choice(list(palavras_texto2), size=num_palavras_texto2, replace=False))
        
        # Certificar que o cromossomo tenha pelo menos algumas palavras dos dois textos
        while len(cromossomo) < 5:  # Garantir um número mínimo de palavras por cromossomo
            cromossomo.append(np.random.choice(list(palavras_texto1 | palavras_texto2)))
        
        # Criar um vetor do mesmo tamanho que o vocabulário, preenchido com zeros
        vetor_cromossomo = np.zeros(len(vocab))
        
        # Para cada palavra no cromossomo, encontrar seu índice no vocabulário
        # e atribuir um valor positivo (1.0 + mutação)
        for palavra in cromossomo:
            if isinstance(palavra, str):  # se for uma palavra
                idx = np.where(vocab == palavra)[0]
                if len(idx) > 0:
                    vetor_cromossomo[idx[0]] = 1.0 + np.random.uniform(-amplitude_mutacao, amplitude_mutacao)
        
        populacao.append(vetor_cromossomo)
    
    return np.array(populacao)

def cromossomo_para_palavras(cromossomo, vocabulário):
    indices_ordenados = np.argsort(cromossomo)[::-1]
    palavras_ordenadas = [vocabulário[i] for i in indices_ordenados]
    
    return palavras_ordenadas

def calcular_similaridade(vetor1, vetor2):
    return cosine_similarity([vetor1], [vetor2])[0][0]

def avaliar_populacao(populacao, vetor_texto1, vetor_texto2):
    similaridades = []
    
    for cromossomo in populacao:
        # Calcular similaridade do cromossomo com ambos os textos
        sim_texto1 = calcular_similaridade(cromossomo, vetor_texto1)
        sim_texto2 = calcular_similaridade(cromossomo, vetor_texto2)
        
        # A similaridade do cromossomo será a média das duas similaridades
        similaridade_media = (sim_texto1 + sim_texto2) / 2
        similaridades.append(similaridade_media)
    
    aptidoes = [aptidao_suavizada(sim) for sim in similaridades]

    return similaridades, aptidoes

def aptidao_suavizada(similaridade):
    # Definindo o intervalo de suavização entre 0.45 e 0.55
    limite_inferior = 0.45
    limite_superior = 0.55
    
    if similaridade == 0 or similaridade == 1 or similaridade == 0.5:
        return 1
    elif 0 < similaridade <= 0.4499:
        return 0.9999 * (1 - similaridade / 0.4499)  # Varia de 99.99 a 0
    elif 0.5501 <= similaridade < 1:
        return 0.9999 * (similaridade - 0.5501) / (1 - 0.5501)  # Varia de 0 a 99.99
    elif limite_inferior < similaridade < 0.5:
        return 0.5 + (similaridade - limite_inferior) * (1 - 0.5)  # Varia de 50 a 100
    elif 0.5 < similaridade < limite_superior:
        return 1 - (similaridade - 0.5) * (1 - 0.5)  # Varia de 100 a 50
    else:
        print("ENTROU NO ELSE DE aptidao_suavizada:", similaridade)
        return 0

def ordenar_populacao(populacao, similaridades, aptidoes):
    # Criar array de índices ordenados com base nas similaridades (ordem decrescente)
    indices_ordenados = np.argsort(aptidoes)[::-1]
    
    # Ordenar população usando os índices
    populacao_ordenada = populacao[indices_ordenados]
    aptidoes_ordenadas = np.array(aptidoes)[indices_ordenados]
    similaridades_ordenadas = np.array(similaridades)[indices_ordenados]
    
    return populacao_ordenada, similaridades_ordenadas, aptidoes_ordenadas

def selecao_torneio(populacao, aptidoes, tamanho_torneio=3):
    indices_selecionados = []
    indices_disponiveis = list(range(len(populacao)))  # Inicialmente, todos os cromossomos estão disponíveis

    # Realizar torneios para selecionar os indivíduos
    while len(indices_selecionados) < len(populacao) // 2:  # Selecionar metade da população para cruzamento
        # Selecionar participantes do torneio a partir dos índices disponíveis
        torneio_indices = np.random.choice(indices_disponiveis, tamanho_torneio, replace=False)
        
        # Mostrar as aptidões dos cromossomos no torneio
        # imp.rodada_torneio(torneio_indices, aptidoes)
        
        # Encontrar o índice do melhor cromossomo no torneio
        melhor_idx = torneio_indices[np.argmax([aptidoes[i] for i in torneio_indices])]
        # Adicionar o vencedor aos selecionados e remover dos disponíveis
        indices_selecionados.append(melhor_idx)
        indices_disponiveis.remove(melhor_idx)
        
        # Mostrar o cromossomo vencedor do torneio
        # print(f"Selecionado para cruzamento: Cromossomo {melhor_idx+1} com Aptidão = {aptidoes[melhor_idx]*100:.2f}%")
    
    # Retorna os cromossomos dos indivíduos selecionados
    return [populacao[idx] for idx in indices_selecionados]

def cruzamento(pop_cross):
    np.random.shuffle(pop_cross)
    populacao_filha = []
    
    # Garantir que o número de filhos seja o mesmo que o número de indivíduos
    for i in range(0, len(pop_cross), 2):
        cromossomo1 = pop_cross[i]
        cromossomo2 = pop_cross[i+1] if i + 1 < len(pop_cross) else pop_cross[0]  # Caso ímpar, cruzar com o primeiro
        
        ponto_corte = np.random.randint(1, len(cromossomo1))
        # print("PONTO DE CORTE:", ponto_corte, "\n")

        # print("Cromossomo 1:", cromossomo1, "\nCromossomo2:", cromossomo2)
        
        filho = np.concatenate((cromossomo1[:ponto_corte], cromossomo2[ponto_corte:]))
        filha = np.concatenate((cromossomo2[:ponto_corte], cromossomo1[ponto_corte:]))

        # print("Filho:", filho, "Filha:", filha)
        
        populacao_filha.append(filho)
        populacao_filha.append(filha)
    
    return np.array(populacao_filha)

def mutacao(pop_mutavel):
    mutantes = []
    for individuo in pop_mutavel:
        # Cria uma cópia do cromossomo para garantir que o original não seja alterado
        individuo_mutado = individuo.copy()
        
        # Seleção aleatória de dois índices para troca
        idx1, idx2 = np.random.choice(len(individuo_mutado), 2, replace=False)
        
        # Troca de posição dos genes
        individuo_mutado[idx1], individuo_mutado[idx2] = individuo_mutado[idx2], individuo_mutado[idx1]

        # Adiciona o cromossomo mutado à população de mutantes
        mutantes.append(individuo_mutado)
    
    return np.array(mutantes)


def evoluir_populacao(pop, vetores1, vetores2, max_geracoes, vocabulario):
    geracao_atual = 0
    aptidao_max = 0  # Inicializando a aptidão máxima como 0

    similaridade_maxima = 1.0  # 100% de similaridade
    similaridade_minima = 0.0  # 0% de similaridade
    similaridade_global = 0;

    while geracao_atual < max_geracoes and aptidao_max < 80:

        print("Geração atual:", geracao_atual, "Aptidão atual:", aptidao_max)

        similaridades, aptidoes = avaliar_populacao(pop, vetores1, vetores2)

        pop, similaridades, aptidoes = ordenar_populacao(pop, similaridades, aptidoes)

        if similaridades[0] == similaridade_maxima:
            print(f"Geração {geracao_atual}: Similaridade 100% alcançada!")
            break
        elif similaridades[0] == similaridade_minima:
            print(f"Geração {geracao_atual}: Similaridade 0% alcançada!")
            break

        # Seleção dos indivíduos para cruzamento e mutação
        individuos_selecionados = selecao_torneio(pop, aptidoes)

        # Cruzamento (geração de filhos) e mutação
        filhos = cruzamento(individuos_selecionados)
        mutantes = mutacao(individuos_selecionados)

        # Adicionar filhos e mutantes à população
        pop_extendida = np.concatenate([pop, filhos, mutantes])
        # Recalcular similaridades e aptidões para a nova população estendida
        similaridades, aptidoes = avaliar_populacao(pop_extendida, vetores1, vetores2)

        # Ordenar a população estendida pela aptidão
        pop, similaridades, aptidoes = ordenar_populacao(pop_extendida, similaridades, aptidoes)

        # Atualizar aptidão máxima
        aptidao_max = aptidoes[0] if aptidao_max < aptidoes[0] else aptidao_max  # Atualiza a aptidão máxima da população

        # Remover os indivíduos menos aptos para manter o tamanho da população
        num_individuos_remover = len(filhos) + len(mutantes)  # Remover a quantidade igual à de indivíduos selecionados
        pop = pop[:-num_individuos_remover]
        similaridades = similaridades[:-num_individuos_remover]
        aptidoes = aptidoes[:-num_individuos_remover]

        geracao_atual += 1
        similaridade_media = np.mean(similaridades)
        similaridade_global = similaridade_media if similaridade_global < similaridade_media else similaridade_global

    if geracao_atual == max_geracoes:
        print(f"Limite de gerações atingido.\nSimilaridade atingida: {similaridade_global}")
    return aptidao_max, similaridade_global, pop[0]


