from random import shuffle, randint
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

        

    def generateHouse(self):
        for i in range(len(self.andares)):
            self.andares[i].createMap(self.width, self.height)

    
        

class Andar:
    def __init__(self, nome):
        #nome do andar 
        self.nome = nome
        #lista dos comodos presentes no andar
        self.comodos = []
        self.corridors = []
        #Como os cômodos foram posicionados
        self.mapa= []

    def print(self):
        print(f"####### {self.nome} #######")
        for comodo in self.comodos:
            comodo.print()
        
    def insertRoom(self, type, width, height):
        newRoom = Comodo(type, width, height)
        self.comodos.append(newRoom)

    
class Comodo:
    def __init__(self, tipo, largura, altura):
        self.tipo = tipo
        self.altura = altura
        self.largura = largura
        self.iniciox, self.inicioy = None, None
        self.portax, self.portay = None, None
        self.janelax, self.janelay = None, None
         

    def print(self):
        print(f'------{self.tipo}')
        print(f'altura: {self.altura}, largura: {self.largura}')
        # print(f'iniciox: {self.iniciox}, inicioY: {self.inicioy} ')
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
        width, height = drawRoomsSize(roomName, casa) 
        casa.andares[0].insertRoom(roomName, width, height)

    remainingSpaceT = calcRemaningSpace(casa.andares[0], casa.width, casa.height)
    remainingSpace1 =  casa.width * casa.height



    #enquanto a lista não está vazia vai distribuindo os comodos pelos andares
    while(remainingRooms):

        roomWidth, roomHeight = drawRoomsSize(remainingRooms[0], casa) 
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
def drawRoomsSize(comodo,casa):

    minS = simbols[comodo].minSize
    maxS = simbols[comodo].maxSize
    
    if minS == maxS:
        return int(minS/2), int(maxS/2)
    
    while True:

        alturaSize = randint(1, 10)
        larguraSize = randint(1, 10)

        if comodo != 'sala' and alturaSize == casa.height or larguraSize == casa.width:
            continue

        if alturaSize*larguraSize >= minS and alturaSize*larguraSize <= maxS and alturaSize <= casa.height and larguraSize <= casa.width:
            if alturaSize > casa.height:
                return alturaSize, larguraSize
            return larguraSize, alturaSize
        
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
        print(f'i: {i} | d: {d}')
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
    # print('GET CLOSER WALLL')
    print(ix, iy, fx, fy)
    print(side)
    # print(f"CORRIDOR: {corridor}")

    currD = 1000.0
    parede = ()
    match side:

        case 'C':
            # print('ENTROU EM C')
            if ix == fx:
                parede = (ix, iy)
            else: 
                for x in range(ix, fx):
                    P = (x,iy)

                    #Evita invadir comodos
                    if planta[iy - 1][x] != ' ' and planta[iy - 1][x] != '*':
                        continue

                    print(f'x: {x}')
                    d = CalcDistPontos(corridor, (x,iy))
                    print(f'x: {x} | d = {d}')
                    #Não sobrepõe comodo
                    if(currD > d):
                        currD = d
                        parede = P

        case 'B':
            # print('ENTROU EM B')
            if ix == fx:
                parede = (ix, fy)
            else: 
                for x in range(ix, fx):
                    P = (x,fy)

                    #Evita invadir comodos
                    if planta[fy + 1][x] != ' ' and planta[fy + 1][x] != '*':
                        continue

                    print(f'x: {x}')
                    d = CalcDistPontos(corridor, (x,fy))
                    print(f'x: {x} | d = {d}')
                    #Não sobrepõe comodo
                    if(currD > d):
                        currD = d
                        parede = P

        case 'E':
            # print('ENTROU EM E')
            if iy == fy:
                parede = (ix, iy)
            else: 
                for y in range(iy, fy):
                    P = (ix,y)
                    
                    #Evita invadir comodos
                    if planta[y][ix - 1] != ' ' and planta[y][ix - 1] != '*':
                        continue

                    print(f'y: {y}')
                    d = CalcDistPontos(corridor, P)
                    print(f'y: {y} | d = {d}')
                    #Não sobrepõe comodo
                    if(currD > d ):
                        currD = d
                        parede = P

        case 'D':
            # print('ENTROU EM D')
            if iy == fy:
                parede = (fx, fy)
            else: 
                for y in range(iy, fy):
                    print(f'y: {y}')
                    P = (fx,y)

                    #Evita invadir comodos
                    if planta[y][fx + 1] != ' ' and planta[y][fx + 1] != '*':
                        continue


                    d = CalcDistPontos(corridor, P)
                    print(f'y: {y} | d = {d}')
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

    # print("addInternalSymbol")
    # print(f'dir: {dir}')

    match dir:
        case 'C':
            for x in range(ix, fx):
                if planta[iy - 1][x] == ' ':
                    r = randint(x, fx)
                    addDoor(planta, comodo, r, iy)
                    addCorridor(planta, corridors, r, iy - 1)
                    return

        case 'B':
            for x in range(ix, fx):
                if planta[fy + 1][x] == ' ':
                    r = randint(x, fx)
                    addDoor(planta, comodo, r, fy)
                    addCorridor(planta, corridors, r, fy + 1)
                    return

        case 'E':
            for y in range(iy, fy):
                if planta[y][ix - 1] == ' ':
                    r = randint(y, fy)
                    addDoor(planta, comodo, ix, r)
                    addCorridor(planta, corridors, ix - 1, r)
                    return
        
        case 'D':
            for y in range(iy, fy):
                if planta[y][fx + 1] == ' ':
                    r = randint(y, fy)
                    addDoor(planta, comodo, fx, r)
                    addCorridor(planta, corridors, fx + 1, r)
                    return


