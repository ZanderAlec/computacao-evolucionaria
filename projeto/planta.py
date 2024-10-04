from random import shuffle, randint, choice
from copy import deepcopy 
import math




#Armazena as informações padrões dos comodos
class ComodosInfo:
    def __init__(self, simbol, minSize, maxSize):
        self.simbol = simbol
        self.minSize = minSize 
        self.maxSize = maxSize 

simbols = dict(
    sala = ComodosInfo("1", 30, 40),
    cozinha = ComodosInfo("2", 10, 15),
    banheiro = ComodosInfo("3", 3, 8),
    corredor = ComodosInfo("*", 2,2),
    escada = ComodosInfo("4", 4, 4),
    salaDeJantar = ComodosInfo("5", 15, 20),
    areaServico = ComodosInfo('6', 6, 10),
    closet = ComodosInfo('7', 3, 4),
    quarto = ComodosInfo('8', 12, 30),
    ginastica = ComodosInfo('9', 20, 30)
)



class Casa:
    def __init__(self, width , height):
        #Armazena os andares
        self.andares = []
        self.width = width
        self.height = height
        self.fitness = 0
        self.portax = ''
        self.portay = ''
        self.usedSpace = 0
        self.totalSpace = 0

    def printHouse(self):
        print(f"fitness: {self.fitness}")
        # print(f"porta de entrada: \n x: {self.portax}, y: {self.portay}")
       
        self.printFloors()

    def printFloors(self):
        for andar in self.andares:
            andar.print()

    def calcFitness(self):
        fitness = 0
        
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

        #Dá um bonus por uso de espaço
        totalspace = self.width * self.height
        usedSpace = 0
        for i in range(0,2):
            usedSpace += totalspace - calcRemaningSpace(self.andares[i], self.width, self.height)

       
        bonusSpaceUsed =  0.2 * usedSpace
        fitness += bonusSpaceUsed
        self.fitness = fitness
        self.usedSpace = usedSpace
        self.totalSpace = totalspace

        

    
class Andar:
    def __init__(self, nome):
        #nome do andar 
        self.nome = nome
        #lista dos comodos presentes no andar
        self.comodos = []
        self.inseridos = []
        self.corridors = []
        #Como os cômodos foram posicionados
        self.planta = []

    def print(self):
        print(f"####### {self.nome} #######")
        for comodo in self.comodos:
            comodo.print()
        
    def insertRoom(self, type, width, height, iniciox=None, inicioy=None):
        newRoom = Comodo(type, width, height)
        newRoom.iniciox = iniciox
        newRoom.inicioy = inicioy
        self.comodos.append(newRoom)

    # Cria uma matriz para representar a planta da casa
    def iniciaPlanta(self, width, height):
        self.planta = [[' ' for _ in range(width)] for _ in range(height)]

    
class Comodo:
    def __init__(self, tipo, largura, altura):
        self.tipo = tipo
        self.largura = largura
        self.altura = altura
        self.iniciox, self.inicioy = None, None
        self.portax, self.portay = None, None
        self.janelax, self.janelay = None, None


    def __eq__(self, outroComodo):
        if isinstance(outroComodo, Comodo):
            return self.tipo == outroComodo.tipo \
                    and self.altura == outroComodo.altura \
                    and self.largura == outroComodo.largura

    def print(self):
        print(f'------{self.tipo}')
        print(f'altura: {self.altura}, largura: {self.largura}')
        print(f'iniciox: {self.iniciox}, inicioY: {self.inicioy} ')
        # print(f'portax: {self.portax}, portay: {self.portay}')
        # print(f'janelax: {self.janelax}, janelay: {self.janelay}')

    #coordenadas de inicio/fim do comodo
    def getCoordinates(self):
        fx = self.largura + self.iniciox - 1
        fy = self.altura + self.inicioy - 1

        return self.iniciox, self.inicioy, fx, fy


#Calcula quanto espaço da área total de uma andar foi ocupada por quartos
def calcRemaningSpace(andar, totalWidth, totalHeight):

    areaTotal = totalWidth * totalHeight
    for room in andar.comodos:
        roomm2 = room.altura * room.largura
        areaTotal -= roomm2

    return areaTotal




