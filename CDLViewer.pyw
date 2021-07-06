import PySimpleGUI as sg
import math
import numpy as np
import matplotlib.pyplot as plt
import LDTtoList

def Plotar(arquivo, titulo, legenda):
    LDT = LDTtoList.LDT(arquivo)
    maximo = math.ceil(max(LDT.LumInt[0])/100)*100
    Planes = len(LDT.LumInt)
    theta = list(np.radians(range(0,180+5,5)))
    r1 = LDT.LumInt[0][:0:-1]+LDT.LumInt[0]
    r2 = LDT.LumInt[Planes-1][:0:-1]+LDT.LumInt[Planes-1]

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.plot(theta, r1, 'r--')
    ax.plot(theta, r2, 'b')
    ax.set_theta_zero_location('W')
    ax.set_thetagrids(range(0,360,15))
    #ax.set_rticks(list(range(100,maximo,100))) # [100, 200, 300, 400, 500])
    labels = ["{0}°".format(x) for x in np.abs(range(-90,180+90,15))]
    ax.set_xticklabels(labels)
    #ax.set_rmax(300)
    ax.set_rlabel_position(30)  # Move radial labels away from plotted line
    #ax.set_thetamin(0)
    ax.set_thetamax(180)
    ax.fill_between(theta, 0, r1, alpha=0.2, color='y')
    ax.fill_between(theta, 0, r2, alpha=0.2, color='y')
    ax.grid(True)
    ax.text(1, 0.75, 'cd/klm',
            horizontalalignment='right',
            verticalalignment='bottom',
            transform=ax.transAxes)

    if titulo: ax.set_title(LDT.LumName)
    if legenda: plt.legend(["C0 - C180", "C90 - C270"])
    plt.show()


layout = [[sg.T("")], [sg.Text("Selecione um arquivo: "), sg.Input(key="File", size=(80,None)), sg.FileBrowse('...',file_types=(("LDT Files", "*.ldt"),))],
          [sg.Checkbox("Exibir título", True, key="Titulo")],
          [sg.Checkbox("Exibir legenda", True, key="Legenda")],
          [sg.Button("Plotar")]]
###Building Window
window = sg.Window('CDL Viewer', layout, size=(800,180))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event == "Plotar":
        arquivo = values["File"]
        print(arquivo)
        Plotar(arquivo, values["Titulo"], values["Legenda"])