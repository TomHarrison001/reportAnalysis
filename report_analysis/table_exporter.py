from reportlab.lib import colors
from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def Export(t, output_path):
    doc = SimpleDocTemplate('table.pdf', pagesize=letter)
    doc.build([t])
    renderPDF.drawToFile(doc, output_path + '\\table.pdf')


def CreateTable(D):
    data = [[' ', 'Response', 'Discretion', 'Intell.']]

    for key in ['NA', 'NC', 'NE', 'NH', 'NL', 'NN', 'NR', 'NS', 'NW']:
        record = [key]
        for i in range(3):
            record.append(FormatPercentage(D, key, i))
        data.append(record)

    t = Table(data, 5 * [0.9 * inch], 10 * [0.4 * inch])
    t.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
    # ('TEXTCOLOR', (1, 1), (-2, -2), colors.red),
    # ('VALIGN', (0, 0), (0, -1), 'TOP'),
    # ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
    # ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
    # ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
    # ('TEXTCOLOR', (0, -1), (-1, -1), colors.green),
    ('INNERGRID', (0, 0), (-1, -1), colors.black),
    ('BOX', (0, 0), (-1, -1), colors.black),
    ]))

    return t


def FormatPercentage(D, key, i):
    percentage = round((D[key][i]/sum(D[key]) * 100))
    return f'{D[key][i]} ({percentage}%)'
