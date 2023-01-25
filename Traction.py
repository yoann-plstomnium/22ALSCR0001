#Exemple de traitement de données laboratoire
import pandas
import pandas as pd
import os
import glob
import datetime
from openpyxl import load_workbook
import xlrd
from tkinter import *

root = Tk()
root.geometry('200x200')
InputStrings = StringVar()
Entry(root, textvariable=InputStrings).pack()

def GetString():
    root.title(os.path.basename(file_name))
    print(InputStrings.get())
    Button(root, text='Fill your name; then click on me', command=OutputText).pack()
    root.mainloop()

def OutputText():
    global OutString
    OutString = InputStrings.get()
    root.withdraw()
    root.quit()

class IHM(Frame):
    def __init__(self, fenetre, height, width):
        Frame.__init__(self, fenetre)
        self.numberLines = height
        self.numberColumns = width
        self.pack(fill=BOTH)
        self.data = list()
        for i in range(self.numberLines):
            line = list()
            for j in range(self.numberColumns):
                cell = Entry(self)
                cell.insert(0, 0)
                line.append(cell)
                cell.grid(row=i, column=j)
            self.data.append(line)

        self.results = list()
        for i in range(self.numberColumns):
            cell = Entry(self)
            cell.insert(0, 0)
            cell.grid(row=self.numberLines, column=i)
            self.results.append(cell)
        self.buttonSum = Button(self, text="somme des colonnes", fg="red", command=self.sumCol)
        self.buttonSum.grid(row=self.numberLines, column=self.numberColumns)

    def sumCol(self):
        for j in range(self.numberColumns):
            result = int(0)
            for i in range(self.numberLines):
                result += int(self.data[i][j].get())
            self.results[j].delete(0, END)
            self.results[j].insert(0, result)

directory = os.path.dirname(os.path.abspath(__file__)) + "\0-raw data"
path = "C:/Users/yoann.skoczek/PycharmProjects/PODF_Example/0-raw data/"
files = glob.glob(os.path.join(path,"*.xls"))

for file_name in files:
#    GetString()
    #name_of_technician = OutString
    #interface = IHM(root,6,5)
    #interface.mainloop()
    workbook = xlrd.open_workbook(file_name)
    worksheets = workbook.sheets()
    for sht in worksheets:
        if not sht.name in ['Paramètres','Résultats','Statistiques']:
            df = pandas.read_excel(workbook,sheet_name=sht.name)
            df.shape
            sample = df.columns[0]
            df['Echantillon'] = sample
            df.rename(columns={df.columns[0]: 'Allongement'}, inplace=True)
            df.rename(columns={df.columns[1]: 'Force'}, inplace=True)
            df = df.drop(labels=[0,1],axis=0)
            df['Techncien'] = name_of_technician
            df.to_csv(file_name.replace(".xls", sample + "_consolidated.csv").replace("0-raw data", "1-consolidated data"), "\t",decimal=",")