#retorno valores aletórias da largura e altura
def drawRoomsSize(nomeComodo,casa):

    minS = simbols[nomeComodo].minSize
    maxS = simbols[nomeComodo].maxSize
    
    if minS == maxS:
        return int(minS/2), int(maxS/2)
    
    while True:

        alturaSize = randint(1, 10)
        larguraSize = randint(1, 10)

        if nomeComodo != 'sala' and alturaSize == casa.height - 2 or larguraSize == casa.width - 2:
            continue

        if alturaSize*larguraSize >= minS and alturaSize*larguraSize <= maxS and alturaSize <= casa.height - 2 and larguraSize <= casa.width - 2:
            if alturaSize > casa.height - 2:
                return alturaSize, larguraSize
    
            return larguraSize, alturaSize
        

def setRoomMinSize(nomeComodo, casa):
    minS = simbols[nomeComodo].minSize

    if minS % 2 == 0:
        metade = int(minS / 2)
        v1 = metade
        v2 = 2
    else:
        v1 = minS
        v2 =  1

    rand = randint(0, 1)
    if rand == 0:
        alturaSize = v1
        larguraSize = v2
    else:
        alturaSize = v2
        larguraSize = v1

    if alturaSize > casa.height - 2:
        return alturaSize, larguraSize
    
    return larguraSize, alturaSize
        

#Preenche todos os andares da casa com comodos
def sorteiaComodos(casa, direcao):

    #Comodos obrigatórios do térreo
    RoomsT = ['sala', 'cozinha', 'escada', 'salaDeJantar']
    #Quartos que não foram adicionados no terreo
    remainingRooms = [x for x in list(simbols.keys()) if x not in RoomsT and x != 'corredor']
    remainingRooms.extend(['quarto'] * 2)

    shuffle(remainingRooms)
    
    #Sorteia os valores do térreo---------------------------------
    for i in range(0,len(RoomsT)):
        casa.andares[0].inseridos.append(i)
        width, height = drawRoomsSize(RoomsT[i], casa) 
        casa.andares[0].insertRoom(RoomsT[i], width, height, iniciox=0, inicioy=0)  # Defina valores iniciais apropriados

    #Tenta inserir os obrigatórios no terreo:
    couberam = drawAndar(casa, casa.andares[0], direcao)

    if not couberam:
        for i in range(len(RoomsT)):
            width, height = setRoomMinSize(casa.andares[0].comodos[i].tipo, casa)
            casa.andares[0].comodos[i].largura = width
            casa.andares[0].comodos[i].altura = height
        
        couberam = drawAndar(casa, casa.andares[0], direcao)

        if not couberam:
            return False
   

    #----------------------------------------------------------------------------

    casa.andares[1].insertRoom('escada', 2,2, iniciox=0, inicioy=0)  # Defina valores iniciais apropriados
    casa.andares[2].insertRoom('escada', 2,2, iniciox=0, inicioy=0)  # Defina valores iniciais apropriados

    drawAndar(casa, casa.andares[1], direcao)
    drawAndar(casa,  casa.andares[2], direcao)

    casa.andares[1].inseridos.append(0)
    casa.andares[2].inseridos.append(0)

    #enquanto a lista não está vazia vai distribuindo os comodos pelos andares
    while(remainingRooms):

        roomWidth, roomHeight = drawRoomsSize(remainingRooms[0], casa) 
        tryMin = False

        if remainingRooms[0] == 'areaServico':
                        #'terreo', '1andar', 'laje
            andares = [casa.andares[0], casa.andares[1], casa.andares[2]]
        else:           
                         #'terreo', '1andar',
             andares = [casa.andares[0], casa.andares[1]]

        escolha = choice(andares)
        

        casaInvalida = False
        #Tenta inserir em todos os comodos
        while True:
            #Reduz o comodo ao tamanho mínimo pra tentar caber
            if tryMin:
                roomWidth, roomHeight = setRoomMinSize(remainingRooms[0], casa)
            else:
                escolha.insertRoom(remainingRooms[0], roomWidth, roomHeight, iniciox=0, inicioy=0)

            coube =  drawAndar(casa, escolha, direcao, False, escolha.inseridos)

            #Tenta outro andar
            if tryMin and not coube:
                andares.remove(escolha)

                if andares:
                    tryMin = False
                    escolha = choice(andares)
                    continue
                else:
                    casaInvalida = True
                    break

            if coube:
                escolha.inseridos.append(len(escolha.comodos) - 1)
                remainingRooms.pop(0)
                break
            else:
                tryMin = True

        if casaInvalida: return False
        
    return True
            

   


