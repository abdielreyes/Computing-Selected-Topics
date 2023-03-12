import pygame as pg
from collections import deque
from random import choice, randrange
import numpy as np
import pickle
import time
import datetime
import tkinter as tk
from  tkinter import filedialog
from pprint import pprint
import matplotlib.pyplot as plt
black = (0, 29, 36)
class Ant:
    def __init__(self, app, pos, direction, type):
        self.type = type
        if type == 0:
            self.color = (239, 71, 111) #red reina
        if type == 1:
            self.color = (255, 209, 102) #yellow reproductora
        if type == 2:
            self.color = (6, 214, 160) #green trabajador
        if type == 3:
            self.color = (17, 138, 178) #blue soldado
        self.x, self.y = pos
        self.life = 0
        #para rotar la hormiga, solo cambiamos la posicion[0] de increments al final del array
        #y asi se va rotando entre las direcciones
        self.increments = deque([(1, 0), (0, 1), (-1, 0), (0, -1)])
        self.increments.rotate(direction)

    def run(self,app):
        value = app.grid[self.y][self.x]
        #cambiamos el valor de una celda ocupada/desocupada en el mapa
        app.grid[self.y][self.x] = not value

        SIZE = app.CELL_SIZE
        rect = self.x * SIZE, self.y * SIZE, SIZE - 1, SIZE - 1
        if value:
            pg.draw.rect(app.screen, pg.Color(black), rect)
        else:
            pg.draw.rect(app.screen, self.color, rect)
        #por hormiga, recorremos las direcciones
        self.increments.rotate(1) if value else self.increments.rotate(-1)
        dx, dy = self.increments[0]
        self.x = (self.x + dx) % app.COLS
        self.y = (self.y + dy) % app.ROWS
        self.life += 1


class App:
    def __init__(self, WIDTH=1080, HEIGHT=720, CELL_SIZE=20):
        pg.init()
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])
        self.clock = pg.time.Clock()
        self.screen.fill(black)
        self.CELL_SIZE = CELL_SIZE
        self.ROWS, self.COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
        self.grid = [[0 for col in range(self.COLS)] for row in range(self.ROWS)]
        self.ants = []
        self.running = False
        self.iterations = 0
        self.plot_pop = []
    def generate_random_ants(self):
        for i in range(int(self.COLS*self.ROWS/2)):
            direction = np.random.randint(0,4)
            type = np.random.randint(0,4)
            c,r = randrange(self.COLS), randrange(self.ROWS)
            rect = c * self.CELL_SIZE, r * self.CELL_SIZE, self.CELL_SIZE - 1, self.CELL_SIZE - 1
            a = Ant(self, (c,r), direction, 
            type)
            pg.draw.rect(self.screen, a.color, rect)
            self.ants.append(a)
    def generate_ant(self,x,y):
        direction = np.random.randint(0,4)
        type = np.random.randint(0,100)
        if(type<=1):
            type = 0 #1%
        elif(type <= 9):
            type = 1 #9%
        elif(type<=35):
            type = 2 #35%
        else:
            type = 3 #55%
        # type = np.random.randint(0,2)
        a = Ant(self, (x,y), direction, 
        type)
        rect = x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE - 1, self.CELL_SIZE - 1
        pg.draw.rect(self.screen, a.color, rect)
        self.ants.append(a) 
    def create_mouse_ant(self):
        mx,my = int(pg.mouse.get_pos()[0]/self.CELL_SIZE), int(pg.mouse.get_pos()[1]/self.CELL_SIZE)
        value = self.grid[my][mx]
        self.grid[my][mx] = not value
        rect = mx * self.CELL_SIZE, my * self.CELL_SIZE, self.CELL_SIZE - 1, self.CELL_SIZE - 1
        if value:
            pg.draw.rect(self.screen, pg.Color(black), rect)
            self.ants.pop()
        else:
            self.generate_ant(mx,my)
    def get_grid_values(self,x,y):
        if x >= self.ROWS:
            x -= self.ROWS
        elif x < 0:
            x += self.ROWS
        if y >= self.COLS:
            y -= self.COLS
        elif y < 0:
            y += self.COLS
        return self.grid[x][y]
    def graph(self,b : list,s:int):
        s = np.array(s)
        population = np.divide(np.array(b),s)
        populationlog = np.divide(np.log10(population),s)
        plt.plot(population,label="Densidad de poblacion")
        plt.plot(populationlog, label="Densidad de poblacion base 10")
        plt.legend()
        plt.show()
    
    def run(self):
        
        while True:
            #actualizamos mapa
            if(self.running):
                for i,a in enumerate(self.ants):
                    if(self.running):
                        a.run(app=self)
                        self.iterations += 1
                        
                        self.plot_pop.append(len(self.ants))
                        if a.life > 80:
                            
                            del self.ants[i]
            #analizamos colisiones
                for i,a in enumerate(self.ants):
                    for abc in self.ants[:-i]:
                        x,y = abc.x, abc.y
                        if ((x-a.x) == 1 or (x-a.x) == 1) and ((y-a.y) == 1 or (y-a.y) == 1):
                            if abc.type == 0 and a.type == 1:
                                #nace hormiga
                                self.generate_ant(a.x,a.y)
                            if abc.type == 0 and a.type == 0:
                                #pelea reinas
                                if abc.life == a.life:
                                    survive = np.random.randint(0,2)
                                    if survive == 1:
                                        if self.ants.count(a) >0 : self.ants.remove(a)
                                        if self.ants.count(abc) > 0:self.ants.remove(abc)
                                    

            for i in pg.event.get():
                if i.type == pg.QUIT:
                    exit()
                if i.type == pg.KEYDOWN:
                    if i.key == pg.K_SPACE:
                        self.running = not self.running
                    if i.key == pg.K_r:
                        self.__init__()
                        break
                    if i.key == pg.K_g:
                        self.generate_random_ants()
                    if i.key == pg.K_k:
                        self.ants.pop()
                    if i.key == pg.K_s:
                        a = [self.grid,self.ants]
                        with open(f'langton_{self.COLS}_{self.ROWS}_{int(time.mktime(datetime.datetime.now().timetuple()))}.ant', 'wb') as f:
                            pickle.dump(a,f)
                    if i.key == pg.K_l:
                        file_path = filedialog.askopenfilename(filetypes=(
                        ("Ant Files","*.ant"),
                        ("All Files", "*.*")
                        ))
                        print(file_path)
                        if file_path != "":
                            with open(file_path, 'rb') as f:
                                data = pickle.load(f)
                                self.grid = data[0]
                                self.ants = data[1]
                                [ant.run(app=self) for ant in self.ants]
                    if i.key == pg.K_p and (not self.running):
                        self.graph(self.plot_pop,int(self.COLS*self.ROWS))
                if i.type == pg.MOUSEBUTTONDOWN:
                    self.create_mouse_ant()                   
            pg.display.flip()
            pg.display.set_caption(f'Langton Ant {len(self.ants)} ants, {self.iterations} iterations, running={self.running}, {self.ROWS}x{self.COLS}')
            self.clock.tick(60)


if __name__ == '__main__':
    app = App()
    app.run()