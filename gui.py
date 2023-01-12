import PySimpleGUI as sg

GRAPH_SIZE = (1000, 800)
START = (500, 400)       # We'll assume X and Y are both this value
SQ_SIZE = 40                # Both width and height will be this value

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



while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    print(event, values) if event != sg.TIMEOUT_EVENT else None # our normal debug print, but for this demo, don't spam output with timeouts


    if event == "-GRAPH-":  # if there's a "Graph" event, then it's a mouse movement. Move the square
        x, y = values["-GRAPH-"]        # get mouse position
        window["-GRAPH-"].relocate_figure(circle, x - SQ_SIZE // 2, y + SQ_SIZE // 2)   # Move using center of square to mouse pos
        window["-GRAPH-"].move_figure(other_circle, 1, 0)

window.close()