import ler_textos as lt
import similaridade as simil
import numpy as np
import imprimir as imp

caminho_arquivo = 'textos.txt'
textos = lt.carregar_textos(caminho_arquivo)
max_gens = 100

# print(textos)

vetores, vocabulario = simil.vetorizar_textos(textos)

# imp.vocabulário(vetores, vocabulario)

populacao_inicial = simil.gerar_populacao_inicial(vetores[0], vetores[1], vocabulario)

# Ver população inicial
# imp.populacao(populacao_inicial, vocabulario)

# similaridades, aptidoes = simil.avaliar_populacao(populacao_inicial, vetores[0], vetores[1])
# print("APTIDÕES: ", aptidoes, "\n")

#Ver similaridades iniciais
# imp.similaridades(similaridades)
# imp.grafico_aptidao(similaridades, aptidoes)

# populacao_ord, similaridades_ord, aptidoes_ord = simil.ordenar_populacao(populacao_inicial, similaridades, aptidoes)

#Ver população ordenada pela similaridade
# imp.pop_simil_apt(populacao_ord, similaridades_ord, aptidoes_ord)

# similaridade_media_total = np.mean(similaridades_ord)
# print(f"\nSimilaridade Média Total: {similaridade_media_total*100:.2f}%")

# individuos_selecionados = simil.selecao_torneio(populacao_ord, aptidoes_ord)
# filhos = simil.cruzamento(individuos_selecionados)
# mutantes = simil.mutacao(individuos_selecionados)

# imp.compare_pops(individuos_selecionados, filhos, vocabulario)
# imp.compare_pops(individuos_selecionados, mutantes, vocabulario)

aptidao_max, similaridade_max, melhor_individuo = simil.evoluir_populacao(populacao_inicial, vetores[0], vetores[1], max_gens, vocabulario)

print("Melhor Indivíduo:", simil.cromossomo_para_palavras(melhor_individuo, vocabulario))
print("Similaridade:", similaridade_max)
print("Aptidão:", aptidao_max)