#retorna o a,b e c da equação
def calcEquacaoGeralReta(xi, xf, yi, yf):
    a = yi - yf
    b = xf - xi
    c = (xi*yf) - (yi*xf)

    return (a,b,c)
        
#encontrar o corredor mais próximo da parede
def calcDistPontoReta(corredor, reta):   
    xc, yc = corredor
    a,b,c = reta
    sEquacao = abs((a*xc) + (b*yc) + c)

    A = a**2
    B = b**2
    pitagoras = float(math.sqrt(A + B))
    if pitagoras == 0: pitagoras = 1.0
    return float(sEquacao / pitagoras)

#anda o array o de corredores e retorna o indice do mais proximo da reta
def getCloserCorridorReta(corridors, reta): 

    # print("GET CLOSER CORRIDOR")
    menorDist = 10000.0
    indexMenorDist = 0.0

    for i in (0, len(corridors) - 1):
        d = calcDistPontoReta(corridors[i], reta)
        if (d < menorDist):
            menorDist = d
            indexMenorDist = i

    return indexMenorDist, menorDist

#Anda o array de corredores e retonra o indice mais proximo de um ponto
def getCloserCorridorPoint(corridors, point):
    menorDist = 10000.0
    indexMenorDist = 0.0

    for i in (0, len(corridors) - 1):
        d = CalcDistPontos(corridors[i], point)
        if(d < menorDist):
            menorDist = d
            indexMenorDist = i

    return indexMenorDist, menorDist

def CalcDistPontos(corredor, ponto):
    xc, yc = corredor
    xp, yp = ponto

    A =  abs(xc - xp) ** 2
    B = abs(yc - yp) ** 2

    return math.sqrt(A + B)

#retorna a posição da parede mais próxima do corredor
def getCloserWall(comodo, side, corridor, planta):
    ix, iy, fx, fy = comodo.getCoordinates()

    currD = 1000.0
    parede = ()
    match side:

        case 'C':
            if ix == fx:
                parede = (ix, iy)
            else: 
                for x in range(ix, fx):
                    P = (x,iy)

                    #Evita invadir comodos
                    if planta[iy - 1][x] != ' ' and planta[iy - 1][x] != '*' and planta[iy][x].isdigit():
                        continue

                    d = CalcDistPontos(corridor, (x,iy))
                    #Não sobrepõe comodo
                    if(currD > d):
                        currD = d
                        parede = P

        case 'B':
            if ix == fx:
                parede = (ix, fy)
            else: 
                for x in range(ix, fx):
                    P = (x,fy)

                    #Evita invadir comodos
                    if planta[fy + 1][x] != ' ' and planta[fy + 1][x] != '*' and planta[fy][x].isdigit():
                        continue

                    d = CalcDistPontos(corridor, (x,fy))
                    #Não sobrepõe comodo
                    if(currD > d):
                        currD = d
                        parede = P

        case 'E':
            if iy == fy:
                parede = (ix, iy)
            else: 
                for y in range(iy, fy):
                    P = (ix,y)
                    
                    #Evita invadir comodos
                    if planta[y][ix - 1] != ' ' and planta[y][ix - 1] != '*' and planta[y][ix].isdigit():
                        continue

                    d = CalcDistPontos(corridor, P)
                    #Não sobrepõe comodo
                    if(currD > d ):
                        currD = d
                        parede = P

        case 'D':
            if iy == fy:
                parede = (fx, fy)
            else: 
                for y in range(iy, fy):
                    P = (fx,y)

                    #Evita invadir comodos
                    if planta[y][fx + 1] != ' ' and planta[y][fx + 1] != '*' and planta[y][fx].isdigit():
                        continue

                    d = CalcDistPontos(corridor, P)
                    if(currD > d ):
                        currD = d
                        parede = P

    return parede

def addDoor(planta, comodo, x, y):
    planta[y][x] = 'p'
    comodo.portax = x
    comodo.portay = y

def addCorridor(planta, corridors, x,y):
    
    newcorr = (x,y)
    if newcorr in corridors:
        return

    planta[y][x] = '*'
    corridors.append(newcorr)

#Adiciona a porta em uma posição específica
def addDoorCorridor(comodo, corridors, planta, dir, x, y):
    
    match dir:
        case 'C':
            addDoor(planta, comodo, x, y)
            addCorridor(planta, corridors, x, y - 1)

        case 'B':
            addDoor(planta, comodo, x, y)
            addCorridor(planta, corridors, x, y + 1)

        case 'E':
            addDoor(planta, comodo, x, y)
            addCorridor(planta, corridors, x - 1, y)
        
        case 'D':
            addDoor(planta, comodo, x, y)
            addCorridor(planta, corridors, x + 1, y)