def conectaCorredores(planta, corridors, pInicio, pFim):
    xi, yi = pInicio
    xf, yf = pFim

    # print(f'inicio: {pInicio}')
    # print(f'fim: {pFim}')

    #Define as prioridades de movimetno
    prior = ['', '', '', '']
    if xf > xi:
        prior[0] = 'D'
        prior[3] = 'E'
    else:
        prior[0] = 'E'
        prior[3] = 'D'

    if yf > yi:
        prior[1] = 'B'
        prior[2] = 'C'
    else: 
        prior[1] = 'C'
        prior[2] = 'B'

    print(f'prior: {prior}')

    for i in range(0,4):
        
        for p in prior:
            match p:
                case 'E':
                    # print(f'CAIU EM {p}')
                    if planta[yi][xi - 1] == ' ':
                        # print("ENTROU")
                        addCorridor(planta, corridors, xi - 1, yi)
                        xi = xi - 1
                        break

                case 'D':
                    # print(f'CAIU EM {p}')
                    if planta[yi][xi + 1] == ' ':
                        # print("ENTROU")
                        addCorridor(planta, corridors, xi + 1, yi)
                        xi = xi + 1
                        break

                case 'B':
                    # print(f'CAIU EM {p}')
                    if planta[yi + 1][xi] == ' ':
                        # print("ENTROU")
                        addCorridor(planta, corridors, xi, yi +1)
                        yi = yi + 1
                        break

                case 'C':
                    # print(f'CAIU EM {p}')
                    if planta[yi -1][xi] == ' ':
                        # print("ENTROU")
                        addCorridor(planta, corridors, xi, yi - 1)
                        yi = yi - 1
                        break
                
        print(xi, yi)

