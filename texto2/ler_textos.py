def carregar_arquivos(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        conteudo = arquivo.read()
        textos = [texto.strip() for texto in conteudo.split("\n\n") if texto.strip()]
    return textos