#Adiciona a porta em uma posição aleatória da parede
def addDoorCorridorRandom(comodo, corridors, planta, dir):
    ix, iy, fx, fy = comodo.getCoordinates()

    match dir:
        case 'C':
            for x in range(ix, fx):
                if  planta[iy - 1][x] == ' ' and planta[iy][x].isdigit():
                    r = randint(x, fx)
                    addDoor(planta, comodo, r, iy)
                    addCorridor(planta, corridors, r, iy - 1)
                    return

        case 'B':
            for x in range(ix, fx):
                if planta[fy + 1][x] == ' ' and planta[fy][x].isdigit():
                    r = randint(x, fx)
                    addDoor(planta, comodo, r, fy)
                    addCorridor(planta, corridors, r, fy + 1)
                    return

        case 'E':
            for y in range(iy, fy):
                if planta[y][ix - 1] == ' ' and planta[y][ix].isdigit():
                    r = randint(y, fy)
                    addDoor(planta, comodo, ix, r)
                    addCorridor(planta, corridors, ix - 1, r)
                    return
        
        case 'D':
            for y in range(iy, fy):
                if planta[y][fx + 1] == ' ' and planta[y][fx].isdigit():
                    r = randint(y, fy)
                    addDoor(planta, comodo, fx, r)
                    addCorridor(planta, corridors, fx + 1, r)
                    return




def addInternalDoors(comodo, corridors, planta, width, height):


    #TODO: colocar corredores na escada
    if comodo.tipo == 'escada':
        return

    ix, iy, fx, fy = comodo.getCoordinates()
    sides = checkInternalWalls(comodo, width, height)

    #primeiro comodo:
    if(len(corridors) == 0):
        r = 0
        if(len(sides) > 1):
            r = randint(0, len(sides) - 1)

        addDoorCorridorRandom(comodo, corridors, planta, sides[r])
        return
        
    #TODO: Não funciona???
    #verifica se há corredores colados a parede
    for side in sides:
        match side:
            case 'C':
                #Caso só tenha 1m de lado
                if ix == fx and  planta[iy - 1][ix] == '*' and planta[iy][ix].isdigit():
                    addDoor(planta, comodo, ix , iy)
                    addCorridor(planta, corridors, ix, iy - 1)

                else: 
                    for x in range(ix, fx):
                        if planta[iy - 1][x] == '*'  and planta[iy][ix].isdigit():
                            addDoor(planta, comodo, x , iy)
                            addCorridor(planta, corridors, x , iy - 1)
                            return

            case 'B':
                 #Caso só tenha 1m de lado
                if ix == fx and planta[fy + 1][ix] == '*' and planta[fy][ix].isdigit():
                    addDoor(planta, comodo, ix , fy)
                    addCorridor(planta, corridors, ix, fy + 1)

                else: 
                    for x in range(ix, fx):
                        if planta[fy + 1][x] == '*' and planta[fy][ix].isdigit():
                            addDoor(planta, comodo, x , fy)
                            addCorridor(planta, corridors, x , fy + 1)
                            return

            case 'E':
                 #Caso só tenha 1m de lado
                if iy == fy and  planta[iy][ix + 1] == '*' and planta[iy][ix].isdigit():
                    addDoor(planta, comodo, ix , fy)
                    addCorridor(planta, corridors, ix - 1 , fy)

                else: 
                    for y in range(iy, fy):
                        if planta[y][ix - 1] == '*' and planta[y][ix].isdigit():
                            addDoor(planta, comodo, ix , y)
                            addCorridor(planta, corridors, ix - 1, y)
                            return
            
            case 'D':
                 #Caso só tenha 1m de lado
                if iy == fy and  planta[iy][fx + 1] == '*' and planta[iy][fx].isdigit():
                    addDoor(planta, comodo, fx , iy)
                    addCorridor(planta, corridors, fx + 1 , iy)

                else: 
                    for y in range(iy, fy):
                        if planta[y][fx + 1] == '*' and planta[y][fx].isdigit():
                            addDoor(planta, comodo, fx , y)
                            addCorridor(planta, corridors, fx + 1 , y)
                            return


    #busca o corredor mais proximo pra inserir
    indexMenor = 0
    distMenor = 10000
    sideMenor = []
    for side in sides:

        sideMenor.append((side, distMenor))

        rx0, rxi, ry0, ryi = 0,0,0,0
        #Define as coordenadas da reta lado
        match(side):
            case 'C':
                rx0 = ix
                rxi = fx
                ry0 = iy - 1
                ryi = iy - 1 
            case 'B':
                rx0 = ix
                rxi = fx
                ry0 = fy + 1
                ryi = fy + 1
            case 'E':
                rx0 = ix - 1
                rxi = ix - 1
                ry0 = iy 
                ryi = fy
            case 'D':
                rx0 = fx + 1
                rxi = fx + 1
                ry0 = iy 
                ryi = fy 

        if ((side == 'C' or side == 'B') and rx0 == rxi) or ((side == 'D' or side == 'E') and ry0 == ryi):
            point = (rx0, ryi)
            i,d = getCloserCorridorPoint(corridors, point)
        else:
            reta = calcEquacaoGeralReta(rx0, rxi, ry0, ryi)
            i, d = getCloserCorridorReta(corridors, reta)

        if (distMenor > d):
            distMenor = d
            indexMenor = i
            
            for i, (s, _) in enumerate(sideMenor):
                if s == side:
                    itemp = i
                    break

            sideMenor[itemp] = (side, d)
           

    sideMenor.sort(key=lambda x: x[1])

    #tenta colocar na melhor parede, se não conseguir, tenta nas outras
    while(len(sideMenor) != 0):
        
        values = getCloserWall(comodo, sideMenor[0][0], corridors[indexMenor], planta)
        if(len(values) == 2):
            x , y = values
            addDoorCorridor(comodo,corridors, planta, sideMenor[0][0], x, y)
            return
        
        sideMenor.pop(0)
        