def addInternalDoors(comodo, corridors, planta, width, height):

    print(comodo.tipo)

    #TODO: colocar corredores na escada
    if comodo.tipo == 'escada':
        return

    ix, iy, fx, fy = comodo.getCoordinates()
    sides = checkInternalWalls(comodo, width, height)

    print(sides)
    # print(f'lencorridors: {len(corridors)}')

    #primeiro comodo:
    if(len(corridors) == 0):
        # print("len corridors 0")
        r = 0
        if(len(sides) > 1):
            r = randint(0, len(sides) - 1)

        print(f'r = {r}')

        addDoorCorridorRandom(comodo, corridors, planta, sides[r])
        return
        
    #TODO: Não funciona???
    #verifica se há corredores colados a parede
    for side in sides:
        # print(f'side: {side}')
        match side:
            case 'C':
                #Caso só tenha 1m de lado
                if ix == fx and  planta[iy - 1][ix] == '*':
                    addDoor(planta, comodo, ix , iy)
                    addCorridor(planta, corridors, ix, iy - 1)

                else: 
                    for x in range(ix, fx):
                        if planta[iy - 1][x] == '*':
                            addDoor(planta, comodo, x , iy)
                            addCorridor(planta, corridors, x , iy - 1)
                            return

            case 'B':
                 #Caso só tenha 1m de lado
                if ix == fx and  planta[fy + 1][ix] == '*':
                    addDoor(planta, comodo, ix , fy)
                    addCorridor(planta, corridors, ix, fy + 1)

                else: 
                    for x in range(ix, fx):
                        if planta[fy + 1][x] == '*':
                            addDoor(planta, comodo, x , fy)
                            addCorridor(planta, corridors, x , fy + 1)
                            return

            case 'E':
                 #Caso só tenha 1m de lado
                if iy == fy and  planta[iy][ix + 1] == '*':
                    addDoor(planta, comodo, ix , fy)
                    addCorridor(planta, corridors, ix - 1 , fy)

                else: 
                    for y in range(iy, fy):
                        if planta[y][ix - 1] == '*':
                            addDoor(planta, comodo, ix , y)
                            addCorridor(planta, corridors, ix - 1, y)
                            return
            
            case 'D':
                 #Caso só tenha 1m de lado
                if iy == fy and  planta[iy][fx + 1] == '*':
                    addDoor(planta, comodo, fx , iy)
                    addCorridor(planta, corridors, fx + 1 , iy)

                else: 
                    for y in range(iy, fy):
                        if planta[y][fx + 1] == '*':
                            addDoor(planta, comodo, fx , y)
                            addCorridor(planta, corridors, fx + 1 , y)
                            return


    #busca o corredor mais proximo pra inserir
    indexMenor = 0
    distMenor = 10000
    sideMenor = []
    for side in sides:

        sideMenor.append((side, distMenor))
        # print(f'side: {side}')
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

        # print(f'coordenadas reta: {rx0, rxi, ry0, ryi}')

        if ((side == 'C' or side == 'B') and rx0 == rxi) or ((side == 'D' or side == 'E') and ry0 == ryi):
            point = (rx0, ryi)
            # print(f'point: {point}')
            i,d = getCloserCorridorPoint(corridors, point)
        else:
            reta = calcEquacaoGeralReta(rx0, rxi, ry0, ryi)
            i, d = getCloserCorridorReta(corridors, reta)
            # print(f"reta: {reta}")
        
    
        # print(f"index do corredor mais proximo: {i}")
        # print(f'corredor mais prox: {corridors[i]}')

        if (distMenor > d):
            distMenor = d
            indexMenor = i
            
            for i, (s, _) in enumerate(sideMenor):
                if s == side:
                    itemp = i
                    break

            sideMenor[itemp] = (side, d)
           

    sideMenor.sort(key=lambda x: x[1])
    # print(f'sorted: {sideMenor}')

    #tenta colocar na melhor parede, se não conseguir, tenta nas outras
    while(len(sideMenor) != 0):
        
        values = getCloserWall(comodo, sideMenor[0][0], corridors[indexMenor], planta)
        if(len(values) == 2):
            x , y = values
            # print(f'PAREDE: { x , y}')
            addDoorCorridor(comodo,corridors, planta, sideMenor[0][0], x, y)
            conectaCorredores(planta, corridors, values, corridors[indexMenor])
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
def checkExternalWalls(comodo, width, height):
    sides = []

    ix, iy, fx, fy = comodo.getCoordinates()

    #esquerda
    if ix-1 < 0:
        sides.append('E')
    #cima
    if iy - 1 < 0:
        sides.append('C')
    #baixo
    if  fy + 1 > height:
        sides.append('B')
    #direita
    if fx + 1 > width:
        sides.append('D')

    return sides



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


