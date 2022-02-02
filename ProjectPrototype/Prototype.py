import pandas as pd
import datetime
import os

outputFilePath = "output/{}.csv"

# Merge the data from all file into a pd.DataFrame
def createDataFrame():
    dataFrames = []

    for fileName in os.listdir('./input'):
        df = pd.read_csv('./input/{}'.format(fileName))
        df = df.drop(columns=[
            'Acceso_Estacion',
            'Day_Group_Type',
            'Dispositivo',
            'Emisor',
            'Fase',
            'Hora_Pico_SN',
            'Linea',
            'Nombre_Perfil',
            'Operador',
            'Saldo_Despues_Transaccion',
            'Saldo_Previo_a_Transaccion',
            'Tipo_Tarifa',
            'Tipo_Tarjeta',
            'Valor',
            'ID_Vehiculo',
            'Ruta',
            'Tipo_Vehiculo',
            'Sistema'
        ])
        dataFrames.append(df)

    df = pd.concat(dataFrames, axis=0)
    return df

def getTargetStations():
    targetStations = pd.read_csv('./stations.target.csv')
    targetStations = targetStations.set_index('Estaciones_Objetivo')
    return targetStations.index.tolist()

def setOutputDataFrame(date, stationsList, interval = 1440):
    columns = ['Interval_Start', 'Interval_End']
    columns.extend(stationsList)

    # 2020-01-01 16:47:21 UTC
    data = []

    countedMinutes = 0
    fm = interval % 60
    fh = int(interval / 60)
    hour = fh
    minutes = fm
    calculatedDate = datetime.datetime.fromisoformat(date)
    day = calculatedDate.day

    while countedMinutes <= 1440 - interval:
        row = [calculatedDate.isoformat()]
        calculatedDate = calculatedDate.replace(day=day, hour=hour, minute=minutes)
        row.append(calculatedDate.isoformat())
        row.extend([0 for i in range(len(stationsList))])

        hour += fh
        minutes += fm
        if minutes >= 60:
            hour += int(minutes / 60)
            minutes = minutes % 60
        if hour >= 24:
            hour = hour % 24
            day += 1

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
        outputDf = setOutputDataFrame(day, targetStations, 15)

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