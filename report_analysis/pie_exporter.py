from reportlab.graphics.shapes import *
from reportlab.lib import colors
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics import renderPDF

def Export(d, output_path):
    renderPDF.drawToFile(d, output_path + '\\pies.pdf', '')


def CreateDrawing(x, y, D):
    d = Drawing(x, y)
    keys = ['NA', 'NC', 'NE', 'NH', 'NL', 'NN', 'NR', 'NS', 'NW']
    for i in range(3):
        for j in range(3):
            CreatePie(d, D, 75 + 225 * j, 575 - 225 * i, keys[3 * i + j])
    
    items = [(colors.lightblue, 'Incident Response'),
             (colors.lightgreen, 'Officer Discretion'),
             (colors.orangered, 'Intelligence Led')]
    swatches = Legend(fontSize=15, alignment='left', x=80, y=80,
                      columnMaximum=3, colorNamePairs=items)
    d.add(swatches, 'legend')

    return d


def CreatePie(d, D, x, y, key):
    d.add(Rect(x, y, 200, 200, fillColor=colors.white))
    pc = Pie(x=x+25, y=y+25, width=150, height=150, data=D)
    
    perc = [round((x/sum(D[key]) * 100), 1) for x in D]
    pc.slices[0].fillColor = colors.lightgreen
    pc.slices[1].fillColor = colors.lightblue
    pc.slices[2].fillColor = colors.orangered
    d.add(pc)
    d.add(String(x+85, y-17, key, fontSize=18, fillColor=colors.black))