def addWindows(andar, planta, width, height):

    for comodo in andar.comodos:
        if comodo.tipo == 'escada':
            continue
        
        sides = checkExternalWalls(comodo, width, height)

        #um canto aleatório pra por a janela
        if len(sides) != 0:
            r = randint(0, len(sides) - 1)

            addExternalSimbol(comodo, planta, sides[r], 'w')


          
                    
            

# Função para desenhar a casa no terminal
def drawHouse(casa, direcao):
    # Obtém as dimensões da casa
    width = casa.width
    height = casa.height

    # Cria uma matriz para representar a planta da casa
    planta = [[' ' for _ in range(width)] for _ in range(height)]
    stair_position = None  # Armazena a posição da escada

    # Preenche a matriz com os cômodos
    for andar in casa.andares:
        for comodo in andar.comodos:
            # Encontra uma posição livre para o cômodo
            comodo.print()
            
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
                        
                        # Armazena a posição da escada do primeiro andar
                        if comodo.tipo == 'escada' and stair_position is None:
                            stair_position = (x, y)
                        
                        # Sai dos loops após posicionar o cômodo
                        break
                else:
                    continue
                break
            
            # Adiciona a porta da frente
            if comodo.tipo == 'sala':
                addExternalSimbol(comodo, planta, direcao, 'P')

        # Coloca a escada na mesma posição nos andares subsequentes
        if stair_position and andar.nome != 'Térreo':
            x, y = stair_position
            for i in range(2):  # Assumindo que a escada ocupa 2x2
                for j in range(2):
                    planta[y+i][x+j] = simbols['escada'].simbol

            # addCorridors(planta, comodo, width, height)


            addInternalDoors(comodo, andar.corridors, planta, width, height)
        addWindows(andar, planta, width, height)

        # Imprime a planta da casa
        print("\nPlanta da Casa:")
        print("+" + "-" * (width) + "+")
        for linha in planta:
            print("|" + "".join(linha) + "|")
        print("+" + "-" * (width) + "+")

        # Imprime a legenda
        print("\nLegenda:")
        for tipo, info in simbols.items():
            print(f"{info.simbol}: {tipo}")
        
        planta = [[' ' for _ in range(width)] for _ in range(height)]

def geraPopInicial( width, height):

    for i in range(0, popSize):
        casa = Casa(width, height)

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
    remaning1A = [x for x in casa.andares[1].comodos if x.tipo != 'escada']

    if len(remaingT) != 0:

        rt = randint(0,  len(remaingT) - 1) if len(remaingT) > 1 else 0
        r1 = randint(0,  len(remaning1A) - 1)

        roomt = remaingT[rt]
        indexrt = casa.andares[0].comodos.index(roomt)
        room1 = remaning1A[r1]

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
            newW, newH =  drawRoomsSize(casa.andares[i].comodos[rand].tipo, casa)
            if(space >= newW * newH):
                casa.andares[i].comodos[rand].altura, casa.andares[i].comodos[rand].altura = newW, newH

    casa.calcFitness()
    return casa



pop = []
popSize = 10
geracoes = 2
# dir = 'N'
def main():
    # width = int(input("Digite a largura da casa: "))
    # height = int(input("Digite a altura da casa: "))
    # dir = input("Digite a direção da casa: ")
    # dir = dir.upper() #COLOCANDO EM MAIUSCULO
    width = 25
    height = 15
    dir = 'C'
    geraPopInicial(width, height)
    # printPop(pop)
    pop.sort(key = getFitness, reverse = True)

    print(pop[0].fitness)
    drawHouse(pop[0], dir)
    for andar in pop[0].andares:
        print(andar.corridors)

    # # # TODO: desenhar as casas
    # for i in range(0, geracoes):
    #     print("-------------------------------")
    #     selectParentes()
    #     pop.sort(key = getFitness, reverse = True)
    #     printPop(pop)



    # print(pop[0].fitness)
    # drawHouse(pop[0], dir)

    # pop[0].printHouse()
    



if __name__ == "__main__":
    main()
