from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

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
    
    return similaridades

def ordenar_populacao(populacao, similaridades):
    # Criar array de índices ordenados com base nas similaridades (ordem decrescente)
    indices_ordenados = np.argsort(similaridades)[::-1]
    
    # Ordenar população usando os índices
    populacao_ordenada = populacao[indices_ordenados]
    similaridades_ordenadas = np.array(similaridades)[indices_ordenados]
    
    return populacao_ordenada, similaridades_ordenadas
