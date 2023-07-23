"""This is the main command line interface"""

from txt_parser import ExtractData
from pie_exporter import CreateDrawing, ExportDrawing
from table_exporter import CreateTable, ExportTable

def main(import_file, sheet_name, output_path, conf=None):
    data = ExtractData(import_file, sheet_name)
    drawing = CreateDrawing(800, 900, data)
    ExportDrawing(drawing, output_path)

    table = CreateTable(data)
    ExportTable(table, output_path)

    # def f(x):
    #     return {
    #         'incident response': 0,
    #         'officer discretion': 1,
    #         'intelligence-led': 2,
    #     }[x]

def api():
    import_file = 'C:\\users\\tomha\\Documents\\Work\\Work 4\\full.xlsx'
    output_path = 'C:\\users\\tomha\\Documents\\Work\\Work 4\\output'
    sheet_name = 'sheet1'
    main(import_file, sheet_name, output_path)

if __name__ == '__main__':
    api()
