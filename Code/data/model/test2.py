import PySimpleGUI as sg

def output_window(results):
    orginstats = results
    orginstats = list(orginstats.items())
    layout_origin = [[x[0],x[1]] for x in orginstats]
    lay_origin = [[sg.Text(f'{x[0]}:{x[1]}')] for x in layout_origin]
    return(lay_origin)
    
dic = {'A':4,'B':5}
sg.theme('Green')
print(output_window(dic))
layout = output_window(dic)
print(type(layout))
window = sg.Window('test', layout)
while True:

    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        quit()
    elif 'Submit' in event:
        break
window.close()