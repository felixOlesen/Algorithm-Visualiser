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

GRAPH_SIZE = (800, 800)
START = (400, 400)       # We'll assume X and Y are both this value
CIRCLE_SIZE = 5                # Both width and height will be this value

layout = [[sg.Graph(
            canvas_size=GRAPH_SIZE, graph_bottom_left=(0, 0), graph_top_right=GRAPH_SIZE,   # Define the graph area
            drag_submits=True,      # mouse move events
            enable_events=True,
            background_color='lightblue',
            key="-GRAPH-",
            pad=0)]]

window = sg.Window("Simple Circle Movement", layout, finalize=True, margins=(0,0))

class PSO:
    def __init__(self, PopSize=5, Gen=20, FitFunc="himmelblau"):
        # Initializing PSO params
        self.PopSize = PopSize
        self.Gen = Gen
        self.C1 = 2
        self.C2 = 2
        self.WMIN = 0.001
        self.WMAX = 1
        self.VMAX = 1
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
            ind_i = (random.uniform(self.X1MIN, self.X1MAX), random.uniform(self.X2MIN, self.X2MAX))
            self.Pop.append(ind_i)
            print(self.Pop)



    
        

'''
PSO PSEUDO CODE
HIGH LEVEL:
do
    for each particle
        calculate the objective of the particle
        update pbest if required
        update gbest if required
    end

    update inertia weight

    for each particle
        update the velocity (V)
        update the position (X)
    end
while end condition is not satisfied

LOW LEVEL:
for t=1 : maximum generation
    for i = 1 : population size
        if f(x_id(t)) < f(p_t(t)) then p_i(t) = x_id(t)
            f(p_g(t)) = min_t(f(p_t(t)))
        end
        for d = 1 : dimension
            v_id(t+1) = wv_id(t) + c1r1(p_i-x_id(t)) + c2r2(p_g - x_id(t))
            x_id(t+1) = x_id(t) + v_id(t+1)

            if v_id(t+1) > v_max then v_id(t+1) = v_max
            else if v_id(t+1) < v_max then v_id(t+1) = v_min
            end

            if x_id(t+1) > x_max then x_id(t+1) = x_max
            else if x_id(t+1) < x_min then x_id(t+1) = x_min
            end
        end
    end
end
'''

'''
TODO: 

PSO Functions:
- Initialize control params
- Initialize population of N particles
    - Individual(x1, x2)
    - pbest = update afer each individual update
    - gbest = update after every particle has been updated

'''

