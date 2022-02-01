from black import out
from numpy import fmax
import pandas as pd
import datetime
import os
import re

outputFilePath = "output/{}.csv"

# Get the files names that have extension .input.csv
def getDataFiles():
    return [file for file in os.listdir('./') if re.match(r'.*\.input.csv$', file)]

# Merge the data from all file into a pd.DataFrame
def createDataFrame():
    dataFiles = getDataFiles()
    dataFrames = []

    for fileName in dataFiles:
        dataFrames.append(pd.read_csv(fileName))

    df = pd.concat(dataFrames, axis=0)
    df = df.rename(columns={'Unnamed: 0': ''})
    df = df.set_index(keys='')
    return df

def getTargetStations():
    targetStations = pd.read_csv('./stations.target.csv')
    targetStations = targetStations.set_index('Estaciones_Objetivo')
    return targetStations.index.tolist()

def setOutputDataFrame(date, stationsList, interval = 1339):
    columns = ['Interval_Start', 'Interval_End']
    columns.extend(stationsList)

    # 2020-01-01 16:47:21 UTC
    data = []

    countedMinutes = 0
    fm = interval % 60
    fh = int(interval / 60)
    hour = fh
    minutes = fm
    calculatedDate = datetime.datetime.fromisoformat(date).replace()

    while countedMinutes < 1440 - interval:
        row = [calculatedDate.isoformat()]
        calculatedDate = calculatedDate.replace(hour=hour, minute=minutes)
        row.append(calculatedDate.isoformat())
        row.extend([0 for i in range(len(stationsList))])

        hour += fh
        minutes += fm
        if minutes >= 60:
            hour += int(minutes / 60)
            minutes = minutes % 60

        countedMinutes += interval

        data.append(row)

    df = pd.DataFrame(columns=columns, data=data)

    return df

def main():
    df = createDataFrame()
    targetStations = getTargetStations()

    # Filter with only the stations we are interested in
    df = df[df['Estacion_Parada'].isin(targetStations)]

    # Get the dates
    dates = df.value_counts(subset=['Fecha_Clearing']).to_frame().reset_index()['Fecha_Clearing'].values

    for day in dates:
        outputDf = setOutputDataFrame(day, targetStations, 240)

        reg = df[df['Fecha_Clearing'] == day]

        # Count the data
        userStation = reg.value_counts(subset=['Numero_Tarjeta', 'Estacion_Parada'])
        userStation = userStation[userStation.values == 1].to_frame().reset_index()

        usersCount = reg.value_counts(subset=['Numero_Tarjeta'])
        usersCount = usersCount[usersCount.values == 2].to_frame().reset_index()

        reg = reg[reg['Numero_Tarjeta'].isin(userStation['Numero_Tarjeta'])]
        reg = reg[reg['Numero_Tarjeta'].isin(usersCount['Numero_Tarjeta'])]
        reg = reg.sort_values('Fecha_Transaccion')
        cards = reg['Numero_Tarjeta'].values

        for card in cards:
            user = reg[reg['Numero_Tarjeta'] == card]
            visitedStations = user['Estacion_Parada'].values
            if targetStations.index(visitedStations[0]) < targetStations.index(visitedStations[1]):
                user = user[user['Estacion_Parada'] == visitedStations[0]]
            else:
                user = user[user['Estacion_Parada'] == visitedStations[1]]

            date = user['Fecha_Transaccion'].values[0]
            date = date[0:len(date)-4]
            date = pd.to_datetime(date)

            row = (pd.to_datetime(outputDf['Interval_Start']) <= date) & (pd.to_datetime(outputDf['Interval_End']) > date)
            column = user['Estacion_Parada'].values[0]

            outputDf.loc[row, column] = outputDf[row][column] + 1

        outputDf.to_csv(outputFilePath.format(day))

main()
    