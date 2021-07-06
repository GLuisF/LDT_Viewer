import PySimpleGUI as sg
import math
import numpy as np
import matplotlib.pyplot as plt
import LDTtoList
# Note the matplot tk canvas import
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import os

def Plotar(arquivo, titulo, legenda, eficiencia):
    ldt = LDTtoList.ldt(arquivo)
    # maximo = math.ceil(max(ldt.LumInt[0])/100)*100
    Planes = len(ldt.LumInt)
    theta = list(np.radians(range(0,180+5,5)))
    if ldt.Isym == 3:
        r1 = ldt.LumInt[int((Planes+1)/2-1)][:0:-1]+ldt.LumInt[int((Planes+1)/2-1)]
        r2 = ldt.LumInt[0][:0:-1]+ldt.LumInt[Planes-1]
    else:
        r1 = ldt.LumInt[0][:0:-1]+ldt.LumInt[0]
        r2 = ldt.LumInt[Planes-1][:0:-1]+ldt.LumInt[Planes-1]

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.plot(theta, r1, 'r--', label="C0 - C180")
    ax.plot(theta, r2, 'b', label = "C90 - C270")
    ax.set_theta_zero_location('W')
    ax.set_thetagrids(range(0,360,15))
    #ax.set_rticks(list(range(100,maximo,100))) # [100, 200, 300, 400, 500])
    labels = ["{0}°".format(x) for x in np.abs(range(-90,180+90,15))]
    ax.set_xticklabels(labels)
    #ax.set_rmax(300)
    #ax.set_rlabel_position(90)  # Move radial labels away from plotted line
    #ax.set_thetamin(0)
    ax.set_thetamax(180)
    ax.fill_between(theta, 0, r1, alpha=0.2, color='y')
    ax.fill_between(theta, 0, r2, alpha=0.2, color='y')
    ax.grid(True)
    ax.text(1, 0.75, 'cd/klm',
            horizontalalignment='right',
            verticalalignment='bottom',
            transform=ax.transAxes)
    if eficiencia: ax.text(0.1, 0.25, f'η={round(ldt.lorl)}%',
            horizontalalignment='right',
            verticalalignment='bottom',
            transform=ax.transAxes)
    if titulo: ax.set_title(ldt.LumName)
    if legenda: plt.legend(loc = "lower right")
    plt.show()
    return fig

caminho = '' # "C:\Cloud\Desenvolvimento\Onno\Ensaios fotométricos\Avena\Transparente.ldt"
layout = [[sg.T("")], [sg.Text("Selecione um arquivo: "), sg.Input(caminho,key="File", size=(75,None)), sg.FileBrowse('...',file_types=(("ldt Files", "*.ldt"),))],
          [sg.Checkbox("Exibir título", True, key="Titulo")],
          [sg.Checkbox("Exibir legenda", True, key="Legenda")],
          [sg.Checkbox("Exibir eficiência", True, key="Eficiencia")],
          [sg.Button("Plotar")],
          [sg.Canvas(key='-CANVAS-')]]
###Building Window
window = sg.Window('CDL Viewer', layout, size=(750,200),icon='icon.ico')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event == "Plotar":
        if values['File'] != '':
            arquivo = values["File"]
            print(arquivo)
            figure = Plotar(arquivo, values["Titulo"], values["Legenda"], values["Eficiencia"])
            #figure_canvas_agg = FigureCanvasTkAgg(figure, window['-CANVAS-'].TKCanvas)
            #figure_canvas_agg.draw()
            #figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)