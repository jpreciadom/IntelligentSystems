import pandas as pd
import os
import re

def getDataFiles():
    return [file for file in os.listdir('./') if re.match(r'.*\.fullinput.csv$', file)]

def main():
    dataFiles = getDataFiles()
    for index, fileName in enumerate(dataFiles):
        df = pd.read_csv(fileName)
        df.to_csv("dataset{}.input.csv".format(index + 1), columns=['Estacion_Parada', 'Fecha_Clearing', 'Fecha_Transaccion', 'Numero_Tarjeta'])

main()