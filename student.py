"""Example client."""
import asyncio
import getpass
import json
import os
import copy
import datetime
import math
from common import * 

# Next 4 lines are not needed for AI agents, please remove them from your code!
# import pygame
import websockets

# pygame.init()
# program_icon = pygame.image.load("data/icon2.png")
# pygame.display.set_icon(program_icon)

class SearchNode:
    def __init__(self,state,parent,ordens,heuristica): 
        self.state = state
        self.parent = parent
        self.ordens = ordens
        self.heuristica = heuristica
        #self.depth = depth
        

    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    def __repr__(self):
        return str(self)


class SearchTree:

    # construtor
    def __init__(self,problem, strategy='greedy'): 
        self.problem = problem
        root = SearchNode(problem, None,[],0)
        #self.all_nodes = [root]
        self.open_nodes = [root]
        #self.open_states=[]
        self.strategy = strategy
        self.solution = None
        self.non_terminals = 0
    
    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state["grid"]]
        path = self.get_path(node.parent)
        path += [node.state["grid"]]
        return(path)

    def solucao(self,node,map,ordens,p):
        cursor = node.state.get("cursor")
        selected = node.state.get("selected")
        #print(selected)
        if (selected != p):
            ordens.append(" ")
        if ((cursor[0] != map.piece_coordinates(p)[1].x) or (cursor[1] != map.piece_coordinates(p)[1].y)):
            while( map.piece_coordinates(p)[1].x < cursor[0]):   #enquanto a coordenada x da peça for menor q a do cursor
                ordens.append("a")
                cursor[0] += -1
            while( map.piece_coordinates(p)[1].x > cursor[0]):
                ordens.append("d")
                cursor[0] += 1
            while(map.piece_coordinates(p)[1].y < cursor[1]):
                ordens.append("w")
                cursor[1] += -1
            while( map.piece_coordinates(p)[1].y > cursor[1]):    
                ordens.append("s")
                cursor[1] += 1
        if (cursor[0] == map.piece_coordinates(p)[1].x) and (cursor[1] == map.piece_coordinates(p)[1].y):
            if selected != p:
                ordens.append(" ")
                node.state["selected"] = p
                
        #print(cursor)
        #print(ordens)
        #return(ordens)
        return None

    # procurar a solucao
    def search(self):
        # ordens = []      
        while self.open_nodes != []:
            #nodeID = self.open_nodes.pop(0)
            node = self.open_nodes.pop(0)
            #node = self.all_nodes[nodeID]
            #self.open_states += node.state
            map = Map(node.state.get("grid"))
            if map.test_win():              #o if está a dar sempre true.... faltava os ()
                self.solution = node
                #self.terminals = len(self.open_nodes)+1
                print("SOLUCAO ENCONTRADA")
                return node.ordens
            lnewnodes = []
            self.non_terminals += 1
            for (x,y,p) in self.acoes(map):
                #print(f'1 - {self.get_path(node)}') 
                #print(node.state)
                newNode = copy.deepcopy(node)
                #temnode = SearchNode(node.state,node.parent,node.ordens)   #copia temporario do node para nao alterar 
                self.solucao(newNode,map,newNode.ordens,p)
                map.move(p,Coordinates(x,y))               #estamos sempre a mexer no mesmo mapa causando assim o problema 
                self.solucao(newNode,map,newNode.ordens,p)   #traduzir o move para instruções em array
                print(newNode.ordens)              
                newNode.state["grid"] = repr(map)
                #newstate = self.problem.domain.result(node.state,a)
                #print(repr(map))
                #print(newNode.state["grid"])
                #newstate = node.state
                #print(node)
                #print(newstate)        
                #print(f'2 - {self.get_path(node)}')    
                #print(self.open_states)               
                if newNode.state["grid"] not in self.get_path(node): 
                    #if newstate not in self.open_states:
                    #if node not in self.get_path(node):
                    print("novo nó")
                    newnode = SearchNode(newNode.state,node,newNode.ordens,self.heuristic(newNode.state["grid"],map))
                    lnewnodes.append(newnode)
                    #lnewnodes.append(len(self.all_nodes))
                    #self.all_nodes.append(newnode)
                    #self.open_states.append(newstate)
                map.move(p,Coordinates(-(x),-(y)))
            self.add_to_open(lnewnodes)
        return []

    def acoes(self,map):
        acoes=[]
        #print(map.coordinates)
        for (x,y,p) in map.coordinates:
            try:
                to = Coordinates(1,0)                   #verificar se a peça de pode mover para a direita
                map.move(p,to)                          
                to = Coordinates(-1,0)                  #colocar a peça de volta no sitio para nao modificar o map 
                map.move(p,to)
            except :
                pass
            else:
                if (1,0,p) not in acoes:
                    acoes.append((1,0,p))
            
            try:                                            #verificar esquerda
                to = Coordinates(-1,0)
                map.move(p,to)
                to = Coordinates(1,0)
                map.move(p,to)
            except MapException as err:
                #print(err)
                pass
            else:
                if (-1,0,p) not in acoes:
                    acoes.append((-1,0,p))

            try:                                            #verificar baixo
                to = Coordinates(0,1)
                map.move(p,to)
                to = Coordinates(0,-1)
                map.move(p,to)
            except:
                pass
            else:
                if (0,1,p) not in acoes:
                    acoes.append((0,1,p))

            try:                                            #verificar cima
                to = Coordinates(0,-1)
                map.move(p,to)
                to = Coordinates(0,+1)
                map.move(p,to)
            except:
                pass
            else:
                if (0,-1,p) not in acoes:
                    acoes.append((0,-1,p))   
        #print(acoes)                        
        return acoes

    def __str__(self):
        return "no(" + str(SearchTree.search(self)) + ")"
    def __repr__(self):
        return str(self)


    def heuristic(self, grelha, mapa):
        pieces, grid, movements = grelha.split(" ")
        ignorar,contar = grid.split("AA")
        grid_size = math.sqrt(len(grid))
        trabalho = 0
        (x,y) = mapa.piece_coordinates("A")[1].x,mapa.piece_coordinates("A")[1].y
        #if some piece is in the same line as A
        for (x_compare,y_compare,p) in mapa.coordinates:
            if p == "A":
                continue
            if y == y_compare and x > x_compare:
                trabalho +=1
        distancia_fim = grid_size - x
        return distancia_fim+trabalho

    

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'greedy':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda node: node.heuristica)

