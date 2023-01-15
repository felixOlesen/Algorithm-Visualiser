import PySimpleGUI as sg
import numpy as np

GRAPH_SIZE = (1000, 900)
START = (500, 400)       # We'll assume X and Y are both this value
SQ_SIZE = 5                # Both width and height will be this value

# McCormick Function 
# Global Minimum at: x1 = -0.54719, x2 = -1.54719
# 

def MccormickFunc(x1, x2):
    result = np.sin(x1+x2)+((x1-x2)**2)-(1.5*x1)+(2.5*x2)+1
    return result

print(MccormickFunc(-0.54719,-1.54719))

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
    def __init__(self, P=20, G=100):
        '''Initialising the algorithm visualiser'''
        self.P = P
        self.G = G

'''
PSO PSEUDO CODE
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
Fitness Functions:
Beale Function
Himmelblau's Function
McCormick Function
'''

