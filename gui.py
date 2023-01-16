import PySimpleGUI as sg
import numpy as np
import random

GRAPH_SIZE = (1000, 900)
START = (450, 450)       # We'll assume X and Y are both this value
SQ_SIZE = 5                # Both width and height will be this value

# McCormick Function 
# Global Minimum at: x1 = -0.54719, x2 = -1.54719
# Bounded in range: x1 ∈ [-1.5, 4], x2 ∈ [-3, 4]

def MccormickFunc(x1, x2):
    return np.sin(x1+x2)+((x1-x2)**2)-(1.5*x1)+(2.5*x2)+1


# Beale Function 
# Global Minimum at: x1 = 3, x2 = 0.5
# Bounded in range: x1 ∈ [-4.5, 4.5], x2 ∈ [-4.5, 4.5]

def BealeFunc(x1, x2):
    return (1.5 - x1 + x1*x2)**2 + (2.25 - x1 + x1*x2**2)**2 + (2.625 - x1 + x1*x2**3)**2


# Himmelblau's Function 
# Global Minima at: 
# x1 = 3, x2 = 2
# x1 = -2.805118, x2 = 3.131312
# x1 = -3.779310, x2 = -3.283186
# x1 = 3.584428, x2 = -1.848126
# Bounded in range: x1 ∈ [-5, 5], x2 ∈ [-5, 5]

def HimmelblauFunc(x1, x2):
    return (x1**2 + x2 - 11)**2 + (x1 + x2**2 - 7)**2


def CalcFitness(x1, x2, fitFunc):
        fitness = 0
        if fitFunc == "himmelblau":
            fitness = HimmelblauFunc(x1, x2)
        elif fitFunc == "beale":
            fitness = BealeFunc(x1, x2)
        elif fitFunc == "mccormick":
            fitness = MccormickFunc(x1, x2)
        return fitness

class PSO:
    def __init__(self, PopSize=10, Gen=50, FitFunc="beale"):
        # Initializing PSO params
        self.PopSize = PopSize
        self.Gen = Gen
        self.C1 = 0.3
        self.C2 = 0.6
        self.WMIN = 0.001
        self.WMAX = 0.5
        self.VMAX = 2
        self.VMIN = -2
        self.V_INITIAL = 0.01
        self.Pop = list()
        self.FitFunc = FitFunc

        if FitFunc == "himmelblau":
            self.X1MIN = -4.5
            self.X1MAX = 4.5
            self.X2MIN = -4.5
            self.X2MAX = 4.5
        elif FitFunc == "beale":
            self.X1MIN = -5
            self.X1MAX = 5
            self.X2MIN = -5
            self.X2MAX = 5
        elif FitFunc == "mccormick":
            self.X1MIN = -1.5
            self.X1MAX = 4
            self.X2MIN = -3
            self.X2MAX = 4
        

    def PopulateSpace(self):
        for i in range(self.PopSize):
            ind_i = np.array([random.uniform(self.X1MIN, self.X1MAX), random.uniform(self.X2MIN, self.X2MAX), self.V_INITIAL, self.V_INITIAL])
            self.Pop.append(ind_i)
        print(self.Pop)
    
    def UpdateParticle(self, ind, pbest, gbest):
        # ind = nparray(x1, x2, v1, v2)
        # r1, r2 = random numbers in range [0,1]
        # old_vi = old velocity for decision var i after weights appplied
        # personal = persona1 best vector after weights applied
        # glob = global best vector after weights applied
        # new_vi = new velocity for decision var i
        for i in range(2):
            r1 = random.random()
            r2 = random.random()
            old_vi = self.WMAX * ind[i+2]
            personal = self.C1 * r1 * (pbest[i] - ind[i])
            glob = self.C2 * r2 * (gbest[i] - ind[i])
            new_vi = old_vi + personal + glob

            #if new_vi < self.VMIN:
            #    new_vi = self.VMIN
            #elif new_vi > self.VMAX:
            #    new_vi = self.VMAX
            ind[i+2] = new_vi

            new_pos = ind[i] + new_vi
            if i == 0 and new_pos < self.X1MIN:
                new_pos = self.X1MIN
            elif i == 0 and new_pos > self.X1MAX:
                new_pos = self.X1MAX
            elif i == 1 and new_pos < self.X2MIN:
                new_pos = self.X2MIN
            elif i == 1 and new_pos > self.X2MAX:
                new_pos = self.X2MAX
            ind[i] = new_pos

        return ind

    def PSOLoop(self):
        gbest = np.array([0,0,0,0])
        for gen in range(self.Gen):
            
            particle_index = 0
            for part in self.Pop:

                part_fitness = CalcFitness(part[0], part[1], self.FitFunc)
                

                if gen == 0:
                    pbest = part
                elif part_fitness < CalcFitness(pbest[0], pbest[1], self.FitFunc):
                    pbest = part
                
                if gen == 0 and particle_index == 0:
                    gbest = part
                elif part_fitness < CalcFitness(gbest[0], gbest[1], self.FitFunc):
                    gbest = part

                self.Pop[particle_index] = self.UpdateParticle(part, pbest, gbest)
                particle_index += 1

            print("Current global best position: (X1: ",gbest[0], " X2: ", gbest[1])
            print("Global Best Fitness: ", CalcFitness(pbest[0], pbest[1], self.FitFunc))


pso = PSO()
pso.PopulateSpace()
pso.PSOLoop()

'''
TODO: 
GUI Stuff
- Set the center of the graph
- Draw the circles for each individual
- Draw circle for global minima
- Update position with velocity or position of particles from update function
'''

layout = [[sg.Graph(
            canvas_size=GRAPH_SIZE, graph_bottom_left=(0, 0), graph_top_right=GRAPH_SIZE,   # Define the graph area
            drag_submits=True,      # mouse move events
            enable_events=True,
            background_color='lightblue',
            key="-GRAPH-",
            pad=0)]]

window = sg.Window("Simple Circle Movement", layout, finalize=True, margins=(0,0))

# draw the square we'll move around
#square = window["-GRAPH-"].draw_rectangle(START, (START[0]+SQ_SIZE, START[1]+SQ_SIZE), fill_color='black')
circle = window["-GRAPH-"].draw_circle(START,
    SQ_SIZE,
    fill_color = "green",
    line_color = "green",
    line_width = 1)
other_circle = window["-GRAPH-"].draw_circle(START,
    SQ_SIZE,
    fill_color = "red",
    line_color = "red",
    line_width = 1)

for i in range(300):
    window["-GRAPH-"].move_figure(other_circle, 1, 0)

delay_boi = 1000
while True:
    event, values = window.read(timeout=delay_boi)
    if event == sg.WIN_CLOSED:
        break
    #print(event, values) if event != sg.TIMEOUT_EVENT else None # our normal debug print, but for this demo, don't spam output with timeouts
    window["-GRAPH-"].move_figure(other_circle, 1, 0)

    #if event == "-GRAPH-":  # if there's a "Graph" event, then it's a mouse movement. Move the square
    #    x, y = values["-GRAPH-"]        # get mouse position
    #    window["-GRAPH-"].relocate_figure(circle, x - SQ_SIZE // 2, y + SQ_SIZE // 2)   # Move using center of square to mouse pos
    #    window["-GRAPH-"].move_figure(other_circle, 1, 0)

window.close()