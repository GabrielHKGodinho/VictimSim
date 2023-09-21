## EXPLORER AGENT
### @Author: Tacla, UTFPR
### It walks randomly in the environment looking for victims.

import sys
import os
import random
from abstract_agent import AbstractAgent
from physical_agent import PhysAgent
from abc import ABC, abstractmethod


class Explorer(AbstractAgent):

    def __init__(self, env, config_file, resc):
        """ Construtor do agente random on-line
        @param env referencia o ambiente
        @config_file: the absolute path to the explorer's config file
        @param resc referencia o rescuer para poder acorda-lo
        """

        super().__init__(env, config_file)
        
        # Specific initialization for the rescuer
        self.resc = resc           # reference to the rescuer agent
        self.rtime = self.TLIM     # remaining time to explore  

        # Criar uma matriz vazia
        self.mapa = []

        # Armazena a posição do agente na matriz
        self.xPos = int(self.rtime/2)
        self.yPos = int(self.rtime/2)

        # Posição da base
        self.base = int(self.rtime/2)

        # Preencher a matriz com elementos (vamos usar 0 como exemplo)
        for _ in range(int(self.rtime)):
            linha = [-3] * int(self.rtime)
            self.mapa.append(linha)

        

    def deliberate(self) -> bool:
        """ The agent chooses the next action. The simulator calls this
        method at each cycle. Must be implemented in every agent"""

        # No more actions, time almost ended
        if self.rtime < 1.0: 
            # time to wake up the rescuer
            # pass the walls and the victims (here, they're empty)
            print(f"{self.NAME} I believe I've remaining time of {self.rtime:.1f}")
            self.resc.go_save_victims([],[]) # primeiro parametro sao as paredes segundo as vitimas
            return False
        
        dx = random.choice([-1, 0, 1])

        if dx == 0:
           dy = random.choice([-1, 1])
        else:
           dy = random.choice([-1, 0, 1])
        
        # Check the neighborhood obstacles
        obstacles = self.body.check_obstacles()


        # Moves the body to another position
        result = self.body.walk(dx, dy)
        if result == 1:
            self.preencheMapa()


        # Atualiza a posição atual
        self.xPos += dx
        self.yPos += dy


        # Update remaining time
        if dx != 0 and dy != 0:
            self.rtime -= self.COST_DIAG
        else:
            self.rtime -= self.COST_LINE

        # Test the result of the walk action
        if result == PhysAgent.BUMPED:
            walls = 1  # build the map- to do
            # print(self.name() + ": wall or grid limit reached")

        if result == PhysAgent.EXECUTED:
            # check for victim returns -1 if there is no victim or the sequential
            # the sequential number of a found victim
            seq = self.body.check_for_victim()
            if seq >= 0:
                vs = self.body.read_vital_signals(seq)
                self.rtime -= self.COST_READ
                # print("exp: read vital signals of " + str(seq))
                # print(vs)
                
        return True
     
    def preencheMapa(self):
        loc =  [[0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]]

        min = 100000
        xMin = 0
        yMin = 0

        for y in [-1,0,1]:
            for x in [-1, 0, 1]:
                loc[y][x] = self.mapa[int(self.yPos) + y][int(self.xPos) +x]
                if loc[y][x] < min and loc[y][x] > 0:
                    xMin = y
                    yMin = x
                    min = loc[y][x]
        
        if min == 100000:
            if self.xPos == len(self.mapa)//2 or self.yPos == len(self.mapa)//2:
                self.mapa[self.yPos][self.xPos] = 1
            else:
                self.mapa[self.yPos][self.xPos] = 1.5

        elif xMin == self.xPos or yMin == self.yPos:
            self.mapa[self.yPos][self.xPos] = min + 1
        else:
            self.mapa[self.yPos][self.xPos] = min + 1.5

        for y in range(int(self.rtime)):
            for x in range(int(self.rtime)):
                print(self.mapa[y][x], end= ' ')
            print()
        print()


    
        



                
        