#Retonra uma lista de paredes do comodo que estão dentro da casa
def checkInternalWalls(comodo, width, height):
    sides = []

    ix, iy, fx, fy = comodo.getCoordinates()

    if (fx + 1) < width:
        sides.append('D')
    
    if (fy + 1) < height:
        sides.append('B')

    if (ix - 1) > 0:
        sides.append('E')

    if (iy - 1) > 0:
        sides.append('C') 
    
    return sides

#Retorna uma lista com todas as paredes viradas pra rua  do comodo
def checkExternalWalls(comodo, width, height, direcao):

    sides = []

    ix, iy, fx, fy = comodo.getCoordinates()

    #esquerda
    if ix-1 == 0:
        sides.append('E')
    #cima
    if iy - 1 == 0:
        sides.append('C')
    #baixo
    if  fy + 1 == height - 1:
        sides.append('B')
    #direita
    if fx + 1 == width - 1:
        sides.append('D')

    return sides


def addFrontDoor(casa, comodo, planta, dir):
        ix, iy, fx, fy = comodo.getCoordinates()
        match dir:
            case 'C':
                r = randint(ix, fx)
                planta[iy][r] = 'P'
                casa.portax = r
                casa.portay = iy

            case 'B':
                r = randint(ix, fx)
                planta[fy][r] = 'P'
                casa.portax = r
                casa.portay = fy

            case 'E':
                r = randint(iy, fy)
                planta[r][ix] = 'P'
                casa.portax = ix
                casa.portay = r

            case 'D':
                r = randint(iy, fy)
                planta[r][fx] = 'P'
                casa.portax = fx
                casa.portay = r

#Adiciona um simbolo em alguma posição das paredes externas do comodo
def addExternalSimbol(comodo, planta, dir, simbol):
    ix, iy, fx, fy = comodo.getCoordinates()

    match dir:
        case 'C':
            r = randint(ix, fx)
            planta[iy][r] = simbol
            comodo.janelax = r
            comodo.janelay = iy

        case 'B':
            r = randint(ix, fx)
            planta[fy][r] = simbol
            comodo.janelax = r
            comodo.janelay = fy


        case 'E':
            r = randint(iy, fy)
            planta[r][ix] = simbol
            comodo.janelax = ix
            comodo.janelay = r

        case 'D':
            r = randint(iy, fy)
            planta[r][fx] = simbol
            comodo.janelax = fx
            comodo.janelay = r



