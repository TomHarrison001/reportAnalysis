from reportlab.graphics.shapes import *
from reportlab.lib import colors
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics import renderPDF

def ExportDrawing(d, output_path):
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
    swatches = Legend()
    swatches.fontSize = 15
    swatches.alignment = 'left'
    swatches.x = 80
    swatches.y = 80
    swatches.columnMaximum = 3
    swatches.colorNamePairs = items
    d.add(swatches, 'legend')

    return d


def CreatePie(d, D, x, y, key):
    d.add(Rect(x, y, 200, 200, fillColor=colors.white))
    d.add(String(x+85, y-17, key, fontSize=18, fillColor=colors.black))
    pc = Pie()
    pc.x = x + 25
    pc.y = y + 25
    pc.width = 150
    pc.height = 150
    pc.data = D[key]
    perc = [round((x/sum(D[key]) * 100), 1) for x in D[key]]
    pc.labels = [str(perc[0]), str(perc[1]), str(perc[2])]
    pc.slices[0].fillColor = colors.lightgreen
    pc.slices[1].fillColor = colors.lightblue
    pc.slices[2].fillColor = colors.orangered
    d.add(pc)
