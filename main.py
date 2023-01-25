#Exemple de traitement de données laboratoire
import pandas as pd
import os
import glob
import datetime


directory = os.path.dirname(os.path.abspath(__file__)) + "\0-raw data"
path = "C:/Users/yoann.skoczek/PycharmProjects/PODF_Example/0-raw data/"
files = glob.glob(os.path.join(path,"*.txt"))

for file_name in files:
    var_date = os.path.basename(file_name)[os.path.basename(file_name).find("_____") + 5:]
    var_date = datetime.datetime(int("20"+var_date[0:2]),int(var_date[2:4]),int(var_date[4:6]),int(var_date[6:8]),int(var_date[8:10]))
    output = pd.read_csv(file_name, sep="\t", decimal=",")
    output.shape
    output['Projet'] = os.path.basename(file_name)[0:os.path.basename(file_name).find("_")]
    output['OneLab'] = os.path.basename(file_name)[os.path.basename(file_name).find("_") + 1:os.path.basename(file_name).find("__")]
    output['Methode'] = os.path.basename(file_name)[os.path.basename(file_name).find("__") + 2:os.path.basename(file_name).find("___")]
    output['Echantillon'] = os.path.basename(file_name)[os.path.basename(file_name).find("___") + 3:os.path.basename(file_name).find("____")]
    output['CT'] = os.path.basename(file_name)[os.path.basename(file_name).find("____") + 4:os.path.basename(file_name).find("_____")]
    output['Niveau'] = 0
    output.rename(columns={'Date': 'Duree'}, inplace=True)
    output.rename(columns = {'Résistance':'Resistance'}, inplace = True)
    output['Date'] = var_date

    for new_itr, select_row in output.iterrows():
        # Application de l'offset de 'Volume'; création de la colonne de 'Duree'
        if new_itr == 0:
            offset = float(select_row['Volume'])
            output.at[new_itr, 'Volume'] = float(select_row['Volume']) - offset
            offset2 = float(select_row['Duree'])
            output.at[new_itr, 'Duree'] = float(select_row['Duree']) - offset2
        else:
            output.at[new_itr, 'Volume'] = float(select_row['Volume']) - offset
            output.at[new_itr, 'Duree'] = float(select_row['Duree']) - offset2

        # Détermination du sens de l'essai
        if new_itr == 0:
            output.at[new_itr, 'Niveau'] = "Jaugeage"
            vol_lastitr = float(select_row['Volume'])
            niv_lastitr = "Jaugeage"
        else:
            if float(select_row['Volume']) > vol_lastitr:
                output.at[new_itr, 'Niveau'] = "Jaugeage"
                niv_lastitr = "Jaugeage"
            elif float(select_row['Volume']) < vol_lastitr:
                output.at[new_itr, 'Niveau'] = "Dejaugeage"
                niv_lastitr = "Dejaugeage"
            else:
                output.at[new_itr, 'Niveau'] = niv_lastitr
            vol_lastitr = float(select_row['Volume'])

    output.to_csv(file_name.replace(".txt","_consolidated.csv").replace("0-raw data","1-consolidated data"),"\t", decimal=",")