async def agent_loop(server_address="localhost:8000", agent_name="Edu's"):
    """Example client loop."""
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        # Next 3 lines are not needed for AI agent
        # SCREEN = pygame.display.set_mode((299, 123))
        # SPRITES = pygame.image.load("data/pad.png").convert_alpha()
        # SCREEN.blit(SPRITES, (0, 0))
        keys = []
        while True:           
            try:              
                
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server
                #print(state.get("cursor"))
                #print(state)
                #t = SearchTree(state)   #map(state.get("grid"))   -- inside
                #print(t.search)
                key = ""
                # if 'piece' in state and 'game' in state:
                #     if len(list_of_keys) != 0:
                #         key = list_of_keys.pop(0)
                #     else:
                #         list_of_keys = agent(state)  
                # for event in pygame.event.get():     #tenho de carregar para algo acontecer
                #t = SearchTree(state)
                if 'grid' in state:
                    if len(keys) != 0:
                        key = keys.pop(0)
                    else:
                        start_time = datetime.datetime.now()
                        t = SearchTree(state)
                        keys = t.search()
                        end_time = datetime.datetime.now()
                        print(end_time - start_time)

                        #print(keys)
                               
                # for i in range(0,len(teste),1):  
                #     key = teste[i]
                #     print(i)
                #     # print(len(teste))

                    await websocket.send(
                                json.dumps({"cmd": "key", "key": key})
                            )  # send key command to server - you must implement this send in the AI agent
                    #break
                    # Next lines are only for the Human Agent, the key values are nonetheless the correct ones!
                    #key = ""
                    # for event in pygame.event.get():
                    #     if event.type == pygame.QUIT:
                    #         pygame.quit()

                    #     if event.type == pygame.KEYDOWN:
                    #         if event.key == pygame.K_UP:
                    #             key = "w"
                    #         elif event.key == pygame.K_LEFT:
                    #             key = "a"
                    #         elif event.key == pygame.K_DOWN:
                    #             key = "s"
                    #         elif event.key == pygame.K_RIGHT:
                    #             key = "d"
                    #         elif event.key == pygame.K_SPACE:
                    #             key = " "

                    #         elif event.key == pygame.K_d:
                    #             import pprint

                    #             pprint.pprint(state)
                            

                            # await websocket.send(
                            #     json.dumps({"cmd": "key", "key": key})
                            # )  # send key command to server - you must implement this send in the AI agent
                            # break
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return

            # Next line is not needed for AI agent
            # pygame.display.flip()


# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
