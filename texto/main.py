import ler_textos as lt
import similaridade as simil
import numpy as np

caminho_arquivo = 'textos.txt'
textos = lt.carregar_textos(caminho_arquivo)

# print(textos)

vetores, vocabulario = simil.vetorizar_textos(textos)

# print("\nVocabulário:", vocabulario)
# print("\nVetores TF-IDF:", vetores)

populacao_inicial = simil.gerar_populacao_inicial(vetores[0], vetores[1], vocabulario)

# print("População Inicial:")
# print(populacao_inicial, "\n")

# Ver população inicial
for i, cromossomo in enumerate(populacao_inicial):
    palavras = simil.cromossomo_para_palavras(cromossomo, vocabulario)
    print(f"Cromossomo {i+1}: {palavras}")

similaridades = simil.avaliar_populacao(populacao_inicial, vetores[0], vetores[1])


# for i, sim in enumerate(similaridades):
#     print(f"Similaridade do Cromossomo {i+1}: {sim*100:.2f}%")


populacao_ord, similaridades_ord = simil.ordenar_populacao(populacao_inicial, similaridades)

for i, (cromossomo, sim) in enumerate(zip(populacao_ord, similaridades_ord)):
    print(f"Cromossomo {i+1}: Similaridade = {sim*100:.2f}%")

similaridade_media_total = np.mean(similaridades_ord)
print(f"\nSimilaridade Média Total: {similaridade_media_total*100:.2f}%")