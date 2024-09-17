from random import shuffle, randint
from copy import deepcopy 


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
    salaDeJantar = ComodosInfo("SJ", 15, 20),
    areaServico = ComodosInfo('AS', 6, 10),
    closet = ComodosInfo('Cl', 3, 4),
    quarto = ComodosInfo('Q', 12, 30),
    ginastica = ComodosInfo('G', 20, 30)
)


class Casa:
    def __init__(self, width = 22, height = 5):
        #Armazena os andares
        self.andares = []
        self.width = width
        self.height = height
        self.fitness = 0

    def printFloors(self):
        for floor in self.andares:
            print(f"####### {floor.nome} #######")
            for room in floor.comodos:
                room.print()

    def calcFitness(self):
        fitness = 0
        spaceRemaining = 1
        for i in range(len(self.andares)):
            for comodo in self.andares[i].comodos:
                if i == 0: 
                    if comodo.tipo == 'areaServico' or comodo.tipo == 'banheiro':
                        fitness+= 10
                
                elif i == 1: 
                    if comodo.tipo == 'quarto' or comodo.tipo == 'closet':
                        fitness+= 10

                elif i == 2:
                    if comodo.tipo == 'areaServico':
                        fitness+= 10

            
        for i in range(0,2):
            spaceRemaining += calcRemaningSpace(self.andares[i], self.width, self.height)

        bonusSpaceUsed = 0 if spaceRemaining == 0 else 10 / spaceRemaining
        fitness += bonusSpaceUsed
        self.fitness = fitness

        

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

        
    def insertRoom(self, type, width, height):
        newRoom = Comodo(type, width, height)
        self.comodos.append(newRoom)

    def startMap(self, width, height):  
        # Inicializa a matriz mapa com espaços vazios  
        self.mapa = [['0' for _ in range(width)] for _ in range(height)]  
        self.printMap(height)
        
    def printMap(self, height):
        print('\n')
        for linha in self.mapa:  
            print(' '.join(linha))  

    # def insertRoom(self,room, width, heigth):
    #     largura = room.largura
    #     altura = room.altura

    #     larg = False
    #     #1 - altura
    #     #2 - largura
    #     for x in range(heigth):
    #         for y in range(width):
    #             if(self.mapa[x][y] != '0' and self.mapa[x][y + 1] == '0'):
    #                 if(largura - y != '0'):
    #                     break
    #             elif y == largura:
    #                 larg = True
    #             else  :
    #                 self.mapa[x][y] = 'c'

    #     self.printMap(heigth)



    def createMap(self, width, height):
        nextRoom  = 0

        self.startMap(width, height)

        doorP = width // 2

        self.mapa[0][doorP] = 'p'
        self.printMap(height)

        print('\n')

        self.insertRoom(self.comodos[0], width, height)

        
class Comodo:
    def __init__(self, tipo, largura, altura):
        self.tipo = tipo
        self.altura = altura
        self.largura = largura

    def print(self):
        print(f'{self.tipo}, {self.altura}, {self.largura}')



#Calcula quanto espaço da área total de uma andar foi ocupada por quartos
def calcRemaningSpace(andar, totalWidth, totalHeight):

    totalm2 = totalWidth * totalHeight
    for room in andar.comodos:
        roomm2 = room.altura * room.largura
        totalm2 -= roomm2

    return totalm2


#Preenche todos os andares da casa com comodos
def sorteiaComodos(casa):

    #Comodos obrigatórios do térreo
    RoomsT = ['sala', 'cozinha', 'escada', 'salaDeJantar']
    #Quartos que não foram adicionados no terreo
    remainingRooms = [x for x in list(simbols.keys()) if x not in RoomsT and x != 'corredor']
    remainingRooms.extend(['quarto'] * 2)

    shuffle(remainingRooms)

    #Sorteia os valores do térreo
    for roomName in RoomsT:
        width, height = drawRoomsSize(roomName) 
        casa.andares[0].insertRoom(roomName, width, height)

    remainingSpaceT = calcRemaningSpace(casa.andares[0], casa.width, casa.height)
    remainingSpace1 =  casa.width * casa.height



    #enquanto a lista não está vazia vai distribuindo os comodos pelos andares
    while(remainingRooms):

        roomWidth, roomHeight = drawRoomsSize(remainingRooms[0]) 
        roomSize = roomWidth * roomHeight
        floor = 0

        #se ambos os quartos tem espaço pra colocar, sorteia quem recebe o quarto
        if remainingSpaceT >= roomSize and remainingSpace1 >= roomSize :
            #chance da laje receber area de serviço
            if(remainingRooms[0] == 'areaServico'):
                floor = randint(0,2)
            else:
                floor = randint(0,1)

        elif remainingSpaceT >= roomSize and remainingSpace1 < roomSize:
            floor = 0
            
        elif remainingSpace1 >= roomSize and remainingSpaceT < roomSize:
            floor = 1
            

        if floor == 0:
            remainingSpaceT -= roomSize
        elif floor == 1:
            remainingSpace1 -= roomSize

        casa.andares[floor].insertRoom(remainingRooms[0], roomWidth, roomHeight)
        remainingRooms.pop(0) 

    casa.andares[1].insertRoom('escada', 2,2)
    casa.andares[2].insertRoom('escada', 2,2)
    
