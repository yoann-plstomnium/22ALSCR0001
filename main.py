#Exemple de traitement de données laboratoire
import pandas
import pandas as pd
import numpy as np
import csv
import os
import glob
import datetime
import matplotlib.pyplot as plt


directory = os.path.dirname(os.path.abspath(__file__)) + "\raw data"
path = "C:/Users/yoann.skoczek/PycharmProjects/PODF_Example/raw data/"
files = glob.glob(os.path.join(path,"*.txt"))
for file_name in files:
    #print(os.path.basename(file_name).find("_"))
    var_date = os.path.basename(file_name)[os.path.basename(file_name).find("____") + 4:]
    var_date = datetime.datetime(int("20"+var_date[0:2]),int(var_date[2:4]),int(var_date[4:6]),int(var_date[6:8]),int(var_date[8:10]))
    output = pd.read_csv(file_name, sep="\t", decimal=",")
    output.shape
    output['Projet'] = os.path.basename(file_name)[0:os.path.basename(file_name).find("_")]
    output['OneLab'] = os.path.basename(file_name)[os.path.basename(file_name).find("_") + 1:os.path.basename(file_name).find("__")]
    output['Methode'] = os.path.basename(file_name)[os.path.basename(file_name).find("__") + 2:os.path.basename(file_name).find("___")]
    output['Echantillon'] = os.path.basename(file_name)[os.path.basename(file_name).find("___") + 3:os.path.basename(file_name).find("____")]
    output['CT'] = "Compiegne"
    output['Niveau'] = 0
    output.rename(columns={'Date': 'Duree'}, inplace=True)
    output.rename(columns = {'Résistance':'Resistance'}, inplace = True)
    output['Date'] = var_date

    for new_itr, select_row in output.iterrows():
        if new_itr == 0:
            offset = float(select_row['Volume'])
            output.at[new_itr, 'Volume'] = float(select_row['Volume']) - offset
            offset2 = float(select_row['Duree'])
            output.at[new_itr, 'Duree'] = float(select_row['Duree']) - offset2
        else:
            output.at[new_itr, 'Volume'] = float(select_row['Volume']) - offset
            output.at[new_itr, 'Duree'] = float(select_row['Duree']) - offset2

        if float(select_row['Resistance']) > 350:
            output.at[new_itr, 'Niveau'] = "Reservoir vide"
        elif float(select_row['Resistance']) < 50:
            output.at[new_itr, 'Niveau'] = "Reservoir plein"
        else:
            output.at[new_itr, 'Niveau'] = "En cours de remplissage"

    output.to_csv(file_name.replace(".txt","_consolidated.csv"),"\t", decimal=",")