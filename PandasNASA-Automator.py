import os
import pandas as pd
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
    doy = pd.DataFrame()
    date = pd.DataFrame()

    outList = []

    if var == 'humidity':
        colName = 'RH2M'
    elif var == 'radiation':
        colName = 'TOA_SW_DWN'
    else:
        colName = 'WS2M'

    first = True
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

        # only populate DOY if on the first file (avoids duplicates)
        if first:
            for y in year.drop_duplicates(inplace=False):
                # get number of times y appears in year
                # create list with range going to number
                rangeList = pd.Series(range(1, len(year.loc[year == y]) + 1))
                doy = pd.concat([doy.reset_index(drop=True), rangeList.reset_index(drop=True)], axis=0, ignore_index=False)
            doy.rename(columns={doy.columns[0] : 'DOY'}, inplace=True)

        # assemble Date column from year, month, and day columns
        date['Date'] = year.astype(str) + '-' + mo.astype(str) + '-' + dy.astype(str)

        column = pd.Series(inDF[colName]).to_frame()
        column.rename(columns={colName : locName}, inplace=True)

        # add column onto outCur
        outCur = pd.concat([outCur.reset_index(drop=True), column.reset_index(drop=True)], axis=1, ignore_index=False)

        # add outCur to list
        outList.append(outCur)
        first = False

    # add date info in before location column data
    outList.insert(0, date.reset_index(drop=True))
    outList.insert(0, doy.reset_index(drop=True))
    outList.insert(0, year.reset_index(drop=True))

    outDF = pd.concat(outList, axis=1, ignore_index=False)
    # write outDF to CSV file
    outDF.to_csv(outFilePath, index=False)