#retorno valores aletórias da largura e altura
def drawRoomsSize(comodo):

    minS = simbols[comodo].minSize
    maxS = simbols[comodo].maxSize
    
    if minS == maxS:
        return int(minS/2), int(maxS/2)
    
    while True:

        alturaSize = randint(1, 10)
        larguraSize = randint(1, 10)
        if alturaSize*larguraSize >= minS and alturaSize*larguraSize <= maxS:
            return alturaSize, larguraSize
   

# Função para desenhar a casa no terminal
def drawHouse(casa):
    # Obtém as dimensões da casa
    width = casa.width
    height = casa.height

    # Cria uma matriz para representar a planta da casa
    planta = [['*' for _ in range(width)] for _ in range(height)]

    # Preenche a matriz com os cômodos
    for andar in casa.andares:
        for comodo in andar.comodos:
            # Encontra uma posição livre para o cômodo
            comodo.print()
            for y in range(height - comodo.altura + 1):
                for x in range(width - comodo.largura + 1):
                    if all(planta[y+i][x+j] == '*' for i in range(comodo.altura) for j in range(comodo.largura)):
                        # Preenche o espaço do cômodo na matriz
                        for i in range(comodo.altura):
                            for j in range(comodo.largura):
                                planta[y+i][x+j] = simbols[comodo.tipo].simbol

                        # Sai dos loops após posicionar o cômodo
                        break
                else:
                    continue
                break

        # Imprime a planta da casa
        print("\nPlanta da Casa:")
        print("+" + "-" * (width ) + "+")
        for linha in planta:
            print("|" + "".join(linha) + "|")
        print("+" + "-" * (width) + "+")

        # Imprime a legenda
        print("\nLegenda:")
        for tipo, info in simbols.items():
            print(f"{info.simbol}: {tipo}")
        
        planta = [['*' for _ in range(width)] for _ in range(height)]




def geraPopInicial():

    for i in range(0, popSize):
        casa = Casa()

        #inicializa os andares
        casa.andares = [Andar('Térreo'), Andar('1 Andar'), Andar('Laje')]
    
        #preenche os andares da casa com comodos aleatórios
        sorteiaComodos(casa)
        casa.calcFitness()
        pop.append(casa)
    

def printPop(pop):
    for i in range(len(pop)):
        print('\n')
        pop[i].printFloors()
        print(f'\n{pop[i].fitness}')
        

def getFitness(casa):
    return casa.fitness

#Retorna uma sublista com cromossomos aleatórios e distintos
def drawSubPop(pop, size):
    subPop = []
    tempPop = deepcopy(pop)
    for i in range(size):
        r = randint(0, len(tempPop) - 1)
        subPop.append(tempPop[r])
        tempPop.pop(r)

    return subPop

#Substitui os piores cromossomos pelos novos
def insertIntoPop(pop, newCromossomes):
    sizePop = len(pop) - 1
    for i in range(len(newCromossomes)):
        pop[sizePop - i] = newCromossomes[i]

#Seleção por torneio.
#Insere 3 novos mutantes toda geração
def selectParentes():
    newMutants = []

    for i in range(3):
        r = randint(2, len(pop))
        subPop = drawSubPop(pop, r)
        subPop.sort(key = getFitness, reverse = True)
        mutant = mutate(subPop[0])
        newMutants.append(mutant)

    insertIntoPop(pop, newMutants)

def mutate(casa):
    
    #muta os andares---------------------------
    #Quartos que não podem ser mutados
    fixedT = ['sala', 'cozinha', 'escada', 'salaDeJantar']
    remaingT = [x for x in casa.andares[0].comodos if x.tipo not in fixedT]

    if len(remaingT) != 0:
        remaing1F = casa.andares[1].comodos

        rt = randint(0,  len(remaingT) - 1) if len(remaingT) > 1 else 0
        r1 = randint(0,  len(remaing1F) - 1)

        roomt = remaingT[rt]
        indexrt = casa.andares[0].comodos.index(roomt)
        room1 = casa.andares[1].comodos[r1]

        #Realizar a troca
        casa.andares[0].comodos.remove(roomt)
        casa.andares[1].comodos.pop(r1)

        casa.andares[0].comodos.insert(r1, room1)
        casa.andares[1].comodos.insert(indexrt, roomt)

    #muta o tamanho dos comodos ----
    for i in range(0,2):
        rand = randint(1, 100)
        if rand >= 50:
            rand = randint(0, len(casa.andares[i].comodos) - 1)
            #Só muda o valor do cômodo se ele couber  
            space = calcRemaningSpace(casa.andares[i], casa.width, casa.height)
            newW, newH =  drawRoomsSize(casa.andares[i].comodos[rand].tipo)
            if(space >= newW * newH):
                casa.andares[i].comodos[rand].altura, casa.andares[i].comodos[rand].altura = newW, newH

    casa.calcFitness()
    return casa



pop = []
popSize = 2
geracoes = 2

def main():
    geraPopInicial()
    printPop(pop)
    pop.sort(key = getFitness, reverse = True)

    # # TODO: desenhar as casas
    # for i in range(0, geracoes):
    #     print("-------------------------------")
    #     selectParentes()
    #     pop.sort(key = getFitness, reverse = True)
    #     printPop(pop)
    drawHouse(pop[0])



if __name__ == "__main__":
    main()

