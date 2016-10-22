import logger
import quandlAdapter
import dataFilter as filter
import modelTrainer


class ResultsProcessor:

    def __init__(self, trainingStartDate, trainingEndDate, tickers, projectionDate, baseDate):
        self.trainingStartDate = trainingStartDate
        self.trainingEndDate = trainingEndDate
        self.tickers = tickers
        self.projectionDate = projectionDate
        self.baseDate = baseDate

    def processResults(self):
        # Setup logging.
        applicationLogger = logger.Logger('Log.log')

        # Setup adapter and respective logger.
        adapter = quandlAdapter.QuandlAdapter('QuandlAPIKey.txt')

        # Retrieve necessary data from Quandl.
        databaseName = 'WIKI'

        rawData = adapter.retrieveTrainingData(databaseName, self.tickers, self.trainingStartDate, self.trainingEndDate)

        # Define and apply filter to data.
        dataFilter = filter.DataFilter()
        dataFilter.addFilters(['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Volume', 'Ex-Dividend', 'Split Ratio', 'Adj. Close'])
        filteredData = dataFilter.applyFiltersAndFillMissingData(rawData)

        # Train models.
        trainedModels = modelTrainer.ModelTrainer(filteredData, self.baseDate, self.projectionDate)
        trainedModels.trainModels('Adj. Close', ['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Volume', 'Ex-Dividend', 'Split Ratio'], 0.3)

        # Use models to predict stock price.
        latestRawData = adapter.retrieveLatestData(databaseName, rawData.keys(), self.baseDate)
        filteredLatestData = dataFilter.applyFiltersAndFillMissingData(latestRawData)
        xColumns = ['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Volume', 'Ex-Dividend', 'Split Ratio']
        modelResults = {}

        # Gather optimal model predictions.
        for key in filteredData.keys():
            prediction = trainedModels.predict(filteredLatestData, xColumns, key)
            modelResults.update({key: prediction})

        applicationLogger.closeLogFile()
