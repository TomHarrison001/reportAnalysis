"""This is the main command line interface"""

from configparser import ConfigParser
from pathlib import Path
from argparse import ArgumentParser

from txt_parser import ExtractData
from pie_exporter import CreateDrawing, Export as PieExport
from table_exporter import CreateTable, Export as TableExport

def main(import_file, sheet_name, output_path, conf=None):
    D = ExtractData(import_file, sheet_name)
    d = CreateDrawing(800, 900, D)
    PieExport(d, output_path)

    t = CreateTable(D)
    TableExport(t, output_path)

    # def f(x):
    #     return {
    #         'incident response': 0,
    #         'officer discretion': 1,
    #         'intelligence-led': 2,
    #     }[x]

    # def createMultiLab(df):
    #     labs = []
    #     # !Initiated = officer responding (0)
    #     # Initiated and !Intel = officer discretion (1)
    #     # Initiated and Intel = intelligence led (2)
    #     for index, row in df.iterrows():
    #         if row['Initiated'] == 0:
    #             lab = 0
    #         elif row['Intell'] == 0:
    #             lab = 1
    #         else:
    #             lab = 2
    #         labs.append(lab)
    #     df['multi'] = labs
    #     return df

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
