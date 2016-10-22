import quandl
import logging

from directoryManipulator import DirectoryManipulator
from datetime import date
from dateutil.parser import parse


# QuandlAdapter class is responsible for all interactions with Quandl data services.
class QuandlAdapter:

    def __init__(self, quandlKeyFileName):

        self.registerKeyWithQuandl(self.retrieveKeyFromFile(quandlKeyFileName))


    def retrieveKeyFromFile(self, quandlKeyFileName):

        try:
            quandlFile = open(quandlKeyFileName, 'r')
        except IOError:
            logging.error('[QuandlAdapter]: Error retrieving Quandl API key from file ' + quandlKeyFileName +
                              '. Please specify correct file name.')
            quit()

        quandlKey = quandlFile.read()

        try:
            quandlFile.close()
        except IOError:
            logging.error('[QuandlAdapter]: Error could not close Quandl key file.')

        return quandlKey

    def registerKeyWithQuandl(self, quandlKey):

        quandl.ApiConfig.api_key = quandlKey

    def retrieveTrainingData(self, databaseName, datasetTickers, startDate, endDate):

        dataSetCollection ={}

        # Create folders for each of the specified stock tickers.
        directoryManipulator = DirectoryManipulator()
        directoryManipulator.makeStockFoldersAndTextFiles(datasetTickers)

        for datasetTicker in datasetTickers:
            datasetQueryName = databaseName+'/'+datasetTicker
            paramCollection = self.createParamDefinition(startDate, endDate)
            dataset = quandl.Dataset(datasetQueryName).data(params=paramCollection).to_pandas()

            if not dataset.empty:
                dataSetCollection.update({datasetTicker: dataset})
                directoryManipulator.editStockTrainingTextFile(datasetTicker, "Training data available between "+startDate+" and "+endDate+".")
                directoryManipulator.editStockTrainingTextFile(datasetTicker, "")
            else:
                directoryManipulator.editStockTrainingTextFile(datasetTicker, "No training data available between "+startDate+" and "+endDate+". Not included in analysis.")
                directoryManipulator.editStockPredictionTextFile(datasetTicker, "No training data available between "+startDate+" and "+endDate+". Not included in analysis.")

        return dataSetCollection

    def retrieveLatestData(self, databaseName, datasetTickers, baseDate):

        dataSetCollection = {}

        directoryManipulator = DirectoryManipulator()

        for datasetTicker in datasetTickers:
            isDataAvailableForBaseDate = False

            # Query Quandl for base date.
            datasetQueryName = databaseName+'/'+datasetTicker
            paramCollection = self.createParamDefinition(baseDate, baseDate)
            dataset = quandl.Dataset(datasetQueryName).data(params=paramCollection).to_pandas()

            if not dataset.empty:
                isDataAvailableForBaseDate = True
                dataSetCollection.update({datasetTicker: dataset})
                directoryManipulator.editStockPredictionTextFile(datasetTicker, "Data available for " + baseDate + ", models will use this data in projection.")
                directoryManipulator.editStockPredictionTextFile(datasetTicker, "")

            # This checks the base date, if no data available on base date then next applicable date is found.
            tempBaseDate = parse(baseDate)
            while not isDataAvailableForBaseDate:
                directoryManipulator.editStockPredictionTextFile(datasetTicker, "Data not available for " + str(tempBaseDate) + ". Will try to retrieve data for " +str(date(tempBaseDate.year, tempBaseDate.month, tempBaseDate.day - 1))+".")
                tempBaseDate = date(tempBaseDate.year, tempBaseDate.month, tempBaseDate.day - 1)

                paramCollection = self.createParamDefinition(str(tempBaseDate), str(tempBaseDate))
                dataset = quandl.Dataset(datasetQueryName).data(params=paramCollection).to_pandas()

                if not dataset.empty:
                    isDataAvailableForBaseDate = True
                    dataSetCollection.update({datasetTicker: dataset})
                    directoryManipulator.editStockPredictionTextFile(datasetTicker, "Data available for " + str(tempBaseDate) + ", models will use this data in projection.")
                    directoryManipulator.editStockPredictionTextFile(datasetTicker, "")

        return dataSetCollection



    def createParamDefinition(self, startDate, endDate):

        return {'start_date': startDate, 'end_date': endDate}
