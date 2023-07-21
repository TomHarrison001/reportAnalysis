"""This is the main command line interface"""

from pathlib import Path

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
    # import file will be terminal arg
    import_file = 'C:\\users\\tomha\\Documents\\Work\\Work 4\\import\\full.xlsx'
    # sheet_name will be terminal arg
    sheet_name = 'Sheet1'
    # output_path will be terminal arg
    output_path = 'C:\\users\\tomha\\Documents\\Work\\Work 4\\output'
    main(import_file, sheet_name, output_path)

if __name__ == '__main__':
    api()
