import matplotlib.pyplot as plt
import similaridade as simil

def vocabulario(vetores, vocabulario):
    print("\nVocabulário:", vocabulario)
    # print("\nVetores TF-IDF:", vetores)

def populacao(pop, vocabulario):
    print("População:")

    #vetores
    # print(pop, "\n")

    for i, cromossomo in enumerate(pop):
        palavras = simil.cromossomo_para_palavras(cromossomo, vocabulario)
        print(f"Cromossomo {i+1}: {palavras}")

def compare_pops(pop1, pop2, vocabulario):
    populacao(pop1, vocabulario)
    print()
    populacao(pop2, vocabulario)

def similaridades(similaridades):
    for i, sim in enumerate(similaridades):
        print(f"Similaridade do Cromossomo {i+1}: {sim*100:.2f}%")

def pop_simil_apt(pop, similaridades, apts):
    for i, (cromossomo, sim, apt) in enumerate(zip(pop, similaridades, apts)):
        print(f"Cromossomo {i+1}: Similaridade = {sim*100:.2f}%, Aptidão = {apt*100:.2f}%")

def rodada_torneio(torneio_indices, aptidoes):
    print(f"\nRodada de Torneio:")
    for idx in torneio_indices:
        print(f"Cromossomo {idx+1}: Aptidão = {aptidoes[idx]*100:.2f}%")

def grafico_aptidao(similaridades, aptidoes):

    # print(simil, aptidoes)

    # Plotar a função de aptidão (LINHA)
    # plt.plot(similaridades, aptidoes, label="Função de Aptidão Suavizada")

    # plt.axvline(0.45, color='r', linestyle='--', label="Limite Inferior (45%)")
    # plt.axvline(0.55, color='r', linestyle='--', label="Limite Superior (55%)")

    # plt.title("Função de Aptidão Suavizada com Faixa de Tolerância")
    # plt.xlabel("Similaridade")
    # plt.ylabel("Aptidão")
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    # Plotar a função de aptidão (PONTOS)
    plt.scatter(similaridades, aptidoes, color="blue", label="Função de Aptidão Suavizada", alpha=0.5, s=10)
    
    plt.axvline(0.45, color='red', linestyle='--', label="Limite Inferior (45%)")
    plt.axvline(0.55, color='red', linestyle='--', label="Limite Superior (55%)")
    
    plt.title("Função de Aptidão Suavizada com Faixa de Tolerância")
    plt.xlabel("Similaridade")
    plt.ylabel("Aptidão")
    plt.legend()
    plt.grid(True)
    plt.show()