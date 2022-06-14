import csv
import os

inDir = 'Input Files'
outDir = 'Output Files'
varList = ['humidity', 'radiation', 'windspeed']

coords = []
names = []

with open('locations_sub.csv', 'r', newline='') as locFile:
    locReader = csv.reader(locFile)

    for location in locReader:
        coords.append('_'.join([location[0], location[1]])) # Lat_Lon
        names.append(location[2])



if not os.path.exists(outDir):
    # create output directory
    os.mkdir(outDir)
    print('[output directory created]')

for var in varList:
    # create/open and populate respective file

    outFileName = 'NEW_' + var + '.csv'
    outFilePath = os.path.join(outDir, outFileName)

    # list stores data across input files to be put into output file
    list = [['YEAR', 'DOY', 'Date']]
    list.extend([[], [], []])

    # open current file
    with open(outFilePath, 'w', newline='') as outFile:
        outWriter = csv.writer(outFile)

        print('-------------------------------------------------')
        print(var + ' csv output: [in progress]')


        # iterate through input files (located in 'Input Files' folder)
        for inFileName in os.listdir(inDir):
            inFilePath = os.path.join(inDir, inFileName)


            lat = inFileName.split('_')[2]
            # Lat_Lon
            lon = inFileName.split('_')[4].split('.')[0] + '.' + inFileName.split('_')[4].split('.')[1]
            loc = '_'.join([lat, lon])

            if loc in coords:
                locName = names[coords.index(loc)] # Match lat_lon with location name
            else:
                locName = loc

            print(locName + ' csv input: [in progress]')

            with open(inFilePath, 'r', newline='') as inFile:
                inReader = csv.reader(inFile)

                # skip 12 rows to get to data
                for n in range(12):
                    next(inReader)

                col = varList.index(var) + 3 # column where info is stored
                doy = 1
                outCol = 4 # column where data is to be outputted

                # load contents of file into data list
                for row in inReader:
                    # check if row is blank
                    if row:
                        # take contents of each row and add to list
                        #name = str(row[0]) + str(" ph")
                        #date = row[4]
                        year = str(row[0]) # year
                        mo = str(row[1]) # month
                        dy = str(row[2]) # day
                        data = str(row[col]) # data

                        # create date, add 0 if single digit
                        date = '-'.join([year, mo.rjust(2, '0'), dy.rjust(2, '0')])

                        # check if a new location column needs to be created
                        if locName not in list[0]:
                            # add new column
                            list[0].append(locName)
                            list.append([])

                        # check if new year is started to reset DOY
                        if year not in list[1]:
                            doy = 1 # reset DOY

                        # check if date has already been added
                        if date not in list[3]:
                            # add row of date info if not added
                            list[1].append(year)
                            list[2].append(doy)
                            list[3].append(date)

                        outCol = list[0].index(locName) + 1 # set column to output

                        # check if data has already been added
                        if not ((date in list[3]) and (len(list[outCol]) >= len(list[3]))):
                            list[outCol].append(str(data)) # extract data into list

                        doy += 1 # increment DOY
            print(locName + ' csv input: [complete]')
            print('')
        numOfColumns = len(list[0])
        numOfRows = len(list[1])

        outWriter.writerow(list[0]) # write header row to output file

        # iterate through data and write to output file row-by-row
        for i in range(numOfRows):
            rowList = []
            for j in range(1, numOfColumns + 1):
                rowList.append(list[j][i])
            outWriter.writerow(rowList)

        print(var + ' csv output: [complete]')
