from sentence_transformers import SentenceTransformer, util
import random

import ler_textos as lt
caminho_arquivo = 'textos.txt'
textos = lt.carregar_textos(caminho_arquivo)

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

import spacy

# Carregar o modelo em português do spaCy
nlp = spacy.load("pt_core_news_md")

# Função para extrair palavras e suas classes gramaticais
def extrair_classes(texto, texto_nome):
    doc = nlp(texto)  # Processar o texto com o spaCy
    palavras_extraidas = []
    classes_permitidas = ["VERB", "AUX", "NOUN", "ADJ", "ADV", "PRON"]
    
    # Iterar sobre as palavras do texto e pegar suas classes
    for token in doc:
        # Filtrar apenas palavras (ignorar pontuação, por exemplo)
        if not token.is_punct and token.pos_ in classes_permitidas:
            palavras_extraidas.append({
                'texto': texto_nome.lower(),  # Nome do texto em minúsculas
                'palavra': token.text,  # A palavra extraída
                'classe': token.pos_   # A classe gramatical da palavra (verbo, substantivo, etc.)
            })
    
    return palavras_extraidas

def extrair_texto(texto_label):
    texto = ''
    for item in texto_label:
        texto += item['palavra'] + ' '
    return texto.strip()

# Exemplos de textos
texto1 = textos[0]
texto2 = textos[1]

# Extrair palavras dos textos
texto_labels1 = extrair_classes(texto1, 'Texto 1')
texto_labels2 = extrair_classes(texto2, 'Texto 2')

texto1 = extrair_texto(texto_labels1)
texto2 = extrair_texto(texto_labels2)

embedding1 = model.encode(texto1, convert_to_tensor=True)
embedding2 = model.encode(texto2, convert_to_tensor=True)

# Calcule a similaridade usando a métrica de cosseno
similarity = util.pytorch_cos_sim(embedding1, embedding2)

print(f"Similaridade entre os textos: {similarity.item()}")

# Combinar os resultados
resultados = texto_labels1 + texto_labels2

# # Exibir o resultado
# for item in resultados:
#     print(f"Texto: {item['texto']} | Palavra: {item['palavra']} | Classe: {item['classe']}")

def gerar_populacao_inicial(texto_labels1, texto_labels2, tamanho_populacao=10):
    # Calcula o tamanho do cromossomo (metade da soma total de palavras)
    tamanho_cromossomo = (len(texto_labels1) + len(texto_labels2)) // 2
    
    populacao = []
    
    # Combina as palavras dos dois textos
    todas_palavras = texto_labels1 + texto_labels2
    
    for _ in range(tamanho_populacao):
        # Cria um novo cromossomo
        palavras_cromossomo = []
        
        # Seleciona palavras aleatórias
        palavras_disponiveis = todas_palavras.copy()
        
        for _ in range(tamanho_cromossomo):
            if palavras_disponiveis:
                # Escolhe uma palavra aleatória
                palavra = random.choice(palavras_disponiveis)
                palavras_cromossomo.append(palavra['palavra'])
                
                # Remove a palavra escolhida para evitar repetição
                palavras_disponiveis = [p for p in palavras_disponiveis 
                                      if p['palavra'] != palavra['palavra']]
        
        # Junta as palavras em uma única string
        cromossomo = ' '.join(palavras_cromossomo)
        populacao.append(cromossomo)
    
    return populacao

# Exemplo de uso:
populacao = gerar_populacao_inicial(texto_labels1, texto_labels2)

def calcular_similaridade_populacao(populacao, texto1, texto2, model):
    resultados = []
    
    for cromossomo in populacao:
        # Calcula embeddings
        emb_cromossomo = model.encode(cromossomo, convert_to_tensor=True)
        emb_texto1 = model.encode(texto1, convert_to_tensor=True)
        emb_texto2 = model.encode(texto2, convert_to_tensor=True)
        
        # Calcula similaridades
        sim1 = util.pytorch_cos_sim(emb_cromossomo, emb_texto1).item()
        sim2 = util.pytorch_cos_sim(emb_cromossomo, emb_texto2).item()
        
        # Calcula média das similaridades
        media_sim = (sim1 + sim2) / 2
        
        resultados.append({
            'cromossomo': cromossomo,
            'similaridade_texto1': sim1,
            'similaridade_texto2': sim2,
            'media_similaridade': media_sim
        })
    
    # Ordena por média de similaridade (maior para menor)
    resultados_ordenados = sorted(resultados, 
                                key=lambda x: x['media_similaridade'], 
                                reverse=True)
    
    return resultados_ordenados

# Calcula similaridades e ordena
resultados = calcular_similaridade_populacao(populacao, texto1, texto2, model)

# Exibe os resultados
print("\nCromossomos ordenados por similaridade média:")
for i, res in enumerate(resultados):
    print(f"\nCromossomo {i+1}:")
    print(f"Texto: {res['cromossomo']}")
    print(f"Similaridade texto1: {res['similaridade_texto1']:.4f}")
    print(f"Similaridade texto2: {res['similaridade_texto2']:.4f}")
    print(f"Média similaridade: {res['media_similaridade']:.4f}")

