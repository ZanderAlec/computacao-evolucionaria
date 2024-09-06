from random import shuffle, randint

min = 68
scale = 0.5

#Armazena as informações padrões dos comodos
class ComodosInfo:
    def __init__(self, simbol, minSize, maxSize):
        self.simbol = simbol
        self.minSize = minSize * scale
        self.maxSize = maxSize * scale

simbols = dict(
    sala = ComodosInfo("S", 30, 40),
    cozinha = ComodosInfo("C", 10, 15),
    banheiro = ComodosInfo("B", 3, 8),
    corredor = ComodosInfo("*", 2,2),
    escada = ComodosInfo("e", 2, 2),
    salaDeJantar = ComodosInfo("SJ", 15, 20)
)




class Casa:
    def __init__(self, tamanho = 68):
        #Armazena os andares
        self.andares = []
        self.tamanho = tamanho

    def cria_andar(self, nome, listaComodos):
        novoAndar = Andar(nome,listaComodos)
        self.andares.append(novoAndar)
        

class Andar:
    def __init__(self, nome):
        #nome do andar 
        self.nome = nome
        #lista dos comodos presentes no andar
        self.comodos = []
        #Como os cômodos foram posicionados
        self.mapa= []

    def insereComodo(self, comodo):
        self.comodos.append(comodo)

class Comodo:
    def __init__(self, tipo, altura, largura):
        self.tipo = tipo
        self.altura = altura
        self.largura = largura


#Como só tem um andar, a função apenas embaralha
#No futuro ela deverá determinar quais comodos farão parte de qual andar
def sorteiaComodos():
    #A idéia é que todos os andares possíveis estejam aqui
    #Assim, poderemos sortear qual cômodo vai em cada andar
    comodos = list(simbols.keys())
    comodos.remove('corredor')

    #embaralha os comodos
    shuffle(comodos)

    return comodos
    

#retorno valores aletórias da latura e largura
#Acredito que o programa ja calculou 68 como minimo pro max de tudo
def sorteiaTamanhoComodo(comodo):

    minS = simbols[comodo].minSize
    maxS = simbols[comodo].maxSize

    alturaSize = randint(minS, maxS)
    larguraSize = randint(minS, maxS)

    return alturaSize, larguraSize



def geraPopInicial():
    pop = []
    casa1 = Casa()
    #Guarda quanto de tamanho o andar ainda tem disponível
    tamRestante = casa1.tamanho

    #randomiza a ordem de inserir os comodos
    print(f'tamRestante {tamRestante}')
    comodosAdd = sorteiaComodos()
    print(comodosAdd)

    andar1 = Andar('Térreo')

    #randomizar o tamanho dos comodos
    for i in range(len(comodosAdd)):
        a, h = sorteiaTamanhoComodo(comodosAdd[i])
        novoComodo = Comodo(comodosAdd[i], a, h)
        andar1.insereComodo(novoComodo)


    
    #print comodos
    print(f"####### {andar1.nome} #######")
    for i in range(len(andar1.comodos)):
        print(andar1.comodos[i].tipo, andar1.comodos[i].altura, andar1.comodos[i].largura)






geraPopInicial()