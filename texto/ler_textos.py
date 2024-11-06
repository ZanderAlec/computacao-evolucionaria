def carregar_textos(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        conteudo = arquivo.read().strip()
    # Divide os textos com base em duas quebras de linha consecutivas
    textos = conteudo.split("\n\n")
    return textos
