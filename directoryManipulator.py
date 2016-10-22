import os
import shutil

from matplotlib import pyplot
from numpy import matlib
from numpy import mean


# This class is responsible for creating folders and files for the model results.
class DirectoryManipulator:

    TRAINING_TEXT_FILE_NAME = 'train_results.txt'
    PREDICTION_TEXT_FILE_NAME = 'prediction_results.txt'
    CONSOLIDATED_TEXT_FILE_NAME = 'final_results.txt'

    def makeResultsFolder(self):

        if os.path.exists('Results'):
            shutil.rmtree('Results', ignore_errors=True)

        os.mkdir('Results')

    def makeStockFoldersAndTextFiles(self, tickers):

        self.makeResultsFolder()

        for ticker in tickers:
            # Create stock folders.
            folderDirectory = 'Results/' + ticker
            os.mkdir(folderDirectory)

            # Create stock text files.
            file = open(folderDirectory + '/' + self.TRAINING_TEXT_FILE_NAME, 'w')
            file.close()

            file = open(folderDirectory + '/' + self.PREDICTION_TEXT_FILE_NAME, 'w')
            file.close()

        file = open('Results/' + self.CONSOLIDATED_TEXT_FILE_NAME, 'w')
        file.close()

    def editStockTextFile(self, ticker, fileType, messages):

        if fileType == self.CONSOLIDATED_TEXT_FILE_NAME:
            # We are editing the final prediction text file.
            file = open('Results/'+fileType, 'a')

            for message in messages:
                file.write(message)

            file.write("\n")
            file.close()

        else:
            # We are editing a stock text file.
            file = open('Results/'+ticker+'/'+fileType, 'a')

            for message in messages:
                file.write(message)

            file.write("\n")
            file.close()

    def editFinalPredictionTextFile(self, messages):

        self.editStockTextFile('', self.CONSOLIDATED_TEXT_FILE_NAME, messages)

    def editStockTrainingTextFile(self, ticker, messages):

        self.editStockTextFile(ticker, self.TRAINING_TEXT_FILE_NAME, messages)

    def editStockPredictionTextFile(self, ticker, messages):

        self.editStockTextFile(ticker, self.PREDICTION_TEXT_FILE_NAME, messages)

    def createPlot(self, title, ticker, xDataCollection, yDataCollection, legendCollection, xAxisName, yAxisName, plotName):

        pyplot.figure(figsize=(15, 10))
        for i in xrange(len(xDataCollection)):

            pyplot.plot(xDataCollection[i], yDataCollection[i], label= legendCollection[i])

        pyplot.legend()
        pyplot.ylabel(yAxisName)
        pyplot.xlabel(xAxisName)
        pyplot.title(title)
        pyplot.savefig('Results/'+ticker+'/'+plotName+".pdf")
        pyplot.close()

    def createLinearModelPredictionsPlot(self, ticker, xPredicted, xActual, yPredicted, yActual):

        xDataCollection= []
        xDataCollection.append(xPredicted)
        xDataCollection.append(xActual)

        yDataCollection= []
        yDataCollection.append(yPredicted)
        yDataCollection.append(yActual)

        legendCollection= []
        legendCollection.append("Predicted")
        legendCollection.append("Actual")

        self.createPlot(ticker +": Actual vs Predicted", ticker, xDataCollection, yDataCollection, legendCollection, "Dates", "Prices", "Linear_Prediction")

    def createTreeModelPredictionsPlot(self, ticker, xPredicted, xActual, yPredicted, yActual):

        xDataCollection= []
        xDataCollection.append(xPredicted)
        xDataCollection.append(xActual)

        yDataCollection= []
        yDataCollection.append(yPredicted)
        yDataCollection.append(yActual)

        legendCollection= []
        legendCollection.append("Predicted")
        legendCollection.append("Actual")

        self.createPlot(ticker +": Actual vs Predicted", ticker, xDataCollection, yDataCollection, legendCollection, "Dates", "Prices", "Tree_Prediction")

    def createKNNModelPredictionsPlot(self, ticker, xPredicted, xActual, yPredicted, yActual):

        xDataCollection= []
        xDataCollection.append(xPredicted)
        xDataCollection.append(xActual)

        yDataCollection= []
        yDataCollection.append(yPredicted)
        yDataCollection.append(yActual)

        legendCollection= []
        legendCollection.append("Predicted")
        legendCollection.append("Actual")

        self.createPlot(ticker +": Actual vs Predicted", ticker, xDataCollection, yDataCollection, legendCollection, "Dates", "Prices", "KNN_Prediction")

    def createEnsemblePredictionsPlot(self, ticker, xPredicted, xActual, yPredicted, yActual):

        xDataCollection= []
        xDataCollection.append(xPredicted)
        xDataCollection.append(xActual)

        yDataCollection= []
        yDataCollection.append(yPredicted)
        yDataCollection.append(yActual)

        legendCollection= []
        legendCollection.append("Predicted")
        legendCollection.append("Actual")

        self.createPlot(ticker +": Actual vs Predicted", ticker, xDataCollection, yDataCollection, legendCollection, "Dates", "Prices", "Ensemble_Prediction")

    def createLinearModelDifferencesPlot(self, ticker, xDifferences, yDifferences):

        xDataCollection= []
        xDataCollection.append(xDifferences)
        xDataCollection.append(xDifferences)

        yDataCollection= []
        yDataCollection.append(yDifferences)
        yDataCollection.append(matlib.repmat(mean(yDifferences), len(yDifferences), 1))

        legendCollection= []
        legendCollection.append("% Absolute Differences")
        legendCollection.append("% Absolute Differences Mean")

        self.createPlot(ticker +": Actual vs Predicted Differences", ticker, xDataCollection, yDataCollection, legendCollection, "Dates", "Prices", "Linear_Differences")

    def createTreeModelDifferencessPlot(self, ticker, xDifferences, yDifferences):

        xDataCollection= []
        xDataCollection.append(xDifferences)
        xDataCollection.append(xDifferences)

        yDataCollection= []
        yDataCollection.append(yDifferences)
        yDataCollection.append(matlib.repmat(mean(yDifferences), len(yDifferences), 1))

        legendCollection= []
        legendCollection.append("% Absolute Differences")
        legendCollection.append("% Absolute Differences Mean")

        self.createPlot(ticker +": Actual vs Predicted Differences", ticker, xDataCollection, yDataCollection, legendCollection, "Dates", "Prices", "Tree_Differences")

    def createKNNModelDifferencesPlot(self, ticker, xDifferences, yDifferences):

        xDataCollection= []
        xDataCollection.append(xDifferences)
        xDataCollection.append(xDifferences)

        yDataCollection= []
        yDataCollection.append(yDifferences)
        yDataCollection.append(matlib.repmat(mean(yDifferences), len(yDifferences), 1))

        legendCollection= []
        legendCollection.append("% Absolute Differences")
        legendCollection.append("% Absolute Differences Mean")

        self.createPlot(ticker +": Actual vs Predicted Differences", ticker, xDataCollection, yDataCollection, legendCollection, "Dates", "Prices", "KNN_Difference")

    def createEnsembleDifferencesPlot(self, ticker, xDifferences, yDifferences):

        xDataCollection= []
        xDataCollection.append(xDifferences)
        xDataCollection.append(xDifferences)

        yDataCollection= []
        yDataCollection.append(yDifferences)
        yDataCollection.append(matlib.repmat(mean(yDifferences), len(yDifferences), 1))

        legendCollection= []
        legendCollection.append("% Absolute Differences")
        legendCollection.append("% Absolute Differences Mean")

        self.createPlot(ticker +": Actual vs Predicted Differences", ticker, xDataCollection, yDataCollection, legendCollection, "Dates", "Prices", "Ensemble_Difference")
