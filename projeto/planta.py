from random import shuffle, randint

min = 68
scale = 0.5

#Armazena as informações padrões dos comodos
class ComodosInfo:
    def __init__(self, simbol, minSize, maxSize):
        self.simbol = simbol
        self.minSize = minSize 
        self.maxSize = maxSize 

simbols = dict(
    sala = ComodosInfo("S", 30, 40),
    cozinha = ComodosInfo("C", 10, 15),
    banheiro = ComodosInfo("B", 3, 8),
    corredor = ComodosInfo("*", 2,2),
    escada = ComodosInfo("e", 4, 4),
    salaDeJantar = ComodosInfo("SJ", 15, 20)
)




class Casa:
    def __init__(self, width = 8, height = 9):
        #Armazena os andares
        self.andares = []
        self.width = width
        self.height = height

    def cria_andar(self, nome, listaComodos):
        novoAndar = Andar(nome,listaComodos)
        self.andares.append(novoAndar)

    def generateHouse(self):
        for i in range(len(self.andares)):
            self.andares[i].createMap(self.width, self.height)
        

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

    def startMap(self, width, height):
         #inicia a matriz
        line = []
        for x in range(width):
            line.append(' ')

        for y in range(height):
            self.mapa.append(line)

        self.printMap(height)
        
       

    def printMap(self, height):
        print('\n')
        for x in range(height):
            print(self.mapa[x])

    def createMap(self, width, height):
        nextRoom  = 0

        self.startMap(width, height)

        doorP = width // 2

        self.mapa[0][doorP] = 'p'
        self.printMap(height)

        print('\n')

        





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

    if minS == maxS:
        return int(minS/2), int(maxS/2)
    
    while True:

        alturaSize = randint(1, 10)
        larguraSize = randint(1, 10)
        if alturaSize*larguraSize >= minS and alturaSize*larguraSize <= maxS:
            return alturaSize, larguraSize
   
  


def geraPopInicial():
    pop = []
    casa1 = Casa()
    #Guarda quanto de tamanho o andar ainda tem disponível
    tamRestante = casa1.width * casa1.height

    print(casa1.width, casa1.height)

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

    andar1.createMap(casa1.width, casa1.height)




geraPopInicial()

# def drawMap():
#     altura = 8
#     largura = 9
#     for i in range(0,largura):
#         print('# ', end='')
#         if i == largura - 1:
#             print()
#             #espaços com o tem que ser feito com um for
#             for j in range(1, altura -1):
#                 print('#                 #')
#             for i in range(0,largura):
#                 print('# ', end='')



# drawMap()

class Mapa:  
    def __init__(self):  
        self.mapa = []  

    def startMap(self, width, height):  
        # Inicializa a matriz mapa com espaços vazios  
        self.mapa = [[' ' for _ in range(width)] for _ in range(height)]  

    def printMap(self, height):  
        for linha in self.mapa:  
            print(' '.join(linha))  

    def createMap(self, width, height):  
        nextRoom = 0  

        self.startMap(width, height)  

        doorP = width // 2  

        # Coloca 'p' na posição específica  
        self.mapa[0][doorP] = 'p'  
        self.printMap(height)  

        print('\n')  

# Exemplo de uso  
mapa = Mapa()  
mapa.createMap(5, 3)  