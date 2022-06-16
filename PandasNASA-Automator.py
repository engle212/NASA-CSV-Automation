import os
import pandas as pd
#pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

inDir = 'Input Files'
outDir = 'Output Files'
varList = ['humidity', 'radiation', 'windspeed']

if not os.path.exists(outDir):
    # create output directory
    os.mkdir(outDir)
    print('[output directory created]')

coords = pd.read_csv('locations_sub.csv', names=['Lat', 'Lon', 'Name'])
coords = coords.astype(str)
coords['latLon'] = coords[['Lat', 'Lon']].apply('_'.join, axis=1)

for var in varList:
    outFileName = 'NEW_' + var + '.csv'
    outFilePath = os.path.join(outDir, outFileName)

    # create outDF for current var
    outDF = pd.DataFrame()
    year = pd.Series(str)
    doy = pd.Series(str)
    date = pd.Series(str)

    outList = []

    if var == 'humidity':
        colName = 'RH2M'
    elif var == 'radiation':
        colName = 'TOA_SW_DWN'
    else:
        colName = 'WS2M'


    # create inDF for each input file
    for inFileName in os.listdir(inDir):
        outCur = pd.DataFrame()
        locName = ''

        inFilePath = os.path.join(inDir, inFileName)
        inDF = pd.read_csv(inFilePath, skiprows=11)

        lat = inFileName.split('_')[2]
        # Lat_Lon
        lon = inFileName.split('_')[4].split('.')[0] + '.' + inFileName.split('_')[4].split('.')[1]
        loc = '_'.join([lat, lon])

        if loc in coords:
            locName = names[coords.index(loc)] # Match lat_lon with location name
        else:
            locName = loc


        inDF.dropna(how="all", inplace=True) # Remove empty rows
        # read each input file into outCur

        #inDF.drop_duplicates(subset=['Name', 'Date'], inplace=True)
        inDF.reset_index(drop=True, inplace=True)

        year = inDF.iloc[:, 0]
        mo = inDF.iloc[:, 1]
        dy = inDF.iloc[:, 2]
        num = 0
        for y in year.drop_duplicates(inplace=False):
            num = num + 1
        print(doy)

        date = '-'.join([year, mo.rjust(2, '0'), dy.rjust(2, '0')])

        date = inDF.iloc[:, 2]

        column = pd.Series(inDF[colName]).to_frame()

        column.rename(columns={colName : locName}, inplace=True)
        outCur = pd.concat([outCur.reset_index(drop=True), column.reset_index(drop=True)], axis=1, ignore_index=False)

        outList.append(outCur)

    outList.insert(0, date.reset_index(drop=True))
    outList.insert(0, doy.reset_index(drop=True))
    outList.insert(0, year.reset_index(drop=True))



    outDF = pd.concat(outList, axis=1, ignore_index=False)
    print(outDF)
    # write outDF to CSV file
    outDF.to_csv(outFilePath, index=False)