def addWindows(comodo, planta, width, height, dir):

    if comodo.tipo == 'escada':
        return
    
    sides = checkExternalWalls(comodo, width, height, dir)

    #um canto aleatório pra por a janela
    if len(sides) != 0:
        r = choice(sides)
        addExternalSimbol(comodo, planta, r, 'w')

# Adiciona corredores para acesso a todos os cômodos
def addCorridors(planta, corridors, width, height):   
    for y in range(1, height - 1):  # Ajuste os limites para evitar índices fora do intervalo
        for x in range(1, width - 1):  # Ajuste os limites para evitar índices fora do intervalo
            if planta[y][x] == ' ':
                # Verifica se há cômodos adjacentes
                if (x > 0 and planta[y][x-1] != ' ' and planta[y][x-1] != simbols['corredor'].simbol) or \
                    (x < width-1 and planta[y][x+1] != ' ' and planta[y][x+1] != simbols['corredor'].simbol) or \
                    (y > 0 and planta[y-1][x] != ' ' and planta[y-1][x] != simbols['corredor'].simbol) or \
                    (y < height-1 and planta[y+1][x] != ' ' and planta[y+1][x] != simbols['corredor'].simbol):
                    planta[y][x] = simbols['corredor'].simbol
                    addCorridor(planta, corridors, x, y)  # Corrigido a ordem dos parâmetros

    # Conecta os corredores horizontalmente
    for y in range(1, height - 1):  # Ajuste os limites para evitar índices fora do intervalo
        start = None
        for x in range(1, width - 1):  # Ajuste os limites para evitar índices fora do intervalo
            if planta[y][x] == simbols['corredor'].simbol:
                addCorridor(planta, corridors, x, y)  # Corrigido a ordem dos parâmetros
                if start is None:
                    start = x
            elif start is not None:
                for i in range(start, x):
                    planta[y][i] = simbols['corredor'].simbol
                    addCorridor(planta, corridors, i, y)  # Corrigido a ordem dos parâmetros
                start = None

    # Conecta os corredores verticalmente
    for x in range(1, width - 1):  # Ajuste os limites para evitar índices fora do intervalo
        start = None
        for y in range(1, height - 1):  # Ajuste os limites para evitar índices fora do intervalo
            if planta[y][x] == simbols['corredor'].simbol:
                addCorridor(planta, corridors, x, y)  # Corrigido a ordem dos parâmetros
                if start is None:
                    start = y
            elif start is not None:
                for i in range(start, y):
                    planta[i][x] = simbols['corredor'].simbol
                    addCorridor(planta, corridors, x, i)  # Corrigido a ordem dos parâmetros
                start = None
          
                    
#Coloca os comodos na planta do andar
def drawAndar(casa, andar, direcao, reset = True, inseridos = None):
    # Obtém as dimensões da casa
    width = casa.width
    height = casa.height

    # Define a ordem de preenchimento com base na direção
    if direcao == 'C':
        x_range = range(1, width - 1)
        y_range = range(1, height - 1)
    elif direcao == 'D':
        x_range = range(width - 2, 0, -1)
        y_range = range(1, height - 1)
    elif direcao == 'B':
        x_range = range(1, width - 1)
        y_range = range(height - 2, 0, -1)
    elif direcao == 'E':
        x_range = range(1, width - 1)
        y_range = range(1, height - 1)
    else:
        x_range = range(1, width - 1)
        y_range = range(1, height - 1)

    # Preenche a matriz com os cômodos
    if not andar.planta or reset:
        reset = True
        andar.iniciaPlanta(width, height)

    planta = andar.planta

    i = 0
    for comodo in andar.comodos:
        # Encontra uma posição livre para o cômodo
        # comodo.print()

        if not reset and i in inseridos:
            i += 1
            continue
        
        placed = False
        for y in y_range:
            for x in x_range:
                if (x + comodo.largura <= width - 1 and y + comodo.altura <= height - 1 and
                    all(planta[y+i][x+j] == ' ' for i in range(comodo.altura) for j in range(comodo.largura))):
                    # Preenche o espaço do cômodo na matriz
                    for i in range(comodo.altura):
                        for j in range(comodo.largura):
                            planta[y+i][x+j] = simbols[comodo.tipo].simbol

                    comodo.iniciox = x
                    comodo.inicioy = y
                    placed = True
                    break
            if placed:
                break

        if not placed:
            return False

        # Adiciona a porta da frente
        if comodo.tipo == 'sala':
                addFrontDoor(casa, comodo, planta, direcao)

        addWindows(comodo, planta, width, height, direcao)
        # Adiciona portas internas 
        # Adiciona corredores e conecta todos os cômodos
        addInternalDoors(comodo, andar.corridors, planta, width, height)
        addCorridors(planta, andar.corridors, width, height)

        i += 1

    return True
        
