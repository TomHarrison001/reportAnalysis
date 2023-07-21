from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def ExportTable(table, output_path):
    doc = SimpleDocTemplate(output_path + '\\table.pdf', pagesize=letter)
    elements = []
    elements.append(table)
    doc.build(elements)


def CreateTable(data):
    records = [[' ', 'Response', 'Discretion', 'Intell.']]

    for key in ['NA', 'NC', 'NE', 'NH', 'NL', 'NN', 'NR', 'NS', 'NW']:
        record = [key]
        for i in range(3):
            record.append(FormatPercentage(data, key, i))
        records.append(record)

    table = Table(records, 5 * [0.9 * inch], 10 * [0.4 * inch])
    table.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
    # ('TEXTCOLOR', (1, 1), (-2, -2), colors.red),
    # ('VALIGN', (0, 0), (0, -1), 'TOP'),
    # ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
    # ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
    # ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
    # ('TEXTCOLOR', (0, -1), (-1, -1), colors.green),
    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))

    return table


def FormatPercentage(data, key, i):
    percentage = round((data[key][i]/sum(data[key]) * 100), 1)
    return f'{data[key][i]} ({percentage}%)'