def printPlantaCasa(casa):

    for andar in casa.andares:

        print("\nPlanta da Casa:")
        print("+" + "-" * (casa.width) + "+")
        for linha in andar.planta:
            print("|" + "".join(linha) + "|")
        print("+" + "-" * (casa.width) + "+")

        # Imprime a legenda
        print("\nLegenda:")
        for tipo, info in simbols.items():
            print(f"{info.simbol}: {tipo}")


def geraPopInicial( width, height, direcao):

    while len(pop) != popSize:
        casa = Casa(width, height)

        #inicializa os andares
        casa.andares = [Andar('Térreo'), Andar('1 Andar'), Andar('Laje')]
    
        #preenche os andares da casa com comodos aleatórios
        criado = sorteiaComodos(casa, direcao)
        if not criado and len(pop) == 0:
            print("Tamanho da casa não cabe todos os cômodos, por favor insira uma area maior.")
            break
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
def selectParentes(direcao):
    newMutants = []

    #Gera mutantes até encontrar um válido
    while len(newMutants) != 3:
        r = randint(2, len(pop))
        subPop = drawSubPop(pop, r)
        subPop.sort(key = getFitness, reverse = True)
        mutant = mutate(subPop[0], direcao)

        if not mutant:
            continue

        newMutants.append(mutant)

    insertIntoPop(pop, newMutants)

def mutate(pai, direcao):

    mutante =  deepcopy(pai)
    
    comodosT = mutante.andares[0].comodos
    comodos1A = mutante.andares[1].comodos

    mutaveisT = [comodo for comodo in comodosT if comodo.tipo not in ['sala', 'cozinha', 'salaDeJantar', 'escada']]
    mutaveis1A = [comodo for comodo in comodos1A if comodo.tipo != 'escada']

    if len(mutaveisT) != 0:
        c = choice(mutaveisT)
        c2 = choice(mutaveis1A)

        indexT = comodosT.index(c)
        index1A = comodos1A.index(c2)

        comodosT[indexT] = c2
        comodos1A[index1A] = c
       

        for i in range(len(mutante.andares) - 1):
            resultado = drawAndar(mutante, mutante.andares[i], direcao)
            if not resultado:
                return None



    #chance de aumentar o tamanho do comodo
    rand = randint(1,100)
    if rand > 50:
        rand = randint(1,100)
        if rand > 50:
            andarSort = mutante.andares[0]
            comodoSort = choice(comodosT)
        else:
            andarSort = mutante.andares[1]
            comodoSort = choice(comodos1A)
       
        largura, altura = drawRoomsSize(comodoSort.tipo, mutante)
        index = andarSort.comodos.index(comodoSort)

        #guarda as configurações atuais:
        curPlanta = andarSort.planta
        curLargura =  andarSort.comodos[index].largura
        curAltura = andarSort.comodos[index].altura

        andarSort.comodos[index].largura = largura
        andarSort.comodos[index].altura = altura
        
        #tenta inserir
        resultado = drawAndar(mutante, andarSort, direcao)

        #Se não consegue descarta a mudança
        if not resultado:
            andarSort.planta = curPlanta
            andarSort.comodos[index].largura = curLargura
            andarSort.comodos[index].altura = curAltura
    
    mutante.calcFitness()
    return mutante



pop = []
popSize = 10
geracoes = 100
def main():
    # width = int(input("Digite a largura da casa: "))
    # height = int(input("Digite a altura da casa: "))
    # dir = input("Digite a direção da casa: ")
    # dir = dir.upper() #COLOCANDO EM MAIUSCULO
    width = 25
    height = 15
    dir = 'C'
    geraPopInicial(width, height, dir)
    # printPop(pop)
    pop.sort(key = getFitness, reverse = True)

    # # # TODO: desenhar as casas
    for i in range(0, geracoes):
        print("-------------------------------")
        selectParentes(dir)
        pop.sort(key = getFitness, reverse = True)
        # printPop(pop)

    
    printPlantaCasa(pop[0])
    pop[0].fitness
    pop[0].printHouse()



if __name__ == "__main__":
    main()